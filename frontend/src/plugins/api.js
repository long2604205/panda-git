import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// (Optional) Thêm interceptors nếu cần
api.interceptors.request.use(config => {
  // Thêm token nếu có
  // config.headers.Authorization = 'Bearer ...';
  return config;
});

export default api;
