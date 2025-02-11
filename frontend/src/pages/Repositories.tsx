import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import CommitsHistPie from "../components/CommitsHistPie";
import ErrorMessage from "../components/ErrorMessage";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Modal from "../components/Modal";
import Navbar from "../components/Navbar";
import OptionSelector from "../components/OptionSelector";
import Prompt from "../components/Prompt";
import Table from "../components/Table";
import UploadSection from "../components/UploadSection";
import { repoURLCSV } from "../constants/Descriptions";
import { commitTableHeaders } from "../constants/constants";
import repoURL from "../assets/repo_url.png";
import {
  downloadCsv,
  fetchWithRateLimit,
  generateCsvContent,
  getUserAvatarUrl,
  handleFileChange as handleFileChangeUtil,
  handleWaitTime as handleWaitTimeUtil,
  validateCsvFile,
} from "../utils/helpers";
import {
  checkDuplicate,
  fetchBranches,
  fetchBranchCommits,
  fetchCommitDetails,
  fetchRateLimit,
  saveToDatabase,
} from "../utils/queries";

import Papa from "papaparse";

const Contributions: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fatal, setFatal] = useState<string | null>(null);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const navigate = useNavigate();
  const [queryOption, setQueryOption] = useState<string>("allBranches");

  const [noRateLimit, setNoRateLimit] = useState<boolean>(false);
  const [totTime, setTotTime] = useState<number>(1000);
  const [remTime, setRemTime] = useState<number>(1000 - 1);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [tableHeader, setTableHeader] = useState<string[]>([]);
  const [tableData, setTableData] = useState<string[][] | null>(null);

  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const [loading, setLoading] = useState<boolean>(true);

  const loadRateLimit = async () => {
    const rateLimitData = await fetchRateLimit(setFatal);
    setRateLimit(rateLimitData);
  };

  useEffect(() => {
    setTableHeader(commitTableHeaders);
    const avatarUrl = getUserAvatarUrl();
    abortControllerRef.current = new AbortController();
    if (avatarUrl) {
      setAvatarUrl(avatarUrl);
    } else {
      navigate("/login");
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
    handleFileChangeUtil({ event, setErrors, setFile });
  };

  const handleWaitTime = (waitTime: number) => {
    return handleWaitTimeUtil(waitTime, setTotTime, setRemTime, setNoRateLimit);
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
      console.error(`Error parsing URL: ${url}`, error);
      throw new Error(`Invalid URL: ${url}`);
    }
  };

  const gatherCommits = async (
    repo: string,
    owner: string,
    branch: string,
    useDefault: boolean = false
  ) => {
    let commits: string[] = [];
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    do {
      let commitsPage = await fetchWithRateLimit(
        fetchBranchCommits,
        handleWaitTime,
        owner,
        repo,
        branch,
        useDefault,
        setFatal,
        endCursor
      );
      const pageInfo = commitsPage.pageInfo;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      commitsPage.commits.forEach((repo: any) => {
        commits.push(repo.oid);
      });
    } while (hasNextPage);
    return commits;
  };

  const gatherRepoBranches = async (repo: string, owner: string) => {
    let branchNames: string[] = [];
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    do {
      let branchesPage = await fetchWithRateLimit(
        fetchBranches,
        handleWaitTime,
        owner,
        repo,
        setFatal,
        endCursor
      );
      if ("error" in branchesPage) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          repo: `Invalid repo ${repo} and owner ${owner}`,
        }));
        setTableData(null);
        setFile(null);
        setLoading(false);
        return null;
      }
      const pageInfo = branchesPage.pageInfo;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      branchesPage.nodes.forEach((repo: any) => {
        branchNames.push(repo.name);
      });
    } while (hasNextPage);
    return branchNames;
  };

  const processRepoURL = async (url: string, signal: AbortSignal) => {
    const { owner, repo } = parseGithubUrl(url);
    if (queryOption === "allBranches") {
      const repoBranches = await gatherRepoBranches(repo, owner);
      if (!repoBranches) {
        return;
      }
      for (const branch of repoBranches) {
        if (signal.aborted) {
          return;
        }
        const repoContributions = await gatherCommits(
          repo,
          owner,
          branch,
          false
        );
        for (const oid of repoContributions) {
          if (signal.aborted) {
            return;
          }
          let commitResponse = await fetchWithRateLimit(
            fetchCommitDetails,
            handleWaitTime,
            owner,
            repo,
            oid,
            setFatal
          );
          let commit = commitResponse.commit;
          const row = [
            repo,
            commit.author || "N/A",
            commit.author_email || "N/A",
            commit.author_login || "N/A",
            branch,
            commit.authoredDate,
            commit.changedFilesIfAvailable,
            commit.additions,
            commit.deletions,
            commit.message,
            commit.parents,
            JSON.stringify(commit.lang_stats),
          ];
          addTableRow(row);
        }
      }
    } else {
      const repoContributions = await gatherCommits(repo, owner, "", true);
      for (const oid of repoContributions) {
        if (signal.aborted) {
          return;
        }
        let commitResponse = await fetchWithRateLimit(
          fetchCommitDetails,
          handleWaitTime,
          owner,
          repo,
          oid,
          setFatal
        );
        let commit = commitResponse.commit;
        const row = [
          repo,
          commit.author || "N/A",
          commit.author_email || "N/A",
          commit.author_login || "N/A",
          "default",
          commit.authoredDate,
          commit.changedFilesIfAvailable,
          commit.additions,
          commit.deletions,
          commit.message,
          commit.parents,
          JSON.stringify(commit.lang_stats),
        ];
        addTableRow(row);
      }
    }
    loadRateLimit();
  };

  const processRepoURLs = async (
    data: string[][] | string,
    signal: AbortSignal
  ) => {
    for (let i = 1; i < data.length; i++) {
      if (signal.aborted) {
        return;
      }
      const repoUrl = data[i][0];
      await processRepoURL(repoUrl, signal);
      loadRateLimit();
    }
  };

  const handleSubmit = async () => {
    const signal = abortControllerRef.current?.signal;
    if (!file) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        file: "No file selected",
      }));
      return;
    }

    try {
      await validateCsvFile(file);
    } catch (error) {
      if (error instanceof Error) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file: error.message,
        }));
      } else {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file: "An unknown error occurred",
        }));
      }
      return;
    }

    try {
      Papa.parse(file, {
        complete: async (result: Papa.ParseResult<string[]>) => {
          setLoading(true);
          await processRepoURLs(result.data as string[][], signal!);
          setLoading(false);
        },
        header: false,
      });
    } catch (error) {
      if (error instanceof Error) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file: error.message,
        }));
      } else {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file: "An unknown error occurred",
        }));
      }
      setLoading(false);
      return;
    }
  };

  const handleExport = () => {
    if (tableData) {
      const csvContent = generateCsvContent(tableHeader, tableData);
      downloadCsv(csvContent, "repository_commits.csv");
    } else {
      alert("No contributions to export");
    }
  };

  const handleBackToOptions = () => {
    setTableData(null);
    setFile(null);
  };

  const handleSave = async (name: string) => {
    const response = await checkDuplicate(
      { name, type: "Repo Commits" },
      setFatal
    );

    if (response.exists) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        errorMessage:
          "A dataset of this type with this name already exists. Please choose a different name.",
      }));
      setIsPromptOpen(true);
    } else {
      await saveToDatabase(
        {
          name,
          type: "Repo Commits",
          tableHeader: tableHeader,
          tableData: tableData || [],
        },
        setFatal
      );
      setIsModalVisible(true);
      setErrors((prevErrors) => ({ ...prevErrors, errorMessage: "" }));
    }
  };

  const handleCloseModal = () => {
    setIsModalVisible(false);
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
                demoImage={repoURL}
                handleFileChange={handleFileChange}
                title="Upload Repository URLs"
                description={repoURLCSV}
              />
              {errors.file && <ErrorMessage error={errors.file} />}
              <div className="text-gray-300 mb-4">
                Note: Querying all the commits from a repository is a very
                resource-intensive operation. The rate limit of 5,000 requests
                will be quickly exhausted. If you are working with a large
                number of repositories or very large repositories, it is
                recommended to query a smaller number of repositories at a time.
              </div>
              <Button
                handleAction={handleSubmit}
                text={"Submit"}
                disabled={loading}
              />
            </>
          ) : (
            <>
              <h2 className="text-2xl font-bold text-white mb-4">
                Commits in Given Repositories
              </h2>
              {!loading && (
                <CommitsHistPie headers={tableHeader} data={tableData} />
              )}
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
                    errorMessage={errors.errorMessage}
                  />
                  {isModalVisible && (
                    <Modal
                      title="Success"
                      message="Data saved successfully."
                      onClose={handleCloseModal}
                      success={true}
                    />
                  )}
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
