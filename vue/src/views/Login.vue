<template>
    <h1>Login</h1>
    <form @submit.prevent="login">
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
                email: "",
                password: "",
                access_token: ""
            }
        }
    },

    methods: {

        async login() {
            const response = await axios.post('http://127.0.0.1:5000/login', this.formdata)
            console.log(response)
            alert(response.data.msg)
            this.access_token = response.data.access_token
            localStorage.setItem('access_token', this.access_token)
            if(response.data.role === 'admin'){
                this.$router.push('/admin')
            }
            //  else {
            //     this.$router.push('/user')
            // }
        }

    }

}
</script>