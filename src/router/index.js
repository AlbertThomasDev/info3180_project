import { createRouter, createWebHistory } from 'vue-router'
// import AppHome from '../components/AppHome.vue'
import UserLoginView from '../views/UserLoginView.vue'
import UserRegisterView from '../views/UserRegisterView.vue'
import UserView from '../views/UserView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // { path: '/', name: 'home', component: AppHome },
    { path:'/login', name: 'login', component: UserLoginView},
    { path:'/register', name: 'register', component: UserRegisterView},
    { path: '/user', name: 'user', component: UserView }
    
    
    // { path: '/reports', name: 'reports', component: AppReports }

  ]
})

export default router