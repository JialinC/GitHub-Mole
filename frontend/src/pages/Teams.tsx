import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";

import ava from "../assets/app_logo.png";
import githubIDs from "../assets/github_ids.png";
import selfData from "../assets/self_data.png";

import Button from "../components/Button";
import ErrorMessage from "../components/ErrorMessage";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import OptionSelector from "../components/OptionSelector";
import SelectionSection from "../components/SelectionSection";
import Spinner from "../components/Spinner";
import Table from "../components/Table";
import TotalHistogram from "../components/TotalHistogram";
import UploadSection from "../components/UploadSection";

import { gitHubCSV, langsDesc, selfDataFile } from "../constants/Descriptions";
import { languages, teamTableHeaders } from "../constants/constants";

import {
  addLoadingRow,
  calLangStats,
  calculateLifetime,
  castTableData,
  chunkArray,
  fetchWithRateLimit,
  getUserAvatarUrl,
  handleFileChange as handleFileChangeUtil,
  handleWaitTime as handleWaitTimeUtil,
  parseCSV,
  validateGitHubIdsFile,
  validateSelfDataFile,
} from "../utils/helpers";
import {
  fetchARepos,
  fetchContributions,
  fetchProfile,
  fetchRateLimit,
  formTeam,
} from "../utils/queries";

import "../styles/styles.css";
import { Stringifier } from "postcss";

