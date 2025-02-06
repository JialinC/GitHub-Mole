import React from "react";

interface CardButtonProps {
  icon: React.ReactNode;
  text: string;
  navigateTo: string;
}

const CardButton: React.FC<CardButtonProps> = ({ icon, text, navigateTo }) => {
  return (
    <a
      href={navigateTo}
      target="_self"
      className="block p-6 max-w-sm bg-gray-700 rounded-lg border border-gray-600 shadow-md hover:bg-gray-900 transition-transform transform hover:scale-105"
    >
      <div className="flex flex-col items-center">
        {icon}
        <h5 className="mb-2 text-l font-bold tracking-tight text-white">
          {text}
        </h5>
      </div>
    </a>
  );
};

export default CardButton;
