import React, { useState, useEffect } from "react";
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";

interface YearSelectionProps {
  years: number[];
  selectedYear: number;
  handleYearClick: (year: number) => void;
}

const YearSelection: React.FC<YearSelectionProps> = ({
  years,
  selectedYear,
  handleYearClick,
}) => {
  const selectedYearIndex = years.indexOf(selectedYear);
  const [startIndex, setStartIndex] = useState(selectedYearIndex);

  const handlePrevClick = () => {
    setStartIndex((prevIndex) => Math.max(prevIndex - 1, 0));
  };

  const handleNextClick = () => {
    setStartIndex((prevIndex) => Math.min(prevIndex + 1, years.length - 5));
  };

  const visibleYears = years.slice(
    Math.min(startIndex, years.length - 5),
    startIndex + 5
  );

  return (
    <div className="flex items-center justify-center mb-4 overflow-hidden w-full">
      <button
        onClick={handlePrevClick}
        disabled={startIndex === 0}
        className="px-2 py-1 bg-gray-800 rounded text-white"
      >
        <FaArrowLeft />
      </button>
      {/* <div className="flex space-x-4 mx-4"> */}
      <div className="flex overflow-x-auto scrollbar-hide mx-4 space-x-4 px-2 w-full max-w-xs sm:max-w-md md:max-w-lg justify-center">
        {visibleYears.map((year) => (
          <button
            key={year}
            onClick={() => handleYearClick(year)}
            className={`px-4 py-2 rounded-lg border ${
              selectedYear === year
                ? "bg-blue-500 text-white border-blue-500"
                : "bg-gray-800 text-gray-400 border-gray-600"
            } hover:bg-blue-600 hover:text-white transition-colors`}
          >
            {year}
          </button>
        ))}
      </div>
      <button
        onClick={handleNextClick}
        disabled={startIndex + 5 >= years.length}
        className="px-2 py-1 bg-gray-800 rounded text-white"
      >
        <FaArrowRight />
      </button>
    </div>
  );
};

export default YearSelection;
