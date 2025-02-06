import React, { useState, useEffect } from "react";
import Select from "react-select";
import { COLORS } from "../constants/constants";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

interface GraphComponentProps {
  headers: string[];
  data: (string | number | JSX.Element)[][];
}

interface AggregatedData {
  lang: string;
  additions: number;
  deletions: number;
}

const getColor = (index: number) => COLORS[index % COLORS.length];

const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}: any) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
    >
      {`${(percent * 100).toFixed(1)}%`}
    </text>
  );
};

const UserCommitsHistPie: React.FC<GraphComponentProps> = ({
  headers,
  data,
}) => {
  const [selectedAuthor, setSelectedAuthor] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [selectedRepo, setSelectedRepo] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [selectedBranch, setSelectedBranch] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [aggregatedData, setAggregatedData] = useState<AggregatedData[]>([]);
  const getHeaderIndex = (headers: string[], field: string): number => {
    return headers.indexOf(field);
  };
  const authorIndex = getHeaderIndex(headers, "Author Login");
  const repoIndex = getHeaderIndex(headers, "Repository");
  const branchIndex = getHeaderIndex(headers, "Branch");
  const langIndex = getHeaderIndex(headers, "Languages");

  const authors = Array.from(
    new Set(data.map((commit) => commit[authorIndex] as string))
  ).map((author) => ({ value: author, label: author }));

  const repos = selectedAuthor
    ? Array.from(
        new Set(
          data
            .filter(
              (commit) =>
                commit[authorIndex] === selectedAuthor.value &&
                commit[repoIndex] !== "N/A"
            )
            .map((commit) => commit[repoIndex] as string)
        )
      ).map((repo) => ({ value: repo, label: repo }))
    : [];

  const branches =
    selectedRepo && selectedAuthor
      ? Array.from(
          new Set(
            data
              .filter(
                (commit) =>
                  commit[repoIndex] === selectedRepo.value &&
                  commit[authorIndex] === selectedAuthor.value
              )
              .map((commit) => commit[branchIndex] as string)
          )
        ).map((branch) => ({ value: branch, label: branch }))
      : [];

  const handleAuthorChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedAuthor(selectedOption);
    setSelectedRepo(null);
    setSelectedBranch(null);
  };

  const handleRepoChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedRepo(selectedOption);
    setSelectedBranch(null);
  };

  const handleBranchChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedBranch(selectedOption);
  };

  const aggregateData = (
    repo: string,
    branch: string,
    author: string
  ): AggregatedData[] => {
    const filteredData = data.filter(
      (commit) =>
        commit[repoIndex] === repo &&
        commit[branchIndex] === branch &&
        commit[authorIndex] === author
    );
    const aggregation = filteredData.reduce((acc, commit) => {
      const lang_stats = JSON.parse(commit[langIndex] as string);
      Object.keys(lang_stats).forEach((key) => {
        if (!acc[key]) {
          acc[key] = {
            lang: key,
            additions: lang_stats[key]["additions"],
            deletions: lang_stats[key]["deletions"],
          };
        } else {
          acc[key].additions += lang_stats[key]["additions"];
          acc[key].deletions += lang_stats[key]["deletions"];
        }
      });
      return acc;
    }, {} as Record<string, AggregatedData>);

    return Object.values(aggregation);
  };

  useEffect(() => {
    if (selectedRepo && selectedAuthor && selectedBranch) {
      const data = aggregateData(
        selectedRepo.value,
        selectedBranch.value,
        selectedAuthor.value
      );
      setAggregatedData(data);
    } else {
      setAggregatedData([]);
    }
  }, [selectedBranch, selectedAuthor, selectedRepo]);

  const formatXAxis = (tickItem: string) => {
    return tickItem.length > 8 ? `${tickItem.slice(0, 5)}...` : tickItem;
  };

  const formatYAxis = (tickItem: number) => {
    return tickItem >= 1000000
      ? tickItem.toExponential(2)
      : tickItem.toLocaleString();
  };

  const sortedAdditionsData = aggregatedData
    .filter((item) => item.additions > 0)
    .sort((a, b) => b.additions - a.additions);

  const sortedDeletionsData = aggregatedData
    .filter((item) => item.deletions > 0)
    .sort((a, b) => b.deletions - a.deletions);

  return (
    <div className="bg-gray-800 rounded-lg shadow-md">
      <div className="mb-4">
        <label className="mr-2 text-white font-bold">Select User:</label>
        <Select
          value={selectedAuthor}
          onChange={handleAuthorChange}
          options={authors}
          placeholder="Select an User"
          className="mb-4"
        />
        {selectedAuthor && (
          <>
            <label className="mr-2 text-white font-bold">
              Select Repository:
            </label>
            <Select
              value={selectedRepo}
              onChange={handleRepoChange}
              options={repos}
              placeholder="Select a repository"
              className="mb-4"
            />
          </>
        )}
        {selectedRepo && (
          <>
            <label className="mr-2 text-white font-bold">Select Branch:</label>
            <Select
              value={selectedBranch}
              onChange={handleBranchChange}
              options={branches}
              placeholder="Select a branch"
            />
          </>
        )}
      </div>
      {aggregatedData.length > 0 && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {sortedAdditionsData.length > 0 && (
            <div style={{ width: "100%", marginBottom: "2rem" }}>
              <h3 className="text-2xl font-bold text-white text-center">
                Additions by Languages
              </h3>
              <div style={{ overflowX: "auto" }}>
                <div
                  style={{
                    width: `${Math.max(
                      sortedAdditionsData.length * 120,
                      200
                    )}px`,
                    margin: "0 auto",
                  }}
                >
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={sortedAdditionsData} margin={{ left: 10 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="lang"
                        stroke="#ffffff"
                        tickFormatter={formatXAxis}
                        textAnchor="middle"
                      />
                      <YAxis stroke="#ffffff" tickFormatter={formatYAxis} />
                      <Tooltip />
                      <Bar dataKey="additions">
                        {sortedAdditionsData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={getColor(index)} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}
          {sortedDeletionsData.length > 0 && (
            <div style={{ width: "100%", marginBottom: "2rem" }}>
              <h3 className="text-2xl font-bold text-white text-center">
                Deletions by Languages
              </h3>
              <div style={{ overflowX: "auto" }}>
                <div
                  style={{
                    width: `${Math.max(
                      sortedDeletionsData.length * 120,
                      200
                    )}px`,
                    margin: "0 auto",
                  }}
                >
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={sortedDeletionsData} margin={{ left: 10 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="lang"
                        stroke="#ffffff"
                        tickFormatter={formatXAxis}
                        textAnchor="middle"
                      />
                      <YAxis stroke="#ffffff" tickFormatter={formatYAxis} />
                      <Tooltip />
                      <Bar dataKey="deletions">
                        {sortedDeletionsData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={getColor(index)} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              width: "100%",
            }}
          >
            {sortedAdditionsData.length > 0 && (
              <div>
                <h3 className="text-2xl font-bold text-white text-center">
                  Additions by Languages
                </h3>
                <PieChart width={400} height={400}>
                  <Pie
                    data={sortedAdditionsData.map((item) => ({
                      name: item.lang,
                      value: item.additions,
                    }))}
                    cx="50%"
                    cy="50%"
                    label={renderCustomizedLabel}
                    labelLine={false}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {sortedAdditionsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={getColor(index)} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </div>
            )}
            {sortedDeletionsData.length > 0 && (
              <div>
                <h3 className="text-2xl font-bold text-white text-center">
                  Deletions by Languages
                </h3>
                <PieChart width={400} height={400}>
                  <Pie
                    data={sortedDeletionsData.map((item) => ({
                      name: item.lang,
                      value: item.deletions,
                    }))}
                    cx="50%"
                    cy="50%"
                    label={renderCustomizedLabel}
                    labelLine={false}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {sortedDeletionsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={getColor(index)} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default UserCommitsHistPie;
