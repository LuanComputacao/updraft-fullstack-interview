import axios from 'axios';

export const getHeaders = (contentType = 'application/json') => {
  const header = {
    'Content-Type': contentType,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'X-Requested-With',
    'X-Updraft-Tenant': location.host,
  };
  return header;
};

const getHostName = () => `http://${location.host}/api`;

export const apiClient = axios.create({
  baseURL: getHostName(),
  headers: getHeaders(),
});
