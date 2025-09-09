<template>
  <div class="editor-wrapper">
    <div class="editor-container">
      <div ref="editorLeftRef" class="monaco-editor"></div>
      <button class="run-button-absolute" @click="runLeft">▶ Run</button>
    </div>
    <div class="editor-container">
      <div ref="editorRightRef" class="monaco-editor"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as monaco from 'monaco-editor'

const editorLeftRef = ref(null)
const editorRightRef = ref(null)

const  model = ref(null)

onMounted(() => {
  // Editor bên trái
  const editorLeft = monaco.editor.create(editorLeftRef.value, {
    value: [
      'function hello() {',
      '  console.log("Left Editor");',
      '}'
    ].join('\n'),
    language: 'javascript',
    theme: 'vs-dark',
    fontSize: 14,
    minimap: { enabled: false },
    automaticLayout: true
  })

  model.value = editorLeft.getModel()

  const widgetLeft = {
    getId: () => 'run-left.widget',
    getDomNode: () => {
      if (!widgetLeft.domNode) {
        const btn = document.createElement('button')
        btn.innerText = '▶ Run'
        btn.className = 'run-button'
        btn.onclick = () => alert('Run left code')
        widgetLeft.domNode = btn
      }
      return widgetLeft.domNode
    },
    getPosition: () => ({
      position: { lineNumber: 2, column: 10 },
      preference: [monaco.editor.ContentWidgetPositionPreference.ABOVE]
    })
  }
  editorLeft.addContentWidget(widgetLeft)

  // Editor bên phải
  const editorRight = monaco.editor.create(editorRightRef.value, {
    value: [
      'function world() {',
      '  console.log("Right Editor");',
      '}'
    ].join('\n'),
    language: 'javascript',
    theme: 'vs-dark',
    fontSize: 14,
    minimap: { enabled: false },
    automaticLayout: true
  })

  const widgetRight = {
    getId: () => 'run-right.widget',
    getDomNode: () => {
      if (!widgetRight.domNode) {
        const btn = document.createElement('button')
        btn.innerText = '▶ Run'
        btn.className = 'run-button'
        btn.onclick = () => alert('Run right code')
        widgetRight.domNode = btn
      }
      return widgetRight.domNode
    },
    getPosition: () => ({
      position: { lineNumber: 2, column: 10 },
      preference: [monaco.editor.ContentWidgetPositionPreference.ABOVE]
    })
  }
  editorRight.addContentWidget(widgetRight)
})

function runLeft() {
  alert(model.value.getLineContent(1))
}


</script>

<style scoped>
.editor-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  gap: 16px;
  background-color: #1e1e1e;
}

.editor-container {
  flex: 1;
  height: 90vh;
  border: 1px solid #333;
  position: relative;
  max-width: 50%;
  min-width: 400px;
}

.monaco-editor {
  width: 100%;
  height: 100%;
}

/* Button nằm trong Monaco */
:global(.run-button) {
  background-color: #0e639c;
  color: white;
  border: none;
  padding: 3px 6px;
  font-size: 12px;
  border-radius: 4px;
  cursor: pointer;
  z-index: 50;
  position: absolute;
  transform: translateY(-4px);
}
.run-button-absolute {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background-color: #0e639c;
  color: white;
  border: none;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  z-index: 10;
}
</style>
