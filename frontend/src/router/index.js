import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
// Librarian home view (default for users with role "bibliothecaire")
const LibrarianHome = () => import('@/views/LibrarianHomeView.vue');

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/catalog', name: 'Catalog', component: () => import('@/views/CatalogView.vue') },
  { path: '/search', name: 'Search', component: () => import('@/views/SearchView.vue') },
  { path: '/librarian', name: 'LibrarianHome', component: LibrarianHome, meta: { requiresAuth: true } },
  { path: '/works/:id', name: 'Work', component: () => import('@/views/WorkView.vue'), meta: { requiresAuth: true } },
  {
    path: '/moderation/:id',
    name: 'Moderation',
    component: () => import('@/views/ModerationView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue') },
  {
    path: '/submit',
    name: 'SubmitFile',
    component: () => import('@/views/SubmitFileView.vue'),
    meta: { requiresAuth: true }
  },
    { path: '/transcribing', name: 'Transcribing', component: () => import('@/views/TranscribingView.vue'), meta: { requiresAuth: true } },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuth = !!localStorage.getItem('token');
  const role = localStorage.getItem('role');
  if (to.meta && to.meta.requiresAuth && !isAuth) {
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  }
  // If visiting the public home and user is a librarian, redirect to librarian home
  if ((to.name === 'Home' || to.path === '/') && isAuth && role === 'bibliothecaire') {
    return next({ name: 'LibrarianHome' });
  }
  next();
});

export default router;