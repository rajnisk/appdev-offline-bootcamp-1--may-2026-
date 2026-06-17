<template>
    <h1>Home page {{ msg }} </h1>
    <button @click="popAlert()">click me</button>
<br>
    <input v-model="name" type="text" name="name" id="name" placeholder="name">

    <p>{{ numA }}</p>
    <p v-if="numA==4" >
        given number is 4
    </p>
    <p v-else>
        given number is not 4
    </p>
    <p v-show="numA==3">
        given number is 3
    </p>

    <table>
        <thead>
            <tr>
                <td>id</td>
                <td>name</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in data">
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
            </tr>
        </tbody>

    </table>


</template>

<script>

export default{
data(){
    return{
        msg:'hello world!',
        name:'--',
        data:[
            {id:1, name:'john'},
            {id:2, name:'doe'},
            {id:3, name:'smith'},
        ]
    
    }
},

methods:{
    popAlert(){
    alert(this.name)
    },
},
computed:{
    numA(){
    return 5;
    },
},

created(){
alert('created')
},
mounted(){
    alert('mounted')
}

}
</script>