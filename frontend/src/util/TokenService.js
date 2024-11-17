export const igSaveToken = (token) => {
  localStorage.setItem("access_token", token);
};

export const igGetToken = () => {
  return localStorage.getItem("access_token");
};

export const igClearToken = () => {
  localStorage.removeItem("access_token");
};

export const igSaveRefreshToken = (token) => {
  localStorage.setItem("refresh_token", token);
};

export const igGetRefreshToken = () => {
  return localStorage.getItem("refresh_token");
};

export const igClearRefreshToken = () => {
  localStorage.removeItem("refresh_token");
};

export const tiktokSaveToken = (token) => {
  localStorage.setItem("tiktok_access_token", token);
};

export const tiktokGetToken = () => {
  return localStorage.getItem("tiktok_access_token");
};

export const tiktokClearToken = () => {
  localStorage.removeItem("tiktok_access_token");
};

export const tiktokSaveRefreshToken = (token) => {
  localStorage.setItem("tiktok_refresh_token", token);
};

export const tiktokGetRefreshToken = () => {
  return localStorage.getItem("tiktok_refresh_token");
};

export const tiktokClearRefreshToken = () => {
  localStorage.removeItem("tiktok_refresh_token");
};
