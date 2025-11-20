<template>
  <div v-for="(subNode, name) in node" :key="fullPath(name)" class="tree-group">
    <!-- Group Header -->
    <div
      class="tree-item tree-header"
      :class="{
      'computed-level': computedLevel(subNode) > props.level,
      'level-2-up-folder': isFolder(subNode) && computedLevel(subNode) === 2,
      'level-3-up-folder': isFolder(subNode) && computedLevel(subNode) === 3
      }"
      :data-level="computedLevel(subNode)"
      :style="{ '--level': computedLevel(subNode) }"
      @contextmenu.prevent="openContextMenu(fullPath(name), $event)"
    >

      <!-- Toggle icon -->
      <i
        v-if="isFolder(subNode)"
        class="tree-toggle fas fa-chevron-down branch-toggle"
        :class="{ collapsed: collapsedGroups[fullPath(name)] }"
        @click.stop="toggleGroup(fullPath(name))"
      />

      <!-- Folder / File icon -->
      <i
        v-if="isFolder(subNode)"
        class="fas fa-folder branch-folder me-1"
      />
      <i
        v-else
        :class="['me-1','fas',isMainBranch(name) && props.level === 1 ? 'fa-star branch-star' : 'fa-code-branch text-info']"
        style="width: 1rem; display: inline-block;"
      />

      <!-- Highlighted Name -->
      <span v-html="highlightedName(name, fullPath(name))"></span>
    </div>

    <!-- Nested Children -->
    <div v-if="isFolder(subNode) && shouldShowChildren(subNode, fullPath(name))" class="nested">
    <branch-tree-node
        :node="subNode"
        :path="fullPath(name) + '/'"
        :collapsed-groups="collapsedGroups"
        :toggle-group="toggleGroup"
        :open-context-menu="openContextMenu"
        :search-term="searchTerm"
        :level="level + 1"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  node: { type: Object, required: true },
  path: { type: String, default: '' },
  collapsedGroups: { type: Object, required: true },
  toggleGroup: { type: Function, required: true },
  openContextMenu: { type: Function, required: true },
  searchTerm: { type: String, default: '' },
  level: { type: Number, default: 1 }
})

const isFolder = (subNode) => subNode && Object.keys(subNode).length > 0

const fullPath = (name) => props.path + name

const computedLevel = (subNode) => {
  if (props.level === 1 && !isFolder(subNode)) {
    return props.level + 1
  }
  return props.level
}

const isMainBranch = (name) => {
  return name === 'master' || name === 'main'
}

const highlightedName = (name, path) => {
  if (!props.searchTerm) return name
  const term = props.searchTerm.toLowerCase()
  if (name.toLowerCase().includes(term) || path.toLowerCase().includes(term)) {
    const escapedTerm = props.searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`(${escapedTerm})`, 'gi')
    return name.replace(regex, `<span class="highlight">$1</span>`)
  }
  return name
}

const shouldShowChildren = (subNode, path) => {
  if (!props.searchTerm) {
    return !props.collapsedGroups[path]
  }
  return hasSearchMatch(subNode, path)
}

const hasSearchMatch = (node, basePath) => {
  for (const key in node) {
    const currentPath = basePath + '/' + key

    if (key.toLowerCase().includes(props.searchTerm.toLowerCase())) {
      return true
    }

    if (isFolder(node[key]) && hasSearchMatch(node[key], currentPath)) {
      return true
    }
  }
  return false
}
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

.tree-item.computed-level {
  padding-left: calc(var(--level) * 18px);
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

.branch-toggle,
.branch-folder {
  color: #727272;
}
.branch-star {
  color: #FFEE58;
}
.tree-item.level-2-up-folder {
  padding: 4px 0 4px calc(var(--level) * 12px) !important;
}
.tree-item.level-3-up-folder {
  padding: 4px 0 4px calc(var(--level) * 15px) !important;
}
</style>
