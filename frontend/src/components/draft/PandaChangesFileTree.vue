<template>
  <div class="file-tree">
    <!-- Changes Section -->
    <div
      class="section-header"
      :class="{ collapsed: !changesSectionExpanded }"
    >
      <i
        class="fas fa-caret-down collapse-icon"
        :class="{ collapsed: !changesSectionExpanded }"
        @click="toggleChangesSection"
      ></i>
      <input
        type="checkbox"
        class="file-checkbox"
      >
      <span class="section-title">Changes {{ changedFiles.length }} files</span>
    </div>
    <transition name="collapse">
      <div v-show="changesSectionExpanded" class="section-content">
        <ul class="file-list">
          <li
            v-for="file in changedFiles"
            :key="file.id"
            class="file-item"
          >
            <input
              type="checkbox"
              class="file-checkbox"
              :id="`file-${file.id}`"
              v-model="file.selected"
              @click="toggleFileSelection(file, $event)"
              @click.stop
              @change="onFileSelectionChange(file)"
            >
            <i :class="getFileIconClass(file)"></i>
            <span class="file-name">{{ file.name }}</span>
            <span v-if="file.path" class="file-path">{{ file.path }}</span>
          </li>
        </ul>
      </div>
    </transition>

    <!-- Unversioned Files Section -->
    <div
      class="section-header"
      :class="{ collapsed: !unversionedSectionExpanded }"
    >
      <i
        class="fas fa-caret-down collapse-icon"
        :class="{ collapsed: !unversionedSectionExpanded }"
        @click="toggleUnversionedSection"
      ></i>
      <input
        type="checkbox"
        class="file-checkbox"
      >
      <span class="section-title">Unversioned Files {{ unversionedFiles.length }} file</span>
    </div>
    <transition name="collapse">
      <div v-show="unversionedSectionExpanded" class="section-content">
        <ul class="file-list">
          <li
            v-for="file in unversionedFiles"
            :key="file.id"
            class="file-item"
          >
            <input
              type="checkbox"
              class="file-checkbox"
              :id="`file-${file.id}`"
              v-model="file.selected"
              @click="toggleFileSelection(file, $event)"
              @click.stop
              @change="onFileSelectionChange(file)"
            >
            <i :class="getFileIconClass(file)"></i>
            <span class="file-name">{{ file.name }}</span>
            <span v-if="file.path" class="file-path">{{ file.path }}</span>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  initialChangedFiles: {
    type: Array,
    default: () => []
  },
  initialUnversionedFiles: {
    type: Array,
    default: () => [
      {
        id: 5,
        name: 'package-lock.json',
        type: 'json',
        locked: true,
        selected: false
      }
    ]
  }
})

// Emits
const emit = defineEmits(['file-selection-changed', 'section-toggled'])

// Reactive data
const changesSectionExpanded = ref(true)
const unversionedSectionExpanded = ref(true)
const changedFiles = ref([...props.initialChangedFiles])
const unversionedFiles = ref([...props.initialUnversionedFiles])

// Computed properties
const selectedFiles = computed(() => {
  const selected = []
  changedFiles.value.forEach(file => {
    if (file.selected) selected.push(file)
  })
  unversionedFiles.value.forEach(file => {
    if (file.selected) selected.push(file)
  })
  return selected
})

const totalSelectedCount = computed(() => selectedFiles.value.length)

// Methods
const toggleChangesSection = () => {
  changesSectionExpanded.value = !changesSectionExpanded.value
  emit('section-toggled', {
    section: 'changes',
    expanded: changesSectionExpanded.value
  })
}

const toggleUnversionedSection = () => {
  unversionedSectionExpanded.value = !unversionedSectionExpanded.value
  emit('section-toggled', {
    section: 'unversioned',
    expanded: unversionedSectionExpanded.value
  })
}

const toggleFileSelection = (file, event) => {
  if (event.target.type !== 'checkbox') {
    file.selected = !file.selected
    onFileSelectionChange(file)
  }
}

const onFileSelectionChange = (file) => {
  emit('file-selection-changed', {
    file: file,
    selected: file.selected,
    allSelected: selectedFiles.value
  })
}

