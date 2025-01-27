import React, { useEffect, useState } from "react";
import CustomHeatmap from "../components/CustomHeatmap";
import YearSelection from "../components/YearSelection";
import { FaDatabase, FaGithub, FaUsers, FaCodeBranch } from "react-icons/fa";
import CardButton from "../components/CardButton";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Loading from "../components/Loading";
import ErrorPage from "../components/Error";
import ErrorMessage from "../components/ErrorMessage";
import { formatDate, convertToLocalTime } from "../utils/helpers";
import { CurUser, Contributions } from "../types/Types";
import {
  fetchCurUser,
  fetchContributions,
  fetchContribYears,
  fetchCalendar,
  fetchRateLimit,
} from "../utils/queries";

const Dashboard: React.FC = () => {
  const [rateLimit, setRateLimit] = useState<any>(null);
  const [curUser, setCurUser] = useState<CurUser | null>(null);
  const [contributions, setContributions] = useState<Contributions | null>(
    null
  );
  const [contribYears, setContribYears] = useState<number[]>([]);
  const [selectedYear, setSelectedYear] = useState<number>(0);
  const [contribDates, setContribDates] = useState<{
    [key: string]: [number, number];
  } | null>(null);
  const [joinDate, setJoinDate] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getContribWeeks = async (login: string, year: number) => {
    const januaryFirst = new Date(Date.UTC(year, 0, 1));
    const start = januaryFirst.toISOString();
    const [join, weeks] = await fetchCalendar(login, setError, start);
    if (join) {
      setJoinDate(join.occurredAt.split("T")[0]);
    }
    const contributionsDict: { [key: string]: [number, number] } = {};
    weeks.forEach(
      (week: {
        contributionDays: {
          contributionCount: number;
          date: string;
          weekday: number;
        }[];
      }) => {
        week.contributionDays.forEach(
          (day: {
            contributionCount: number;
            date: string;
            weekday: number;
          }) => {
            contributionsDict[day.date] = [day.contributionCount, day.weekday];
          }
        );
      }
    );
    if (!(januaryFirst.toISOString().split("T")[0] in contributionsDict)) {
      const weekStart = new Date(januaryFirst);
      weekStart.setUTCDate(januaryFirst.getUTCDate() - 10);
      const preStart = weekStart.toISOString();
      const [_, Jan1stWeeks] = await fetchCalendar(
        login,
        setError,
        preStart,
        start
      );
      const Jan1stWeek = Jan1stWeeks[Jan1stWeeks.length - 1].contributionDays;
      const Jan1st = Jan1stWeek[Jan1stWeek.length - 1];
      contributionsDict[Jan1st.date] = [
        Jan1st.contributionCount,
        Jan1st.weekday,
      ];
    }
    setContribDates(contributionsDict);
  };

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");

    if (accessToken) {
      localStorage.setItem("access_token", accessToken);
      if (refreshToken) {
        localStorage.setItem("refresh_token", refreshToken);
      }
    }

    const getCurUser = async () => {
      const storedUser = localStorage.getItem("curUser");
      if (storedUser) {
        setCurUser(JSON.parse(storedUser));
        return JSON.parse(storedUser);
      } else {
        const user = await fetchCurUser(setError);
        setCurUser(user);
        localStorage.setItem("curUser", JSON.stringify(user));
        return user;
      }
    };

    const getContributions = async (login: string) => {
      const storedContribution = localStorage.getItem("contributions");
      if (storedContribution) {
        setContributions(JSON.parse(storedContribution));
      } else {
        const contribs = await fetchContributions(login, setError);
        setContributions(contribs);
        localStorage.setItem("contributions", JSON.stringify(contribs));
      }
    };

    const getContribYears = async (login: string) => {
      const storedYears = localStorage.getItem("years");
      if (storedYears) {
        setContribYears(JSON.parse(storedYears));
        setSelectedYear(JSON.parse(storedYears)[0]);
        return JSON.parse(storedYears)[0];
      } else {
        const years = await fetchContribYears(login, setError);
        setContribYears(years);
        setSelectedYear(years[0]);
        localStorage.setItem("years", JSON.stringify(years));
        return years[0];
      }
    };

    const fetchData = async () => {
      setLoading(true);
      const user = await getCurUser();
      await getContributions(user.login);
      const year = await getContribYears(user.login);
      await getContribWeeks(user.login, year);
      setRateLimit(await fetchRateLimit(setError));
      setLoading(false);
    };

    fetchData();
  }, []);

  const handleYearClick = async (year: number) => {
    setContribDates(null);
    setSelectedYear(year);
    if (curUser?.login) {
      await getContribWeeks(curUser.login, year);
    }
    setRateLimit(await fetchRateLimit(setError));
  };

  const formattedDate = formatDate(curUser?.created_at || "");
  const localTime = convertToLocalTime(rateLimit?.resetAt || "");

  const stats = [
    { label: "Number of commits", value: contributions?.commit },
    { label: "Number of gists", value: curUser?.gists },
    { label: "Number of issues", value: curUser?.issues },
    { label: "Number of projects", value: curUser?.projects },
    { label: "Number of repositories", value: curUser?.repositories },
    { label: "Number of pull requests", value: curUser?.pull_requests },
    {
      label: "Number of pull request reviews",
      value: contributions?.pr_review,
    },
    {
      label: "Number of repository discussions",
      value: curUser?.repository_discussions,
    },
    { label: "Number of followers", value: curUser?.followers },
    { label: "Number of following", value: curUser?.following },
    { label: "Number of watching", value: curUser?.watching },
    {
      label: "Number of starred repositories",
      value: curUser?.starred_repositories,
    },
    { label: "Number of commit comments", value: curUser?.commit_comments },
    { label: "Number of gist comments", value: curUser?.gist_comments },
    { label: "Number of issue comments", value: curUser?.issue_comments },
    {
      label: "Number of repository discussion comments",
      value: curUser?.repository_discussion_comments,
    },
  ];

  if (loading || !curUser || !contributions || !rateLimit) {
    return <Loading />;
  }

  if (error) {
    return <ErrorPage message={error} />;
  }

  return (
    <div className="min-h-screen flex flex-col text-gray-300">
      <Navbar avatarUrl={curUser?.avatarUrl} rateLimit={rateLimit} />
      <main className="flex-grow container mx-auto p-6">
        <div className="p-6 bg-gray-800 rounded-lg shadow-lg">
          {loading ? (
            <div className="flex justify-center items-center h-40">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500"></div>
            </div>
          ) : error ? (
            <ErrorMessage error={error} />
          ) : (
            <div className="flex items-center mb-8">
              {/* Profile Section */}
              <div className="w-1/4 flex flex-col items-center">
                <div className="relative w-32">
                  <img
                    src={curUser?.avatarUrl || ""}
                    alt="User Profile"
                    className="rounded-full w-32 h-32 border-4 border-gray-600 shadow-lg hover:shadow-xl transition-shadow duration-300 ease-in-out transform hover:scale-105"
                  />
                  <div className="absolute bottom-0 right-0 bg-green-500 border-2 border-gray-800 rounded-full w-6 h-6"></div>
                </div>
                <ul className="text-gray-400 text-sm text-center space-y-1 mt-4">
                  <li>
                    <span className="font-medium">Account created on:</span>{" "}
                    {formattedDate}
                  </li>
                  <li>
                    <span className="font-medium">Rate limit left:</span>{" "}
                    {rateLimit?.remaining}
                  </li>
                  <li>
                    <span className="font-medium">Reset at:</span> {localTime}
                  </li>
                </ul>
              </div>

              {/* Stats Section */}
              <div className="w-3/4 ml-8">
                <h2 className="text-2xl font-bold text-gray-100 mb-4">
                  {curUser?.login || ""}'s GitHub Stats
                </h2>
                <ul className="grid grid-cols-2 gap-x-8 list-disc list-inside">
                  {stats.map((stat, index) => (
                    <li key={index} className="mb-2">
                      <span className="font-semibold text-gray-200">
                        {stat.label}: {stat.value}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
          {contribDates ? (
            <div>
              <CustomHeatmap
                joinDate={joinDate}
                contributions={contribDates}
                selectedYear={selectedYear}
              />
            </div>
          ) : (
            <div className="flex justify-center items-center h-40">
              <div className="animate-spin rounded-full h-8 w-8 border-4 border-t-4 border-t-white border-gray-500"></div>
            </div>
          )}
          <YearSelection
            years={contribYears}
            selectedYear={selectedYear}
            handleYearClick={handleYearClick}
          />
          {/* Action Buttons */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
            <CardButton
              icon={<FaDatabase className="text-6xl mb-4 text-blue-400" />}
              text="View Mining History Data"
              navigateTo="/history"
            />
            <CardButton
              icon={<FaGithub className="text-6xl mb-4 text-gray-200" />}
              text="Mine GitHub Contributions"
              navigateTo="/contributions"
            />
            <CardButton
              icon={<FaUsers className="text-6xl mb-4 text-green-400" />}
              text="Form Development Teams"
              navigateTo="/teams"
            />
            <CardButton
              icon={<FaCodeBranch className="text-6xl mb-4 text-purple-400" />}
              text="Mine Commits in Repository"
              navigateTo="/repositories"
            />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Dashboard;
