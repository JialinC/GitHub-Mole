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
  author: string;
  additions: number;
  deletions: number;
  commits: number;
}

const getColor = (index: number) => COLORS[index % COLORS.length];

const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
  index,
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

const CommitsHistPie: React.FC<GraphComponentProps> = ({ headers, data }) => {
  const [selectedRepo, setSelectedRepo] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [selectedBranch, setSelectedBranch] = useState<{
    value: string;
    label: string;
  } | null>({ value: "ALL", label: "ALL" });
  const [aggregatedData, setAggregatedData] = useState<AggregatedData[]>([]);
  const getHeaderIndex = (headers: string[], field: string): number => {
    return headers.indexOf(field);
  };
  const repoIndex = getHeaderIndex(headers, "Repository");
  const branchIndex = getHeaderIndex(headers, "Branch");
  const authorIndex = getHeaderIndex(headers, "Author");
  const loginIndex = getHeaderIndex(headers, "Author Login");
  const addIndex = getHeaderIndex(headers, "Additions");
  const delIndex = getHeaderIndex(headers, "Deletions");

  const repos = Array.from(
    new Set(data.map((commit) => commit[repoIndex] as string))
  ).map((repo) => ({ value: repo, label: repo }));

  const branches = selectedRepo
    ? Array.from(
        new Set(
          data
            .filter((commit) => commit[repoIndex] === selectedRepo.value)
            .map((commit) => commit[branchIndex] as string)
        )
      ).map((branch) => ({ value: branch, label: branch }))
    : [];

  const handleRepoChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedRepo(selectedOption);
    setSelectedBranch({ value: "ALL", label: "ALL" });
  };

  const handleBranchChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedBranch(selectedOption);
  };

  const aggregateData = (repo: string, branch: string): AggregatedData[] => {
    const filteredData = data.filter(
      (commit) =>
        commit[repoIndex] === repo &&
        (branch === "ALL" || commit[branchIndex] === branch)
    );

    const aggregation = filteredData.reduce((acc, commit) => {
      const authorLogin = commit[loginIndex] as string;
      const author = commit[authorIndex] as string;
      const key = authorLogin !== "N/A" ? authorLogin : author;

      if (!acc[key]) {
        acc[key] = { author: key, additions: 0, deletions: 0, commits: 0 };
      }

      acc[key].additions += commit[addIndex] as number;
      acc[key].deletions += commit[delIndex] as number;
      acc[key].commits += 1;

      return acc;
    }, {} as Record<string, AggregatedData>);

    return Object.values(aggregation);
  };

  useEffect(() => {
    if (selectedRepo) {
      const data = aggregateData(
        selectedRepo.value,
        selectedBranch?.value || "ALL"
      );
      setAggregatedData(data);
    } else {
      setAggregatedData([]);
    }
  }, [selectedRepo, selectedBranch]);

  const formatXAxis = (tickItem: string) => {
    return tickItem.length > 9 ? `${tickItem.slice(0, 6)}...` : tickItem;
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

  const sortedCommitsData = aggregatedData
    .filter((item) => item.commits > 0)
    .sort((a, b) => b.commits - a.commits);

  return (
    <div className="bg-gray-800 rounded-lg shadow-md">
      <div className="mb-4">
        <label className="mr-2 text-white font-bold">Select Repository:</label>
        <Select
          value={selectedRepo}
          onChange={handleRepoChange}
          options={repos}
          placeholder="Select a repository"
          className="mb-4"
        />
        {selectedRepo && (
          <>
            <label className="mr-2 text-white font-bold">Select Branch:</label>
            <Select
              value={selectedBranch}
              onChange={handleBranchChange}
              options={[{ value: "ALL", label: "ALL" }, ...branches]}
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
          <div style={{ width: "100%", marginBottom: "2rem" }}>
            <h3 className="text-2xl font-bold text-white text-center">
              Additions by Author
            </h3>
            <div style={{ overflowX: "auto" }}>
              <div
                style={{
                  width: `${Math.max(sortedAdditionsData.length * 120, 200)}px`,
                  margin: "0 auto",
                }}
              >
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={sortedAdditionsData} margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="author"
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
          <div style={{ width: "100%", marginBottom: "2rem" }}>
            <h3 className="text-2xl font-bold text-white text-center">
              Deletions by Author
            </h3>
            <div style={{ overflowX: "auto" }}>
              <div
                style={{
                  width: `${Math.max(sortedDeletionsData.length * 120, 200)}px`,
                  margin: "0 auto",
                }}
              >
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={sortedDeletionsData} margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="author"
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
          <div style={{ width: "100%", marginBottom: "2rem" }}>
            <h3 className="text-2xl font-bold text-white text-center">
              Commits by Author
            </h3>
            <div style={{ overflowX: "auto" }}>
              <div
                style={{
                  width: `${Math.max(sortedCommitsData.length * 100, 200)}px`,
                  margin: "0 auto",
                }}
              >
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={sortedCommitsData} margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="author"
                      stroke="#ffffff"
                      tickFormatter={formatXAxis}
                      textAnchor="middle"
                    />
                    <YAxis stroke="#ffffff" tickFormatter={formatYAxis} />
                    <Tooltip />
                    <Bar dataKey="commits">
                      {sortedCommitsData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getColor(index)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              width: "100%",
            }}
          >
            <div>
              <h3 className="text-2xl font-bold text-white text-center">
                Additions by Author
              </h3>
              <PieChart width={400} height={400}>
                <Pie
                  data={sortedAdditionsData.map((item) => ({
                    name: item.author,
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
            <div>
              <h3 className="text-2xl font-bold text-white text-center">
                Deletions by Author
              </h3>
              <PieChart width={400} height={400}>
                <Pie
                  data={sortedDeletionsData.map((item) => ({
                    name: item.author,
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
            <div>
              <h3 className="text-2xl font-bold text-white text-center">
                Commits by Author
              </h3>
              <PieChart width={400} height={400}>
                <Pie
                  data={sortedCommitsData.map((item) => ({
                    name: item.author,
                    value: item.commits,
                  }))}
                  cx="50%"
                  cy="50%"
                  label={renderCustomizedLabel}
                  labelLine={false}
                  outerRadius={150}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sortedCommitsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getColor(index)} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CommitsHistPie;
