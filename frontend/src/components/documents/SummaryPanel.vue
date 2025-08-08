<template>
  <aside class="summary-panel">
    <div class="header">
      <h3 class="m-0">AI Summary</h3>
      <div class="actions">
        <Button label="Generate" size="small" :disabled="isGenerating" @click="onGenerate" />
        <Button label="Save" size="small" severity="success" :disabled="!canSave" @click="onSave" />
        <Button
          label="Delete"
          size="small"
          severity="danger"
          :disabled="!hasSummary"
          @click="onDelete"
        />
      </div>
    </div>

    <div v-if="state === 'idle'" class="state idle">
      <p>Generate an AI summary for this document. You can edit before saving.</p>
    </div>

    <div v-if="state === 'generating'" class="state generating" aria-live="polite">
      <p class="text-500 flex align-items-center gap-2">
        <i class="pi pi-spin pi-spinner" />
        Generating summary…
      </p>
      <Button
        v-if="isGenerating"
        label="Cancel"
        size="small"
        severity="secondary"
        @click="onCancel"
      />
    </div>

    <div class="editor">
      <p v-if="state === 'error'" class="text-red-500 text-center">
        {{ errorMessage || 'Summary generation failed. Please try again.' }}
      </p>
      <p v-else-if="state === 'ready'" class="text-500 text-center">
        {{ hasSummary ? 'Edit your summary below:' : 'No summary generated yet.' }}
      </p>
      <RichTextEditor v-model="summaryHtml" placeholder="The summary will appear here..." />
    </div>
  </aside>
</template>

<script setup>
import Button from 'primevue/button';
import { computed, defineProps, onMounted, ref } from 'vue';

import RichTextEditor from '@/components/rte/RichTextEditor.vue';
import {
  deleteSummary,
  getSummary,
  saveSummary,
  streamSummary,
  updateSummary,
} from '@/services/http/summary_api';

const props = defineProps({
  documentId: { type: String, required: true },
});

const state = ref('idle'); // idle | generating | ready | error
const summaryHtml = ref('');
const errorMessage = ref('');
const isGenerating = computed(() => state.value === 'generating');
const hasSummary = computed(() => !!summaryHtml.value && summaryHtml.value.trim().length > 0);
const canSave = computed(() => state.value !== 'generating' && hasSummary.value);
let controller;
const MAX_RETRIES = 1; // simple reconnection attempts

const loadSummary = async () => {
  const res = await getSummary(props.documentId).catch(() => null);
  if (res && res.summary_html) {
    summaryHtml.value = res.summary_html;
    state.value = 'ready';
  }
};

onMounted(loadSummary);

const onGenerate = async () => {
  controller = new AbortController();
  summaryHtml.value = '';
  errorMessage.value = '';
  state.value = 'generating';

  const start = async (attempt = 0) => {
    try {
      await streamSummary(
        props.documentId,
        {},
        ({ event, data }) => {
          if (event === 'chunk' && data && data.text) {
            summaryHtml.value += data.text;
          }
          if (event === 'error') {
            errorMessage.value = (data && data.message) || 'Summary generation failed.';
            state.value = 'error';
          }
          if (event === 'done') {
            state.value = 'ready';
          }
        },
        controller.signal
      );
    } catch (e) {
      if (controller?.signal?.aborted) {
        return; // user canceled
      }
      if (attempt < MAX_RETRIES) {
        // basic backoff then retry from scratch
        await new Promise((r) => setTimeout(r, 500 * (attempt + 1)));
        summaryHtml.value = '';
        await start(attempt + 1);
      } else {
        console.error('Summary generation failed', e);
        state.value = 'error';
        if (!errorMessage.value) errorMessage.value = 'Unexpected error. Please try again.';
      }
    }
  };

  await start(0);
};

const onCancel = () => {
  if (controller) controller.abort();
  state.value = 'idle';
};

const onSave = async () => {
  if (!hasSummary.value) return;
  const current = await getSummary(props.documentId).catch(() => null);
  if (current && current.summary_html) {
    await updateSummary(props.documentId, summaryHtml.value);
  } else {
    await saveSummary(props.documentId, summaryHtml.value);
  }
};

const onDelete = async () => {
  await deleteSummary(props.documentId);
  summaryHtml.value = '';
  state.value = 'idle';
};
</script>

<style scoped>
.summary-panel {
  width: 380px;
  padding: 0.75rem;
}
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.editor {
  margin-top: 0.5rem;
  flex-grow: 1;
}
.state.generating {
  min-height: 2rem;
}
.text-red-500 {
  color: #ef4444;
}
</style>
