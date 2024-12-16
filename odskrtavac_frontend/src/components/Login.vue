<template>
    <form @submit.prevent="login">
        <h1>Chury je vůl!!</h1>
        <input v-model="username" type="text" placeholder="Jméno" required />
        <input v-model="password" type="password" placeholder="Heslo" required />
        <div ref="returnMessage">{{ message }}</div>
        <button type="submit">Přihlásit se</button>
    </form>
  </template>
  
<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
    name: 'Login',
    setup() {
        const router = useRouter();
        const username = ref('');
        const password = ref('');
        const message = ref('');

        async function login() {
            try {
                const {data} = await axios.post('user-api/login/', {
                    username: username.value,
                    password: password.value
                }, {
                    withCredentials: true
                });
                
                axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
                localStorage.setItem('refresh_token', data.refresh);

                router.push({ name: 'dashboard' });
            } catch (error) {
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
  
