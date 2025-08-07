import { createRouter, createWebHistory } from 'vue-router';

import CreateDocumentPage from '@/views/AddEditDocumentPage.vue';
import HomePage from '@/views/HomePage.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/documents/create',
    name: 'create-document',
    component: CreateDocumentPage,
  },
  {
    path: '/documents/edit/:id',
    name: 'edit-document',
    component: CreateDocumentPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
