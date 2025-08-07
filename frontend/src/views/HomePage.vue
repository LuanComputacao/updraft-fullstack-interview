<template>
  <div class="h-full w-full flex flex-column gap-2 justify-content-center align-items-center">
    <div class="flex w-full justify-content-start">
      <h1>Dashboard</h1>
    </div>
    <div class="flex w-full bg-white p-3 shadow-2 border-round flex-column gap-3">
      <DocumentSectionHeader @create="onCreate" />
      <DocumentsTable @edit="onEdit" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

import DocumentSectionHeader from '@/components/documents/DocumentSectionHeader.vue';
import DocumentsTable from '@/components/documents/DocumentsTable.vue';

const router = useRouter();

const onCreate = () => {
  router.push('/documents/create');
};

const onEdit = (documentId) => {
  router.push(`/documents/edit/${documentId}`);
};
</script>
