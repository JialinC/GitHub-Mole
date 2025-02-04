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
  Legend,
} from "recharts";

interface GraphComponentProps {
  headers: string[];
  data: any[][];
}

const HistPie: React.FC<GraphComponentProps> = ({ headers, data }) => {
  const githubId = headers.indexOf("GitHub ID");
  const name = headers.indexOf("Name");
  const langs = headers.indexOf("Language Stats");

  const [selectedUser, setSelectedUser] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [selectedRepo, setSelectedRepo] = useState<{
    value: string;
    label: string;
  } | null>({ value: "ALL", label: "ALL" });
  const [sortedLanguageStats, setSortedLanguageStats] = useState<
    { name: string; value: number }[]
  >([]);

  const users = Array.from(new Set(data.map((row) => row[githubId]))).map(
    (user) => ({
      value: user,
      label: user,
    })
  );

  const repos = selectedUser
    ? Array.from(
        data
          .filter(
            (row) => row[githubId] === selectedUser.value && row[name] !== "N/A"
          )
          .map((row) => ({ value: row[name], label: row[name] }))
      )
    : [];

  const handleUserChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedUser(selectedOption);
    setSelectedRepo({ value: "ALL", label: "ALL" });
  };

  const handleRepoChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedRepo(selectedOption);
  };

  const getLanguageStats = (repoData: any[]) => {
    const languageStats: { [key: string]: number } = {};
    repoData.forEach((row) => {
      if (row[langs] === "N/A") return {};
      const stats = JSON.parse(row[langs]);
      console.log("stats:" + stats);
      Object.keys(stats).forEach((lang) => {
        if (!languageStats[lang]) {
          languageStats[lang] = 0;
        }
        languageStats[lang] += stats[lang];
      });
    });
    return Object.entries(languageStats).map(([name, value]) => ({
      name,
      value,
    }));
  };

  useEffect(() => {
    if (selectedUser) {
      const filteredData =
        selectedRepo?.value === "ALL"
          ? data.filter((row) => row[githubId] === selectedUser.value)
          : data.filter(
              (row) =>
                row[githubId] === selectedUser.value &&
                row[name] === selectedRepo?.value
            );

      const languageStats = getLanguageStats(filteredData);
      const sortedStats = [...languageStats].sort((a, b) => b.value - a.value);
      setSortedLanguageStats(sortedStats);
    } else {
      setSortedLanguageStats([]);
    }
  }, [selectedUser, selectedRepo]);

  const formatXAxis = (tickItem: string) => {
    return tickItem.length > 9 ? `${tickItem.slice(0, 6)}...` : tickItem;
  };

  const formatYAxis = (tickItem: number) => {
    return tickItem >= 1000000
      ? tickItem.toExponential(2)
      : tickItem.toLocaleString();
  };

  const barChartWidth = Math.max(sortedLanguageStats.length * 100, 200);

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
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow-md">
      <div className="mb-4">
        <label className="mr-2 text-white font-bold">Select GitHub ID:</label>
        <Select
          id="user-select"
          options={users}
          onChange={handleUserChange}
          placeholder="Select a User"
          className="mb-4"
        />
        {selectedUser && (
          <>
            <label className="mr-2 text-white font-bold">
              Select Repository:
            </label>
            <Select
              value={selectedRepo}
              options={[{ value: "ALL", label: "ALL" }, ...repos]}
              onChange={handleRepoChange}
              placeholder="Select a Repo"
            />
          </>
        )}
      </div>
      {selectedUser && selectedRepo && sortedLanguageStats.length > 0 && (
        <>
          <h2 className="text-center text-xl text-white font-bold mb-4">
            Language Statistics
          </h2>
          <div className="mt-6 p-6 bg-gray-800 rounded-lg shadow-md">
            <div style={{ overflowX: "auto" }}>
              <div style={{ width: `${barChartWidth}px`, margin: "0 auto" }}>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={sortedLanguageStats} margin={{ left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="name"
                      stroke="#ffffff"
                      tickFormatter={formatXAxis}
                      textAnchor="middle"
                    />
                    <YAxis stroke="#ffffff" tickFormatter={formatYAxis} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#333",
                        borderColor: "#333",
                      }}
                      labelStyle={{ color: "#ffffff" }}
                      itemStyle={{ color: "#ffffff" }}
                    />
                    <Bar dataKey="value">
                      {sortedLanguageStats.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getColor(index)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            <div>
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie
                    data={sortedLanguageStats}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={150}
                    fill="#8884d8"
                    label={renderCustomizedLabel} // Use custom label renderer
                    labelLine={false} // Disable label lines
                  >
                    {sortedLanguageStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={getColor(index)} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#333",
                      borderColor: "#333",
                    }}
                    labelStyle={{ color: "#ffffff" }}
                    itemStyle={{ color: "#ffffff" }}
                  />
                  <Legend
                    layout="vertical"
                    align="right"
                    verticalAlign="middle"
                    wrapperStyle={{ color: "#ffffff" }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
      {sortedLanguageStats.length === 0 ? (
        <div className="mt-6 p-6 bg-gray-800 rounded-lg shadow-md">
          <p className="text-white text-center font-bold">No data available</p>
        </div>
      ) : null}
    </div>
  );
};

export default HistPie;
