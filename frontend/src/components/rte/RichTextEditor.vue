<template>
  <div
    class="w-full border-1 border-round border-gray-300"
    style="min-height: 200px; max-height: 500px; overflow: auto"
  >
    <ToolBar v-if="editor" class="pl-2" :editor="editor" />
    <HorizontalLine />
    <EditorContent :editor="editor" :editable="true" class="text-md w-full p-2" />
  </div>
</template>

<script setup>
import Bold from '@tiptap/extension-bold';
import BulletList from '@tiptap/extension-bullet-list';
import Document from '@tiptap/extension-document';
import Heading from '@tiptap/extension-heading';
import Italic from '@tiptap/extension-italic';
import ListItem from '@tiptap/extension-list-item';
import OrderedList from '@tiptap/extension-ordered-list';
import Paragraph from '@tiptap/extension-paragraph';
import Placeholder from '@tiptap/extension-placeholder';
import Text from '@tiptap/extension-text';
import Underline from '@tiptap/extension-underline';
import { EditorContent, useEditor } from '@tiptap/vue-3';
import { defineEmits, defineModel, defineProps, onBeforeUnmount, watch } from 'vue';

import HorizontalLine from './HorizontalLine.vue';
import ToolBar from './ToolBar.vue';

const props = defineProps({
  placeholder: {
    type: String,
    required: false,
    default: 'Start typing...',
  },
});

const emit = defineEmits(['update']);
const model = defineModel();

const editor = useEditor({
  content: model.value,
  editable: true,
  extensions: [
    Document,
    Paragraph,
    Text,
    Bold,
    Italic,
    Underline,
    ListItem,
    BulletList,
    OrderedList,
    Heading.configure({
      levels: [1, 2, 3, 4],
    }),
    Placeholder.configure({
      placeholder: props.placeholder,
      showOnlyWhenEditable: false,
    }),
  ],
  onUpdate: () => {
    updateEditorContent();
  },
});

onBeforeUnmount(() => {
  editor.value?.destroy();
});

watch(
  () => model.value,
  (newValue) => {
    const editorValue = editor.value?.getHTML();
    const isSame = editorValue === newValue;
    if (isSame || (editorValue === '<p></p>' && newValue === null)) {
      return;
    }
    editor.value?.commands?.setContent(newValue, false);
  }
);

const updateEditorContent = () => {
  let value = editor.value?.getHTML();
  if (value === '<p></p>') {
    value = '';
  }
  model.value = value;
  emit('update', value);
};
</script>

<style lang="scss">
.ProseMirror:focus {
  outline: none;
}

.tiptap {
  font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',
    Arial, sans-serif;

  :first-child {
    margin-top: 0;
  }

  p {
    line-height: 1.6rem;
    margin: 0.5rem 0;
  }

  /* Heading styles */
  h1,
  h2,
  h3,
  h4 {
    line-height: 1.1;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }

  h1 {
    margin-top: 3rem;
    font-size: 2.3rem;
    font-weight: 800;
  }

  h2 {
    font-weight: 700;
    margin-top: 2.5rem;
    font-size: 2rem;
  }

  h3 {
    font-weight: 600;
    margin-top: 2rem;
    font-size: 1.7rem;
  }

  h4 {
    font-weight: 500;
    margin-top: 1.5rem;
    font-size: 1.4rem;
  }

  // List styles
  ul,
  ol {
    padding: 0 1rem;
    margin: 0.5rem 1rem 0.5rem 0.4rem;
    list-style-position: outside;

    li {
      margin: 0.25em 0;
    }

    li p {
      margin-top: 0.25em;
      margin-bottom: 0.25em;
    }

    li ul,
    li ol {
      padding: 0 0.5rem;
      margin: 0rem 0.5rem 0.75rem 0.5rem;
    }
  }

  ul {
    list-style-type: disc;
  }

  ol {
    list-style-type: decimal;
  }

  // Bold, italic, underline styles
  strong {
    font-weight: bold;
  }

  em {
    font-style: italic;
  }

  u {
    text-decoration: underline;
  }

  p.is-editor-empty:first-child::before {
    color: var(--surface-400);
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
  }
}

.ProseMirror {
  padding-bottom: 10px !important;
}
</style>
