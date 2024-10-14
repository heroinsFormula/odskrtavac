<template>
  <div>
    <h2>Logout</h2>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  methods: {
    async logout() {
      try {
        const csrfToken = this.$getCookie('csrftoken'); 
        const response = await fetch("http://localhost:8000/user_api/logout/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken,
          },
          credentials: "include", // Important for session cookies
        });
        if (response.ok) {
          console.log("Logout successful");
          // Redirect or clear session info
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },
};
</script>
