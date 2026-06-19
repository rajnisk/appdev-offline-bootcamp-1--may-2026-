<template>

    <h1> Admin Dashboard</h1>

    <form @submit.prevent="submitForm">
        <input type="text" v-model="formdata.title" placeholder="title">
        <input type="text" v-model="formdata.description" placeholder="description">
        <input type="date" v-model="formdata.due_date" placeholder="due date">
        <select v-model="formdata.assigned_to">
            <option value="">Select Employee</option>
            <option v-for="employee in employees" :value="employee.id">{{ employee.full_name }}</option>
        </select>
        <button type="submit">submit</button>
    </form>


</template>
<script>
import axios from 'axios';

export default {
    data() {
        return {
            formdata: {
                title: "",
                description: "",
                due_date: "",
                assigned_to: ""
            },
            employees: []
        }
    },
    methods: {
        async fetchUsers() {
            const response = await axios.get('http://127.0.0.1:5000/users')
            this.employees = response.data.users
        },
        async submitForm() {
            const access_token = localStorage.getItem('access_token');
            alert(access_token)
            const response = await axios.post('http://127.0.0.1:5000/task', {
                headers: { Authorization: 'Bearer ' + access_token }
            },
                this.formdata)
                alert(access_token)
            console.log(response)
            alert(response.data.msg)
        }
    },
    mounted() {
        this.fetchUsers()
    }



}

</script>