<template>
  <div>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Logout',
  setup() {
    const router = useRouter();

    const logout = async () => {
      await axios.post('user-api/logout/', {}, {withCredentials: true});

      axios.defaults.headers.common['Authorization'] = '';
      localStorage.removeItem('refreshToken');

      await router.push('/login');
    }
    return {
      logout
    };
  }
};
</script>
