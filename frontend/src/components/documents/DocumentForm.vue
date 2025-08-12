<template>
  <div class="flex flex-column gap-4 w-full">
    <Form
      novalidate
      :validation-schema="formSchema"
      :validate-on-mount="false"
      :validate-on-schema="false"
      :initial-values="form"
      class="w-full flex flex-column gap-4"
      @submit="onSubmit"
    >
      <div class="field w-full">
        <label class="block text-md mb-2 text-700 font-semibold" for="title">Title</label>
        <Field v-slot="{ field, errorMessage }" v-model="form.title" name="title">
          <InputText
            v-bind="field"
            class="w-full"
            :class="{ 'p-invalid': errorMessage }"
            placeholder="Enter document title"
          />
          <small v-if="errorMessage" class="block w-full p-error mt-2">{{ errorMessage }}</small>
        </Field>
      </div>

      <div class="field w-full">
        <label class="block text-md mb-2 text-700 font-semibold" for="content">Content</label>
        <Field v-slot="{ errorMessage }" v-model="form.content_html" name="content_html">
          <RichTextEditor
            v-model="form.content_html"
            placeholder="Enter document content..."
            class="w-full"
            :class="{ 'p-invalid': errorMessage }"
          />
          <small v-if="errorMessage" class="block w-full p-error mt-2">{{ errorMessage }}</small>
        </Field>
      </div>

      <div class="flex justify-content-end gap-2">
        <Button
          type="submit"
          :label="isEditMode ? 'Update' : 'Create'"
          icon="pi pi-check"
          severity="primary"
          :disabled="isSubmitting || isLoading"
          :loading="isSubmitting || isLoading"
        />
      </div>
    </Form>
  </div>
</template>

<script setup>
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { useToast } from 'primevue/usetoast';
import { Field, Form } from 'vee-validate';
import { defineEmits, defineProps, onMounted, ref, watch } from 'vue';
import { object, string } from 'yup';

import { useDocumentsStore } from '@/stores/documents';

import RichTextEditor from '../rte/RichTextEditor.vue';

const props = defineProps({
  documentId: {
    type: String,
    default: null,
  },
  isEditMode: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['saved', 'created']);

const documentsStore = useDocumentsStore();
const toast = useToast();
const isSubmitting = ref(false);

const formSchema = object({
  title: string().required('Title is required').max(255, 'Title must have at most 255 characters'),
  content_html: string()
    .required('Content is required')
    .max(50000, 'Content must have at most 50,000 characters')
    .test('not-empty', 'Content cannot be empty', (value) => {
      return value && value.trim().length > 0 && value !== '<p></p>';
    }),
});

const form = ref({
  title: '',
  content_html: '',
});

const isLoading = ref(false);

// Load document data if in edit mode
const loadDocument = async () => {
  if (props.isEditMode && props.documentId) {
    isLoading.value = true;
    try {
      const document = await documentsStore.fetchById(props.documentId);
      if (document) {
        form.value = {
          title: document.title,
          content_html: document.content_html,
        };
      }
    } catch (error) {
      console.error('Error loading document:', error);
    } finally {
      isLoading.value = false;
    }
  }
};

// Watch for documentId changes
watch(() => props.documentId, loadDocument);

// Load document on mount if in edit mode
onMounted(() => {
  if (props.isEditMode) {
    loadDocument();
  }
});

const onSubmit = async () => {
  isSubmitting.value = true;

  try {
    if (props.isEditMode) {
      const result = await documentsStore.update(
        props.documentId,
        form.value.title,
        form.value.content_html
      );

      if (result.success) {
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Document updated successfully',
          life: 3000,
        });
        emit('saved');
      } else {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to update document',
          life: 3000,
        });
      }
    } else {
      const result = await documentsStore.create(form.value.title, form.value.content_html);

      if (result.success) {
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Document created successfully',
          life: 3000,
        });
        emit('created', result.data);
      } else {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to create document',
          life: 3000,
        });
      }
    }
  } catch (error) {
    console.error('Error saving document:', error);

    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: props.isEditMode ? 'Failed to update document' : 'Failed to create document',
      life: 3000,
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>
