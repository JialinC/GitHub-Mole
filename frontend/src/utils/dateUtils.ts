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