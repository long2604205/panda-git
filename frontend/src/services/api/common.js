import api from '@/plugins/api.js'

const commonApi = {
  open: (data) => api.post('/open-repository', data),
  fetch: (data) => api.post('/fetch', data),
  pull: (data) => api.post('/pull', data),
  push: (data) => api.post('/push', data),
};

export default commonApi;
