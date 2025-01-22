import React from "react";

export const gitHubCSV: React.ReactNode = (
  <>
    Please upload a CSV file containing a list of GitHub IDs. The file must
    include a title row with the column title
    <span className="font-semibold text-white"> "GitHub ID"</span>. An example
    file containing four GitHub IDs (A, B, C, D) is shown below:
  </>
);

export const langsDesc: React.ReactNode = (
  <>
    Please select the programming languages you are interested in analyzing for
    the users. The application will query and calculate the code size in these
    languages across the users' repositories. For example, if you select{" "}
    <span className="font-semibold text-white">"Python"</span> and{" "}
    <span className="font-semibold text-white">"Java"</span>, the application
    will retrieve and compute the size of code written in Python and Java within
    various user repositories. If you select{" "}
    <span className="font-semibold text-white">"ALL"</span>, the application
    will calculate the total size of code across all repository types. Note:
    Selecting <span className="font-semibold text-white">"ALL"</span> will
    include code sizes for languages such as{" "}
    <span className="font-semibold text-white">"HTML"</span>, which may not
    align with your specific needs.
  </>
);

export const contribsDesc: React.ReactNode = (
  <>
    Please select the type of contribution you are interested in analyzing for
    the users. The application will query and retrieve detailed information for
    the selected contribution type. For example, if you select{" "}
    <span className="font-semibold text-white">"Commit Comments"</span>, the
    application will retrieve all commit comments made by the user, including
    the content of the comments and the time they were created.
  </>
);

export const ownCSV: React.ReactNode = (
  <>
    Please upload a CSV file containing a list of GitHub IDs. The file must
    include a title row with the column title The file must contain a title row
    that marks the title of each column. The first column must be a user
    identifier in whatever format, and all other columns must contain numbers
    (either integer or double).
    <span className="font-semibold text-white"> "GitHub ID"</span>. An example
    file containing four GitHub IDs (A, B, C, D) is shown below:
  </>
);
