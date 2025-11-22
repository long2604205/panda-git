import api from '@/plugins/api.js'

const commonApi = {
  open: (data) => api.post('/open-repository', data),
  fetch: (data) => api.post('/fetch', data),
  pull: (data) => api.post('/pull', data),
  push: (data) => api.post('/push', data),
  checkout: (data) => api.post('/checkout-branch', data),
};

export default commonApi;
