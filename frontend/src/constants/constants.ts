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
    Contributions:["GitHub ID","Name","Email","Created At","Bio","Company",
        "Watching",
        "Starred Repositories",
        "Following",
        "Followers",
        "Private Contributions",
        "Commit Contributions",
        "Gists",
        "Issues",
        "Projects",
        "Pull Requests",
        "Repositories",
        "Repository Discussions",
        "Gist Comments",
        "Issue Comments",
        "Commit Comments",
        "Repository Discussion Comments",
        "Owned Original Repo",	"Owned Original Repo Size",	"Owned Original Repo Selected Langs Size",
        "Owned Forked Repo", "Owned Forked Repo Size",	"Owned Forked Repo Selected Langs Size",
        "Collaborating Original Repo",	"Collaborating Original Repo Size",	"Collaborating Original Repo Selected Langs Size",
        "Collaborating Forked Repo", "Collaborating Forked Repo Size",	"Collaborating Forked Repo Selected Langs Size"
    ],
    "Commit Comments":["Github ID","Created At","Body Text"],	
    "Gist Comments":["Github ID","Created At","Body Text"],
    "Issue Comments":["Github ID","Created At","Body Text"],
    "Repository Discussion Comments":["Github ID","Created At","Body Text"],
    commits:[], // to be implemented
    "Gists":["Github ID","Created At","Description"],
    "Issues":["Github ID","Created At","Body Text","Title"],
    "Pull Requests":["Github ID","Created At","Body Text"],
    "Repository Discussions":["Github ID","Created At","Body Text"],
    Repositories:["Github ID","Name","Created At","Updated At","Primary Language","Language Stats"]
}
