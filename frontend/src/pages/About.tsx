import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";

import { getUserAvatarUrl } from "../utils/helpers";
import { fetchRateLimit } from "../utils/queries";

const About: React.FC = () => {
  const [fatal, setFatal] = useState<string | null>(null);
  const [avatarUrl, setAvatarUrl] = useState<string>("");
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const navigate = useNavigate();
  const [rateLimit, setRateLimit] = useState<{
    limit: number;
    remaining: number;
  } | null>(null);

  const loadRateLimit = async () => {
    const rateLimitData = await fetchRateLimit(setFatal);
    setRateLimit(rateLimitData);
  };

  useEffect(() => {
    const fetchData = async () => {
      const avatarUrl = getUserAvatarUrl();
      if (avatarUrl) {
        setAvatarUrl(avatarUrl);
        setLoggedIn(true);
        await loadRateLimit();
      }
    };
    fetchData();
  }, []);

  if (fatal) {
    return <ErrorPage message={fatal} />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar {...(loggedIn ? { avatarUrl, rateLimit } : {})}>
        {loggedIn && (
          <a
            href="/dashboard"
            target="_self"
            className="text-white mr-4 text-xl font-bold tracking-wide shadow-lg transition-transform transform hover:scale-105"
          >
            Dashboard
          </a>
        )}
        {!loggedIn && (
          <button
            onClick={() => navigate("/login")}
            className="text-xl font-bold text-white tracking-wide shadow-lg hover:underline hover:scale-105 transform transition-transform duration-200"
          >
            Login
          </button>
        )}
      </Navbar>
      <main className="flex-grow container mx-auto p-4">
        <div className="p-6 bg-gray-800 text-white rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">About GitHub-Mole:</h2>
          <p>
            <strong>GitHub-Mole</strong> is a hybrid web/local application that
            can be deployed for collaborative use or operated locally for
            individual analysis. It enables users to mine and analyze
            comprehensive contribution histories of GitHub users of interest
            while also assisting in the formation of software development teams
            using research-backed algorithms. The application leverages the{" "}
            <strong>GitHub GraphQL and REST APIs</strong> to retrieve detailed
            information about users' contributions, including repositories,
            commits, and other key activities. It features an intuitive,
            user-friendly interface that facilitates efficient data management
            and analysis. Additionally, it incorporates a{" "}
            <strong>backend database</strong> to store mined data, allowing
            users to retrieve their results at any time.
          </p>

          <h2 className="text-l font-bold mt-4 mb-2">Key Features</h2>
          <ul className="list-disc list-inside mb-4">
            <li>
              <strong>User Authentication:</strong> Secure OAuth-based
              authentication via GitHub, enabling users to log in and access
              their GitHub data safely.
            </li>
            <li>
              <strong>Dashboard:</strong> A central dashboard providing an
              overview of a user's GitHub activity, including recent commits,
              contributions, and repository statistics.
            </li>
            <li>
              <strong>Repositories:</strong> A dedicated section displaying
              detailed repository information, including language statistics,
              commit history, and other metadata.
            </li>
            <li>
              <strong>Commits:</strong> A comprehensive commit history view with
              filtering and analysis capabilities.
            </li>
            <li>
              <strong>Contributions:</strong> A breakdown of user contributions
              across repositories, including issues, pull requests, and
              comments.
            </li>
            <li>
              <strong>Software Development Team Formation:</strong> An
              intelligent feature for forming software development teams based
              on GitHub metrics and research-backed algorithms.
            </li>
            <li>
              <strong>Responsive Design:</strong> A fully responsive design
              ensuring an optimal user experience across various devices and
              screen sizes.
            </li>
          </ul>

          <h2 className="text-l font-bold mb-2">Technologies Used</h2>
          <ul className="list-disc list-inside">
            <li>
              <strong>React + Vite + TypeScript:</strong> A high-performance
              frontend framework for an interactive user experience.
            </li>
            <li>
              <strong>Flask:</strong> A lightweight Python-based backend
              framework handling API requests and authentication.
            </li>
            <li>
              <strong>GraphQL & REST API:</strong> Integration with GitHub's
              APIs for flexible and efficient data retrieval.
            </li>
            <li>
              <strong>OAuth:</strong> Secure user authentication via GitHub
              login.
            </li>
            <li>
              <strong>Tailwind CSS:</strong> A modern utility-first CSS
              framework for consistent and stylish UI design.
            </li>
            <li>
              <strong>MySQL:</strong> A robust storage solution that allows
              users to persist mining results for future analysis.
            </li>
          </ul>
          <h2 className="text-2xl font-bold mt-4 mb-4">
            The following papers have been published based on the data collected
            by GitHub-Mole:
          </h2>
          <ul className="list-disc list-inside space-y-4">
            <li>
              Jialin Cui, Runqiu Zhang, Qinjin Jia, Fangtong Zhou, Ruochi Li,
              and Edward F. Gehringer, "A Statistical Study of Female Students
              in a Software Engineering Class: Preparedness, Performance, and
              Contribution"{" "}
              <a
                href="https://drive.google.com/file/d/17wRdx54qm16f32RVFM0o6Hl7ZC0FwLUu/view?usp=drive_link"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Runqiu Zhang, Fangtong Zhou, Ruochi Li, Yang Song, and
              Edward Gehringer, "How Much Effort Do You Need to Expend on a
              Technical Interview? A Study of LeetCode Problem Solving
              Statistics", Conference on Software Engineering Education and
              Training (CSEE&T) 2024, Würzburg, Germany, July 29-August 1, 2024.{" "}
              <span className="font-semibold text-white">
                Received Best Paper award
              </span>{" "}
              <a
                href="https://drive.google.com/file/d/12YMXTLGl0afpd9_6odbvjmuxDoPSvFEs/view"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Runqiu Zhang, Ruochi Li, Fangtong Zhou, Yang Song, and
              Edward Gehringer, "A Comparative Analysis of GitHub Contributions
              Before and After An OSS Based Software Engineering Class,"
              Innovation and Technology in Computer Science Education (ITiCSE)
              2024, Milan, Italy, July 8-10, 2024.{" "}
              <a
                href="https://dl.acm.org/doi/abs/10.1145/3649217.3653535"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Fangtong Zhou, Chengyuan Liu, Qinjin Jia, Yang Song,
              and Edward Gehringer, "Utilizing the Constrained K-Means Algorithm
              and Pre-Class GitHub Contribution Statistics for Forming Student
              Teams," Innovation and Technology in Computer Science Education
              (ITiCSE) 2024, Milan, Italy, July 8-10, 2024.{" "}
              <a
                href="https://dl.acm.org/doi/abs/10.1145/3649217.3653634"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Runqiu Zhang, Ruochi Li, Fangtong Zhou, Yang Song, and
              Edward Gehringer, "How Pre-class Programming Experience Influences
              Students' Contribution to Their Team Project: A Statistical
              Study," 55th ACM Technical Symposium on Computer Science Education
              (SIGCSE 2024), Portland, OR, March 19-23, 2024.{" "}
              <a
                href="https://dl.acm.org/doi/10.1145/3626252.3630870"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Fangtong Zhou, Runqiu Zhang, Ruochi Li, Chengyuan Liu,
              and Edward F. Gehringer, "Predicting students' software
              engineering class performance with machine learning and pre-class
              GitHub metrics," Frontiers in Education 2023, 53rd Annual
              Conference, College Station, TX, October 18-21, 2023.{" "}
              <a
                href="https://ieeexplore.ieee.org/abstract/document/10343357?casa_token=pCOxC80XzHAAAAAA:jWrqfXVKPZbO1C7mMq3o8jaKb5L3a9n3K1K4KjCu0X1YWhMFrRwW7qeWCu5TKOwzjaPRpvGtcQ"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Runqiu Zhang, Ruochi Li, Yang Song, Fangtong Zhou, and
              Edward Gehringer, "Correlating students' class performance based
              on Github metrics: a statistical study," Conference on Innovation
              and Technology in Computer Science Education (ITiCSE) 2023, Turku,
              Finland, July 10–12, 2023, pp. 526–532.{" "}
              <a
                href="https://dl.acm.org/doi/abs/10.1145/3587102.3588799"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
            <li>
              Jialin Cui, Runqiu Zhang, Ruochi Li, Kaida Lou, Chengyuan Liu,
              Yunkai Xiao, Qinjin Jia, and Edward Gehringer, "Can pre-class
              GitHub contributions predict success by student teams?" 2022
              IEEE/ACM 44th International Conference on Software Engineering:
              Software Engineering Education and Training (ICSE-SEET),
              Pittsburgh and online, May 2022.{" "}
              <a
                href="https://ieeexplore.ieee.org/iel7/9793836/9794144/09794264.pdf?casa_token=0D853aJT_lkAAAAA:NHZyeDr_xfR3Jgv2y5m38o2S3BFMJz_KeKI6-PPeytK-NI0rhr48Jw_TqC-qkET2sHcdgyNAr_o"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline"
              >
                link
              </a>
            </li>
          </ul>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default About;
