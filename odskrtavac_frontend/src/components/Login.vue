<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; 


const router = useRouter();
const username = ref('');
const password = ref('');
const message = ref("");

async function login() {
    try {
        const response = await axios.post('http://127.0.0.1:8000/user_api/login/', {
            username: username.value,
            password: password.value
        });

        console.log(response);
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        message.value = response.status;

        
        router.push({ name: 'dashboard' });
    } catch (error) {
        console.log(error);
        message.value = "nepodařilo se přihlásit";
    }
}
</script>

<template>
  <form @submit.prevent="login">
      <h1>Přihlásit se</h1>
      <input v-model="username" type="text" placeholder="Jméno" required />
      <input v-model="password" type="password" placeholder="Heslo" required />
      <div ref="returnMessage">{{ message }}</div>
      <button type="submit">Přihlásit se</button>
  </form>
</template>
