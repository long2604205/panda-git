import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// (Optional) Thêm interceptors nếu cần
instance.interceptors.request.use(config => {
  // Thêm token nếu có
  // config.headers.Authorization = 'Bearer ...';
  return config;
});

const api = {
  get: async (url, config = {}) => {
    try {
      const res = await instance.get(url, config);
      return res.data;
    } catch (err) {
      console.error(`API GET ERROR: ${url}`, err);
      throw err.response?.data || err.message || 'GET Error';
    }
  },
  post: async (url, data = {}, config = {}) => {
    try {
      const res = await instance.post(url, data, config);
      return res.data;
    } catch (err) {
      console.error(`API POST ERROR: ${url}`, err);
      throw err.response?.data || err.message || 'POST Error';
    }
  },
  put: async (url, data = {}, config = {}) => {
    try {
      const res = await instance.put(url, data, config);
      return res.data;
    } catch (err) {
      console.error(`API PUT ERROR: ${url}`, err);
      throw err.response?.data || err.message || 'PUT Error';
    }
  },
  delete: async (url, config = {}) => {
    try {
      const res = await instance.delete(url, config);
      return res.data;
    } catch (err) {
      console.error(`API DELETE ERROR: ${url}`, err);
      throw err.response?.data || err.message || 'DELETE Error';
    }
  },
};

export default api;
