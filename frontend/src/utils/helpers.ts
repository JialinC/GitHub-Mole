import { Repository } from "../types/Types";

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
