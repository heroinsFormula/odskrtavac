<template>
    <form @submit.prevent="register">
    <h1>Registrovat se</h1>
        <input v-model="username" type="text" placeholder="Jméno" required>
        <input v-model="password" type="password" placeholder="Heslo" required>
        <div ref="returnMessage">{{ message }}</div>
    <button type="submit">Registrovat se</button>
    </form>
</template>
  
<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
    name: 'Register',
    setup() {
        const router = useRouter();
        const username = ref('');
        const password = ref('');
        const message = ref('');
    
        async function register() {
            try {
                const response = await axios.post('user-api/register/', {
                    username: username.value,
                    password: password.value
                });
                console.log(response);
            } catch (error) {
                console.log(error);
                message.value = 'Nepodařilo se registrovat!';
            }
        }
        return {
            username,
            password,
            message,
            register
        };
    }
}
</script>
  