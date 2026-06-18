<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <div class="card shadow-sm">
        <div class="card-body">
          <h1 class="h4 mb-3">Register</h1>
          <p v-if="error" class="alert alert-danger py-2">{{ error }}</p>
          <p v-if="success" class="alert alert-success py-2">{{ success }}</p>
          <form @submit.prevent="register">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Email (optional)</label>
              <input v-model="email" type="email" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              {{ loading ? 'Creating…' : 'Register' }}
            </button>
          </form>
          <p class="mt-3 mb-0 small">
            Already have an account?
            <RouterLink to="/login">Login</RouterLink>
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
      email: '',
      password: '',
      error: '',
      success: '',
      loading: false,
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.success = ''
      this.loading = true
      try {
        await axios.post(`${API}/register`, {
          username: this.username,
          password: this.password,
          email: this.email || undefined,
        })
        this.success = 'Account created. You can log in now.'
        this.$router.push('/login')
      } catch (e) {
        this.error = e.response?.data?.msg || 'Registration failed'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
