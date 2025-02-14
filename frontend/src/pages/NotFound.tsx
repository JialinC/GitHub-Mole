import React from "react";
import bg from "../assets/404.png";

const NotFound: React.FC = () => {
  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen bg-gray-100"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <h1 className="text-8xl font-bold text-gray-800 mb-4">
        404 - Page Not Found
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        The page you are looking for does not exist.
      </p>
      <a href="/" className="px-4 py-2 bg-blue-500 text-white rounded">
        Go to Home
      </a>
    </div>
  );
};

export default NotFound;
