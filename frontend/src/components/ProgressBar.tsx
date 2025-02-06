import React from "react";

interface ProgressBarProps {
  remainingTime: number;
  totalTime: number;
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  remainingTime,
  totalTime,
}) => {
  const progressPercentage = ((totalTime - remainingTime) / totalTime) * 100;

  return (
    <div className="relative h-4 bg-gray-700 rounded overflow-hidden">
      {/* Progress Bar */}
      <div
        className="absolute top-0 left-0 h-full bg-blue-500 rounded"
        style={{
          width: `${progressPercentage}%`,
          transition: "width 1s linear",
        }}
      ></div>
      {/* Percentage Display */}
      <div className="absolute inset-0 flex items-center justify-center text-xs text-white font-bold">
        {remainingTime > 0 ? `${Math.round(progressPercentage)}%` : "Done!"}
      </div>
    </div>
  );
};

export default ProgressBar;
