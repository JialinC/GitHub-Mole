import React from "react";

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white p-4">
      <div className="container mx-auto text-center">
        <p className="text-lg">
          Made with ❤️ by
          <a
            href="https://scholar.google.com/citations?user=tCuaIgYAAAAJ"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-600 underline ml-1"
          >
            J
          </a>
        </p>
        <p>
          <a
            href="https://github.com/JialinC/GHTeam"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-600 underline"
          >
            Check it out on GitHub 🚀
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
