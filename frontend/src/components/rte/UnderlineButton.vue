<template>
  <Button
    v-tooltip.top="`Underline (Ctrl+U)`"
    label="U"
    class="p-0 m-0 w-2rem h-2rem"
    :text="!isUnderline"
    severity="secondary"
    :class="`text-${size}`"
    @click="onUnderlineClick"
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

const onUnderlineClick = () => {
  props.editor.chain().focus().toggleUnderline().run();
};

const isUnderline = computed(() => {
  return props.editor.isActive('underline');
});
</script>
