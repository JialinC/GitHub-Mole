import axios from 'axios';
import axiosInstance from "./axiosConfig";
import { PageInfo, FetchFunction, FetchFunctions} from "../types/Types";


const findPageInfo = (data: any): PageInfo | null => {
    if (typeof data === "object" && data !== null) {
      if ("pageInfo" in data) {
        return data.pageInfo;
      }
      for (const key in data) {
        if (data.hasOwnProperty(key)) {
          const result = findPageInfo(data[key]);
          if (result) {
            return result;
          }
        }
      }
    }
    return null;
  };

const fetchData = async (url: string, setError: (error: string | null) => void, params: any = {}, signal?: AbortSignal) => {
  setError(null);
  try {
    const response = await axiosInstance.get(url, { params, signal });
    return response;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled', error.message);
    } else {
      setError(`Error fetching data from endpoint ${url}`);
      console.error(`Error fetching data from endpoint ${url}:`, error);
    }
    throw error;
  }
};

const postData = async (
  url: string,
  setError: (error: string | null) => void,
  data: any = {},
  signal?: AbortSignal
) => {
  setError(null);
  try {
    const response = await axiosInstance.post(url, data, { signal });
    return response;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled', error.message);
    } else {
      setError(`Error posting data to endpoint ${url}`);
      console.error(`Error posting data to endpoint ${url}:`, error);
    }
    throw error;
  }
};


export const fetchRateLimit = async (setError: (error: string | null) => void) => {
    const response = await fetchData("api/graphql/rate-limit", setError, {});
    return response.data.rateLimit;
};

export const fetchCurUser = async (setError: (error: string | null) => void) => {
  const response = await fetchData("api/graphql/current-user-login", setError, {});
  return response.data;
};

export const fetchProfile: FetchFunction = async (login: string, setError: (error: string | null) => void) => {
  const response = await fetchData(`/api/graphql/user-profile-stats/${login}`, setError);
  return response.data;
};

export const fetchContributions: FetchFunction = async (login: string, setError: (error: string | null) => void) => {
  const response = await fetchData(`/api/graphql/user-contributions-collection/${login}`, setError);
  return response.data;
};

export const fetchContribYears: FetchFunction = async (login: string, setError: (error: string | null) => void) => {
  const response = await fetchData(`api/graphql/user-contribution-years/${login}`, setError);
  return response.data;
};

export const fetchCalendar: FetchFunction = async (login: string, setError: (error: string | null) => void, start: string | null = null, end: string | null = null) => {
  const response = await fetchData(`/api/graphql/user-contribution-calendar/${login}`, setError, {start, end});
  return response.data;
};

export const fetchCommitComments: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-commit-comments/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchGistComments: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-gist-comments/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchIssueComments: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-issue-comments/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchRepositoryDiscussionComments: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repository-discussion-comments/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchGists: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-gists/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchIssues: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-issues/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchPullRequests: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-pull-requests/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchRepositoryDiscussions: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repository-discussions/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchARepos: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repositories-a/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchBRepos: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repositories-b/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchCRepos: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repositories-c/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchDRepos: FetchFunction = async (
  login: string,
  setError: (error: string | null) => void,
  end_cursor: string | null = null
) => {
    const response = await fetchData(`/api/graphql/user-repositories-d/${login}`, setError, { end_cursor });
    return response.data;
};

export const fetchFunctions: FetchFunctions = {
  Profile:fetchProfile,
  Contributions:fetchContributions,
  "Commit Comments": fetchCommitComments,
  "Gist Comments": fetchGistComments,
  "Issue Comments": fetchIssueComments,
  "Repository Discussion Comments": fetchRepositoryDiscussionComments,
  Gists: fetchGists,
  Issues: fetchIssues,
  "Pull Requests": fetchPullRequests,
  "Repository Discussions": fetchRepositoryDiscussions,
  "Owned Original Repo": fetchARepos,
  "Owned Forked Repo": fetchBRepos,
  "Collaborating Original Repo": fetchCRepos,
  "Collaborating Forked Repo": fetchDRepos,
};

// Database interaction functions
export const checkDuplicate = async (
  params: { [key: string]: string },
  setError: (error: string | null) => void,
) => {
    const response = await postData(`/api/db/check-duplicate`, setError, params);
    return response.data;
};

export const saveToDatabase = async (
  params: { [key: string]: string | string[][] },
  setError: (error: string | null) => void,
) => {
    const response = await postData(`/api/db/save-data`, setError, params);
    return response.data;
};