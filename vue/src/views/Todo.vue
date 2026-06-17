<template>
    <h1>Todo</h1>
    <form @submit.prevent="addTodo">
        <input v-model="newtext" type="text" name="text" id="todo" placeholder="add new todo">
        <button type="submit">submit</button>
    </form>

  <table>
        <thead>
            <tr>
                <td>todo</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in todoList">
                <td>{{ item.text }}</td>
            </tr>
        </tbody>

    </table>
</template>
<script>
export default{
    data(){
        return{
            todoList:[],
              newtext:''
        }
    },
    
    methods:{
        addTodo(){
            this.todoList.push({
                text: this.newtext
            })

        }
    },
    
}
</script>
