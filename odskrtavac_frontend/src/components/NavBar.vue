<template>
  <header class="fixed top-0 left-0 w-screen bg-black text-white shadow-md z-50">
    <div class="flex justify-between items-center max-w-screen-xl mx-auto px-4 h-16">
      <h1 class="text-xl font-bold">My App</h1>
      <nav>
        <ul class="flex gap-6">
          <li><a href="#home" class="hover:text-gray-300">Home</a></li>
          <li><a href="#about" class="hover:text-gray-300">About</a></li>
          <li><a href="#contact" class="hover:text-gray-300">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style scoped></style>
