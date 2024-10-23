import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import AuthForm from './components/views/AuthForm.vue';
import './interceptors/axios';



const app = createApp(App);
app.use(router);
app.component('AuthForm', AuthForm);
app.mount('#app');
