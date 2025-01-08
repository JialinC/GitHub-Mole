import React, { useEffect, useState } from "react";
import { FaDatabase, FaGithub, FaUsers, FaCodeBranch } from "react-icons/fa";
import CardButton from "../components/CardButton";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Loading from "../components/Loading";
import ErrorPage from "../components/Error";
import axiosInstance from "../utils/axiosConfig";
import { formatDate, convertToLocalTime } from "../utils/helpers";
import { CurUser, Contributions } from "../types";

const Dashboard: React.FC = () => {
  const [rateLimit, setRateLimit] = useState<any>(null);
  const [curUser, setCurUser] = useState<CurUser | null>(null);
  const [contributions, setContributions] = useState<Contributions | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

    const fetchCurUser = async () => {
      setLoading(true);
      setError(null);
      try {
        const storedUser = localStorage.getItem("curUser");
        if (storedUser) {
          console.log(storedUser);
          setCurUser(JSON.parse(storedUser));
        } else {
          const response = await axiosInstance.get(
            "api/graphql/current-user-login"
          );
          setCurUser(response.data);
          localStorage.setItem("curUser", JSON.stringify(response.data));
        }
      } catch (error) {
        setError("Error fetching data from endpoint current-user-login");
        console.error(
          "Error fetching data from endpoint current-user-login:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    const fetchContributions = async (login: string) => {
      setLoading(true);
      setError(null);
      try {
        const storedContribution = localStorage.getItem("contributions");
        if (storedContribution) {
          console.log(storedContribution);
          setContributions(JSON.parse(storedContribution));
        } else {
          const response = await axiosInstance.get(
            `/api/graphql/user-contributions-collection/${login}`
          );
          setContributions(response.data);
          localStorage.setItem("contributions", JSON.stringify(response.data));
        }
      } catch (error) {
        setError(
          "Error fetching data from endpoint user-contributions-collection"
        );
        console.error(
          "Error fetching data from endpoint user-contributions-collection:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    const fetchRateLimit = async () => {
      try {
        const response = await axiosInstance.get("api/graphql/rate-limit");
        setRateLimit(response.data.rateLimit);
      } catch (error) {
        setError("Failed to fetch user information.");
      } finally {
        setLoading(false);
      }
    };

    fetchCurUser();
    fetchContributions(curUser?.login || "");
    fetchRateLimit();
  }, [location.search]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorPage message={error} />;
  }

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

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar avatarUrl={curUser?.avatarUrl} rateLimit={rateLimit}></Navbar>
      <main className="flex-grow container mx-auto p-4">
        <div className="bg-stone-900 bg-opacity-30 p-8 rounded-lg shadow-lg flex items-center mb-8">
          <div className="w-1/7 flex flex-col items-start">
            <div className="relative w-32">
              <img
                src={curUser?.avatarUrl || ""}
                alt="User Profile"
                className="rounded-full w-32 h-32 border-4 border-white shadow-lg hover:shadow-xl transition-shadow duration-300 ease-in-out transform hover:scale-105"
              />
              <div className="absolute bottom-0 right-0 bg-green-500 border-2 border-white rounded-full w-6 h-6"></div>
            </div>
            <ul className="text-white text-sm w-32 text-center space-y-1 mt-4">
              <li>Account created on: {formattedDate}</li>
              <li>Ratelimit left: {rateLimit?.remaining}</li>
              <li>Reset at: {localTime}</li>
            </ul>
          </div>
          <div className="w-6/7 text-white ml-8">
            <h2 className="text-2xl font-bold mb-4">
              {curUser?.login || ""}'s GitHub Stats
            </h2>
            <ul className="grid grid-cols-2 gap-x-8 list-disc list-inside">
              {stats.map((stat, index) => (
                <li key={index} className="mb-2">
                  <span className="font-semibold">
                    {stat.label}: {stat.value}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <CardButton
            icon={<FaDatabase className="text-4xl mb-4" />}
            text="Check Mining History Data"
            navigateTo="/history"
          />
          <CardButton
            icon={<FaGithub className="text-4xl mb-4" />}
            text="Query User GitHub Contribution Data"
            navigateTo="/contributions"
          />
          <CardButton
            icon={<FaUsers className="text-4xl mb-4" />}
            text="Form Software Development Teams"
            navigateTo="/teams"
          />
          <CardButton
            icon={<FaCodeBranch className="text-4xl mb-4" />}
            text="Query Repository Contribution Data"
            navigateTo="/repositories"
          />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Dashboard;
