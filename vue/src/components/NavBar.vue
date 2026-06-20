<template>
  <header class="navbar">
    <span class="brand">Taskmanager</span>
    <button type="button" class="logout-button" @click="$emit('logout')">Logout</button>
  </header>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  background: #ffffff;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
}

.logout-button {
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  background: #111827;
  color: #ffffff;
  cursor: pointer;
}
</style>