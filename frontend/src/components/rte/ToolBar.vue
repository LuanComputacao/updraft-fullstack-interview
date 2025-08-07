<template>
  <div class="flex w-full justify-content-between align-items-center">
    <div class="flex gap-0">
      <HeadingMenu :editor="props.editor" />
      <VerticalLine />
      <BoldButton :editor="props.editor" />
      <ItalicButton :editor="props.editor" />
      <UnderlineButton :editor="props.editor" />
      <VerticalLine />
      <BulletListButton :editor="props.editor" />
      <OrderedListButton :editor="props.editor" />
    </div>
  </div>
</template>
<script setup>
import { Editor } from '@tiptap/vue-3';
import { computed, defineProps, provide } from 'vue';

import BoldButton from './BoldButton.vue';
import BulletListButton from './BulletListButton.vue';
import HeadingMenu from './HeadingMenu.vue';
import ItalicButton from './ItalicButton.vue';
import OrderedListButton from './OrderedListButton.vue';
import UnderlineButton from './UnderlineButton.vue';
import VerticalLine from './VerticalLine.vue';
const props = defineProps({
  editor: {
    type: Editor,
    required: true,
  },
  size: {
    type: String,
    default: 'sm',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
});

provide(
  'size',
  computed(() => props.size)
);
</script>
