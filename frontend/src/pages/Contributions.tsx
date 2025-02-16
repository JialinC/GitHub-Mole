import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Papa from "papaparse";

import githubIDs from "../assets/github_ids.png";

import Button from "../components/Button";
import ErrorMessage from "../components/ErrorMessage";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Histogram from "../components/Histogram";
import Modal from "../components/Modal";
import Navbar from "../components/Navbar";
import OptionSelector from "../components/OptionSelector";
import Prompt from "../components/Prompt";
import RepoHistPie from "../components/RepoHistPie";
import SelectionSection from "../components/SelectionSection";
import Spinner from "../components/Spinner";
import Table from "../components/Table";
import TotalHistogram from "../components/TotalHistogram";
import UploadSection from "../components/UploadSection";

import { gitHubCSV, langsDesc, contribsDesc } from "../constants/Descriptions";
import {
  contributions,
  languages,
  numericalValue,
  repoTypes,
  tableHeaders,
} from "../constants/constants";

import { FetchFunctionKeys } from "../types/Types";

import {
  addLoadingRow,
  addNARow,
  calLangStats,
  calculateLifetime,
  castTableData,
  chunkArray,
  downloadCsv,
  fetchWithRateLimit,
  getUserAvatarUrl,
  generateCsvContent,
  handleFileChange as handleFileChangeUtil,
  handleWaitTime as handleWaitTimeUtil,
  isValidGitHubId,
  parseCSV,
  toCamelCase,
  validateGitHubIdsFile,
} from "../utils/helpers";
import {
  checkDuplicate,
  fetchFunctions,
  fetchRateLimit,
  saveToDatabase,
} from "../utils/queries";

