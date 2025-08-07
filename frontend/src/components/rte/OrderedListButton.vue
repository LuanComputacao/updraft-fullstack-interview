<template>
  <Button
    v-tooltip.top="`Ordered List (Ctrl+Shift+7)`"
    icon="pi pi-list-check"
    class="p-0 m-0 w-2rem h-2rem"
    :text="!isOrderedList"
    severity="secondary"
    :class="`text-${size}`"
    @click="onOrderedListClick"
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

const onOrderedListClick = () => {
  props.editor.chain().focus().toggleOrderedList().run();
};

const isOrderedList = computed(() => {
  return props.editor.isActive('orderedList');
});
</script>
