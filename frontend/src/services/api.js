import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Интерцептор для добавления токена к запросам
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_role");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export const authAPI = {
  login: (username, password) =>
    api.post("/auth/login", `username=${username}&password=${password}`, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }),
};

export const productsAPI = {
  getProducts: () => api.get("/products/"),
  getProduct: (id) => api.get(`/products/${id}`),
  getProductByQR: (qrCode) => api.get(`/products/qr/${qrCode}`),
  createProduct: (data) => api.post("/products/", data),
};
