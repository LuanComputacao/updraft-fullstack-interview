import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import * as api from '../http/documents_api';

export const useDocumentsStore = defineStore('documents', () => {
  // State
  const documents = ref([]);
  const isLoading = ref(false);

  // Getters
  const getDocuments = computed(() => documents.value);
  const getDocumentById = computed(() => (id) => documents.value.find((doc) => doc.id === id));
  const getDocumentsCount = computed(() => documents.value.length);

  // Actions
  const fetchDocuments = async () => {
    isLoading.value = true;

    try {
      const response = await api.getDocumentCollection();
      documents.value = response.data.items || [];
    } catch (err) {
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchSingleDocument = async (id) => {
    isLoading.value = true;

    try {
      let document = documents.value.find((doc) => doc.id === id);
      if (document) {
        return document;
      }

      // If not found locally, fetch all documents and try again
      await fetchDocuments();
      document = documents.value.find((doc) => doc.id === id);
      if (!document) {
        throw new Error('Document not found');
      }

      return document;
    } catch (err) {
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const addDocument = async (title, contentHtml) => {
    isLoading.value = true;

    try {
      const payload = {
        title,
        content_html: contentHtml,
      };
      const response = await api.createDocument(payload);
      const newDocument = response.data;

      // Add to local state
      documents.value.push(newDocument);

      return { success: true, data: newDocument };
    } catch (err) {
      console.error(err);
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const updateDocument = async (id, title, contentHtml) => {
    isLoading.value = true;

    try {
      const payload = {
        title,
        content_html: contentHtml,
      };
      const response = await api.updateDocument(id, payload);
      const updatedDocument = response.data;

      // Update local state
      const index = documents.value.findIndex((doc) => doc.id === id);
      if (index !== -1) {
        documents.value[index] = { ...documents.value[index], ...updatedDocument };
      }

      return { success: true, data: updatedDocument };
    } catch (err) {
      console.error(err);
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const softDeleteDocument = async (id) => {
    isLoading.value = true;

    try {
      await api.softDeleteDocument(id);
      documents.value = documents.value.filter((doc) => doc.id !== id);
      return { success: true };
    } catch (err) {
      console.error(err);
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const clearDocuments = () => {
    documents.value = [];
  };

  return {
    // State
    documents,
    isLoading,

    // Getters
    getDocuments,
    getDocumentById,
    getDocumentsCount,

    // Actions
    fetchDocuments,
    fetchSingleDocument,
    addDocument,
    updateDocument,
    softDeleteDocument,
    clearDocuments,
  };
});
