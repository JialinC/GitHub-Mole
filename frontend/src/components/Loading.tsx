import { ClipLoader } from "react-spinners";

const Loading = ({ size = 150, color = "#ff0000" }) => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <ClipLoader size={size} color={color} loading={true} />
    </div>
  );
};

export default Loading;
