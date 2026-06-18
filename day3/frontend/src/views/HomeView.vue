<template>
  <div>
    <h1 class="h3 mb-4">My Tasks</h1>
    <p v-if="error" class="alert alert-danger py-2">{{ error }}</p>

    <p v-if="loading" class="text-muted">Loading…</p>
    <p v-else-if="!tasks.length" class="text-muted">No tasks assigned yet.</p>

    <div v-else class="list-group">
      <div v-for="task in tasks" :key="task.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-start gap-2">
          <div>
            <strong>{{ task.title }}</strong>
            <p v-if="task.description" class="mb-1 text-muted small">
              {{ task.description }}
            </p>
            <span v-if="task.deadline" class="badge text-bg-secondary">
              Due: {{ task.deadline }}
            </span>
          </div>
        </div>
        <div class="mt-2">
          <label class="form-label small mb-0">Status</label>
          <select
            v-model="task.status"
            class="form-select form-select-sm"
            style="max-width: 220px"
            @change="updateStatus(task)"
          >
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>
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
      tasks: [],
      loading: false,
      error: '',
    }
  },
  mounted() {
    this.loadTasks()
  },
  methods: {
    authHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async loadTasks() {
      this.loading = true
      this.error = ''
      try {
        const res = await axios.get(`${API}/tasks`, { headers: this.authHeaders() })
        this.tasks = res.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not load tasks'
      } finally {
        this.loading = false
      }
    },
    async updateStatus(task) {
      this.error = ''
      try {
        await axios.put(
          `${API}/tasks/${task.id}`,
          { status: task.status },
          { headers: this.authHeaders() }
        )
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not update status'
        await this.loadTasks()
      }
    },
  },
}
</script>
