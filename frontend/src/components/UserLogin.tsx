import React, { useState, useEffect } from "react";

// Define the shape of the data you expect from the API, adjust as needed.
interface User {
  login: string;
  name: string;
  id: string;
  email: string;
  createdAt: string;
}

interface ApiResponse {
  user: User;
}

const UserLogin: React.FC = () => {
  const [data, setData] = useState<ApiResponse | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("/api/graphql/current-user-login");
      const result: ApiResponse = await response.json();
      setData(result);
    };

    fetchData();
  }, []);

  return (
    <div>
      {data && (
        <div>
          <p>Login: {data.user.login}</p>
          <p>Name: {data.user.name}</p>
          <p>ID: {data.user.id}</p>
          <p>Email: {data.user.email}</p>
          <p>Created At: {data.user.createdAt}</p>
        </div>
      )}
    </div>
  );
};

export default UserLogin;
