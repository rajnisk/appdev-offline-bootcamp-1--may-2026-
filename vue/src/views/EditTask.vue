<template>
  <div>
    <NavBar @logout="logout" />

    <main>
      <h1>Edit Task</h1>

      <div v-if="loading">Loading...</div>

      <form v-else @submit.prevent="saveTask">
        <input v-model="form.title" placeholder="title" />
        <input v-model="form.description" placeholder="description" />
        <input type="date" v-model="form.due_date" />

        <select v-model="form.assigned_to">
          <option value="">Unassigned</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.full_name }}</option>
        </select>

        <select v-model="form.status">
          <option value="pending">pending</option>
          <option value="in-progress">in-progress</option>
          <option value="done">done</option>
        </select>

        <button type="submit">Save</button>
        <button type="button" @click="cancel">Cancel</button>
      </form>
    </main>

    <FooterBar />
  </div>
</template>

<script>
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'

export default {
  components: { NavBar, FooterBar },
  data() {
    return {
      loading: true,
      employees: [],
      form: {
        title: '',
        description: '',
        due_date: '',
        assigned_to: '',
        status: 'pending'
      }
    }
  },
  methods: {
    async fetchUsers() {
      const response = await axios.get('http://127.0.0.1:5000/users')
      this.employees = response.data.users || []
    },
    async fetchTask() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        this.$router.push('/login')
        return
      }
      try {
        const taskId = this.$route.params.id
        const res = await axios.get(`http://127.0.0.1:5000/task/${taskId}`, {
          headers: { Authorization: 'Bearer ' + token }
        })
        const task = res.data.task
        this.form = {
          title: task.title || '',
          description: task.description || '',
          due_date: task.due_date ? task.due_date.slice(0, 10) : '',
          assigned_to: task.assigned_to || '',
          status: task.status || 'pending'
        }
      } catch (err) {
        if (err.response && err.response.status === 401) {
          localStorage.removeItem('access_token')
          this.$router.push('/login')
          return
        }
        alert(err.response?.data?.msg || 'Failed to load task')
      } finally {
        this.loading = false
      }
    },
    async saveTask() {
      const token = localStorage.getItem('access_token')
      try {
        await axios.put(`http://127.0.0.1:5000/task/${this.$route.params.id}`, this.form, {
          headers: { Authorization: 'Bearer ' + token }
        })
        this.$router.push('/admin')
      } catch (err) {
        if (err.response && err.response.status === 401) {
          localStorage.removeItem('access_token')
          this.$router.push('/login')
          return
        }
        alert(err.response?.data?.msg || 'Failed to save task')
      }
    },
    cancel() {
      this.$router.push('/admin')
    },
    logout() {
      localStorage.removeItem('access_token')
      this.$router.push('/login')
    }
  },
  mounted() {
    this.fetchUsers()
    this.fetchTask()
  }
}
</script>