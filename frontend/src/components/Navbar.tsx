import React, { useState } from "react";
import logoImage from "../assets/app_logo.png";
import { Link } from "react-router-dom";

interface NavbarProps {
  children?: React.ReactNode;
  avatarUrl?: string;
  rateLimit?: { limit: number; remaining: number } | null;
}

const Navbar: React.FC<NavbarProps> = ({ children, avatarUrl, rateLimit }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  let menuTimeout: ReturnType<typeof setTimeout>;

  const handleMouseEnter = () => {
    clearTimeout(menuTimeout);
    setIsMenuOpen(true);
  };

  const handleMouseLeave = () => {
    menuTimeout = setTimeout(() => {
      setIsMenuOpen(false);
    }, 500);
  };

  const handleLogout = () => {
    // Implement logout functionality here
    console.log("User logged out");
  };

  return (
    <nav className="bg-red-600 text-white p-4">
      <div className="flex justify-between items-center w-full px-4">
        <div className="flex items-center">
          <img
            src={logoImage}
            alt="GitHub-Mole Logo"
            className="h-10 w-10 mr-2"
          />
          <div className="text-xl font-bold text-white tracking-wide shadow-lg">
            GitHub-Mole
          </div>
        </div>
        <div className="flex items-center">
          {children}
          {avatarUrl && (
            <div
              className="relative flex items-center ml-4"
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              <div className="flex items-center">
                <img
                  src={avatarUrl}
                  alt="User Avatar"
                  className="w-8 h-8 rounded-full border-2 border-white"
                />
                {rateLimit && (
                  <div className="flex flex-col items-center text-white text-xs ml-2">
                    <span className="font-bold">Limit Left:</span>
                    <span className="font-bold">
                      {rateLimit.remaining} / {rateLimit.limit}
                    </span>
                  </div>
                )}
              </div>
              {isMenuOpen && (
                <div
                  className="absolute top-12 right-0 bg-white text-black rounded shadow-lg w-48"
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  <Link
                    to="/profile"
                    className="block px-4 py-2 hover:bg-gray-200"
                  >
                    User Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-200"
                  >
                    Log Out
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
