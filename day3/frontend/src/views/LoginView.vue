<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <div class="card shadow-sm">
        <div class="card-body">
          <h1 class="h4 mb-3">Login</h1>
          <p v-if="error" class="alert alert-danger py-2">{{ error }}</p>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              {{ loading ? 'Logging in…' : 'Login' }}
            </button>
          </form>
          <p class="mt-3 mb-0 small">
            No account?
            <RouterLink to="/register">Register</RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false,
    }
  },
  methods: {
    async login() {
      this.error = ''
      this.loading = true
      try {
        const res = await axios.post(`${API}/login`, {
          username: this.username,
          password: this.password,
        })
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('username', res.data.user.username)
        localStorage.setItem('role', res.data.user.role)
        const redirect = this.$route.query.redirect
        if (redirect) {
          this.$router.push(redirect)
        } else if (res.data.user.role === 'admin') {
          this.$router.push('/admin')
        } else {
          this.$router.push('/')
        }
      } catch (e) {
        this.error = e.response?.data?.msg || 'Login failed'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
