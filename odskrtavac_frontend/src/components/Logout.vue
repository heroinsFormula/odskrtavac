<template>
  <div>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'LogoutComponent',
  setup() {
    const router = useRouter();

    const logout = async () => {
      try {
        const refresh_token = localStorage.getItem('refresh_token');
        
        if (!refresh_token) {
          return;
        }

        await axios.post('http://localhost:8000/user-api/logout/', { refresh_token });
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        router.push('/login');
      } catch (error) {
        console.error('Logout failed', error);
      }
    };

    return {
      logout
    };
  }
};
</script>
