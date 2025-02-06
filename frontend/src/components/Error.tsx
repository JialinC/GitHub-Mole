import React from "react";
import bg from "../assets/error.png";

interface ErrorPageProps {
  message: string;
}

const ErrorPage: React.FC<ErrorPageProps> = ({ message }) => {
  return (
    <div
      className="flex items-center justify-center min-h-screen bg-red-100"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <div className="bg-white p-6 rounded shadow-md text-center">
        <h1 className="text-2xl font-bold text-red-600">Error</h1>
        <p className="mt-4 text-gray-700">{message}</p>
      </div>
    </div>
  );
};

export default ErrorPage;
