import axios from "axios";

const api = axios.create({
  baseURL: "/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("access") ||
      localStorage.getItem("access_token");

    console.log("URL :", config.url);
    console.log("TOKEN :", token);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    const space = localStorage.getItem("active_space");

    if (space) {
      config.params = {
        ...(config.params || {}),
        space,
      };
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;