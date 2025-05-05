import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserLoginView from '../views/UserLoginView.vue'
import UserRegisterView from '../views/UserRegisterView.vue'
import UserView from '../views/UserView.vue'

import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import NewProfileView from '../views/NewProfileView.vue'
import ShowAllProfiles from '../views/ShowAllProfiles.vue'
import MatchMeView from '../views/MatchMeView.vue'
import Top20Fav from '../views/Top20Fav.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path:'/login', name: 'login', component: UserLoginView },
    { path:'/register', name: 'register', component: UserRegisterView },
    { path: '/users/:userId', name: 'userview', component: UserView },
    { path: '/profiles/new', name: 'newprofile', component: NewProfileView },
    { path: '/profiles/:profile_id', name: 'profileview', component: ProfileDetailsView },
    { path: '/profiles', name: 'profiles', component: ShowAllProfiles },
    { path: '/matchme', name: 'matchme', component: MatchMeView},
    { path: '/top20fav', name: 'top20fav', component: Top20Fav }

  ]
})

export default router