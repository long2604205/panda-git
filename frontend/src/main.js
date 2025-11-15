import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// Import Font Awesome CSS
import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';
import api from '@/plugins/api.js'
const app = createApp(App)

app.config.globalProperties.$api = api;
app.use(createPinia())
app.use(router)

app.mount('#app')
