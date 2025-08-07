<template>
  <Button
    v-tooltip.top="`Italic (Ctrl+I)`"
    label="I"
    class="p-0 m-0 w-2rem h-2rem"
    :text="!isItalic"
    severity="secondary"
    :class="`text-${size}`"
    @click="onItalicClick"
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

const onItalicClick = () => {
  props.editor.chain().focus().toggleItalic().run();
};

const isItalic = computed(() => {
  return props.editor.isActive('italic');
});
</script>
