import React from "react";
import logo from "../assets/mole.png"; // Adjust the path as necessary

interface NavbarProps {
  children?: React.ReactNode;
}

const Navbar: React.FC<NavbarProps> = ({ children }) => {
  return (
    <nav className="bg-red-600 text-white p-4">
      <div className="flex justify-between items-center w-full px-4">
        <div className="flex items-center">
          <img src={logo} alt="GitHub-Mole Logo" className="h-8 w-8 mr-2" />
          <div className="text-xl font-bold text-white tracking-wide shadow-lg">
            GitHub-Mole
          </div>
        </div>
        <div>{children}</div>
      </div>
    </nav>
  );
};

export default Navbar;
