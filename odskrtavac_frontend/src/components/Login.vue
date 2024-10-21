<template>
    <form @submit.prevent="login">
        <h1>Přihlásit se</h1>
        <input v-model="username" type="text" placeholder="Jméno" required />
        <input v-model="password" type="password" placeholder="Heslo" required />
        <div ref="returnMessage">{{ message }}</div>
        <button type="submit">Přihlásit se</button>
    </form>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from '../api/axios';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
        const router = useRouter();
        const username = ref('');
        const password = ref('');
        const message = ref('');
  
        async function login() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/user-api/login/', {
                    username: username.value,
                    password: password.value
                });
  
                console.log(response);
  
                // Assuming your API returns expires_in along with access and refresh tokens
                const { access, refresh, expires_in } = response.data;
  
                localStorage.setItem('access_token', access);
                localStorage.setItem('refresh_token', refresh);
                localStorage.setItem('token_expiry_time', Date.now() + expires_in * 1000); // Set expiration time
  
                message.value = response.status;
  
                router.push({ name: 'dashboard' });
            } catch (error) {
                console.log(error);
                message.value = 'Nepodařilo se přihlásit!';
            }
        }
  
        return {
            username,
            password,
            message,
            login
        };
    }
  }
  </script>
  