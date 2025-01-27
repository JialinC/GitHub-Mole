import React from "react";

interface TableProps {
  headers: string[];
  data: (string | JSX.Element)[][];
  cellWidth?: string; // Optional cell width parameter
}

const ViewTable: React.FC<TableProps> = ({
  headers,
  data,
  cellWidth = "auto",
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
                    style={{ width: cellWidth }}
                  >
                    <div
                      className="overflow-hidden text-ellipsis whitespace-nowrap"
                      title={header}
                    >
                      {header}
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
                      style={{ width: cellWidth }}
                    >
                      <div
                        className="overflow-hidden text-ellipsis whitespace-nowrap"
                        title={typeof cell === "string" ? cell : undefined}
                        style={
                          React.isValidElement(cell)
                            ? { width: "160px" }
                            : { width: cellWidth }
                        }
                      >
                        {cell}
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ViewTable;
