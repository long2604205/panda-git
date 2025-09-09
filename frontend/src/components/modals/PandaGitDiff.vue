<template>
  <base-form
    ref="refCompareCode"
    v-model="visible"
    title="Panda Git Diff Workspace"
  >
    <template #content>
      <div class="toolbar-panel">
        <div class="toolbar-action col-md-12 d-flex">
          <button class="btn btn-toolbar" @click="goToPrevDiff" :disabled="currentDiffIndex <= 0">
            <i class="fa-solid fa-arrow-up"></i>
          </button>
          <button class="btn btn-toolbar"
                  @click="goToNextDiff"
                  :disabled="currentDiffIndex >= diffs.length - 1">
            <i class="fa-solid fa-arrow-down"></i>
          </button>
          <button class="btn btn-toolbar" @click="logModifiedContent">
            <i class="fa-regular fa-file-code"></i>
          </button>

          <div class="vertical-line"></div>
          <button class="btn btn-toolbar">
            <i class="fa-solid fa-left-long"></i>
          </button>
          <button class="btn btn-toolbar">
            <i class="fa-solid fa-right-long"></i>
          </button>
        </div>
      </div>

      <div class="row diff-workspace">
        <div ref="editorContainer" class="editor-container"></div>
      </div>
    </template>
  </base-form>
</template>

<script setup lang="js">
import BaseForm from '@/components/modals/BaseForm.vue'
import { originalCode, modifiedCode } from '@/data/datasample.js'
import '@/monaco-worker-loader.js'
import * as monaco from 'monaco-editor'
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

const editorContainer = ref(null)
const status = ref('Loading...')
const diffs = ref([])
const currentDiffIndex = ref(0)

let diffEditor = null

const logModifiedContent = () => {
  if (!diffEditor) {
    console.warn('Editor chưa sẵn sàng')
    return
  }

  const modifiedContent = diffEditor.getModel()?.modified.getValue()
  console.log('📝 Modified content:\n', modifiedContent)
}


const goToNextDiff = () => {
  if (currentDiffIndex.value < diffs.value.length - 1) {
    currentDiffIndex.value++
    navigateToCurrentDiff()
    status.value = `Moved to diff ${currentDiffIndex.value + 1}`
  } else {
    status.value = 'Already at last diff'
  }
}

const goToPrevDiff = () => {
  if (currentDiffIndex.value > 0) {
    currentDiffIndex.value--
    navigateToCurrentDiff()
    status.value = `Moved to diff ${currentDiffIndex.value + 1}`
  } else {
    status.value = 'Already at first diff'
  }
}

const navigateToCurrentDiff = () => {
  const current = diffs.value[currentDiffIndex.value]
  if (!current || !diffEditor) return

  const modifiedEditor = diffEditor.getModifiedEditor()
  const targetLine = current.modifiedStartLineNumber ?? current.originalStartLineNumber ?? 1

  modifiedEditor.setPosition({ lineNumber: targetLine, column: 1 })
  modifiedEditor.revealLineInCenter(targetLine)
  modifiedEditor.focus()
}

onMounted(async () => {
  await nextTick()
  if (!editorContainer.value) return

  diffEditor = monaco.editor.createDiffEditor(editorContainer.value, {
    theme: 'vs-dark',
    renderSideBySide: true,
    automaticLayout: true,
    readOnly: false,
    originalEditable: false,
  })

  const originalModel = monaco.editor.createModel(originalCode, 'javascript')
  const modifiedModel = monaco.editor.createModel(modifiedCode, 'javascript')

  diffEditor.setModel({ original: originalModel, modified: modifiedModel })

  await new Promise((resolve) => setTimeout(resolve, 500)) // wait for diffs to be calculated

  diffs.value = diffEditor.getLineChanges() || []
  if (diffs.value.length > 0) {
    currentDiffIndex.value = 0
    status.value = `Ready! ${diffs.value.length} diffs found`
    navigateToCurrentDiff()
  } else {
    status.value = 'No differences found'
  }
})

onBeforeUnmount(() => {
  if (diffEditor) diffEditor.dispose()
})
const visible = ref(false)
</script>

<style scoped lang="scss">
.code-line {
  height: 1.5em;
  padding-left: 5px;
  white-space: pre-wrap;
  word-break: break-word;
}
:deep(.modal-body) {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

.line-added {
  background-color: #294436 !important;
  color: #9ccc65 !important;
}

.line-removed {
  background-color: #442c2e !important;
  color: #ef9a9a !important;
}

.line-modified {
  background-color: #3c3f41 !important;
  color: #ffd54f !important;
}

.diff-workspace {

  .original-workspace, .modified-workspace {
    padding: 0;
  }

  .code-editor-container {
    display: flex;
    color: #d4d4d4;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    border-radius: 5px;
  }

  .line-numbers {
    background-color: #252526;
    padding: 10px 5px;
    color: #858585;
    text-align: right;
    user-select: none;
    width: 40px;
    overflow: hidden;
  }

  .line-numbers div {
    height: 1.5em;
  }

  .code-editor {
    padding: 10px;
    width: 100%;
    white-space: pre-wrap;
    line-height: 1.5em;
    overflow: hidden;
  }

  .code-editor:focus-visible {
    outline: unset;
  }
}

.toolbar-panel {
  background-color: var(--bg-secondary);
  height: 36px;
  min-height: 36px;
  align-items: center;
}

.toolbar-action {
  height: 100%;
  align-items: center;
}

.vertical-line {
  width: 1px;
  height: 70%;
  background-color: var(--bg-tertiary);
  margin: 0 5px;
}

.btn-toolbar {
  color: var(--text-secondary);
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  outline: none;
  box-shadow: none;
  border: none; /* cũng nên set luôn */
}

.btn-toolbar:disabled {
  border: unset;
}

.btn-toolbar:focus,
.btn-toolbar:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}

button:focus,
button:active {
  box-shadow: none !important;
  border-color: transparent !important;
}
</style>
<style scoped>
.editor-container {
  flex: 1;
  height: 500px;
  border: 1px solid #444;
}

/* Custom highlighting for current diff */
:global(.current-diff-line) {
  background-color: rgba(255, 255, 0, 0.2) !important;
}

:global(.current-diff-glyph) {
  background-color: #ffff00 !important;
  width: 4px !important;
}
</style>
