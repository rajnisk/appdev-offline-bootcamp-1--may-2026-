<template>
    <div class="admin-dashboard">
        <NavBar @logout="logout" />

        <main class="dashboard-content">
            <h1>Admin Dashboard</h1>

            <section class="create">
                <h2>Create Task</h2>
                <form @submit.prevent="submitForm">
                    <input type="text" v-model="formdata.title" placeholder="title">
                    <input type="text" v-model="formdata.description" placeholder="description">
                    <input type="date" v-model="formdata.due_date" placeholder="due date">
                    <select v-model="formdata.assigned_to">
                        <option value="">Select Employee</option>
                        <option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.full_name }}</option>
                    </select>
                    <button type="submit">Create</button>
                </form>
            </section>

            <section class="list">
                <h2>All Tasks</h2>
                <div v-if="tasks.length === 0">No tasks yet</div>
                <ul>
                    <li v-for="task in tasks" :key="task.id">
                        <strong>{{ task.title }}</strong> — {{ task.status }}
                        <div>Assigned to: {{ findEmployeeName(task.assigned_to) || '—' }}</div>
                        <div>Due: {{ task.due_date ? task.due_date.slice(0,10) : '—' }}</div>
                        <button @click="editTask(task.id)">Edit</button>
                        <button @click="deleteTask(task.id)">Delete</button>
                    </li>
                </ul>
            </section>
        </main>

        <FooterBar />
    </div>
</template>
<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'

export default {
    components: {
        NavBar,
        FooterBar
    },
    data() {
        return {
            formdata: {
                title: "",
                description: "",
                due_date: "",
                assigned_to: ""
            },
            employees: []
            ,
            tasks: []
        }
    },
    methods: {
        async fetchUsers() {
            const response = await axios.get('http://127.0.0.1:5000/users')
            this.employees = response.data.users
        },
        async fetchTasks() {
            const token = localStorage.getItem('access_token')
            if (!token) {
                // no token -> go to login
                this.$router.push('/login')
                return
            }
            try {
                const res = await axios.get('http://127.0.0.1:5000/task', { headers: { Authorization: 'Bearer ' + token } })
                this.tasks = res.data.tasks || []
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    localStorage.removeItem('access_token')
                    alert('Session expired or unauthorized — please login')
                    this.$router.push('/login')
                    return
                }
                console.error(err)
            }
        },
        async submitForm() {
            const access_token = localStorage.getItem('access_token');
            if (!access_token) return this.$router.push('/login')
            try {
                const response = await axios.post(
                    'http://127.0.0.1:5000/task',
                    this.formdata,
                    {
                        headers: { Authorization: 'Bearer ' + access_token }
                    }
                )
                console.log(response)
                alert(response.data.msg)
                this.formdata = { title: "", description: "", due_date: "", assigned_to: "" }
                this.fetchTasks()
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    localStorage.removeItem('access_token')
                    alert('Session expired or unauthorized — please login')
                    this.$router.push('/login')
                    return
                }
                alert(err.response?.data?.msg || 'Failed to create task')
            }
        },
        findEmployeeName(id) {
            const e = this.employees.find(x => x.id === id)
            return e ? e.full_name : null
        },
        editTask(taskId) {
            this.$router.push(`/task/${taskId}/edit`)
        },
        async deleteTask(id) {
            if (!confirm('Delete this task?')) return
            const token = localStorage.getItem('access_token')
            try {
                await axios.delete(`http://127.0.0.1:5000/task/${id}`, { headers: { Authorization: 'Bearer ' + token } })
                this.fetchTasks()
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    localStorage.removeItem('access_token')
                    alert('Session expired or unauthorized — please login')
                    this.$router.push('/login')
                    return
                }
                alert(err.response?.data?.msg || 'Failed to delete')
            }
        },
        logout() {
            localStorage.removeItem('access_token')
            this.$router.push('/login')
        }
    },
    mounted() {
        this.fetchUsers()
        this.fetchTasks()
    }
}

</script>
