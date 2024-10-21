<template>
    <form @submit.prevent="register">
    <h1>Registrovat se</h1>
        <input v-model="username" type="text" placeholder="Jméno" required>
        <input v-model="password" type="password" placeholder="Heslo" required>
        <div ref="returnMessage">{{ message }}</div>
    <button type="submit">Registrovat se</button>
    </form>
</template>
  
<script>import { ref } from 'vue';
import axios from '../api/axios';
import { useRouter } from 'vue-router';

export default {
    setup() {
        const router = useRouter();
        const username = ref('');
        const password = ref('');
        const message = ref('');
    
        async function register() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/user-api/register/', {
                    username: username.value,
                    password: password.value
                });
                
                console.log(response);

                if (response.status === 201 || response.status === 200) {
                    const loginResponse = await axios.post('http://127.0.0.1:8000/user-api/login/', {
                        username: username.value,
                        password: password.value
                    });

                    console.log(loginResponse);

                    localStorage.setItem('access_token', loginResponse.data.access);
                    localStorage.setItem('refresh_token', loginResponse.data.refresh);

                    router.push({ name: 'dashboard' });
                } else {
                    message.value = 'Nepodařilo se registrovat!';
                }
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
  