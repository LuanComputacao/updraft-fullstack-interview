<template>
  <Toast position="top-center" />
  <ConfirmDialog :pt="{ root: { class: 'max-w-30rem' } }" />
  <section class="h-full w-full p-2 flex justify-content-center">
    <div class="w-full max-w-custom">
      <RouterView />
    </div>
  </section>
</template>

<script>
import ConfirmDialog from 'primevue/confirmdialog';
import Toast from 'primevue/toast';
export default {
  name: 'App',
  components: { Toast, ConfirmDialog },
};
</script>

<style>
.max-w-custom {
  max-width: 1200px;
}
</style>
