import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import UserCommitsHistPie from "../components/UserCommitsHistPie";
import ErrorMessage from "../components/ErrorMessage";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Modal from "../components/Modal";
import Navbar from "../components/Navbar";
import OptionSelector from "../components/OptionSelector";
import Prompt from "../components/Prompt";
import Spinner from "../components/Spinner";
import Table from "../components/Table";
import UploadSection from "../components/UploadSection";
import { gitHubCSV } from "../constants/Descriptions";
import { commitTableHeaders } from "../constants/constants";
import githubIDs from "../assets/github_ids.png";
import {
  downloadCsv,
  fetchWithRateLimit,
  generateCsvContent,
  getUserAvatarUrl,
  handleFileChange as handleFileChangeUtil,
  handleWaitTime as handleWaitTimeUtil,
  parseCSV,
  validateGitHubIdsFile,
} from "../utils/helpers";
import {
  checkDuplicate,
  fetchRepoNames,
  fetchBranches,
  fetchContributorContributions,
  fetchCommitDetails,
  fetchRateLimit,
  saveToDatabase,
} from "../utils/queries";

const Commits: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fatal, setFatal] = useState<string | null>(null);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [invalidIDs, setInvalidIDs] = useState<string[]>([]);

  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const navigate = useNavigate();

  const [queryOption, setQueryOption] = useState<string>("oneUser");
  const [githubId, setGithubId] = useState("");

  const [noRateLimit, setNoRateLimit] = useState<boolean>(false);
  const [totTime, setTotTime] = useState<number>(1000);
  const [remTime, setRemTime] = useState<number>(1000 - 1);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [showTable, setShowTable] = useState<boolean>(false);
  const [tableHeader, setTableHeader] = useState<string[]>([]);
  const [tableData, setTableData] = useState<string[][] | null>([]);

  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const [loading, setLoading] = useState<boolean>(false);

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
    setErrors({});
    setQueryOption(event.target.value);
    setTableData([]);
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

  const gatherRepoNames = async (githubId: string) => {
    let ghid;
    let repoNames: { [key: string]: string }[] = [];
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    do {
      let userRepoNamesPage = await fetchWithRateLimit(
        fetchRepoNames,
        handleWaitTime,
        githubId,
        setFatal,
        endCursor
      );
      if ("error" in userRepoNamesPage) {
        setInvalidIDs((prevInvalidIDs) => [...prevInvalidIDs, githubId]);
        return null;
      }
      ghid = userRepoNamesPage.id;
      const pageInfo = userRepoNamesPage.pageInfo;
      const repos = userRepoNamesPage.repos;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      repos.forEach((repo: any) => {
        repoNames.push({ name: repo.name, owner: repo.owner.login });
      });
    } while (hasNextPage);
    return { repoNames, ghid };
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
      const pageInfo = branchesPage.pageInfo;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      branchesPage.nodes.forEach((repo: any) => {
        branchNames.push(repo.name);
      });
    } while (hasNextPage);
    return branchNames;
  };

  const gatherContributorContributions = async (
    repo: string,
    owner: string,
    branch: string,
    userId: string
  ) => {
    let commits: string[] = [];
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    do {
      let commitsPage = await fetchWithRateLimit(
        fetchContributorContributions,
        handleWaitTime,
        owner,
        repo,
        branch,
        userId,
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

  const processGitHubId = async (login: string, signal: AbortSignal) => {
    const repoNames = await gatherRepoNames(login);
    if (!repoNames) {
      return;
    }
    const userId = repoNames.ghid;
    const repos = repoNames.repoNames;
    let commitCount = 0;
    for (const { name: repo, owner } of repos) {
      if (signal.aborted) {
        return;
      }
      const repoBranches = await gatherRepoBranches(repo, owner);
      for (const branch of repoBranches) {
        if (signal.aborted) {
          return;
        }
        const repoContributions = await gatherContributorContributions(
          repo,
          owner,
          branch,
          userId
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
          commitCount++;
          addTableRow(row);
        }
      }
      loadRateLimit();
    }
    if (commitCount === 0) {
      const row = [
        "N/A",
        "N/A",
        "N/A",
        login,
        "N/A",
        "N/A",
        "0",
        "0",
        "0",
        "N/A",
        "0",
        "N/A",
      ];
      addTableRow(row);
    }
  };

  const processGitHubIds = async (
    data: string[][] | string,
    signal: AbortSignal
  ) => {
    for (let i = 1; i < data.length; i++) {
      const githubID = data[i][0];
      await processGitHubId(githubID, signal);
      loadRateLimit();
    }
  };

  const handleSubmit = async () => {
    const signal = abortControllerRef.current?.signal;
    if (queryOption === "groupUsers") {
      if (!file) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file: "No file selected",
        }));
        return;
      }

      try {
        await validateGitHubIdsFile(file);
      } catch (error) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          file:
            error instanceof Error
              ? error.message
              : "An unknown error occurred",
        }));
        return;
      }

      setLoading(true);
      setShowTable(true);
      try {
        const result = await parseCSV(file);
        await processGitHubIds(result.data as string[][], signal!);
      } catch (error) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          processing:
            error instanceof Error
              ? error.message
              : "An unknown error occurred",
        }));
      } finally {
        setLoading(false);
      }
    } else {
      if (!githubId) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          githubId: "Please enter a GitHub ID",
        }));
        return;
      }

      setLoading(true);
      setShowTable(true);
      try {
        await processGitHubId(githubId, signal!);
      } catch (error) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          processing:
            error instanceof Error
              ? error.message
              : "An unknown error occurred",
        }));
      } finally {
        setLoading(false);
      }
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
    setErrors({});
    setInvalidIDs([]);
    setShowTable(false);
    setTableData([]);
    setFile(null);
  };

  const handleSave = async (name: string) => {
    const response = await checkDuplicate(
      { name, type: "User Commits" },
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
          type: "User Commits",
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
          {!showTable ? (
            <>
              <h2 className="text-2xl font-bold text-white mb-4">
                Mine ALL Commits by a User/a group of Users
              </h2>
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="oneUser"
                labelText="Query all commits made by a single user."
              />
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="groupUsers"
                labelText="Query all commits made by a group of users."
              />
              {queryOption === "oneUser" && (
                <div className="mb-4">
                  <label
                    htmlFor="githubId"
                    className="text-lg font-bold text-white mb-4 block"
                  >
                    Enter GitHub ID
                  </label>
                  <input
                    type="text"
                    id="githubId"
                    value={githubId}
                    onChange={(e) => setGithubId(e.target.value)}
                    placeholder="Please enter the GitHub ID you are curious about, e.g., JialinC."
                    className="w-full px-3 py-2 text-gray-700 bg-gray-200 rounded-lg focus:outline-none"
                  />
                </div>
              )}
              {queryOption === "groupUsers" && (
                <>
                  <UploadSection
                    demoImage={githubIDs}
                    handleFileChange={handleFileChange}
                    title="Upload GitHub IDs"
                    description={gitHubCSV}
                  />
                  {errors.githubId && <ErrorMessage error={errors.githubId} />}
                </>
              )}

              {errors.file && <ErrorMessage error={errors.file} />}
              <div className="text-gray-300 mb-4">
                <span className="font-semibold text-white">WARNING:</span>{" "}
                Querying all commits made by a single user or a group of users
                is a highly resource-intensive operation. Due to the GitHub API
                rate limit of 5,000 requests per hour, this process can quickly
                exhaust the available quota. If you are working with a large
                number of users or a user with a substantial commit history, it
                is recommended to query a smaller number of users at a time to
                optimize performance and avoid exceeding rate limits. As a
                reference, each commit requires one request. Therefore, if you
                need to query a user with 500 commits, the entire process will
                require at least 500 requests.{" "}
                <span className="font-semibold text-white">
                  The current implementation first collects all repositories
                  associated with the specified user(s), including both forked
                  and original repositories, as well as those owned or
                  collaborated on. It then retrieves all branches from these
                  repositories and, for each branch, gathers the OIDs of all
                  commits made by the specified user(s). For each commit, the
                  tool collects the list of changed files along with their
                  addition and deletion counts. The number of lines added and
                  deleted for each programming language is inferred based on the
                  modified files.
                </span>{" "}
              </div>
              <Button
                handleAction={handleSubmit}
                text={"Submit"}
                disabled={loading}
              />
              <div className="bg-gray-800 rounded-lg shadow-md mt-4 text-white">
                <h2 className="text-2xl font-bold mb-4">
                  How GitHub Calculates Commit Contributions
                </h2>
                <p className="mb-2">
                  GitHub contributions are counted in the "Contributions" graph
                  on a user's profile. The key rules for counting commits are:
                </p>
                <ul className="list-disc list-inside mb-4">
                  <li className="mb-2">
                    <span className="font-semibold">
                      ✅ Commits That Count Towards Contributions
                    </span>
                    <ul className="list-disc list-inside ml-6">
                      <li>
                        Must be in the default branch (usually main or master,
                        but can be changed by repo settings).
                      </li>
                      <li>
                        Must be in a forked repo where the commit is in the
                        default branch and the fork has at least one star.
                      </li>
                      <li>
                        The user must be the author of the commit (i.e., the
                        email in the commit must match their GitHub account).
                      </li>
                      <li>
                        Commits must be pushed to GitHub (local commits don't
                        count).
                      </li>
                      <li>
                        The repository must be public OR the user must be a
                        contributor to a private repo.
                      </li>
                    </ul>
                  </li>
                  <li className="mb-2">
                    <span className="font-semibold">
                      ❌ Commits That Do NOT Count
                    </span>
                    <ul className="list-disc list-inside ml-6">
                      <li>
                        Commits in non-default branches (e.g., feature-branch,
                        develop) do not count towards profile contributions.
                      </li>
                      <li>
                        Commits in forks (unless the fork has at least one
                        star).
                      </li>
                      <li>
                        Commits made using an email that is not associated with
                        the user's GitHub account.
                      </li>
                      <li>Commits that are not pushed to GitHub.</li>
                    </ul>
                  </li>
                </ul>
              </div>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                All Commits for Given User/Users
                {loading && <Spinner />}
              </h2>
              {!loading && (
                <UserCommitsHistPie headers={tableHeader} data={tableData} />
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
              {invalidIDs.length > 0 && (
                <ErrorMessage
                  error={
                    "The following GitHub IDs are invalid: " +
                    invalidIDs.toString()
                  }
                />
              )}
              {errors.processing && <ErrorMessage error={errors.processing} />}
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

export default Commits;
