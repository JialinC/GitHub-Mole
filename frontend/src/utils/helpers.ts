import { Repository } from "../types/Types";
import { Dispatch, SetStateAction } from 'react';
import Papa from 'papaparse';

export const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };
  
export const convertToLocalTime = (utcTimeString: string): string => {
  return new Date(utcTimeString).toLocaleString();
};

export const isoTimeToLocalTime = (isoTime: string): string => {
  return new Date(isoTime).toLocaleString();
};

export const getUserAvatarUrl = (): string | null => {
  const storedUser = localStorage.getItem("curUser");
  if (storedUser) {
    const user = JSON.parse(storedUser);
    return user.avatarUrl;
  }
  return null;
};

export const calculateLifetime = (createdAt: string): number => {
  const ghStart = new Date(createdAt);
  const ghEnd = new Date();
  const differenceInTime = ghEnd.getTime() - ghStart.getTime();
  const differenceInDays = differenceInTime / (1000 * 3600 * 24);
  return Math.floor(differenceInDays);
};

export const calLangStats = (
  repos: Repository[],
  selectedLangs: Set<string>,
  langSet: Set<string>
): { selectedSize: number; totalSize: number } => {
  let selectedSize = 0;
  let totalSize = 0;
  for (const repo of repos) {
    const languages = repo.languages;
    for (const language of languages.edges) {
      const lang = language.node.name;
      const lsize = language.size;
      totalSize += lsize;
      if (selectedLangs.has("All") || selectedLangs.has(lang)) {
        selectedSize += lsize;
      }
      langSet.add(lang);
    }
  }
  return { selectedSize, totalSize };
};

export const chunkArray = (array: string[], chunkSize: number): string[][] => {
  const chunks = [];
  for (let i = 0; i < array.length; i += chunkSize) {
    chunks.push(array.slice(i, i + chunkSize));
  }
  return chunks;
};

export const addLoadingRow = (setTableData: React.Dispatch<React.SetStateAction<string[][] | null>>, l: number) => {
  const row = Array(l).fill("Loading...");
  setTableData((prevData) => (prevData ? [...prevData, row] : [row]));
};

export const addNARow = (setTableData: React.Dispatch<React.SetStateAction<string[][] | null>>, l: number) => {
  const row = Array(l).fill("N/A");
  setTableData((prevData) => (prevData ? [...prevData, row] : [row]));
};

export const removeLastRow = (setTableData: React.Dispatch<React.SetStateAction<string[][] | null>>) => {
  setTableData((prevData) => {
    if (!prevData || prevData.length === 0) return prevData;
    return prevData.slice(0, -1);
  });
};

export const toCamelCase = (str: string): string => {
  return str
    .split(' ')
    .map((word, index) => {
      if (index === 0) {
        return word.toLowerCase();
      }
      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    })
    .join('');
};


interface HandleFileChangeParams {
  event: React.ChangeEvent<HTMLInputElement>;
  setErrors: Dispatch<SetStateAction<{ [key: string]: string }>>;
  setFile: Dispatch<SetStateAction<File | null>>;
  maxSizeInMB?: number;
}

export const handleFileChange = ({
  event,
  setErrors,
  setFile,
  maxSizeInMB = 5, // Default maximum file size is 5 MB
}: HandleFileChangeParams) => {
  if (event.target.files && event.target.files.length > 0) {
    const selectedFile = event.target.files[0];
    if (selectedFile.size > maxSizeInMB * 1024 * 1024) {
      setErrors((prevErrors) => ({
        ...prevErrors,
        file: `File size exceeds ${maxSizeInMB} MB`,
      }));
      setFile(null);
    } else {
      setErrors((prevErrors) => ({ ...prevErrors, file: "" }));
      setFile(selectedFile);
    }
  }
};


export const validateSelfDataFile = (file: File): Promise<void> => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      complete: (results) => {
        const data = results.data as string[][];

        if (data.length === 0) {
          return reject(new Error("The file is empty."));
        }

        const headers = data[0];
        if (headers.length === 0) {
          return reject(new Error("The file must contain a title row."));
        }

        for (let i = 1; i < data.length; i++) {
          const row = data[i];

          if (row.length !== headers.length) {
            return reject(
              new Error(`Row ${i + 1} does not match the header length.`)
            );
          }

          // Check if the first column is a user identifier (non-empty string)
          if (!row[0] || typeof row[0] !== "string") {
            return reject(
              new Error(`Invalid user identifier in row ${i + 1}.`)
            );
          }

          // Check if all other columns contain numbers (either integer or double)
          for (let j = 1; j < row.length; j++) {
            if (isNaN(Number(row[j]))) {
              return reject(
                new Error(`Invalid number in row ${i + 1}, column ${j + 1}.`)
              );
            }
          }
        }

        resolve();
      },
      error: (error) => {
        reject(new Error(`Failed to parse CSV file: ${error.message}`));
      },
      header: false,
      skipEmptyLines: true,
    });
  });
};

export const validateGitHubIdsFile = (file: File): Promise<void> => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      complete: (results) => {
        const data = results.data as string[][];

        if (data.length === 0) {
          return reject(new Error("The file is empty."));
        }

        const headers = data[0];
        if (headers.length === 0 || headers[0] !== "GitHub ID") {
          return reject(
            new Error(
              'The file must include a title row with the column title "GitHub ID".'
            )
          );
        }

        for (let i = 1; i < data.length; i++) {
          const row = data[i];

          if (row.length !== headers.length) {
            return reject(
              new Error(`Row ${i + 1} does not match the header length.`)
            );
          }

          // Check if the first column is a GitHub ID (non-empty string)
          if (!row[0] || typeof row[0] !== "string") {
            return reject(new Error(`Invalid GitHub ID in row ${i + 1}.`));
          }
        }

        resolve();
      },
      error: (error) => {
        reject(new Error(`Failed to parse CSV file: ${error.message}`));
      },
      header: false,
      skipEmptyLines: true,
    });
  });
};

export const handleWaitTime = (
  waitTime: number,
  setTotTime: Dispatch<SetStateAction<number>>,
  setRemTime: Dispatch<SetStateAction<number>>,
  setNoRateLimit: Dispatch<SetStateAction<boolean>>
): Promise<void> => {
  return new Promise<void>((resolve) => {
    const endTime = Date.now() + (waitTime + 3) * 1000;
    setTotTime(waitTime + 3);
    let bool = true;
    const interval = setInterval(() => {
      const timeLeft = Math.max(0, endTime - Date.now());
      setRemTime(Math.ceil(timeLeft / 1000)); // Update countdown state
      if (bool) {
        setNoRateLimit(true);
        bool = false;
      }
      if (timeLeft === 0) {
        clearInterval(interval);
        setNoRateLimit(false);
        setRemTime(1000 - 1); // Reset countdown state
        setTotTime(1000);
        resolve();
      }
    }, 1000);
  });
};

type FetchFunction = (...args: any[]) => Promise<any>;

export const fetchWithRateLimit = async (
  fetchFunction: FetchFunction,
  handleWaitTime: (waitTime: number, ...args: any[]) => Promise<void>,
  ...args: any[]
): Promise<any> => {
  let response = await fetchFunction(...args);
  if ("no_limit" in response) {
    await handleWaitTime(response.wait_seconds, ...args);
    response = await fetchFunction(...args);
  }
  return response;
};