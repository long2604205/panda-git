<template>
  <div class="wrapper">
    <div ref="editorContainer" class="editor"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as monaco from 'monaco-editor';

const conflictText = `function getUserData() {
<<<<<<< HEAD
  return {
    name: "Alice",
    role: "Developer",
    isActive: true
  };
=======
  return {
    name: "Bob",
    role: "Engineer",
    isActive: false
  };
>>>>>>> feature/fix-user-role
}

function getSettings() {
<<<<<<< HEAD
  return {
    theme: "light",
    notifications: true
  };
=======
  return {
    theme: "dark",
    notifications: false
  };
>>>>>>> feature/setting-theme
}

function getPermissions() {
  return ["read", "write"];
}

function getUserStatus() {
<<<<<<< HEAD
  return "active";
=======
  return "inactive";
>>>>>>> feature/user-status
}`;


const editorContainer = ref();

onMounted(() => {
  const editor = monaco.editor.create(editorContainer.value, {
    value: conflictText,
    language: 'javascript',
    theme: 'vs-dark',
    readOnly: false,
    fontSize: 14,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
  });

  const decorations = [];
  const lines = conflictText.split('\n');
  const conflicts = [];

  let startLine = null;
  let middleLine = null;
  let endLine = null;

  // Detect conflicts
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('<<<<<<<')) {
      startLine = i + 1;
    } else if (line.startsWith('=======')) {
      middleLine = i + 1;
    } else if (line.startsWith('>>>>>>>')) {
      endLine = i + 1;
      if (startLine && middleLine && endLine) {
        conflicts.push({ startLine, middleLine, endLine });
        startLine = middleLine = endLine = null;
      }
    }
  }

  // Render conflicts
  for (const conflict of conflicts) {
    const { startLine, middleLine, endLine } = conflict;

    // Highlight các vùng
    decorations.push(
      {
        range: new monaco.Range(startLine, 1, startLine, 1),
        options: { isWholeLine: true, className: 'conflict-header' },
      },
      {
        range: new monaco.Range(startLine + 1, 1, middleLine - 1, 1),
        options: { isWholeLine: true, className: 'conflict-current' },
      },
      {
        range: new monaco.Range(middleLine + 1, 1, endLine - 1, 1),
        options: { isWholeLine: true, className: 'conflict-incoming' },
      },
      {
        range: new monaco.Range(endLine, 1, endLine, 1),
        options: { isWholeLine: true, className: 'conflict-footer' },
      }
    );

    // Insert buttons
    editor.changeViewZones((accessor) => {
      const domNode = document.createElement('div');
      domNode.className = 'merge-buttons';
      domNode.innerHTML = `
        <button class="accept-current">Accept Current Change</button>
        <button class="accept-incoming">Accept Incoming Change</button>
        <button class="accept-both">Accept Both Changes</button>
        <button class="compare">Compare Changes</button>
      `;

      // Gắn sự kiện tạm thời
      domNode.querySelector('.accept-current').onclick = () => alert('Accepted current');
      domNode.querySelector('.accept-incoming').onclick = () => alert('Accepted incoming');
      domNode.querySelector('.accept-both').onclick = () => alert('Accepted both');
      domNode.querySelector('.compare').onclick = () => alert('Compare not implemented');

      accessor.addZone({
        afterLineNumber: startLine - 1,
        heightInPx: 32,
        domNode,
      });
    });
  }

  editor.deltaDecorations([], decorations);
});
</script>

<style>
.wrapper {
  height: 100vh;
  width: 100%;
}

.editor {
  height: 100%;
  width: 100%;
}

/* Header: <<<<<<< */
.monaco-editor .conflict-header {
  background: #2C7166;
  font-style: italic;
  color: #c0c0c0;
}

/* Footer: >>>>>>> */
.monaco-editor .conflict-footer {
  background: rgba(100, 150, 250, 0.3);
  font-style: italic;
  color: #c0c0c0;
}

/* HEAD content */
.monaco-editor .conflict-current {
  background: #2C7166;
  opacity: 0.5;
}

/* INCOMING content */
.monaco-editor .conflict-incoming {
  background: rgba(100, 150, 250, 0.3);
  opacity: 0.5;
}

/* Buttons */
.merge-buttons {
  pointer-events: auto;
  display: flex;
  gap: 8px;
  padding: 8px 8px 8px 0;
  background-color: #1e1e1e;
  color: white;
  border-bottom: 1px solid #444;
  font-size: 12px;
  z-index: 9999;
  position: relative;
  margin-left: 0;
}

.merge-buttons button {
  background: transparent;
  color: white;
  border: none;
  padding: 2px 6px;
  cursor: pointer;
  pointer-events: auto;
}

.merge-buttons button:hover {
  background: unset;
  color: #0e639c;
}

.accept-current {
  padding-left: 0 !important;
}
</style>