const Contributions: React.FC = () => {
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const navigate = useNavigate();
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [invalidIDs, setInvalidIDs] = useState<string[]>([]);
  const [fatal, setFatal] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [githubId, setGithubId] = useState("");
  const [inputOption, setInputOption] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [queryOption, setQueryOption] = useState<string>("totalContributions");
  const [selectedLangs, setSelectedLangs] = useState<Set<string>>(new Set());
  const [selectedContribution, setSelectedContribution] = useState<string>("");

  const [noRateLimit, setNoRateLimit] = useState<boolean>(false);
  const [totTime, setTotTime] = useState<number>(1000);
  const [remTime, setRemTime] = useState<number>(1000 - 1);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [showTable, setShowTable] = useState<boolean>(false);
  const [tableHeader, setTableHeader] = useState<string[]>([]);
  const [tableData, setTableData] = useState<string[][] | null>([]);
  const [avatarMap, setAvatarMap] = useState<{ [key: string]: string }>({});

  const [timeRange, setTimeRange] = useState({
    isTimeRangeSelected: false,
    startDate: "",
    endDate: "",
    isPresent: false,
  });

  const [isPromptOpen, setIsPromptOpen] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const languageChunks = chunkArray(languages, Math.ceil(languages.length / 4));

  const contributionChunks = chunkArray(
    contributions,
    Math.ceil(contributions.length / 4)
  );

  const loadRateLimit = async () => {
    const rateLimitData = await fetchRateLimit(setFatal);
    setRateLimit(rateLimitData);
  };

  useEffect(() => {
    if (queryOption === "totalContributions") {
      setTableHeader(tableHeaders["Contributions"]);
    } else if (queryOption === "specificContributions") {
      setTableHeader(tableHeaders[selectedContribution]);
    }
  }, [queryOption, selectedContribution]);

  useEffect(() => {
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

  const getHeaderIndex = (headers: string[], field: string): number => {
    return headers?.indexOf(field) ?? -1;
  };

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQueryOption(event.target.value);
    setErrors({});
    setSelectedLangs(new Set());
    setSelectedContribution("");
    setTableData([]);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    handleFileChangeUtil({ event, setErrors, setFile });
  };

  const updateTimeRange = (key: string, value: any) => {
    setTimeRange((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleTimeRangeChange = () => {
    updateTimeRange("isTimeRangeSelected", !timeRange.isTimeRangeSelected);
  };

  const handleInputChange = () => {
    setInputOption(!inputOption);
  };

  const handleStartDateChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    updateTimeRange("startDate", event.target.value);
  };

  const handleEndDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    updateTimeRange("endDate", event.target.value);
  };

  const handlePresentChange = () => {
    updateTimeRange("isPresent", !timeRange.isPresent);
    if (!timeRange.isPresent) {
      updateTimeRange("endDate", new Date().toISOString().split("T")[0]);
    } else {
      updateTimeRange("endDate", "");
    }
  };

  const handleLanguageChange = (language: string) => {
    setErrors((prevErrors) => ({ ...prevErrors, langs: "" }));
    setSelectedLangs((prevSelectedLangs) => {
      const newSelectedLangs = new Set(prevSelectedLangs);
      if (newSelectedLangs.has(language)) {
        newSelectedLangs.delete(language);
      } else {
        newSelectedLangs.add(language);
      }
      return newSelectedLangs;
    });
  };

  const handleContributionChange = (selectedContribution: string) => {
    setErrors((prevErrors) => ({ ...prevErrors, contrib: "" }));
    setSelectedContribution(selectedContribution);
  };

  const handleWaitTime = (waitTime: number) => {
    return handleWaitTimeUtil(waitTime, setTotTime, setRemTime, setNoRateLimit);
  };

  const updateTableData = (
    rowIndex: number,
    columnIndex: number,
    result: string
  ) => {
    setTableData((prevData) =>
      prevData
        ? prevData.map((row, index) =>
            index === rowIndex
              ? [
                  ...row.slice(0, columnIndex),
                  result,
                  ...row.slice(columnIndex + 1),
                ]
              : row
          )
        : null
    );
  };

  const nameIndex = getHeaderIndex(tableHeader, "Name");
  const emailIndex = getHeaderIndex(tableHeader, "Email");
  const createdAtIndex = getHeaderIndex(tableHeader, "Created At");
  const ageIndex = getHeaderIndex(tableHeader, "Age (days)");
  const bioIndex = getHeaderIndex(tableHeader, "Bio");
  const companyIndex = getHeaderIndex(tableHeader, "Company");
  const watchingIndex = getHeaderIndex(tableHeader, "Watching");
  const starredRepoIndex = getHeaderIndex(tableHeader, "Starred Repositories");
  const followingIndex = getHeaderIndex(tableHeader, "Following");
  const followersIndex = getHeaderIndex(tableHeader, "Followers");
  const privateContribIndex = getHeaderIndex(
    tableHeader,
    "Private Contributions"
  );
  const commitsIndex = getHeaderIndex(tableHeader, "Commits");
  const gistsIndex = getHeaderIndex(tableHeader, "Gists");
  const issuesIndex = getHeaderIndex(tableHeader, "Issues");
  const projectsIndex = getHeaderIndex(tableHeader, "Projects");
  const prIndex = getHeaderIndex(tableHeader, "Pull Requests");
  const prReviewsIndex = getHeaderIndex(tableHeader, "Pull Request Reviews");
  const repoIndex = getHeaderIndex(tableHeader, "Repositories");
  const repoDiscussionsIndex = getHeaderIndex(
    tableHeader,
    "Repository Discussions"
  );
  const commitCommentsIndex = getHeaderIndex(tableHeader, "Commit Comments");
  const issueCommentsIndex = getHeaderIndex(tableHeader, "Issue Comments");
  const gistCommentsIndex = getHeaderIndex(tableHeader, "Gist Comments");
  const repoDiscussionCommentsIndex = getHeaderIndex(
    tableHeader,
    "Repository Discussion Comments"
  );

  const updateProfileData = (
    index: number,
    profile: any,
    userContribution: any
  ) => {
    updateTableData(index, nameIndex, profile.name?.toString() || "N/A");
    updateTableData(index, emailIndex, profile.email?.toString() || "N/A");
    updateTableData(
      index,
      createdAtIndex,
      profile.created_at.toString() || "N/A"
    );
    updateTableData(
      index,
      ageIndex,
      calculateLifetime(profile.created_at).toString()
    );
    updateTableData(index, bioIndex, profile.bio?.toString() || "N/A");
    updateTableData(index, companyIndex, profile.company?.toString() || "N/A");
    updateTableData(index, watchingIndex, profile.watching.toString() || "N/A");
    updateTableData(
      index,
      starredRepoIndex,
      profile.starred_repositories?.toString() || "N/A"
    );
    updateTableData(
      index,
      followingIndex,
      profile.following.toString() || "N/A"
    );
    updateTableData(
      index,
      followersIndex,
      profile.followers.toString() || "N/A"
    );
    updateTableData(
      index,
      privateContribIndex,
      userContribution.res_con.toString()
    );
    updateTableData(index, commitsIndex, userContribution.commit.toString());
    updateTableData(index, gistsIndex, profile.gists.toString() || "N/A");
    updateTableData(index, issuesIndex, profile.issues.toString() || "N/A");
    updateTableData(index, projectsIndex, profile.projects.toString() || "N/A");
    updateTableData(index, prIndex, profile.pull_requests.toString() || "N/A");
    updateTableData(
      index,
      prReviewsIndex,
      userContribution.pr_review.toString() || "N/A"
    );
    updateTableData(index, repoIndex, profile.repositories.toString() || "N/A");
    updateTableData(
      index,
      repoDiscussionsIndex,
      profile.repository_discussions.toString() || "N/A"
    );
    updateTableData(
      index,
      commitCommentsIndex,
      profile.commit_comments.toString() || "N/A"
    );
    updateTableData(
      index,
      issueCommentsIndex,
      profile.issue_comments.toString() || "N/A"
    );
    updateTableData(
      index,
      gistCommentsIndex,
      profile.gist_comments.toString() || "N/A"
    );
    updateTableData(
      index,
      repoDiscussionCommentsIndex,
      profile.repository_discussion_comments.toString() || "N/A"
    );
  };

  const updateProfileDataTime = (
    index: number,
    profile: any,
    userContribution: any,
    end: Date
  ) => {
    updateTableData(index, nameIndex, profile.name?.toString() || "N/A");
    updateTableData(index, emailIndex, profile.email?.toString() || "N/A");
    updateTableData(
      index,
      createdAtIndex,
      profile.created_at.toString() || "N/A"
    );
    const ghStart = new Date(profile.created_at);
    const differenceInTime = end.getTime() - ghStart.getTime();
    const differenceInDays = differenceInTime / (1000 * 3600 * 24);
    updateTableData(index, ageIndex, Math.floor(differenceInDays).toString());
    updateTableData(index, bioIndex, profile.bio?.toString() || "N/A");
    updateTableData(index, companyIndex, profile.company?.toString() || "N/A");
    updateTableData(index, watchingIndex, "0");
    updateTableData(index, starredRepoIndex, "0");
    updateTableData(index, followingIndex, "0");
    updateTableData(index, followersIndex, "0");
    updateTableData(
      index,
      privateContribIndex,
      userContribution.res_con.toString()
    );
    updateTableData(index, commitsIndex, userContribution.commit.toString());
    updateTableData(index, projectsIndex, "0");
    updateTableData(
      index,
      prReviewsIndex,
      userContribution.pr_review.toString() || "N/A"
    );
  };

  const fetchAndProcessRepos = async (
    githubID: string,
    index: number,
    fetchKey: keyof typeof fetchFunctions,
    startColumn: number
  ) => {
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    let repoCnt: number = 0;
    let totalSize: number = 0;
    let selectedSize: number = 0;
    const userLangs = new Set<string>();

    do {
      let userReposPage = await fetchWithRateLimit(
        fetchFunctions[fetchKey],
        handleWaitTime,
        githubID,
        setFatal,
        endCursor
      );
      const pageInfo = userReposPage.pageInfo;
      let nodes = userReposPage.nodes;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
      if (timeRange.isTimeRangeSelected) {
        const start = new Date(timeRange.startDate);
        const end = new Date(timeRange.endDate);
        nodes = nodes.filter((repo: any) => {
          const createdAt = new Date(repo.createdAt);
          return createdAt >= start && createdAt <= end;
        });
      }
      repoCnt += nodes.length;
      const { selectedSize: pageSelectedSize, totalSize: pageTotalSize } =
        calLangStats(nodes, selectedLangs, userLangs);
      selectedSize += pageSelectedSize;
      totalSize += pageTotalSize;
    } while (hasNextPage);

    updateTableData(index, startColumn, repoCnt.toString() || "N/A");
    updateTableData(index, startColumn + 1, totalSize.toString() || "N/A");
    updateTableData(index, startColumn + 2, selectedSize.toString() || "N/A");
    updateTableData(index, startColumn + 3, userLangs.size.toString() || "N/A");

    return { userLangs, repoCnt };
  };

  async function countInTime(
    key: keyof typeof fetchFunctions,
    handleWaitTime: any,
    githubID: string,
    setFatal: any,
    start: Date | null,
    end: Date | null
  ): Promise<number> {
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    let ccCnt: number = 0;
    do {
      let response = await fetchWithRateLimit(
        fetchFunctions[key],
        handleWaitTime,
        githubID,
        setFatal
      );
      const { nodes, pageInfo } = response;
      nodes.forEach((node: any) => {
        const createdAt = new Date(node.createdAt);
        if (start && end && (createdAt < start || createdAt > end)) {
          return;
        }
        ccCnt++;
      });
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;
    } while (hasNextPage);
    return ccCnt;
  }

  const totalContriID = async (githubID: string, i: number) => {
    let profile = await fetchWithRateLimit(
      fetchFunctions["Profile"],
      handleWaitTime,
      githubID,
      setFatal
    );
    if (profile.error) {
      setInvalidIDs((prevInvalidIDs) => [...prevInvalidIDs, profile.message]);
      globalThis.invalidCount += 1;
      return;
    }
    addLoadingRow(setTableData, tableHeader.length);
    setAvatarMap((prevAvatarMap) => ({
      ...prevAvatarMap,
      [githubID]: profile.avatarUrl,
    }));

    updateTableData(i - 1, 0, githubID);

    if (!timeRange.isTimeRangeSelected) {
      let userContribution = await fetchWithRateLimit(
        fetchFunctions["Contributions"],
        handleWaitTime,
        githubID,
        setFatal
      );

      updateProfileData(i - 1, profile, userContribution);

      const userALangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Owned Original Repo",
        24
      );
      const userBLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Owned Forked Repo",
        28
      );
      const userCLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Collaborating Original Repo",
        32
      );
      const userDLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Collaborating Forked Repo",
        36
      );

      const totalLangs = new Set([
        ...userALangs.userLangs,
        ...userBLangs.userLangs,
        ...userCLangs.userLangs,
        ...userDLangs.userLangs,
      ]);
      updateTableData(i - 1, 40, totalLangs.size.toString() || "N/A");
    } else {
      const start = new Date(timeRange.startDate);
      const end = new Date(timeRange.endDate);
      let userContribution = await fetchWithRateLimit(
        fetchFunctions["Contributions"],
        handleWaitTime,
        githubID,
        setFatal,
        timeRange.startDate,
        timeRange.endDate
      );
      updateProfileDataTime(i - 1, profile, userContribution, end);

      const list = [
        "Commit Comments",
        "Gist Comments",
        "Issue Comments",
        "Repository Discussion Comments",
        "Gists",
        "Issues",
        "Pull Requests",
        "Repository Discussions",
      ];

      for (const contributionType of list) {
        const ccIndex = getHeaderIndex(tableHeader, contributionType);
        const ccCnt = await countInTime(
          "Commit Comments",
          handleWaitTime,
          githubID,
          setFatal,
          start,
          end
        );
        updateTableData(i - 1, ccIndex, ccCnt.toString() || "N/A");
      }
      const userALangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Owned Original Repo",
        24
      );
      const userBLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Owned Forked Repo",
        28
      );
      const userCLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Collaborating Original Repo",
        32
      );
      const userDLangs = await fetchAndProcessRepos(
        githubID,
        i - 1,
        "Collaborating Forked Repo",
        36
      );

      const totalLangs = new Set([
        ...userALangs.userLangs,
        ...userBLangs.userLangs,
        ...userCLangs.userLangs,
        ...userDLangs.userLangs,
      ]);
      const repoCnt =
        userALangs.repoCnt +
        userBLangs.repoCnt +
        userCLangs.repoCnt +
        userDLangs.repoCnt;
      updateTableData(i - 1, 40, totalLangs.size.toString() || "N/A");
      updateTableData(i - 1, 18, repoCnt.toString());
    }
    loadRateLimit();
  };

  const queryTotalContrib = async (data: string[][], signal: AbortSignal) => {
    globalThis.invalidCount = 0;
    for (let i = 1; i < data.length; i++) {
      if (signal.aborted) {
        break;
      }
      const githubID = data[i][0];
      await totalContriID(githubID, i - globalThis.invalidCount);
    }
  };

  const specificContribID = async (
    githubID: string,
    key: FetchFunctionKeys,
    start: Date | null,
    end: Date | null,
    rowIndex: { value: number }
  ) => {
    let profile = await fetchWithRateLimit(
      fetchFunctions["Profile"],
      handleWaitTime,
      githubID,
      setFatal
    );
    if (profile.error) {
      setInvalidIDs((prevInvalidIDs) => [...prevInvalidIDs, profile.message]);
      return;
    }
    setAvatarMap((prevAvatarMap) => ({
      ...prevAvatarMap,
      [githubID]: profile.avatarUrl,
    }));

    let endCursor: string | null = null;
    let hasNextPage: boolean = false;
    let hasContributions = false;
    let inTimeRange = false;

    do {
      let response = await fetchWithRateLimit(
        fetchFunctions[key],
        handleWaitTime,
        githubID,
        setFatal,
        endCursor
      );
      const { nodes, pageInfo } = response;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;

      if (nodes.length === 0) {
        addNARow(setTableData, tableHeader.length);
        updateTableData(rowIndex.value, 0, githubID);
        rowIndex.value++;
        break;
      }

      hasContributions = true;
      nodes.forEach((node: any) => {
        if (timeRange.isTimeRangeSelected) {
          const createdAt = new Date(node.createdAt);
          if (start && end && (createdAt < start || createdAt > end)) {
            return;
          }
        }
        inTimeRange = true;
        addLoadingRow(setTableData, tableHeader.length);
        updateTableData(rowIndex.value, 0, githubID);
        tableHeader.forEach((header, index) => {
          if (index === 0) return; // Skip GitHub ID column
          const value =
            header === "Primary Language"
              ? node.primaryLanguage?.name || "N/A"
              : header === "Language Stats"
              ? JSON.stringify(
                  node.languages.edges.reduce((acc: any, item: any) => {
                    const key = item.node.name;
                    const value = item.size;
                    if (!acc[key]) {
                      acc[key] = 0;
                    }
                    acc[key] += value;
                    return acc;
                  }, {})
                )
              : node[toCamelCase(header)] || "N/A";
          updateTableData(rowIndex.value, index, value);
        });
        rowIndex.value++;
      });
    } while (hasNextPage);

    if (timeRange.isTimeRangeSelected && hasContributions && !inTimeRange) {
      addNARow(setTableData, tableHeader.length);
      updateTableData(rowIndex.value, 0, githubID);
      rowIndex.value++;
    }
    loadRateLimit();
  };

  const querySpecificContrib = async (
    data: string[][],
    signal: AbortSignal
  ) => {
    const key: FetchFunctionKeys = selectedContribution as FetchFunctionKeys;
    const start = timeRange.isTimeRangeSelected
      ? new Date(timeRange.startDate)
      : null;
    const end = timeRange.isTimeRangeSelected
      ? new Date(timeRange.endDate)
      : null;
    let rowIndex = { value: 0 };
    for (let i = 1; i < data.length; i++) {
      if (signal.aborted) {
        break;
      }
      const githubID = data[i][0];
      await specificContribID(githubID, key, start, end, rowIndex);
    }
  };

  const validateInputs = () => {
    let isValid = true;
    const newErrors: { [key: string]: string } = {};
    if (queryOption === "totalContributions" && selectedLangs.size === 0) {
      newErrors.langs = "No languages selected";
      isValid = false;
    } else if (
      queryOption === "specificContributions" &&
      selectedContribution === ""
    ) {
      newErrors.contrib = "No contribution selected";
      isValid = false;
    }

    if (timeRange.isTimeRangeSelected && timeRange.startDate === "") {
      newErrors.startDate = "Start date not selected";
      isValid = false;
    }

    if (
      timeRange.isTimeRangeSelected &&
      timeRange.endDate === "" &&
      !timeRange.isPresent
    ) {
      newErrors.endDate = "End date not selected";
      isValid = false;
    }

    if (!inputOption && !file) {
      newErrors.file = "No file selected";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async () => {
    if (!validateInputs()) {
      return;
    }
    if (!inputOption) {
      if (file) {
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
      }
      setLoading(true);
      setShowTable(true);
      const signal = abortControllerRef.current?.signal;
      if (file) {
        try {
          const result = await parseCSV(file);
          if (queryOption === "totalContributions") {
            await queryTotalContrib(result.data, signal!);
          } else if (queryOption === "specificContributions") {
            await querySpecificContrib(result.data, signal!);
          }
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
        setLoading(false);
      }
    } else {
      if (githubId === "") {
        setErrors((prevErrors) => ({
          ...prevErrors,
          githubId: "No GitHub ID entered",
        }));
        return;
      }
      if (!isValidGitHubId(githubId)) {
        setErrors((prevErrors) => ({
          ...prevErrors,
          githubId: "Invalid GitHub ID entered",
        }));
        return;
      }
      setLoading(true);
      setShowTable(true);
      try {
        if (queryOption === "totalContributions") {
          await totalContriID(githubId, 1);
        } else if (queryOption === "specificContributions") {
          const key: FetchFunctionKeys =
            selectedContribution as FetchFunctionKeys;
          const start = timeRange.isTimeRangeSelected
            ? new Date(timeRange.startDate)
            : null;
          const end = timeRange.isTimeRangeSelected
            ? new Date(timeRange.endDate)
            : null;
          let rowIndex = { value: 0 };

          await specificContribID(githubId, key, start, end, rowIndex);
        }
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
      let fileName = "";
      if (queryOption === "totalContributions") {
        fileName = "total_contributions.csv";
      } else if (queryOption === "specificContributions") {
        fileName = `${selectedContribution
          .replace(/ /g, "_")
          .toLowerCase()}_contributions.csv`;
      }
      downloadCsv(csvContent, fileName);
    } else {
      alert("No contributions to export");
    }
  };

  const handleBackToOptions = () => {
    setInvalidIDs([]);
    setAvatarMap({});
    setShowTable(false);
    setTableData([]);
    setErrors({});
    setFile(null);
    setSelectedLangs(new Set());
    setSelectedContribution("");
    setTimeRange({
      isTimeRangeSelected: false,
      startDate: "",
      endDate: "",
      isPresent: false,
    });
  };

  const handleCloseModal = () => {
    setIsModalVisible(false);
  };

  const handleSave = async (name: string) => {
    const response = await checkDuplicate(
      {
        name,
        type:
          queryOption === "totalContributions" ? "total" : selectedContribution,
      },
      setFatal
    );

    if (response.exists) {
      setErrorMessage(
        "A dataset of this type with this name already exists. Please choose a different name."
      );
      setIsPromptOpen(true);
    } else {
      setErrorMessage(null);
      let langs = "";
      if (selectedLangs.size != 0) {
        langs = JSON.stringify(Array.from(selectedLangs));
        if (langs.includes("All")) {
          langs = JSON.stringify(["ALL"]);
        }
      }
      await saveToDatabase(
        {
          name,
          type:
            queryOption === "totalContributions"
              ? "total"
              : selectedContribution,
          tableHeader: tableHeader,
          tableData: tableData || [],
          ...(selectedLangs.size != 0 && { langs: langs }),
          startTime: timeRange.startDate,
          endTime: timeRange.endDate,
        },
        setFatal
      );
      setIsModalVisible(true);
      setErrorMessage(null);
    }
  };

  const totHistHeaders = tableHeader?.filter(
    (header) => numericalValue[header]
  );

  const totHistData = castTableData(
    tableData?.map((row: string[]) =>
      Object.keys(numericalValue).map(
        (header: string) => row[tableHeader.indexOf(header)]
      )
    ) || []
  );

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
                Mine User GitHub Contributions
              </h2>
            </>
          ) : (
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              User{" "}
              {queryOption === "totalContributions"
                ? "Total GitHub"
                : selectedContribution}{" "}
              Contributions
              {loading && <Spinner />}
            </h2>
          )}
          {!showTable ? (
            <>
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="totalContributions"
                labelText="Query the total number of each type of GitHub contribution (e.g., commits, pull requests, issues, etc.) for the specified GitHub ID(s)."
              />
              <OptionSelector
                queryOption={queryOption}
                handleOptionChange={handleOptionChange}
                optionValue="specificContributions"
                labelText="Query and retrieve detailed information for a specific category of GitHub contributions (e.g., commit comments, pull requests, etc.) for the specified GitHub ID(s)."
              />
              <label className="text-white font-bold mb-2 block">
                Only interested in a single user?
              </label>
              <div className="flex items-center mb-2">
                <input
                  type="checkbox"
                  id="input"
                  checked={inputOption}
                  onChange={handleInputChange}
                  className="mr-2"
                />
                <label htmlFor="input" className="text-white">
                  Yes
                </label>
              </div>
              {inputOption && (
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
                  {errors.githubId && <ErrorMessage error={errors.githubId} />}
                </div>
              )}
              {!inputOption && (
                <>
                  <UploadSection
                    demoImage={githubIDs}
                    handleFileChange={handleFileChange}
                    title="Upload GitHub IDs"
                    description={gitHubCSV}
                  />
                  {queryOption === "totalContributions" && (
                    <div className="text-gray-300 mb-4">
                      Note: The rate limit of 5000 requests should be sufficient
                      to query the total contributions of over 200 average
                      GitHub users. However, in cases where a user has an
                      extensive and significant contribution history, the rate
                      limit consumption may increase. Additionally, querying
                      contributions for large number of users (i.e. 1000) at
                      once can exceed the rate limit. We recommend breaking your
                      input into smaller CSV files, each containing around 200
                      users, for optimal experience.
                    </div>
                  )}
                  {errors.file && <ErrorMessage error={errors.file} />}
                </>
              )}
              <div className="mb-6">
                <label className="text-white font-bold mb-2 block">
                  Are you interested in querying the user contributions in a
                  specific time period?
                </label>
                <div className="flex items-center mb-2">
                  <input
                    type="checkbox"
                    id="timeRange"
                    checked={timeRange.isTimeRangeSelected}
                    onChange={handleTimeRangeChange}
                    className="mr-2"
                  />
                  <label htmlFor="timeRange" className="text-white">
                    Yes
                  </label>
                </div>
                <p className="text-gray-300 text-sm">
                  If not selected, the app will collect all stats from the
                  account creation date until now. We recommend not selecting
                  this option unless you specifically need stats for a certain
                  period. Note that some data may not be available for a
                  specific period, they are the number of watchings, starred
                  Repos, followings, followers, and projects during that time.
                  If selected, the current implementation will query all
                  contributions from the account creation date and then filter
                  out those not within the selected period based on the{" "}
                  <span className="font-semibold text-white">"createdAt"</span>{" "}
                  field.{" "}
                  <span className="font-semibold text-white">
                    This process consumes more of the rate limit.
                  </span>
                </p>
              </div>
              {timeRange.isTimeRangeSelected && (
                <div className="mb-4">
                  <label className="text-white font-bold mb-2 block">
                    Select the time range:
                  </label>
                  <div className="flex items-center mb-4">
                    <div className="flex items-center mr-4">
                      <label htmlFor="startDate" className="text-white mr-2">
                        Start Date:
                      </label>
                      <input
                        type="date"
                        id="startDate"
                        value={timeRange.startDate}
                        onChange={handleStartDateChange}
                        className="p-2 rounded bg-gray-800 text-white"
                      />
                    </div>
                    <div className="flex items-center mr-4">
                      <label htmlFor="endDate" className="text-white mr-2">
                        End Date:
                      </label>
                      <input
                        type="date"
                        id="endDate"
                        value={timeRange.endDate}
                        onChange={handleEndDateChange}
                        className="p-2 rounded bg-gray-800 text-white"
                        disabled={timeRange.isPresent}
                      />
                    </div>
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="present"
                        checked={timeRange.isPresent}
                        onChange={handlePresentChange}
                        className="mr-2"
                      />
                      <label htmlFor="present" className="text-white">
                        Present
                      </label>
                    </div>
                  </div>
                </div>
              )}
              {errors.startDate && <ErrorMessage error={errors.startDate} />}
              {errors.endDate && <ErrorMessage error={errors.endDate} />}
              {queryOption === "totalContributions" && (
                <SelectionSection
                  title="Select Languages:"
                  description={langsDesc}
                  items={languageChunks}
                  selectedItems={selectedLangs}
                  handleChange={handleLanguageChange}
                  isCheckbox={true}
                />
              )}
              {errors.langs && <ErrorMessage error={errors.langs} />}
              {queryOption === "specificContributions" && (
                <SelectionSection
                  title="Select Contribution:"
                  description={contribsDesc}
                  items={contributionChunks}
                  selectedItems={selectedContribution}
                  handleChange={handleContributionChange}
                  isCheckbox={false}
                />
              )}
              {errors.contrib && <ErrorMessage error={errors.contrib} />}
              <Button
                handleAction={handleSubmit}
                text={"Submit"}
                disabled={loading}
              />
            </>
          ) : (
            <>
              {tableData.length > 0 && (
                <>
                  {!loading && queryOption === "totalContributions" && (
                    <TotalHistogram
                      headers={totHistHeaders}
                      data={totHistData}
                    />
                  )}

                  {!loading && repoTypes.includes(selectedContribution) && (
                    <RepoHistPie headers={tableHeader} data={tableData} />
                  )}

                  {!loading &&
                    !repoTypes.includes(selectedContribution) &&
                    queryOption === "specificContributions" && (
                      <>
                        <h2 className="text-xl font-bold text-white text-center">
                          Number of {selectedContribution} by GitHub ID
                        </h2>
                        <Histogram headers={tableHeader} data={tableData} />
                      </>
                    )}
                </>
              )}
              <Table
                headers={tableHeader}
                data={tableData}
                columnWidth="150px"
                avatar={avatarMap}
                columnSelection={false}
                noRateLimit={noRateLimit}
                remainingTime={remTime}
                totalTime={totTime}
              />
              {invalidIDs.length > 0 && (
                <ErrorMessage
                  error={
                    "The following GitHub ID(s) do not exist: " +
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
                    errorMessage={errorMessage}
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
