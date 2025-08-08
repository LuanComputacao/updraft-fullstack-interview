import { apiClient } from './http_client';

export const getDocumentCollection = async ({ signal } = {}) => {
  return await apiClient.get('/documents/', { signal });
};

export const createDocument = async (payload, { signal } = {}) => {
  return await apiClient.post('/documents/', payload, { signal });
};

export const updateDocument = async (id, payload, { signal } = {}) => {
  return await apiClient.put(`/documents/${id}`, payload, { signal });
};

export const softDeleteDocument = async (id, { signal } = {}) => {
  return await apiClient.delete(`/documents/${id}`, { signal });
};
