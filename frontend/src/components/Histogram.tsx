import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

interface HistogramProps {
  data: any[][];
}

const Histogram: React.FC<HistogramProps> = ({ data }) => {
  console.log(data);
  const countOccurrences = (data: string[][]) => {
    return data.reduce((acc: Record<string, number>, row: string[]) => {
      const githubId = row[0];
      if (row[1] === "N/A") {
        acc[githubId] = 0;
        return acc;
      }
      if (acc[githubId]) {
        acc[githubId] += 1;
      } else {
        acc[githubId] = 1;
      }
      return acc;
    }, {});
  };

  const occurrences = countOccurrences(data);
  const chartData = Object.keys(occurrences)
    .map((key) => ({
      GitHubID: key,
      value: occurrences[key],
    }))
    .sort((a, b) => b.value - a.value);

  const formatXAxis = (tickItem: string) => {
    return tickItem.length > 9 ? `${tickItem.slice(0, 6)}...` : tickItem;
  };

  const formatYAxis = (tickItem: number) => {
    return tickItem >= 1000000
      ? tickItem.toExponential(2)
      : tickItem.toLocaleString();
  };

  return (
    <div className="mt-6 bg-gray-800 rounded-lg shadow-md">
      <div style={{ overflowX: "auto" }}>
        <div
          style={{
            width: `${Math.max(chartData.length * 100, 200)}px`,
            margin: "0 auto",
          }}
        >
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData} margin={{ left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="GitHubID"
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
              <Bar dataKey="value" fill="#0088FE" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Histogram;
