import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import AuthForm from '/src/components/views/AuthForm.vue';

import axios from 'axios';

axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);



const app = createApp(App);
app.use(router);
app.component('AuthForm', AuthForm);
app.mount('#app');
