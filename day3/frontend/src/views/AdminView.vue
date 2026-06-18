<template>
  <div>
    <h1 class="h3 mb-4">Manage Tasks</h1>
    <p v-if="error" class="alert alert-danger py-2">{{ error }}</p>
    <p v-if="message" class="alert alert-success py-2">{{ message }}</p>

    <div v-if="stats" class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <div class="h3 mb-0">{{ stats.total_tasks }}</div>
            <div class="text-muted small">Total tasks</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <div class="h3 mb-0">{{ stats.employees }}</div>
            <div class="text-muted small">Employees</div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body small">
            <span v-for="(count, status) in stats.tasks_by_status" :key="status" class="me-3">
              {{ status }}: {{ count }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <h2 class="h5">Assign new task</h2>
        <form class="row g-2" @submit.prevent="assignTask">
          <div class="col-md-3">
            <input
              v-model="newTask.title"
              type="text"
              class="form-control"
              placeholder="Title"
              required
            />
          </div>
          <div class="col-md-3">
            <input
              v-model="newTask.description"
              type="text"
              class="form-control"
              placeholder="Description"
            />
          </div>
          <div class="col-md-2">
            <select v-model="newTask.user_id" class="form-select" required>
              <option disabled value="">Employee</option>
              <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                {{ emp.username }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <input v-model="newTask.deadline" type="date" class="form-control" required />
          </div>
          <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Assign</button>
          </div>
        </form>
      </div>
    </div>

    <p v-if="loading" class="text-muted">Loading tasks…</p>
    <p v-else-if="!tasks.length" class="text-muted">No tasks yet.</p>

    <div v-else class="table-responsive">
      <table class="table table-bordered bg-white">
        <thead>
          <tr>
            <th>Title</th>
            <th>Assignee</th>
            <th>Deadline</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>
              <input v-model="task.title" class="form-control form-control-sm" />
              <input
                v-model="task.description"
                class="form-control form-control-sm mt-1"
                placeholder="Description"
              />
            </td>
            <td>
              <select v-model="task.user_id" class="form-select form-select-sm">
                <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                  {{ emp.username }}
                </option>
              </select>
            </td>
            <td>
              <input v-model="task.deadline" type="date" class="form-control form-control-sm" />
            </td>
            <td>
              <select v-model="task.status" class="form-select form-select-sm">
                <option>Pending</option>
                <option>In Progress</option>
                <option>Completed</option>
              </select>
            </td>
            <td class="text-nowrap">
              <button class="btn btn-sm btn-outline-primary me-1" @click="saveTask(task)">
                Save
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTask(task.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
      employees: [],
      stats: null,
      loading: false,
      error: '',
      message: '',
      newTask: {
        title: '',
        description: '',
        user_id: '',
        deadline: '',
      },
    }
  },
  mounted() {
    this.loadAll()
  },
  methods: {
    authHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },
    async loadAll() {
      this.loading = true
      this.error = ''
      try {
        const [tasksRes, empRes, statsRes] = await Promise.all([
          axios.get(`${API}/tasks`, { headers: this.authHeaders() }),
          axios.get(`${API}/admin/employees`, { headers: this.authHeaders() }),
          axios.get(`${API}/admin/stats`, { headers: this.authHeaders() }),
        ])
        this.tasks = tasksRes.data
        this.employees = empRes.data
        this.stats = statsRes.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not load data'
      } finally {
        this.loading = false
      }
    },
    async assignTask() {
      this.error = ''
      this.message = ''
      try {
        await axios.post(`${API}/tasks`, this.newTask, { headers: this.authHeaders() })
        this.newTask = { title: '', description: '', user_id: '', deadline: '' }
        this.message = 'Task assigned'
        await this.loadAll()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not assign task'
      }
    },
    async saveTask(task) {
      this.error = ''
      this.message = ''
      try {
        await axios.put(`${API}/tasks/${task.id}`, task, { headers: this.authHeaders() })
        this.message = 'Task saved'
        await this.loadAll()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not save task'
      }
    },
    async deleteTask(id) {
      if (!confirm('Delete this task?')) return
      this.error = ''
      try {
        await axios.delete(`${API}/tasks/${id}`, { headers: this.authHeaders() })
        await this.loadAll()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not delete task'
      }
    },
  },
}
</script>
