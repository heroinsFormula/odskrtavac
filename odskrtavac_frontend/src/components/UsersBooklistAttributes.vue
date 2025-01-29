<template>
  <ul>
    <li class="text-black" v-for="(value, attribute) in booklistAttributes" :key="attribute">
      <strong>{{ attribute }}:</strong> {{ value }}
    </li>
  </ul>
</template>

<script>
import { bookService } from '@/api/bookService';
import { useBookStore } from '@/stores/bookStore';

export default {
  computed: {
    booklistAttributes() {
      const store = useBookStore(); // Access Pinia store
      return store.booklistAttributes; // Reactive values from the store
    },
  },
  async mounted() {
    try {
      const store = useBookStore(); // Access the Pinia store
      const response = await bookService.getBooklistAttributes();
      store.setBooklistAttributes(response.data); // Update the store state with the fetched data
    } catch (error) {
      console.error('Failed to fetch booklist attributes:', error);
    }
  },
};
</script>
