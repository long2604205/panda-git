import api from '@/plugins/api.js'

const commonApi = {
  open: (data) => api.post('/open-repository', data),
};

export default commonApi;
