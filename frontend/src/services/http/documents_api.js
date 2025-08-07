import { apiClient } from './http_client';

export const getDocumentCollection = async () => {
  return await apiClient.get('/documents/');
};

export const createDocument = async (payload) => {
  return await apiClient.post('/documents/', payload);
};

export const updateDocument = async (id, payload) => {
  return await apiClient.put(`/documents/${id}`, payload);
};

export const softDeleteDocument = async (id) => {
  return await apiClient.delete(`/documents/${id}`);
};
