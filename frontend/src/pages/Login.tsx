import axios from "axios";
import React, { useEffect, useState } from "react";
import { FaGithub } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import ErrorPage from "../components/Error";
import Footer from "../components/Footer";
import Loading from "../components/Loading";
import Navbar from "../components/Navbar";

const Login: React.FC = () => {
  const [ssoEnabled, setSsoEnabled] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pat, setPat] = useState<string>("");
  const [accountType, setAccountType] = useState<string>("personal");
  const [enterpriseUrl, setEnterpriseUrl] = useState<string>("");
  const [submitError, setSubmitError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSSOConfig = async () => {
      try {
        const response = await axios.get("/api/helper/sso", { timeout: 5000 });
        setSsoEnabled(response.data.sso_config);
        setError(null);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error("Error fetching SSO configuration:", error.message);
          setError(`Error fetching SSO configuration: ${error.message}`);
        } else {
          console.error("Unexpected error:", error);
          setError("Unexpected error occurred");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchSSOConfig();
  }, []);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitError(null);

    if (!pat) {
      setSubmitError("GitHub PAT is required");
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post("/api/helper/validate-pat", {
        pat,
        accountType,
        apiUrl:
          accountType === "enterprise"
            ? enterpriseUrl
            : "https://api.github.com",
      });
      if (response.data.valid) {
        const { access_token, refresh_token } = response.data;
        navigate(
          `/dashboard?access_token=${access_token}&refresh_token=${refresh_token}`
        );
      } else {
        setSubmitError("Invalid or expired PAT");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setSubmitError(
          `Error submitting PAT: ${
            error.response?.data?.error || error.message
          }`
        );
        console.error("Error submitting PAT:", error.message);
      } else {
        setSubmitError("Unexpected error occurred");
        console.error("Unexpected error:", error);
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorPage message={error} />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow container mx-auto p-4 flex flex-col items-center justify-center text-center">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full">
          <h1 className="text-2xl font-bold text-white mb-4">Login</h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                className="block text-white text-sm font-bold mb-2"
                htmlFor="pat"
              >
                Personal Access Token
              </label>
              <input
                type="text"
                id="pat"
                value={pat}
                onChange={(e) => setPat(e.target.value)}
                className="w-full px-3 py-2 text-gray-700 bg-gray-200 rounded-lg focus:outline-none"
              />
            </div>
            <div className="mb-4">
              <label
                className="block text-white text-sm font-bold mb-2"
                htmlFor="accountType"
              >
                Account Type
              </label>
              <select
                id="accountType"
                value={accountType}
                onChange={(e) => setAccountType(e.target.value)}
                className="w-full px-3 py-2 text-gray-700 bg-gray-200 rounded-lg focus:outline-none"
              >
                <option value="personal">Personal</option>
                <option value="enterprise">Enterprise</option>
              </select>
            </div>
            {accountType === "enterprise" && (
              <div className="mb-4">
                <label
                  className="block text-white text-sm font-bold mb-2"
                  htmlFor="enterpriseUrl"
                >
                  Enterprise URL
                </label>
                <input
                  type="text"
                  id="enterpriseUrl"
                  value={enterpriseUrl}
                  onChange={(e) => setEnterpriseUrl(e.target.value)}
                  className="w-full px-3 py-2 text-gray-700 bg-gray-200 rounded-lg focus:outline-none"
                />
              </div>
            )}
            {submitError && (
              <p className="text-red-500 text-m ">{submitError}</p>
            )}
            <div className="flex items-center justify-between">
              <button
                type="submit"
                className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full focus:outline-none focus:shadow-outline"
              >
                Submit
              </button>
            </div>
          </form>
          {ssoEnabled && (
            <div className="mt-4">
              <button
                onClick={() =>
                  (window.location.href =
                    "http://127.0.0.1:5000/oauth/authorize")
                }
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full focus:outline-none focus:shadow-outline flex items-center justify-center"
              >
                <FaGithub className="w-6 h-6 mr-2" />
                Login with GitHub
              </button>
            </div>
          )}
        </div>
        <div className="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg text-left">
          <p className="text-white text-sm">
            <strong>NOTE:</strong> Personal GitHub accounts are for individual
            users and provide access to both public and private repositories on
            github.com. Enterprise GitHub accounts cater to organizations and
            offer additional features and controls, including access to a
            private GitHub instance. A Personal Access Token (PAT) generated
            from a personal account can only be used to access the GitHub API at{" "}
            <code className="bg-gray-500 p-1 rounded">
              https://api.github.com
            </code>
            . Similarly, a PAT generated from an enterprise account is limited
            to accessing the GitHub API at the enterprise's specific URL. An
            example of an Enterprise GitHub API URL is{" "}
            <code className="bg-gray-500 p-1 rounded">
              https://api.github.ncsu.edu
            </code>
            .
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Login;
