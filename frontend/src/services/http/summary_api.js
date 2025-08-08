import { getHeaders } from './http_client';

const baseApi = () => `http://${location.host}/api`;

export async function streamSummary(documentId, options = {}, onEvent, signal) {
  const url = `${baseApi()}/documents/${documentId}/summary/stream`;
  const headers = { ...getHeaders('application/json'), Accept: 'text/event-stream' };

  const res = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(options || {}),
    signal,
  });
  if (!res.ok) throw new Error(`Failed to start stream: ${res.status}`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  let done = false;

  const emit = (event, data) => {
    try {
      if (onEvent) onEvent({ event, data });
    } catch (e) {
      // swallow listener errors to avoid breaking the stream
      console.warn('streamSummary listener error', e);
    }
  };

  while (!done) {
    const read = await reader.read();
    done = read.done;
    if (done) break;

    buffer += decoder.decode(read.value, { stream: true });

    let sepIdx;
    // SSE messages are separated by two newlines
    while ((sepIdx = buffer.indexOf('\n\n')) !== -1) {
      const raw = buffer.slice(0, sepIdx).trim();
      buffer = buffer.slice(sepIdx + 2);
      if (!raw) continue;

      const lines = raw.split('\n');
      let event = 'message';
      let data = '';
      for (const line of lines) {
        if (line.startsWith('event:')) event = line.replace('event:', '').trim();
        if (line.startsWith('data:')) data += line.replace('data:', '').trim();
      }
      try {
        data = data ? JSON.parse(data) : {};
      } catch (e) {
        // keep as string when not JSON
      }
      emit(event, data);
    }
  }
  emit('done', {});
}

export async function getSummary(documentId) {
  const url = `${baseApi()}/documents/${documentId}/summary`;
  const res = await fetch(url, { headers: getHeaders('application/json') });
  if (!res.ok) throw new Error(`Failed to get summary: ${res.status}`);
  return await res.json();
}

export async function saveSummary(documentId, content_html) {
  const url = `${baseApi()}/documents/${documentId}/summary`;
  const res = await fetch(url, {
    method: 'POST',
    headers: getHeaders('application/json'),
    body: JSON.stringify({ content_html }),
  });
  if (!res.ok) throw new Error(`Failed to save summary: ${res.status}`);
}

export async function updateSummary(documentId, content_html) {
  const url = `${baseApi()}/documents/${documentId}/summary`;
  const res = await fetch(url, {
    method: 'PUT',
    headers: getHeaders('application/json'),
    body: JSON.stringify({ content_html }),
  });
  if (!res.ok) throw new Error(`Failed to update summary: ${res.status}`);
}

export async function deleteSummary(documentId) {
  const url = `${baseApi()}/documents/${documentId}/summary`;
  const res = await fetch(url, { method: 'DELETE', headers: getHeaders('application/json') });
  if (!res.ok) throw new Error(`Failed to delete summary: ${res.status}`);
}
