import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import AuthForm from './components/views/AuthForm.vue';
import './interceptors/axios';
import * as bootstrap from 'bootstrap/dist/js/bootstrap.bundle';
import './assets/main.css';



const app = createApp(App);
app.use(router);
app.component('AuthForm', AuthForm);
app.provide('bootstrap', bootstrap);
app.mount('#app');
