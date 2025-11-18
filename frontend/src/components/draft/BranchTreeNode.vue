<template>
  <div v-for="(subNode, name) in node" :key="path + name" class="tree-group">
    <!-- Group Header -->
    <div class="tree-item tree-header" @click="toggleGroup(path + name)" :style="{ '--level': level }">
      <i class="fas fa-chevron-down tree-toggle" :class="{ collapsed: collapsedGroups[path + name] }"></i>
      <i :class="icon" class="me-1"></i>
      <span>{{ name }}</span>
    </div>

    <!-- Nested Children -->
    <div v-if="!collapsedGroups[path + name]" class="nested">
      <!-- Leaf -->
      <template v-if="subNode === null">
        <div
          class="tree-item nested"
          :class="{ active: path + name === activeBranch }"
          @contextmenu="openContextMenu(path + name)"
          :style="{ '--level': level + 1 }"
        >
          <i :class="leafIcon" class="me-1"></i>
          <span>{{ name }}</span>
        </div>
      </template>

      <!-- Recursive Branch -->
      <template v-else>
        <BranchTreeNode
          :node="subNode"
          :path="path + name + '/'"
          :collapsedGroups="collapsedGroups"
          :toggleGroup="toggleGroup"
          :activeBranch="activeBranch"
          :openContextMenu="openContextMenu"
          :icon="icon"
          :leafIcon="leafIcon"
          :level="level + 1"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import BranchTreeNode from './BranchTreeNode.vue'

defineProps({
  node: Object,
  path: { type: String, default: '' },
  collapsedGroups: Object,
  toggleGroup: Function,
  activeBranch: String,
  openContextMenu: Function,
  icon: { type: String, default: 'fas fa-folder text-warning' },
  leafIcon: { type: String, default: 'fas fa-code-branch text-success' },
  level: { type: Number, default: 0 } // cấp độ đệ quy
})
</script>

<style scoped>
/* Multi-level tree padding based on level */
.tree-item {
  display: flex;
  align-items: center;
  padding: 4px 0;
  font-size: 14px;
  cursor: pointer;
  border-radius: 5px;
  user-select: none;
  transition: background-color 0.2s ease;
  padding-left: calc(var(--level) * 20px);
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

/* Nested container */
.nested {
  margin-left: 0; /* padding handled by --level */
}

/* Highlight for search match */
::v-deep(.highlight) {
  background-color: #ff9700;
  color: black;
  border-radius: 2px;
  padding: 0 2px;
}
</style>
