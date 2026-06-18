<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <RouterLink class="navbar-brand" to="/">Task Manager</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="mainNav" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li v-if="loggedIn && isEmployee" class="nav-item">
            <RouterLink class="nav-link" to="/">My Tasks</RouterLink>
          </li>
          <li v-if="loggedIn && isAdmin" class="nav-item">
            <RouterLink class="nav-link" to="/admin">Manage Tasks</RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li v-if="loggedIn" class="nav-item">
            <span class="navbar-text me-3">Hi, {{ username }}</span>
          </li>
          <li v-if="loggedIn" class="nav-item">
            <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
          </li>
          <li v-if="!loggedIn" class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
          <li v-if="!loggedIn" class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  computed: {
    loggedIn() {
      return !!localStorage.getItem('token')
    },
    username() {
      return localStorage.getItem('username') || ''
    },
    isAdmin() {
      return localStorage.getItem('role') === 'admin'
    },
    isEmployee() {
      return localStorage.getItem('role') === 'employee'
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.$router.push('/login')
    },
  },
}
</script>
