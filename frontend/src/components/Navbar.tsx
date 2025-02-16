import React, { useState } from "react";
import avatar from "../assets/avatar.png";
import logoImage from "../assets/app_logo.png";
import logoutImage from "../assets/logout.png";
import { useNavigate } from "react-router-dom";

interface NavbarProps {
  children?: React.ReactNode;
  avatarUrl?: string;
  rateLimit?: { limit: number; remaining: number } | null;
}

const Navbar: React.FC<NavbarProps> = ({ children, avatarUrl, rateLimit }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  let menuTimeout: ReturnType<typeof setTimeout>;
  const navigate = useNavigate();

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
    localStorage.clear();
    navigate("/login");
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
          <a
            href="/about"
            target="_self"
            className="text-white mr-4 text-xl font-bold tracking-wide shadow-lg transition-transform transform hover:scale-110 hover:bg-red-700"
          >
            GitHub-Mole
          </a>
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
                  onError={(e) => {
                    (e.target as HTMLImageElement).onerror = null;
                    (e.target as HTMLImageElement).src = avatar;
                  }}
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
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-200"
                    style={{
                      fontSize: "1.3em",
                    }}
                  >
                    <img
                      src={logoutImage}
                      alt="Logout"
                      className="inline-block mr-2"
                      style={{ height: "1.3em" }}
                    />
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
