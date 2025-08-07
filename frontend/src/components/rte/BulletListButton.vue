<template>
  <Button
    v-tooltip.top="`Bullet List (Ctrl+Shift+8)`"
    icon="pi pi-list"
    class="p-0 m-0 w-2rem h-2rem"
    :text="!isBulletList"
    severity="secondary"
    :class="`text-${size}`"
    @click="onBulletListClick"
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

const onBulletListClick = () => {
  props.editor.chain().focus().toggleBulletList().run();
};

const isBulletList = computed(() => {
  return props.editor.isActive('bulletList');
});
</script>
