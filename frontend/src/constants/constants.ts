type TableHeaders = {
    [key: string]: string[];
  };

export const contributions = [
    "Commit Comments",
    "Gist Comments",
    "Issue Comments",
    "Repository Discussion Comments",
    "Gists",
    "Issues",
    "Pull Requests",
    "Repository Discussions",
    "Owned Original Repo",
    "Owned Forked Repo",
    "Collaborating Original Repo",
    "Collaborating Forked Repo",
  ];

  export const languages = [
    "Python",
    "Java",
    "Go",
    "JavaScript",
    "C++",
    "TypeScript",
    "PHP",
    "Ruby",
    "C",
    "C#",
    "Nix",
    "Shell",
    "Rust",
    "Scala",
    "Kotlin",
    "Swift",
    "Dart",
    "Perl",
    "Lua",
    "All",
  ];

  export const teamTableHeaders = ["Github ID","Age (days)","Commits","Comments","PRs & Issues","Lang Counts","Pop Lang Size","Repos"];

  export  const tableHeaders: TableHeaders = { 	
    Contributions:["GitHub ID","Name","Email","Created At","Age (days)","Bio","Company",
        "Watching",
        "Starred Repositories",
        "Following",
        "Followers",
        "Private Contributions",
        "Commits",
        "Gists",
        "Issues",
        "Projects",
        "Pull Requests",
        "Pull Request Reviews",
        "Repositories",
        "Repository Discussions",
        "Commit Comments",
        "Issue Comments",
        "Gist Comments",
        "Repository Discussion Comments",
        "Owned Original Repo",	"Owned Original Repo Size",	"Owned Original Repo Selected Langs Size", "Owned Original Repo Langs Number",
        "Owned Forked Repo", "Owned Forked Repo Size",	"Owned Forked Repo Selected Langs Size", "Owned Forked Repo Langs Number",
        "Collaborating Original Repo",	"Collaborating Original Repo Size",	"Collaborating Original Repo Selected Langs Size", "Collaborating Original Repo Langs Number",
        "Collaborating Forked Repo", "Collaborating Forked Repo Size",	"Collaborating Forked Repo Selected Langs Size", "Collaborating Forked Repo Langs Size Number",
        "Total Langs Number"
    ],
    "Commit Comments":["GitHub ID","Created At","Body Text"],	
    "Gist Comments":["GitHub ID","Created At","Body Text"],
    "Issue Comments":["GitHub ID","Created At","Body Text"],
    "Repository Discussion Comments":["GitHub ID","Created At","Body Text"],
    commits:[], // to be implemented
    "Gists":["GitHub ID","Created At","Description"],
    "Issues":["GitHub ID","Created At","Body Text","Title"],
    "Pull Requests":["GitHub ID","Created At","Body Text"],
    "Repository Discussions":["GitHub ID","Created At","Body Text"],
    "Owned Original Repo":["GitHub ID","Name","Created At","Updated At","Primary Language","Language Stats"],
    "Owned Forked Repo":["GitHub ID","Name","Created At","Updated At","Primary Language","Language Stats"],
    "Collaborating Original Repo":["GitHub ID","Name","Created At","Updated At","Primary Language","Language Stats"],
    "Collaborating Forked Repo":["GitHub ID","Name","Created At","Updated At","Primary Language","Language Stats"],
  }

  export const repoTypes: string[] = ["Owned Original Repo",
    "Owned Forked Repo","Collaborating Original Repo","Collaborating Forked Repo"];