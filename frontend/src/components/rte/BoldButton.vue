<template>
  <Button
    v-tooltip.top="`Bold (Ctrl+B)`"
    label="B"
    class="p-0 m-0 w-2rem h-2rem"
    :text="!isBold"
    severity="secondary"
    :class="`text-${size}`"
    @click="onBoldClick"
  />
</template>
<script setup>
import { Editor } from '@tiptap/vue-3';
import Button from 'primevue/button';
import { computed, defineProps, inject } from 'vue';

const size = inject('size');
const props = defineProps({
  editor: {
    type: Editor,
    required: true,
  },
});

const onBoldClick = () => {
  props.editor.chain().focus().toggleBold().run();
};

const isBold = computed(() => {
  return props.editor.isActive('bold');
});
</script>
