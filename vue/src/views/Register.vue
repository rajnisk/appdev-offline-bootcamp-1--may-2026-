<template>
    <h1>Register</h1>

    <form @submit.prevent="register">

        <input type="text" v-model="formdata.full_name" placeholder="full name">
        <input type="text" v-model="formdata.email" placeholder="email">
        <input type="text" v-model="formdata.password" placeholder="password">
        <button type="submit">submit</button>
    </form>

</template>


<script>
import axios from 'axios';

export default {
    data() {
        return {
            formdata: {
                full_name: "",
                email: "",
                password: ""
            }
        }
    },

    methods: {

        async register() {
            const response = await axios.post('http://127.0.0.1:5000/register', this.formdata)
            console.log(response)
            alert(response.data)
        }

    }

}
</script>