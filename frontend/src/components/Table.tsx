import React from "react";
import loading from "../assets/load.gif";
import ProgressBar from "./ProgressBar";

interface TableProps {
  headers: string[];
  data: string[][];
  avatar?: { [key: string]: string };
  columnWidth?: string;
  columnSelection?: Boolean;
  handleColumnSelection?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  noRateLimit?: boolean;
  remainingTime?: number;
  totalTime?: number;
}

const Table: React.FC<TableProps> = ({
  headers,
  data,
  avatar,
  columnWidth,
  columnSelection,
  handleColumnSelection,
  noRateLimit,
  remainingTime,
  totalTime,
}) => {
  return (
    <div className="mt-6 overflow-auto">
      <div className="overflow-hidden bg-gray-900 rounded-lg shadow-md">
        <div className="overflow-auto max-h-96">
          <table className="min-w-full table-fixed border-collapse">
            <thead className="bg-gray-700 sticky top-0 shadow">
              <tr>
                {headers.map((header, index) => (
                  <th
                    key={index}
                    className="px-4 py-2 text-left text-xs font-semibold text-gray-200 uppercase tracking-wider border-b border-gray-600"
                    style={{
                      width: columnWidth ? columnWidth : "auto",
                    }}
                  >
                    <div
                      className="overflow-hidden text-ellipsis whitespace-nowrap"
                      title={typeof header === "string" ? header : undefined} // Tooltip for long content
                      style={{
                        width: columnWidth ? columnWidth : "auto",
                      }}
                    >
                      {index === 0 ? (
                        header
                      ) : columnSelection ? (
                        <label className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            value={header}
                            onChange={handleColumnSelection}
                            className="w-4 h-4 text-blue-500 bg-gray-800 border-gray-600 rounded focus:ring-blue-500"
                          />
                          <span
                            className="tooltip overflow-hidden text-ellipsis whitespace-nowrap"
                            title={header}
                          >
                            {header}
                          </span>
                        </label>
                      ) : (
                        header
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-gray-800 divide-y divide-gray-700">
              {data.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className="hover:bg-gray-700 transition duration-150"
                >
                  {row.map((cell, cellIndex) => (
                    <td
                      key={cellIndex}
                      className="px-4 py-2 text-sm text-gray-300 border-b border-gray-600"
                    >
                      <div
                        className={`overflow-hidden text-ellipsis whitespace-nowrap ${
                          headers[cellIndex] === "GitHub ID" ? "font-bold" : ""
                        }`}
                        title={typeof cell === "string" ? cell : undefined}
                        style={{
                          width: columnWidth ? columnWidth : "auto",
                        }}
                      >
                        {cell === "Loading..." ? (
                          <img
                            src={loading}
                            alt="Loading"
                            className="w-10 h-10 inline-block"
                          />
                        ) : (
                          <>
                            {headers[cellIndex] === "GitHub ID" &&
                            avatar &&
                            avatar[cell] ? (
                              <img
                                src={avatar[cell]}
                                alt="..."
                                className="w-10 h-10 rounded-full mr-2 inline-block"
                              />
                            ) : null}
                            {cell}
                          </>
                        )}
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
              {noRateLimit && (
                <tr>
                  <td
                    colSpan={headers.length} // Dynamically span all columns
                    className="px-4 py-2 text-sm text-gray-300 border-b border-gray-600"
                  >
                    <ProgressBar
                      remainingTime={remainingTime ?? 0}
                      totalTime={totalTime ?? 0}
                    />
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Table;
