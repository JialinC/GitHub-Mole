import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Button from "../components/Button";
import ViewTable from "../components/ViewTable";
import Histogram from "../components/Histogram";
import TotalHistogram from "../components/TotalHistogram";
import RepoHistPie from "../components/RepoHistPie";
import CommitsHistPie from "../components/CommitsHistPie";
import Modal from "../components/Modal";
import Footer from "../components/Footer";
import ErrorPage from "../components/Error";
import {
  userQueryHeaders,
  viewTableHeaders,
  headerToFieldMap,
  numericalValue,
} from "../constants/constants";
import {
  getUserAvatarUrl,
  generateCsvContent,
  downloadCsv,
} from "../utils/helpers";
import {
  fetchRateLimit,
  fetchUserQueries,
  deleteUserQuery,
  fetchUserContribution,
  deleteUserContribution,
} from "../utils/queries";

const History: React.FC = () => {
  const [fatal, setFatal] = useState<string | null>(null);
  const [tableData, setTableData] = useState<string[][] | null>(null);
  const [showContributions, setShowContributions] = useState(false);
  const [contributionHeaders, setContributionHeaders] = useState<string[]>([]);
  const [contributions, setContributions] = useState<string[][] | null>(null);
  const [contribType, setContribType] = useState<string | null>(null);
  const [histHeader, setHistHeader] = useState<string[]>([]);
  const [histData, setHistData] = useState<string[][]>([[]]);

  const [modal, setModal] = useState<{ [key: string]: any }>({
    isVisible: false,
    title: "",
    message: "",
    success: false,
  });

  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const tableHeaders = [...userQueryHeaders, "Action"];

  const loadRateLimit = async () => {
    const rateLimitData = await fetchRateLimit(setFatal);
    setRateLimit(rateLimitData);
  };

  useEffect(() => {
    const fetchData = async () => {
      const avatarUrl = getUserAvatarUrl();
      if (avatarUrl) {
        setAvatarUrl(avatarUrl);
      }
      await loadRateLimit();
      await getUserQueries();
    };
    fetchData();
  }, []);

  const getUserQueries = async () => {
    const response = await fetchUserQueries(setFatal);
    const tableData = response.map((query: any) => [
      query.ds_name,
      query.data_type,
      query.start_time,
      query.end_time,
      query.queried_at,
      <>
        <button
          onClick={() => {
            fetchContributions(query.id, query.data_type);
          }}
          className="bg-green-500 text-white font-bold py-2 px-4 rounded mr-2 hover:bg-green-700 transition duration-150"
        >
          View
        </button>
        <button
          onClick={() => {
            deleteQuery(query.id);
          }}
          className="bg-red-500 text-white font-bold py-2 px-4 rounded hover:bg-red-700 transition duration-150"
        >
          Delete
        </button>
      </>,
    ]);
    setTableData(tableData);
  };

  const fetchContributions = async (queryId: string, data_type: string) => {
    const response = await fetchUserContribution(queryId, setFatal);
    let headers = viewTableHeaders[data_type];
    const tableData = response.map((contribution: any) => [
      ...headers.map((header) => contribution[headerToFieldMap[header]]),
      <button
        onClick={() => {
          deleteContribution(queryId, data_type, contribution.id);
        }}
        className="bg-red-500 text-white font-bold py-2 px-4 rounded hover:bg-red-700 transition duration-150"
      >
        Delete
      </button>,
    ]);
    headers = [...headers, "Action"];
    setContribType(data_type === "total" ? "Total Contributions" : data_type);
    setHistHeader(headers.filter((header) => numericalValue[header]));
    setHistData(
      tableData?.map((row: string[]) =>
        Object.keys(numericalValue).map(
          (header: string) => row[headers.indexOf(header)]
        )
      )
    );
    setContributionHeaders(headers);
    setContributions(tableData);
    setShowContributions(true);
  };

  const deleteQuery = async (queryId: string) => {
    await deleteUserQuery(queryId, setFatal);
    await getUserQueries();
    setModal({
      isVisible: true,
      title: "Success",
      message: "Data saved successfully.",
      success: true,
    });
  };

  const deleteContribution = async (
    queryId: string,
    type: string,
    contributionId: string
  ) => {
    await deleteUserContribution(queryId, contributionId, setFatal);
    await fetchContributions(queryId, type);
    setModal({
      isVisible: true,
      title: "Success",
      message: "Data deleted successfully.",
      success: true,
    });
  };

  const handleExport = () => {
    if (contributions) {
      const csvContent = generateCsvContent(
        contributionHeaders.slice(0, -1),
        contributions.map((row) => row.slice(0, -1))
      );
      downloadCsv(csvContent, contribType + ".csv");
    } else {
      alert("No contributions to export");
    }
  };

  const handleBackClick = () => {
    setShowContributions(false);
    setContributions([]);
  };

  const handleCloseModal = () => {
    setModal({
      isVisible: false,
      title: "",
      message: "",
      success: false,
    });
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
          <h2 className="text-2xl font-bold text-white mb-4">
            {showContributions ? contribType : "User Queries"}
          </h2>
          {tableData ? (
            showContributions && contributions ? (
              <>
                {contribType === "Repositories" ? (
                  <RepoHistPie
                    headers={contributionHeaders.slice(0, -1)}
                    data={contributions}
                  />
                ) : contribType === "Commits" ? (
                  <CommitsHistPie
                    headers={contributionHeaders.slice(0, -1)}
                    data={contributions}
                  />
                ) : contribType === "Total Contributions" ? (
                  <TotalHistogram headers={histHeader} data={histData} />
                ) : (
                  <>
                    <h3 className="text-2xl font-bold text-white text-center">
                      Number of {contribType} by GitHub ID
                    </h3>
                    <Histogram data={contributions} />
                  </>
                )}
                <ViewTable
                  headers={contributionHeaders}
                  data={contributions}
                  cellWidth="150px"
                />
                <Button handleAction={handleExport} text={"Export Dataset"} />
                <Button
                  handleAction={handleBackClick}
                  text={"View Another Dataset"}
                />
              </>
            ) : (
              <ViewTable
                headers={tableHeaders}
                data={tableData}
                cellWidth="150px"
              />
            )
          ) : (
            <div className="flex justify-center items-center h-40">
              <div className="animate-spin rounded-full h-8 w-8 border-4 border-t-4 border-t-white border-gray-500"></div>
            </div>
          )}
          {modal.isVisible && (
            <Modal
              title={modal.title}
              message={modal.message}
              onClose={handleCloseModal}
              success={modal.success}
            />
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default History;
