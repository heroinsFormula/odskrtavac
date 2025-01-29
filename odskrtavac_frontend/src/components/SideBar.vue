<template>
<!-- ===== Sidebar Start ===== -->
  <aside class="absolute left-0 top-0 z-9999 flex h-screen w-72.5 flex-col overflow-y-hidden bg-black duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0 -translate-x-full">
    <div :class="{
      'w-64': isOpen,
      'w-0': !isOpen
    }" class="bg-gray-800 text-white transition-all duration-300 h-full overflow-hidden">
      <div class="p-4">
        <button @click="toggleDrawer" class="text-gray-300 hover:text-white">
          <span v-if="isOpen">&laquo; Close</span>
          <span v-else>&raquo; Open</span>
        </button>
      </div>

      <div v-if="isOpen" class="mt-4">
        <UsersBooklistAttributes />
      </div>
    </div>

    <div :class="{ 'ml-64': isOpen, 'ml-0': !isOpen }" class="flex-1 bg-gray-100 p-6 transition-all duration-300">
      <slot></slot>
    </div>
  </aside>
<!-- ===== Sidebar End ===== -->
</template>

<script>
import UsersBooklistAttributes from './UsersBooklistAttributes.vue';

export default {
  name: "SidebarDrawer",
  components: {
    UsersBooklistAttributes,
  },
  data() {
    return {
      isOpen: true,
    };
  },
  methods: {
    toggleDrawer() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
