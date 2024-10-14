<script setup>
import { ref } from 'vue';
import axios from 'axios';
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
        async login() {
            await axios.post('http://127.0.0.1:8000/user_api/login/', {
            username: this.username,
            password: this.password
            })
            .then(function (response) {
                console.log(response)
                // message.value = response.data.message;
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                message.value = response.status;
            })
            .catch(function (error) {
                console.log(error)
                message.value = "nepodařilo se přihlásit";
            });
        }
    }
};
</script>
