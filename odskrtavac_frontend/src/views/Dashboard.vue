<script setup>
import BookTable from '/src/components/BookTable.vue';
import NavBar from '/src/components/NavBar.vue';
import SideBar from '@/components/SideBar.vue';
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <NavBar></NavBar>
    <SideBar></SideBar>
    <BookTable>
    </BookTable>
  </div>
</template>

<script>

</script>