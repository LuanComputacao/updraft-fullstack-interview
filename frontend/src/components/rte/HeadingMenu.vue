<template>
  <div>
    <Button
      type="button"
      class="p-0 m-0"
      text
      severity="secondary"
      aria-haspopup="true"
      aria-controls="heading_menu_overlay"
      @click="toggle"
    >
      <div v-tooltip.top="'Text styles'" class="flex align-items-baseline gap-1 p-1">
        <span class="font-bold" :class="`text-${size}`">Aa</span>
        <i class="pi pi-angle-down"></i>
      </div>
    </Button>
    <Menu
      id="heading_menu_overlay"
      ref="menu"
      :model="items"
      :popup="true"
      :pt="{
        root: { class: 'w-auto' },
      }"
    >
      <template #item="{ item }">
        <a
          class="flex align-items-center p-3 cursor-pointer gap-3"
          v-bind="null"
          :class="
            (
              item.level > 0
                ? editor.isActive('heading', { level: item.level })
                : editor.isActive('paragraph')
            )
              ? 'bg-primary-100 hover:bg-primary-100'
              : 'bg-white hover:bg-primary-50'
          "
          @click="onClick(item.level)"
        >
          <div class="ml-2 tiptap">
            <component :is="item.HTMLTag" class="p-0 m-0">{{ item.label }}</component>
          </div>
          <span
            v-if="item.shortcut"
            class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1 font-light"
            >{{ item.shortcut }}</span
          >
        </a>
      </template>
    </Menu>
  </div>
</template>
<script setup>
import { Editor } from '@tiptap/vue-3';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import { defineProps, inject, ref } from 'vue';

const size = inject('size');
const props = defineProps({
  editor: {
    type: Editor,
    required: true,
  },
});

const items = ref([
  { label: 'Normal text', HTMLTag: 'p', shortcut: 'Ctrl+Alt+0', level: 0 },
  { label: 'Heading 1', HTMLTag: 'h1', shortcut: 'Ctrl+Alt+1', level: 1 },
  { label: 'Heading 2', HTMLTag: 'h2', shortcut: 'Ctrl+Alt+2', level: 2 },
  { label: 'Heading 3', HTMLTag: 'h3', shortcut: 'Ctrl+Alt+3', level: 3 },
  { label: 'Heading 4', HTMLTag: 'h4', shortcut: 'Ctrl+Alt+4', level: 4 },
]);

const menu = ref();
const toggle = (event) => {
  menu.value.toggle(event);
};

const onClick = (level) => {
  if (level === 0) {
    props.editor.chain().focus().setParagraph().run();
  } else {
    props.editor.chain().focus().toggleHeading({ level }).run();
  }
};
</script>
