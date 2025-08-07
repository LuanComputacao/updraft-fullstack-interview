<template>
  <div class="flex justify-content-between align-items-center">
    <h2 class="text-2xl font-bold m-0">Documents</h2>
    <Button label="Create Document" icon="pi pi-plus" severity="primary" @click="onCreate" />
  </div>
</template>

<script setup>
import Button from 'primevue/button';
import { defineEmits } from 'vue';

const emit = defineEmits(['create']);

const onCreate = () => {
  emit('create');
};
</script>
