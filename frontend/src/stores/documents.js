import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

import * as api from '@/services/http/documents_api';

export const useDocumentsStore = defineStore('documents', () => {
  // State (normalized)
  const byId = ref({});
  const allIds = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const lastFetchedAt = ref(0);

  // Internal: de-dupe concurrent fetches
  let pendingFetch = null;

  // Getters
  const documentsList = computed(() => allIds.value.map((id) => byId.value[id]).filter(Boolean));
  const documentMap = computed(() => byId.value);
  const documentById = (id) => computed(() => byId.value[id] || null);
  const count = computed(() => allIds.value.length);

  // Helpers
  const upsertMany = (items = []) => {
    const ids = [];
    const map = { ...byId.value };
    for (const it of items) {
      if (!it || !it.id) continue;
      map[it.id] = it;
      ids.push(it.id);
    }
    byId.value = map;
    // maintain stable order: newest first by created_at if present
    const mergedIds = Array.from(new Set([...ids, ...allIds.value]));
    allIds.value = mergedIds;
  };

  const removeOne = (id) => {
    const map = { ...byId.value };
    delete map[id];
    byId.value = map;
    allIds.value = allIds.value.filter((x) => x !== id);
  };

  // Actions
  const fetchCollection = async ({ force = false, signal } = {}) => {
    if (pendingFetch) return pendingFetch;
    if (!force && lastFetchedAt.value && Date.now() - lastFetchedAt.value < 15_000) {
      return; // cached
    }
    isLoading.value = true;
    error.value = null;
    pendingFetch = api
      .getDocumentCollection({ signal })
      .then((res) => {
        const items = res?.data?.items || [];
        upsertMany(items);
        lastFetchedAt.value = Date.now();
      })
      .catch((err) => {
        error.value = err;
      })
      .finally(() => {
        isLoading.value = false;
        pendingFetch = null;
      });
    return pendingFetch;
  };

  const fetchById = async (id, { signal } = {}) => {
    // prefer cache
    if (byId.value[id]) return byId.value[id];
    await fetchCollection({ force: true, signal });
    return byId.value[id] || null;
  };

  const create = async (title, content_html) => {
    isLoading.value = true;
    error.value = null;
    try {
      const res = await api.createDocument({ title, content_html });
      const doc = res?.data;
      if (doc?.id) {
        upsertMany([doc]);
      }
      return { success: true, data: doc };
    } catch (err) {
      error.value = err;
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const update = async (id, title, content_html) => {
    isLoading.value = true;
    error.value = null;
    try {
      const res = await api.updateDocument(id, { title, content_html });
      const doc = res?.data;
      if (doc?.id) {
        upsertMany([doc]);
      }
      return { success: true, data: doc };
    } catch (err) {
      error.value = err;
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const softDelete = async (id) => {
    isLoading.value = true;
    error.value = null;
    try {
      await api.softDeleteDocument(id);
      removeOne(id);
      return { success: true };
    } catch (err) {
      error.value = err;
      return { success: false, error: err };
    } finally {
      isLoading.value = false;
    }
  };

  const clear = () => {
    byId.value = {};
    allIds.value = [];
    error.value = null;
    lastFetchedAt.value = 0;
  };

  const $reset = clear;

  return {
    // state
    byId,
    allIds,
    isLoading,
    error,
    lastFetchedAt,

    // getters
    documentsList,
    documentMap,
    documentById,
    count,

    // actions
    fetchCollection,
    fetchById,
    create,
    update,
    softDelete,
    clear,
    $reset,
  };
});
