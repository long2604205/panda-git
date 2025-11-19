<template>
  <div v-for="(subNode, name) in node" :key="path + name" class="tree-group">
    <!-- Group Header -->
    <div
      class="tree-item tree-header"
      @click="toggleGroup(path + name)"
      :style="{ '--level': level }"
    >
      <!-- Chỉ hiển thị toggle + folder nếu có children thật -->
      <i
        v-if="hasChildren(subNode)"
        class="fas fa-chevron-down tree-toggle"
        :class="{ collapsed: collapsedGroups[path + name] }"
      ></i>

      <i
        v-if="hasChildren(subNode)"
        :class="icon"
        class="me-1"
      ></i>

      <!-- Leaf hoặc nhánh cuối cùng: chỉ show leafIcon -->
      <i
        v-else
        :class="leafIcon"
        class="me-1"
      ></i>

      <span v-html="highlightedName(name, path + name)"></span>
    </div>

    <!-- Nested Children -->
    <div v-if="hasChildren(subNode) && !collapsedGroups[path + name]" class="nested">
      <!-- Leaf -->
      <template v-if="subNode === null">
        <div
          class="tree-item nested"
          :class="{ active: path + name === props.activeBranch }"
          @click.stop="setActiveBranch(path + name)"
          @contextmenu.prevent="props.openContextMenu(path + name)"
          :style="{ '--level': level + 1 }"
        >
          <i :class="leafIcon" class="me-1"></i>
          <span v-html="highlightedName(name, path + name)"></span>
        </div>
      </template>

      <!-- Recursive Branch -->
      <template v-else>
        <BranchTreeNode
          :node="subNode"
          :path="path + name + '/'"
          :collapsedGroups="collapsedGroups"
          :toggleGroup="toggleGroup"
          :activeBranch="props.activeBranch"
          @update:activeBranch="$emit('update:activeBranch', $event)"
          :openContextMenu="props.openContextMenu"
          :icon="icon"
          :leafIcon="leafIcon"
          :level="level + 1"
          :searchTerm="props.searchTerm"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import BranchTreeNode from './BranchTreeNode.vue'

const props = defineProps({
  node: Object,
  path: { type: String, default: '' },
  collapsedGroups: Object,
  toggleGroup: Function,
  activeBranch: String,
  openContextMenu: Function,
  icon: { type: String, default: 'fas fa-folder text-warning' },
  leafIcon: { type: String, default: 'fas fa-code-branch text-success' },
  level: { type: Number, default: 0 },
  searchTerm: { type: String, default: '' }
})

const emit = defineEmits(['update:activeBranch'])

// Highlight tên branch match search (theo name hoặc path)
const highlightedName = (name, fullPath) => {
  if (!props.searchTerm) return name
  const term = props.searchTerm.toLowerCase()
  if (name.toLowerCase().includes(term) || fullPath.toLowerCase().includes(term)) {
    const regex = new RegExp(`(${props.searchTerm})`, 'gi')
    return name.replace(regex, `<span class="highlight">$1</span>`)
  }
  return name
}

// Kiểm tra có children
const hasChildren = (node) => node !== null && Object.keys(node || {}).length > 0

// Click leaf
const setActiveBranch = (path) => {
  emit('update:activeBranch', path)
}

// Hàm init collapsedGroups mặc định
function initCollapsed(tree, pathPrefix = '') {
  for (const key in tree) {
    const fullPath = pathPrefix + key
    if (hasChildren(tree[key])) {
      if (!(fullPath in props.collapsedGroups)) {
        props.collapsedGroups[fullPath] = true
      }
      initCollapsed(tree[key], fullPath + '/')
    }
  }
}

// Watch searchTerm → reset collapsedGroups rồi mở folder chứa match
watch(
  () => props.searchTerm,
  () => {
    // reset tất cả folder về đóng
    resetCollapsed(props.node, props.path)
    // mở folder chứa match
    if (props.searchTerm) toggleCollapseForMatches(props.node, props.path)
  }
)

// reset collapsedGroups về true
function resetCollapsed(tree, pathPrefix = '') {
  for (const key in tree) {
    const fullPath = pathPrefix + key
    if (hasChildren(tree[key])) {
      props.collapsedGroups[fullPath] = true
      resetCollapsed(tree[key], fullPath + '/')
    }
  }
}

// mở folder chứa nhánh match search
function toggleCollapseForMatches(tree, pathPrefix = '') {
  for (const key in tree) {
    const fullPath = pathPrefix + key
    if (
      props.searchTerm &&
      (key.toLowerCase().includes(props.searchTerm.toLowerCase()) ||
        fullPath.toLowerCase().includes(props.searchTerm.toLowerCase()))
    ) {
      const parts = fullPath.split('/')
      let p = ''
      for (let i = 0; i < parts.length - 1; i++) {
        p += parts[i] + '/'
        props.collapsedGroups[p] = false
      }
    }
    if (hasChildren(tree[key])) {
      toggleCollapseForMatches(tree[key], fullPath + '/')
    }
  }
}

// mounted → init collapsed
onMounted(() => {
  initCollapsed(props.node, props.path)
})
</script>

<style scoped>
.tree-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  cursor: pointer;
  border-radius: 5px;
  user-select: none;
  transition: background-color 0.2s ease;
  padding: 4px 0 4px calc(var(--level) * 20px);
}

.tree-item:hover {
  background-color: var(--bg-hover);
}

.tree-item.active {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.tree-toggle {
  width: 12px;
  margin-right: 4px;
  font-size: 10px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.tree-toggle.collapsed {
  transform: rotate(-90deg);
}

.nested {
  margin-left: 0;
}

::v-deep(.highlight) {
  background-color: #ff9700;
  color: black;
  border-radius: 2px;
  padding: 0 2px;
}
</style>
