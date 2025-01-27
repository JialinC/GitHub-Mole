import React, { useState, useEffect, useRef } from "react";
import OptionSelector from "../components/OptionSelector";
import { repoURLCSV } from "../constants/Descriptions";
import UploadSection from "../components/UploadSection";
import ErrorMessage from "../components/ErrorMessage";
import Table from "../components/Table";
import Button from "../components/Button";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import ErrorPage from "../components/Error";
import Prompt from "../components/Prompt";

import { commitTableHeaders } from "../constants/constants";
import githubIDs from "../assets/github_ids.png";
import { getUserAvatarUrl } from "../utils/helpers";
import {
  fetchRateLimit,
  fetchCommits,
  checkDuplicate,
  saveToDatabase,
  fetchBranches,
  fetchBranchCommits,
} from "../utils/queries";

import Papa from "papaparse";

const Contributions: React.FC = () => {
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const [queryOption, setQueryOption] = useState<string>("allBranches");
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string>();
  const [fatal, setFatal] = useState<string | null>(null);

  const [noRateLimit, setNoRateLimit] = useState<boolean>(false);
  const [totTime, setTotTime] = useState<number>(1000);
  const [remTime, setRemTime] = useState<number>(1000 - 1);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [tableHeader, setTableHeader] = useState<string[]>([]);
  const [tableData, setTableData] = useState<string[][] | null>(null);

  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [datasetName, setDatasetName] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const [loading, setLoading] = useState<boolean>(true);

  const loadRateLimit = async () => {
    try {
      const rateLimitData = await fetchRateLimit(setFatal);
      setRateLimit(rateLimitData);
    } catch (error) {
      console.error("Error in loadRateLimit:", error);
    }
  };

  useEffect(() => {
    setTableHeader(commitTableHeaders);
    const avatarUrl = getUserAvatarUrl();
    abortControllerRef.current = new AbortController();
    if (avatarUrl) {
      setAvatarUrl(avatarUrl);
    }
    loadRateLimit();
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQueryOption(event.target.value);
    setTableData(null);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedFile = event.target.files[0];
      const maxSizeInMB = 5; // Set the maximum file size (e.g., 5 MB)
      if (selectedFile.size > maxSizeInMB * 1024 * 1024) {
        setFileError(`File size exceeds ${maxSizeInMB} MB`);
        setFile(null);
      } else {
        setFileError("");
        setFile(selectedFile);
      }
    }
  };

  const handleWaitTime = (waitTime: number) => {
    return new Promise<void>((resolve) => {
      const endTime = Date.now() + (waitTime + 3) * 1000;
      setTotTime(waitTime + 3);
      let bool = true;
      const interval = setInterval(() => {
        const timeLeft = Math.max(0, endTime - Date.now());
        setRemTime(Math.ceil(timeLeft / 1000)); // Update countdown state
        if (bool) {
          setNoRateLimit(true);
          bool = false;
        }
        if (timeLeft === 0) {
          clearInterval(interval);
          setNoRateLimit(false);
          setRemTime(1000 - 1); // Reset countdown state
          setTotTime(1000);
          resolve();
        }
      }, 1000);
    });
  };

  const addTableRow = (rowData: string[]) => {
    setTableData((prevData) => {
      const newData = prevData ? [...prevData] : [];
      newData.push(rowData);
      return newData;
    });
  };

  const parseGithubUrl = (url: string): { owner: string; repo: string } => {
    try {
      const parsedUrl = new URL(url);
      const pathParts = parsedUrl.pathname.split("/").filter(Boolean);
      if (pathParts.length < 2) {
        throw new Error("Invalid URL");
      }
      const owner = pathParts[0];
      const repo = pathParts[1];
      return { owner, repo };
    } catch (error) {
      throw new Error("Invalid URL");
    }
  };

  const processBranch = async (
    owner: string,
    repo: string,
    branch: string = "default branch"
  ) => {
    let endCursor: string | null = null;
    let hasNextPage: boolean = false;
    do {
      let response: any =
        queryOption === "allBranches"
          ? await fetchBranchCommits(
              owner,
              repo,
              `"${branch}"`,
              setFatal,
              endCursor
            )
          : await fetchCommits(owner, repo, setFatal, endCursor);

      if ("no_limit" in response) {
        await handleWaitTime(response.wait_seconds);
        response =
          queryOption === "allBranches"
            ? await fetchBranchCommits(
                owner,
                repo,
                `"${branch}"`,
                setFatal,
                endCursor
              )
            : await fetchCommits(owner, repo, setFatal, endCursor);
      }

      const { pageInfo, commits } = response;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      for (const commit of commits) {
        const row = [
          repo,
          commit.author || "N/A",
          commit.author_email || "N/A",
          commit.author_id || "N/A",
          branch,
          commit.authoredDate,
          commit.changedFilesIfAvailable,
          commit.additions,
          commit.deletions,
          commit.message,
          commit.parents,
        ];
        addTableRow(row);
      }
    } while (hasNextPage);
  };

  const processRepoURL = async (data: string[][], signal: AbortSignal) => {
    setLoading(true);
    for (let i = 1; i < data.length; i++) {
      if (signal.aborted) {
        return;
      }

      const { owner, repo } = parseGithubUrl(data[i][0]);

      if (queryOption === "allBranches") {
        let branches = await fetchBranches(owner, repo, setFatal);
        for (const branch of branches) {
          if (signal.aborted) {
            return;
          }
          await processBranch(owner, repo, branch);
        }
      } else {
        await processBranch(owner, repo);
      }

      loadRateLimit();
    }
    setLoading(false);
  };

  const validateCsvFile = (file: File): Promise<void> => {
    return new Promise((resolve, reject) => {
      Papa.parse(file, {
        complete: (results) => {
          const data = results.data as string[][];

          if (data.length === 0 || data[0].indexOf("Repository URL") === -1) {
            return reject(
              new Error(
                'The file must include a title row with the column title "Repository URL".'
              )
            );
          }

          for (let i = 1; i < data.length; i++) {
            const url = data[i][data[0].indexOf("Repository URL")];
            try {
              const parsedUrl = new URL(url);
              const pathParts = parsedUrl.pathname.split("/").filter(Boolean);

              if (pathParts.length < 2) {
                return reject(
                  new Error(`Invalid URL found in row ${i + 1}: ${url}`)
                );
              }
            } catch (error) {
              return reject(
                new Error(`Invalid URL found in row ${i + 1}: ${url}`)
              );
            }
          }

          resolve();
        },
        error: (error) => {
          reject(new Error(`Failed to parse CSV file: ${error.message}`));
        },
        header: false,
        skipEmptyLines: true,
      });
    });
  };

  const handleSubmit = async () => {
    if (!file) {
      setFileError("No file selected");
      return;
    }

    try {
      await validateCsvFile(file);
    } catch (error) {
      if (error instanceof Error) {
        setFileError(error.message);
      } else {
        setFileError("An unknown error occurred");
      }
    }

    try {
      Papa.parse(file, {
        complete: async (result: Papa.ParseResult<string[]>) => {
          await processRepoURL(result.data as string[][], signal!);
        },
        header: false,
      });
    } catch (error) {
      if (error instanceof Error) {
        setFileError(error.message);
      } else {
        setFileError("An unknown error occurred");
      }
    }

    const signal = abortControllerRef.current?.signal;
  };

  const escapeCsvValue = (value: string) => {
    if (value.includes(",") || value.includes("\n") || value.includes('"')) {
      return `"${value.replace(/"/g, '""')}"`;
    }
    return value;
  };

  const handleExport = () => {
    const csvContent = [
      tableHeader.map(escapeCsvValue).join(","), // Add the headers
      ...(tableData
        ? tableData.map((row) => row.map(escapeCsvValue).join(","))
        : []), // Add the data rows
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    let fileName = "commits.csv";
    link.setAttribute("download", fileName);
    document.body.appendChild(link);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleBackToOptions = () => {
    setTableData(null);
    setFile(null);
  };

  const handleSave = async (name: string) => {
    setDatasetName(name);
    const response = await checkDuplicate({ name, type: "Commits" }, setFatal);

    if (response.exists) {
      setErrorMessage(
        "A dataset of this type with this name already exists. Please choose a different name."
      );
      setIsPromptOpen(true);
    } else {
      setDatasetName("");
      setErrorMessage(null);
      const response = await saveToDatabase(
        {
          name,
          type: "Commits",
          tableHeader: tableHeader,
          tableData: tableData || [],
        },
        setFatal
      );
      console.log(response);
      alert("Data saved successfully.");
      setErrorMessage(null);
    }
  };

  if (fatal) {
    return <ErrorPage message={fatal} />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar avatarUrl={avatarUrl} rateLimit={rateLimit}>
        <a
          href="/dashboard"
          target="_self"
          className="text-white mr-4 text-xl font-bold tracking-wide shadow-lg transition-transform transform hover:scale-105"
        >
          Dashboard
        </a>
      </Navbar>
      <main className="flex-grow container mx-auto p-4">
        <div className="p-6 bg-gray-800 rounded-lg shadow-md">
          {!tableData ? (
            <>
              <h2 className="text-2xl font-bold text-white mb-4">
                Mine Commits Data From Repositories
              </h2>
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="allBranches"
                labelText="Query commits and statistics from all branches (e.g., main branch, feature branches, etc.) in the specified repository."
              />
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="defaultBranch"
                labelText="Query commits and statistics from the default branch (e.g., main or master branch) in the specified repository."
              />
              <UploadSection
                demoImage={githubIDs}
                handleFileChange={handleFileChange}
                title="Upload Repository URLs"
                description={repoURLCSV}
              />
              {fileError && <ErrorMessage error={fileError} />}
              <div className="text-gray-300 mb-4">
                Note: Querying all the commits from a repository is a very
                resource-intensive operation. The rate limit of 5,000 requests
                will be quickly exhausted. If you are working with a large
                number of repositories or very large repositories, it is
                recommended to query a smaller number of repositories at a time.
              </div>
              <Button handleAction={handleSubmit} text={"Submit"} />
            </>
          ) : (
            <>
              <Table
                headers={tableHeader}
                data={tableData}
                columnWidth="150px"
                columnSelection={false}
                noRateLimit={noRateLimit}
                remainingTime={remTime}
                totalTime={totTime}
              />
              {!loading && (
                <>
                  <Button handleAction={handleExport} text={"Export Dataset"} />
                  <Button
                    handleAction={handleBackToOptions}
                    text={"Query Another Dataset"}
                  />
                  <Button
                    handleAction={() => setIsPromptOpen(true)}
                    text={"Save Dataset"}
                  />
                  <Prompt
                    isOpen={isPromptOpen}
                    onClose={() => setIsPromptOpen(false)}
                    onSave={handleSave}
                    errorMessage={errorMessage}
                  />
                </>
              )}
              {noRateLimit && (
                <>
                  <div className="mt-2 text-m text-yellow-300">
                    No rate limit remaining.{" "}
                    {remTime !== null && (
                      <span>Wait time remaining: {remTime}s</span>
                    )}{" "}
                    For more information, see{" "}
                    <a
                      href="https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api#primary-rate-limit"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 underline"
                    >
                      GitHub GraphQL API Rate Limits
                    </a>
                    .
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Contributions;
