import { createRouter, createWebHistory } from 'vue-router'
import Index from '../pages/Index.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import FavoriteDetail from '../pages/FavoriteDetail.vue'
import DatabaseDetail from '../pages/DatabaseDetail.vue'

const routes = [
  {
    path: '/',
    component: Index,
    meta: { title: 'Profiles' }
  },
  {
    path: '/profile/:id',
    component: ProfilePage,
    meta: { title: 'Profile Editor' }
  },
  {
    path: '/favorite/:id',
    component: FavoriteDetail,
    meta: { title: 'Favorite Detail' }
  },
  {
    path: '/database/:id',
    component: DatabaseDetail,
    meta: { title: 'Agency Detail' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = 'Uniden Assistant - ' + (to.meta.title || 'Scanner')
  next()
})

export default router
