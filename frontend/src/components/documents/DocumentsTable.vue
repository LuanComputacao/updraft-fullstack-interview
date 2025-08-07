<template>
  <div class="w-full">
    <DataTable
      v-model:filters="filters"
      :value="documents"
      :loading="isLoading"
      data-key="id"
      paginator
      :rows="10"
      :rows-per-page-options="[5, 10, 20, 50]"
      sort-field="created_at"
      :sort-order="-1"
      filter-display="menu"
      :filters="filters"
    >
      <Column field="title" header="Title" sortable style="width: 40%">
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            class="p-column-filter"
            placeholder="Search by title"
          />
        </template>
      </Column>

      <Column field="created_at" header="Created At" sortable style="width: 30%">
        <template #body="{ data }">
          {{ formatDate(data.created_at) }}
        </template>
      </Column>

      <Column header="Actions" style="width: 30%">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button
              v-tooltip.left="'Edit document'"
              icon="pi pi-pencil"
              size="small"
              severity="secondary"
              text
              @click="onEdit(data)"
            />
            <Button
              v-tooltip.left="'Delete document'"
              icon="pi pi-trash"
              size="small"
              severity="danger"
              text
              @click="onDelete(data)"
            />
          </div>
        </template>
      </Column>

      <template #empty>
        <div class="flex flex-column align-items-center justify-content-center p-4">
          <i class="pi pi-file-o text-6xl text-400 mb-3"></i>
          <span class="text-500">No documents found</span>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { FilterMatchMode } from 'primevue/api';
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import InputText from 'primevue/inputtext';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';
import { defineEmits, onMounted, ref } from 'vue';

import { useDocumentsStore } from '@/services/stores/documents';

const emit = defineEmits(['edit']);

const documentsStore = useDocumentsStore();
const { documents, isLoading } = storeToRefs(documentsStore);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  title: { value: null, matchMode: FilterMatchMode.CONTAINS },
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const onEdit = (document) => {
  emit('edit', document.id);
};

const confirm = useConfirm();
const toast = useToast();

const onDelete = (document) => {
  confirm.require({
    message: `Are you sure you want to delete "${document.title}"?`,
    header: 'Confirm Delete',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        const result = await documentsStore.softDeleteDocument(document.id);

        if (result.success) {
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Document deleted successfully',
            life: 3000,
          });
        } else {
          toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to delete document',
            life: 3000,
          });
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to delete document',
          life: 3000,
        });
      }
    },
  });
};

onMounted(() => {
  documentsStore.fetchDocuments();
});
</script>
