import React, { useState } from "react";
import { FaArrowLeft, FaArrowRight, FaHeart } from "react-icons/fa";
import { Tooltip } from "react-tooltip";
import "./CustomHeatmap.css";

interface Contribution {
  date: string;
  count: number;
}

interface CustomHeatmapProps {
  joinDate: string | null;
  contributions: { [key: string]: [number, number] };
  selectedYear: number;
}

const CustomHeatmap: React.FC<CustomHeatmapProps> = ({
  joinDate,
  contributions,
  selectedYear,
}) => {
  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  const getDateArrayForYear = (year: number) => {
    const startDate = new Date(Date.UTC(year, 0, 1)); // January 1st of the given year
    const endDate = new Date(Date.UTC(year, 11, 31)); // December 31st of the given year
    const arr = [];
    const dt = new Date(startDate);
    while (dt <= endDate) {
      arr.push(dt.toISOString().split("T")[0]); // Add date string in YYYY-MM-DD format
      dt.setUTCDate(dt.getUTCDate() + 1);
    }
    return arr;
  };

  const dateArray = getDateArrayForYear(selectedYear);

  const getColor = (count: number) => {
    if (count >= 15) return "color-scale-4";
    if (count >= 10) return "color-scale-3";
    if (count >= 5) return "color-scale-2";
    if (count > 0) return "color-scale-1";
    return "color-empty";
  };

  const formatDateWithoutYear = (dateString: string) => {
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    const [_, month, day] = dateString.split("-");
    const monthName = months[parseInt(month, 10) - 1];
    const dayNumber = parseInt(day, 10);

    const ordinalSuffix = (day: number) => {
      if (day > 3 && day < 21) return "th"; // special case for 11th to 13th
      switch (day % 10) {
        case 1:
          return "st";
        case 2:
          return "nd";
        case 3:
          return "rd";
        default:
          return "th";
      }
    };

    return `${monthName} ${dayNumber}${ordinalSuffix(dayNumber)}`;
  };

  const formatContributionText = (contrib: number) => {
    return `${contrib} contribution${contrib !== 1 ? "s" : ""}`;
  };

  let weekCount = 0;
  let renderMon = false;
  let curMonth = "Dec";

  return (
    <div className="flex flex-col items-center">
      <div className="overflow-x-auto w-full" style={{ maxWidth: "100%" }}>
        <svg width="1440" height="225" viewBox="0 0 1440 200">
          {weekDays.map((day, index) => (
            <text
              key={day}
              x="20"
              y={50 + index * 25}
              className="text-xs font-bold"
              fill="white"
            >
              {day}
            </text>
          ))}
          {dateArray.map((date) => {
            const [contrib, weekday] = contributions[date];
            const color = getColor(contrib);
            const x = weekCount * 25 + 50; // 53 weeks in a year
            const y = weekday * 25 + 35;
            const [, month] = date.split("-");
            const monthName = months[parseInt(month, 10) - 1];
            if (monthName != curMonth) {
              renderMon = true;
              curMonth = monthName;
            }
            if (weekday === 6) {
              weekCount++;
            }
            return (
              <g key={date}>
                {renderMon && (
                  <>
                    <text
                      x={x}
                      y="25"
                      className="text-xs font-bold"
                      fill="white"
                    >
                      {curMonth}
                    </text>
                    {(renderMon = false)}
                  </>
                )}
                {joinDate === date ? (
                  <FaHeart
                    x={x}
                    y={y}
                    size={20}
                    style={{ fill: "#f87171" }}
                    data-tooltip-id="contribtip"
                    data-tooltip-content={`You Joined GitHub On This Day! ${formatContributionText(
                      contrib
                    )} on ${formatDateWithoutYear(date)}`}
                    data-tooltip-place="top"
                  />
                ) : (
                  <rect
                    x={x}
                    y={y}
                    width="20"
                    height="20"
                    className={color}
                    data-tooltip-id="contribtip"
                    data-tooltip-content={`${formatContributionText(
                      contrib
                    )} on ${formatDateWithoutYear(date)}`}
                    data-tooltip-place="top"
                  />
                )}
              </g>
            );
          })}
        </svg>
        <Tooltip id="contribtip" />
      </div>
    </div>
  );
};

export default CustomHeatmap;
