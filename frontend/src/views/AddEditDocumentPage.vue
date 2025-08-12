<template>
  <div class="h-full w-full flex flex-column gap-2 justify-content-center align-items-center">
    <div class="flex w-full justify-content-start align-items-center gap-2">
      <Button
        v-tooltip.left="'Back to documents'"
        icon="pi pi-arrow-left"
        size="small"
        severity="secondary"
        text
        @click="onCancel"
      />
      <h1>{{ isEditMode ? 'Edit Document' : 'Create Document' }}</h1>
    </div>
    <div class="flex w-full gap-3 flex-column lg:flex-row">
      <div class="bg-white p-3 shadow-2 border-round col-12 lg:col-7">
        <DocumentForm
          :document-id="documentId"
          :is-edit-mode="isEditMode"
          @created="onDocumentCreated"
        />
      </div>
      <div v-if="isEditMode" class="bg-white p-3 shadow-2 border-round col-12 lg:col-5">
        <SummaryPanel :document-id="documentId" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button';
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import DocumentForm from '@/components/documents/DocumentForm.vue';
import SummaryPanel from '@/components/documents/SummaryPanel.vue';

const route = useRoute();
const router = useRouter();

const documentId = computed(() => route.params.id);
const isEditMode = computed(() => !!documentId.value);

const onCancel = () => {
  router.push('/');
};

const onDocumentCreated = (document) => {
  // Route to edit page for the newly created document
  router.push(`/documents/edit/${document.id}`);
};
</script>
