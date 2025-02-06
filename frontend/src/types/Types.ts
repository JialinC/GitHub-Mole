export interface CurUser {
  avatarUrl: string;
  login: string;
  created_at: string;
  followers: number;
  following: number;
  watching: number;
  starred_repositories: number;
  gists: number;
  issues: number;
  projects: number;
  pull_requests: number;
  repositories: number;
  repository_discussions: number;
  commit_comments: number;
  gist_comments: number;
  issue_comments: number;
  repository_discussion_comments: number;
}

export interface Contributions {
  commit: number;
  pr_review: number;
  res_con: number;
}

export interface PageInfo {
  endCursor: string;
  hasNextPage: boolean;
}

export type Repository = {
  languages: {
    edges: {
      node: {
        name: string;
      };
      size: number;
    }[];
  };
};

export type FetchFunction = (login: string, setError: (error: string | null) => void, start?: string | null, end?: string | null, end_cursor?: string | null) => Promise<any>;

export type FetchFunctions = {
  "Profile": FetchFunction;
  "Contributions": FetchFunction;
  "Commit Comments": FetchFunction;
  "Gist Comments": FetchFunction;
  "Issue Comments": FetchFunction;
  "Repository Discussion Comments": FetchFunction;
  "Gists": FetchFunction;
  "Issues": FetchFunction;
  "Pull Requests": FetchFunction;
  "Repository Discussions": FetchFunction;
  "Owned Original Repo": FetchFunction;
  "Owned Forked Repo": FetchFunction;
  "Collaborating Original Repo": FetchFunction;
  "Collaborating Forked Repo": FetchFunction;
};


export type FetchFunctionKeys =
  | "Profile"
  | "Contributions"
  | "Commit Comments"
  | "Gist Comments"
  | "Issue Comments"
  | "Repository Discussion Comments"
  | "Gists"
  | "Issues"
  | "Pull Requests"
  | "Repository Discussions"
  | "Owned Original Repo"
  | "Owned Forked Repo"
  | "Collaborating Original Repo"
  | "Collaborating Forked Repo";