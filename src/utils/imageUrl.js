export const getImageUrl = (path) => {
  return `${import.meta.env.BASE_URL}${path.startsWith('/') ? path.slice(1) : path}`;
};
