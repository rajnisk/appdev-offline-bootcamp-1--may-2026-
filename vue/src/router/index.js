import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Todo from '../views/Todo.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/todo', component: Todo },
  ],
})

export default router