const getFileIconClass = (file) => {
  const baseClasses = 'file-icon'

  if (file.locked) {
    return `fas fa-lock ${baseClasses} locked`
  }

  switch (file.type) {
    case 'css':
      return `fas fa-file-code ${baseClasses} css`
    case 'vue':
      return `fab fa-vuejs ${baseClasses} vue`
    case 'json':
      return `fas fa-file-code ${baseClasses} json`
    case 'js':
      return `fab fa-js-square ${baseClasses} js`
    case 'html':
      return `fab fa-html5 ${baseClasses} html`
    default:
      return `fas fa-file ${baseClasses}`
  }
}

// Public methods (exposed to parent)
const selectAllFiles = () => {
  changedFiles.value.forEach(file => {
    file.selected = true
  })
  unversionedFiles.value.forEach(file => {
    file.selected = true
  })
}

const deselectAllFiles = () => {
  changedFiles.value.forEach(file => {
    file.selected = false
  })
  unversionedFiles.value.forEach(file => {
    file.selected = false
  })
}

const addFile = (file, section = 'changes') => {
  const newFile = {
    id: Date.now(),
    selected: false,
    ...file
  }

  if (section === 'changes') {
    changedFiles.value.push(newFile)
  } else {
    unversionedFiles.value.push(newFile)
  }
}

const removeFile = (fileId) => {
  changedFiles.value = changedFiles.value.filter(file => file.id !== fileId)
  unversionedFiles.value = unversionedFiles.value.filter(file => file.id !== fileId)
}

// Expose methods to parent component
defineExpose({
  selectAllFiles,
  deselectAllFiles,
  addFile,
  removeFile,
  selectedFiles: selectedFiles,
  totalSelectedCount: totalSelectedCount
})

// Watch for changes in selected files
watch(selectedFiles, (newSelected) => {
  console.log('Selected files changed:', newSelected)
}, { deep: true })

watch(
  () => props.initialChangedFiles,
  (newFiles) => {
    changedFiles.value = [...newFiles]
  },
  { immediate: true, deep: true }
)
</script>

<style scoped>
.file-tree {
  border-radius: 4px;
  padding: 0;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  color: #ffffff;
}

.section-header {
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
  user-select: none;
}

.section-header:hover {
  border-radius: 10px;
  background-color: #4a4a4a;
}

.section-header.collapsed {
  border-bottom: none;
}

.collapse-icon {
  margin-right: 8px;
  font-size: 16px;
  transition: transform 0.2s;
  color: #ff9500;
}

.collapse-icon.collapsed {
  transform: rotate(-90deg);
}

.section-title {
  font-weight: 500;
  margin: 0;
}

.section-content {
  overflow: hidden;
}

.file-list {
  padding: 0;
  margin: 0;
  list-style: none;
}

.file-item {
  padding: 6px 12px 6px 48px;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
  cursor: pointer;
}

.file-item:last-child {
  border-bottom: none;
}

.file-item:hover {
  border-radius: 10px;
  background-color: #4a4a4a;
}

.file-checkbox {
  margin-right: 8px;
  width: 14px;
  height: 14px;
  border: 1px solid #666;
  background-color: transparent;
  appearance: none;
  border-radius: 2px;
  position: relative;
  cursor: pointer;
}

.file-checkbox:checked {
  background-color: #007acc;
  border-color: #007acc;
}

.file-checkbox:checked::after {
  content: '✓';
  position: absolute;
  top: -2px;
  left: 1px;
  color: white;
  font-size: 10px;
  font-weight: bold;
}

.file-icon {
  margin-right: 8px;
  font-size: 12px;
  width: 14px;
  text-align: center;
}

.file-icon.css {
  color: #42a5f5;
}

.file-icon.vue {
  color: #4fc08d;
}

.file-icon.json {
  color: #ffd700;
}

.file-icon.js {
  color: #f7df1e;
}

.file-icon.html {
  color: #e34f26;
}

.file-icon.locked {
  color: #ff5252;
}

.file-name {
  flex-grow: 1;
  margin-right: 8px;
}

.file-path {
  color: #888;
  font-size: 11px;
}

/* Transition animations */
.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
