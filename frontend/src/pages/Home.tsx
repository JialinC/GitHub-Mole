import React from "react";
import { useNavigate } from "react-router-dom";
import backgroundImage from "../assets/mole.png";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div
      className="min-h-screen flex flex-col mx-auto bg-cover bg-center"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <Navbar>
        <button
          onClick={() => navigate("/login")}
          className="text-xl font-bold text-white tracking-wide shadow-lg hover:underline hover:scale-105 transform transition-transform duration-200"
        >
          Login
        </button>
      </Navbar>
      <main className="flex-grow container mx-auto p-4 flex flex-col items-center justify-start text-center mt-32">
        <div className="bg-opacity-75 bg-stone-900 p-8 rounded-lg shadow-lg">
          <h1 className="text-4xl font-bold mb-4 text-white">
            Welcome to GitHub-Mole
          </h1>
          <p className="text-lg text-white mb-4 max-w-xl mx-auto">
            This is an open-source APP designed to help you collect GitHub user
            contribution stats and form SDE teams. For details, please check the
            <a
              href="https://github.com/yourusername/your-repo/blob/main/README.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-600 underline mx-1"
            >
              README
            </a>
            file and the
            <a
              href="https://yourdocumentationlink.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-600 underline mx-1"
            >
              DOC
            </a>
            . Click the 'Login' button in the top right corner to get started.
            🌟
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Home;
