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
  headers: string[];
  data: any[][];
}

const Histogram: React.FC<HistogramProps> = ({ headers, data }) => {
  const [selectedField, setSelectedField] = useState<string>(headers[1]);

  const handleFieldChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedField(event.target.value);
  };

  const histogramData = data
    .map((row) => ({
      GitHubID: row[0],
      value: row[headers.indexOf(selectedField)],
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
      <div className="mb-4">
        <label htmlFor="field-select" className="mr-2 text-white font-bold">
          Select Field:
        </label>
        <select
          id="field-select"
          value={selectedField}
          onChange={handleFieldChange}
          className="p-2 border rounded bg-gray-700 text-white"
        >
          {headers.slice(1).map((header, index) => (
            <option
              key={index}
              value={header}
              className="bg-gray-700 text-white"
            >
              {header}
            </option>
          ))}
        </select>
      </div>
      <h2 className="text-xl font-bold text-white text-center">
        {selectedField} by GitHub ID
      </h2>
      <div style={{ overflowX: "auto" }}>
        <div
          style={{
            width: `${Math.max(histogramData.length * 100, 200)}px`,
            margin: "0 auto",
          }}
        >
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={histogramData} margin={{ left: 10 }}>
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
