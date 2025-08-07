import '@/assets/styles.scss';

import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router.js';

const pinia = createPinia();

const app = createApp(App)
  .use(router)
  .use(PrimeVue)
  .use(ToastService)
  .use(ConfirmationService)
  .use(pinia);

app.mount('#app');