const Teams: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [fatal, setFatal] = useState<string | null>(null);
  const [invalidIDs, setInvalidIDs] = useState<string[]>([]);

  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const navigate = useNavigate();
  const [uploadOption, setUploadOption] = useState<string>("githubIds");
  const [selectedLangs, setSelectedLangs] = useState<Set<string>>(new Set());

  const [noRateLimit, setNoRateLimit] = useState<boolean>(false);
  const [totTime, setTotTime] = useState<number>(1000);
  const [remTime, setRemTime] = useState<number>(1000 - 1);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [showTable, setShowTable] = useState<boolean>(false);
  const [tableHeader, setTableHeader] = useState<string[]>(teamTableHeaders);
  const [tableData, setTableData] = useState<string[][] | null>([]);
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [teamSize, setTeamSize] = useState<number>(0);
  const [allowExceed, setAllowExceed] = useState<boolean>(true);
  const [teams, setTeams] = useState<{
    [key: string]: { id: string; type: string }[];
  }>({});
  const [leftOvers, setLeftOvers] = useState<{ id: string; type: string }[]>(
    []
  );
  const [avatarMap, setAvatarMap] = useState<{ [key: string]: string }>({});
  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [processing, setProcessing] = useState<boolean>(true);

  const languageChunks = chunkArray(languages, Math.ceil(languages.length / 4));

  const loadRateLimit = async () => {
    const rateLimitData = await fetchRateLimit(setFatal);
    setRateLimit(rateLimitData);
  };

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

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setUploadOption(value);
    if (value === "ownDataset") {
      setTableHeader([]);
    } else {
      setTableHeader(teamTableHeaders);
    }
    setFile(null);
    setSelectedLangs(new Set());
    setTableData([]);
    setSelectedColumns([]);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    handleFileChangeUtil({ event, setErrors, setFile });
  };

  const handleLanguageChange = (language: string) => {
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

  const handleTeamSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTeamSize(Number(event.target.value));
  };

  const handleAllowExceedChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setAllowExceed(event.target.checked);
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

  const processGitHubID = async (githubID: string, i: number) => {
    let userProfile = await fetchWithRateLimit(
      fetchProfile,
      handleWaitTime,
      githubID,
      setFatal
    );
    if (userProfile.error) {
      setInvalidIDs((prevInvalidIDs) => [
        ...prevInvalidIDs,
        userProfile.message,
      ]);
      globalThis.invalidCount += 1;
      return;
    }
    addLoadingRow(setTableData, tableHeader.length);
    setAvatarMap((prevAvatarMap) => ({
      ...prevAvatarMap,
      [githubID]: userProfile.avatarUrl,
    }));
    updateTableData(i - 1, 0, githubID);
    updateTableData(
      i - 1,
      1,
      calculateLifetime(userProfile.created_at).toString()
    );

    let userContribution = await fetchWithRateLimit(
      fetchContributions,
      handleWaitTime,
      githubID,
      setFatal
    );
    updateTableData(i - 1, 2, userContribution.commit.toString());

    const totalComments =
      userProfile.commit_comments +
      userProfile.issue_comments +
      userProfile.gist_comments +
      userProfile.repository_discussion_comments;
    updateTableData(i - 1, 3, totalComments.toString());

    const issuesPRs = userProfile.issues + userProfile.pull_requests;
    updateTableData(i - 1, 4, issuesPRs.toString());
    let endCursor: string | null = null;
    let hasNextPage: boolean;
    let size: number = 0;
    const userLangs = new Set<string>();
    do {
      let userReposPage = await fetchWithRateLimit(
        fetchARepos,
        handleWaitTime,
        githubID,
        setFatal,
        endCursor
      );
      const pageInfo = userReposPage.pageInfo;
      endCursor = pageInfo?.endCursor || null;
      hasNextPage = pageInfo?.hasNextPage || false;

      const { selectedSize } = calLangStats(
        userReposPage.nodes,
        selectedLangs,
        userLangs
      );
      size += selectedSize;
    } while (hasNextPage);

    updateTableData(i - 1, 5, userLangs.size.toString());
    updateTableData(i - 1, 6, size.toString());
    updateTableData(i - 1, 7, userProfile.repositories.toString());
    loadRateLimit();
  };

  const processGitHubIDs = async (data: string[][], signal: AbortSignal) => {
    globalThis.invalidCount = 0;
    for (let i = 1; i < data.length; i++) {
      if (signal.aborted) {
        return;
      }
      const githubID = data[i][0];
      await processGitHubID(githubID, i - globalThis.invalidCount);
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
      if (uploadOption === "ownDataset") {
        await validateSelfDataFile(file);
      } else if (uploadOption === "githubIds") {
        await validateGitHubIdsFile(file);
      }
    } catch (error) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        file:
          error instanceof Error ? error.message : "An unknown error occurred",
      }));
      return;
    }

    setLoading(true);
    setShowTable(true);
    try {
      const result = await parseCSV(file);
      if (uploadOption === "ownDataset") {
        const data = result.data as string[][];
        const header = data[0];
        const body = data.slice(1);
        setTableHeader(header);
        setTableData(body);
      } else if (uploadOption === "githubIds") {
        await processGitHubIDs(result.data as string[][], signal!);
      }
    } catch (error) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        processing: "Error processing the input file",
      }));
    } finally {
      setLoading(false);
    }
  };

  const handleBackToOptions = () => {
    setInvalidIDs([]);
    setShowTable(false);
    setLoading(false);
    setTableData([]);
    setFile(null);
    setSelectedLangs(new Set());
    setUploadOption("githubIds");
    setErrors({});
    setTableHeader(teamTableHeaders);
    setSelectedColumns([]);
    setLeftOvers([]);
    setProcessing(true);
  };

  const handleColumnSelection = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const column = event.target.value;
    setSelectedColumns((prevSelectedColumns) =>
      event.target.checked
        ? [...prevSelectedColumns, column]
        : prevSelectedColumns.filter((col) => col !== column)
    );
  };

  const handleColumnSubmit = async () => {
    let error = false;
    if (!tableData || teamSize <= 0 || teamSize > tableData.length - 1) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        team: "Invalid team size. It must be greater than 0 and less than the number of rows in the uploaded file.",
      }));
      error = true;
    } else {
      setErrors((prevErrors) => ({ ...prevErrors, team: "" }));
    }
    console.log(selectedColumns, error);
    if (selectedColumns.length === 0) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        column: "Please select at least one column for team formation.",
      }));
      error = true;
    } else {
      setErrors((prevErrors) => ({ ...prevErrors, column: "" }));
    }
    if (error === true) {
      return;
    }

    setProcessing(true);
    const selectedData: { [key: string]: string[] } = {};
    const ids = tableData.map((row) => row[0]);
    selectedData[tableHeader[0]] = ids;
    selectedColumns.forEach((column) => {
      const columnIndex = tableHeader.indexOf(column);
      if (columnIndex !== -1) {
        const columnContent = tableData.slice(0).map((row) => row[columnIndex]);
        selectedData[column] = columnContent;
      }
    });
    const response = await formTeam(
      {
        columns: selectedData,
        teamSize,
        allowExceed,
      },
      setFatal
    );
    const teams = response.teams;
    const leftOvers = response.left_over ? response.left_over : [];
    setTeams(teams);
    setLeftOvers(leftOvers);
    setProcessing(false);
  };

  const handleExport = (data: object, filename: string = "data.json") => {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const castedTableData = tableData ? castTableData(tableData) : [];

  if (fatal) {
    return <ErrorPage message={fatal} />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar avatarUrl={avatarUrl} rateLimit={rateLimit}>
        <Link
          to="/dashboard"
          className="text-white mr-4 text-xl font-bold tracking-wide shadow-lg transition-transform transform hover:scale-105"
        >
          Dashboard
        </Link>
      </Navbar>
      <main className="flex-grow container mx-auto p-4">
        <div className="p-6 bg-gray-800 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
            Form Software Development Teams
            {loading && <Spinner />}
          </h2>
          {!showTable ? (
            <>
              <OptionSelector
                queryOption={uploadOption}
                handleOptionChange={handleOptionChange}
                optionValue="ownDataset"
                labelText="Upload a CSV file containing your own dataset"
              />
              <OptionSelector
                queryOption={uploadOption}
                handleOptionChange={handleOptionChange}
                optionValue="githubIds"
                labelText="Upload a CSV file containing a list of GitHub IDs"
              />
              {uploadOption === "ownDataset" && (
                <UploadSection
                  demoImage={selfData}
                  handleFileChange={handleFileChange}
                  title="Upload Data file"
                  description={selfDataFile}
                />
              )}
              {uploadOption === "githubIds" && (
                <UploadSection
                  demoImage={githubIDs}
                  handleFileChange={handleFileChange}
                  title="Upload GitHub ID file"
                  description={gitHubCSV}
                />
              )}
              {errors.file && <ErrorMessage error={errors.file} />}
              {uploadOption === "githubIds" && (
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
              <Button
                handleAction={handleSubmit}
                text={"Submit"}
                disabled={loading}
              />
            </>
          ) : (
            <>
              <div className="p-2 bg-gray-800 rounded-lg shadow-md">
                <label className="block text-white mb-2">
                  Team Size:
                  <input
                    type="number"
                    value={teamSize}
                    onChange={handleTeamSizeChange}
                    className="ml-2 p-2 rounded-lg bg-gray-800 text-white border border-gray-600"
                  />
                </label>
                {errors.team && <ErrorMessage error={errors.team} />}
              </div>
              <div className="p-2 bg-gray-800 rounded-lg shadow-md">
                <label className="block text-white mb-2">
                  <input
                    type="checkbox"
                    checked={allowExceed}
                    onChange={handleAllowExceedChange}
                    className="mr-2"
                  />
                  Allow teams to exceed the specified size.
                </label>
                <div className="text-white text-sm mb-2">
                  For example, if there are 10 candidates and teams are limited
                  to a size of 3, one candidate will remain unassigned. If this
                  option is enabled, the remaining candidates will be randomly
                  distributed among the existing teams.
                </div>
              </div>
              {!loading && (
                <TotalHistogram headers={tableHeader} data={castedTableData} />
              )}
              <Table
                headers={tableHeader}
                data={tableData}
                columnWidth="150px"
                avatar={avatarMap}
                columnSelection={true}
                handleColumnSelection={handleColumnSelection}
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
              {errors.column && <ErrorMessage error={errors.column} />}
              {errors.processing && <ErrorMessage error={errors.processing} />}
              {!loading && (
                <>
                  <Button
                    handleAction={handleColumnSubmit}
                    text={"Submit Selected Columns"}
                  />
                  <Button
                    handleAction={handleBackToOptions}
                    text={"Back to Upload Options"}
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
        <>
          {!processing && (
            <div className="mt-2 p-6 bg-gray-800 rounded-lg shadow-md mb-2">
              <h2 className="text-2xl font-bold text-white mb-4">
                Teams Formed Based on Selected Metrics:
              </h2>
              <div className="teams-container grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.keys(teams)
                  .sort(
                    (a, b) =>
                      parseInt(a.split(" ")[1]) - parseInt(b.split(" ")[1])
                  )
                  .map((teamName) => (
                    <div
                      key={teamName}
                      className="team-card bg-gray-600 p-6 rounded-lg shadow-lg mb-6 border border-gray-500 transform transition-transform hover:scale-105"
                    >
                      <h3 className="text-xl font-bold text-white mb-4">
                        {teamName}
                      </h3>
                      <div className="team-members">
                        {teams[teamName].map(
                          (member: { id: string; type: string }) => (
                            <div
                              key={member.id}
                              className="team-member flex items-center mb-4 p-2 bg-gray-800 rounded-lg"
                            >
                              <img
                                src={
                                  uploadOption === "githubIds"
                                    ? avatarMap[member.id]
                                    : ava
                                }
                                alt={`${member.id}'s avatar`}
                                className="avatar w-10 h-10 rounded-full mr-4 border-2 border-gray-600"
                              />
                              <div className="text-white">
                                <div className="font-semibold">
                                  GitHub: {member.id}
                                </div>
                                <div className="text-sm">
                                  Cluster: {member.type}
                                </div>
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  ))}
              </div>
              <Button
                handleAction={() => handleExport(teams, "teams.json")}
                text={"Export Teams"}
              />
            </div>
          )}
          {leftOvers && leftOvers.length > 0 && (
            <div className="mt-2 p-6 bg-gray-800 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold text-white mb-4">
                Leftover Members:
              </h2>
              <div className="leftovers-container grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {leftOvers.map((member: { id: string; type: string }) => (
                  <div
                    key={member.id}
                    className="leftover-member flex items-center mb-4 p-2 bg-gray-800 rounded-lg"
                  >
                    <img
                      src={
                        uploadOption === "githubIds"
                          ? avatarMap[member.id]
                          : ava
                      }
                      alt={`${member.id}'s avatar`}
                      className="avatar w-10 h-10 rounded-full mr-4 border-2 border-gray-600"
                    />
                    <div className="text-white">
                      <div className="font-semibold">GitHub: {member.id}</div>
                      <div className="text-sm">Cluster: {member.type}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      </main>
      <Footer />
    </div>
  );
};

export default Teams;
