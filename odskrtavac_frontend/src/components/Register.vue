<script setup>
import { ref } from 'vue';
import axios from 'axios';
</script>


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
const message = ref("");

export default {
    data() {
        return {
        username: '',
        password: ''
        };
    },
    methods: {
        async register() {
            await axios.post('http://127.0.0.1:8000/user_api/register/', {
            username: this.username,
            password: this.password
            })
            .then(function (response) {
                message.value = response.data.message;
            })
            .catch(function (error) {
                message.value = error.response.data.error;
            });
        }
    }
};
</script>
  