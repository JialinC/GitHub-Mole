import React from "react";
import { useNavigate } from "react-router-dom";

interface CardButtonProps {
  icon: React.ReactNode;
  text: string;
  navigateTo: string;
}

const CardButton: React.FC<CardButtonProps> = ({ icon, text, navigateTo }) => {
  const navigate = useNavigate();

  return (
    <button
      className="bg-zinc-500 bg-opacity-80 p-8 rounded-lg shadow-lg text-white flex items-center justify-center flex-col transform transition-transform duration-300 hover:scale-105"
      onClick={() => navigate(navigateTo)}
    >
      {icon}
      <h3 className="text-xl font-bold mb-4">{text}</h3>
    </button>
  );
};

export default CardButton;
