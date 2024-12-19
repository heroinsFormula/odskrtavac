<template>
  <ul>
    <li v-for="(value, attribute) in booklistAttributes" :key="attribute">
      <strong>{{ attribute }}:</strong> {{ value }}
    </li>
  </ul>
</template>

<script>
import { bookService } from '@/api/bookService';

export default {
  data() {
    return {
      booklistAttributes: {}
    };
  },
  methods: {
    async getBooklistAttributes() {
      try {
        const response = await bookService.getBooklistAttributes();
        this.booklistAttributes = response.data;
      } catch (error) {
        console.error("Error fetching booklist attributes:", error);
      }
    }
  },
  mounted() {
    this.getBooklistAttributes();
  }
};
</script>
