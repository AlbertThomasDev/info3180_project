import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserLoginView from '../views/UserLoginView.vue'
import UserRegisterView from '../views/UserRegisterView.vue'
import UserView from '../views/UserView.vue'

import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import NewProfileView from '../views/NewProfileView.vue'
import ShowAllProfiles from '../views/ShowAllProfiles.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path:'/login', name: 'login', component: UserLoginView },
    { path:'/register', name: 'register', component: UserRegisterView },
    { path: '/users/:userId', name: 'userview', component: UserView },
    { path: '/profiles/new', name: 'newprofile', component: NewProfileView },
    { path: '/profiles/:profile_id', name: 'profileview', component: ProfileDetailsView },
    { path: '/profiles', name: 'profiles', component: ShowAllProfiles }
    
    
    // { path: '/reports', name: 'reports', component: AppReports }

  ]
})

export default router