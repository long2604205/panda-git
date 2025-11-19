<template>
  <div v-for="(subNode, name) in node" :key="fullPath(name)" class="tree-group">
    <!-- Group Header -->
    <div
      class="tree-item tree-header"
      :class="{ active: fullPath(name) === activeBranch }"
      :style="{ '--level': level }"
      @click="onItemClick(name, subNode)"
      @contextmenu.prevent="openContextMenu(fullPath(name))"
    >
      <!-- Toggle icon -->
      <i
        v-if="isFolder(subNode)"
        class="tree-toggle fas fa-chevron-down"
        :class="{ collapsed: collapsedGroups[fullPath(name)] }"
        @click.stop="toggleGroup(fullPath(name))"
      ></i>

      <!-- Folder / File icon -->
      <i
        v-if="isFolder(subNode)"
        class="fas fa-folder text-warning me-1"
      ></i>
      <i
        v-else
        class="fas fa-code-branch text-info me-1"
        style="width: 1rem; display: inline-block;"
      ></i>

      <!-- Highlighted Name -->
      <span v-html="highlightedName(name, fullPath(name))"></span>
    </div>

    <!-- Nested Children -->
    <div v-if="isFolder(subNode) && !collapsedGroups[fullPath(name)]" class="nested">
      <branch-tree-verion
        :node="subNode"
        :path="fullPath(name) + '/'"
        :collapsed-groups="collapsedGroups"
        :toggle-group="toggleGroup"
        :active-branch="activeBranch"
        :set-active-branch="setActiveBranch"
        :open-context-menu="openContextMenu"
        :search-term="searchTerm"
        :level="level + 1"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  node: { type: Object, required: true },
  path: { type: String, default: '' },
  collapsedGroups: { type: Object, required: true },
  toggleGroup: { type: Function, required: true },
  activeBranch: { type: String, required: true },
  setActiveBranch: { type: Function, required: true },
  openContextMenu: { type: Function, required: true },
  searchTerm: { type: String, default: '' },
  level: { type: Number, default: 0 }
});

// Kiểm tra folder
const isFolder = (subNode) => subNode && Object.keys(subNode).length > 0;

// full path
const fullPath = (name) => props.path + name;

// Highlight theo search
const highlightedName = (name, path) => {
  if (!props.searchTerm) return name;
  const term = props.searchTerm.toLowerCase();
  if (name.toLowerCase().includes(term) || path.toLowerCase().includes(term)) {
    const escapedTerm = props.searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedTerm})`, 'gi');
    return name.replace(regex, `<span class="highlight">$1</span>`);
  }
  return name;
};

// Click item
const onItemClick = (name, subNode) => {
  if (isFolder(subNode)) props.toggleGroup(fullPath(name));
  else props.setActiveBranch(fullPath(name));
};
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
  padding: 4px 0 4px calc(var(--level, 0) * 20px);
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
