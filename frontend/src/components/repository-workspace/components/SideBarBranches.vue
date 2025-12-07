<template>
  <div class="flex flex-col h-full bg-[var(--bg-side)] overflow-hidden">
    <div class="sidebar-section-title flex items-center justify-between">
      <span id="selected-repo-name" class="truncate max-w-[150px] text-[var(--accent-color)]">
        BRANCHES
      </span>
      <div class="flex gap-2">
        <div
          class="cursor-pointer hover:text-[var(--p-text-main)] px-1 rounded hover:bg-[var(--p-hover)] transition-colors"
          :class="{ 'text-[var(--p-text-main)] bg-[var(--p-hover)]': isMenuOpen }"
          @click.stop="$emit('open-menu', $event)"
        >
          <i
            class="w-4 fa-solid fa-ellipsis fa-lg hover:text-[var(--text-color)] cursor-pointer items-center text-center"
          />
        </div>
      </div>
    </div>

    <div class="px-3 py-2 border-b border-[var(--border-color)] border-opacity-30">
      <input
        type="text"
        v-model="branchFilter"
        class="search-input w-full px-2 py-1 rounded"
        placeholder="Filter branches..."
      />
    </div>

    <div class="flex-1 overflow-y-auto py-1">
      <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-1">
        HEAD (Current branch)
      </div>
      <div
        v-if="currentBranch"
        class="branch-item active-branch"
        @contextmenu.prevent="handleCurrentBranchContext"
      >
        <i class="fa-solid fa-check w-4 text-center mr-1 text-[10px]" />
        <span class="truncate">{{ currentBranch }}</span>
        <span class="ml-auto text-[9px] border border-[var(--border-color)] px-1 rounded">
          HEAD
        </span>
      </div>
      <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-1">
        Local
      </div>
      <git-branch-tree
        ref="treeLocalRef"
        :branches="filteredBranches.local"
        :search-query="branchFilter"
        @select="$emit('select-branch', $event)"
        @branch-context="handleTreeContext"
      />

      <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-2">
        remotes
      </div>
      <git-branch-tree
        ref="treeRemoteRef"
        :branches="filteredBranches.remote"
        :search-query="branchFilter"
        @select="$emit('select-branch', $event)"
        @branch-context="handleTreeContext"
      />
    </div>
  </div>
</template>

<script setup>
import { provide, ref, computed, watch } from 'vue'
import GitBranchTree from '@/components/repository-workspace/components/GitBranchTree.vue'

const props = defineProps(['branches', 'currentBranch', 'isMenuOpen'])
const emit = defineEmits(['select-branch', 'open-menu', 'branch-context'])

const branchFilter = ref('')

// --- 1. Tạo Refs nắm giữ 2 cái cây ---
const treeLocalRef = ref(null)
const treeRemoteRef = ref(null)

// --- 2. Viết hàm gọi xuống cây con (Proxy method) ---
const callExpandAll = () => {
  // Gọi hàm expandAll() có sẵn trong GitBranchTree
  treeLocalRef.value?.expandAll()
  treeRemoteRef.value?.expandAll()
}

const callCollapseAll = () => {
  // Gọi hàm collapseAll() có sẵn trong GitBranchTree
  treeLocalRef.value?.collapseAll()
  treeRemoteRef.value?.collapseAll()
}

const filteredBranches = computed(() => {
  if (!props.branches) return { local: [], remote: [] }
  const filter = branchFilter.value?.toLowerCase() ?? ''

  return {
    local: (props.branches.local || []).filter((b) => b.toLowerCase().includes(filter)),
    remote: (props.branches.remote || []).filter((b) => b.toLowerCase().includes(filter)),
  }
})

const handleTreeContext = ({ event, path }) => {
  // Emit lên PandaGitLeftSideBar.
  // PandaGitLeftSideBar đang lắng nghe @branch-context="openBranchMenu(event, branch)"
  // Nên ta cần truyền tham số thứ 2 là data của branch (ở đây là path string)
  emit('branch-context', event, path)
}

const handleCurrentBranchContext = (event) => {
  if (props.currentBranch) {
    emit('branch-context', event, props.currentBranch)
  }
}

const rootSearchQuery = ref('')
const rootExpandedPaths = ref(new Set())
const rootSelectedPath = ref(null)

const rootHandleSelect = (path) => {
  rootSelectedPath.value = path
  emit('select-branch', path)
}

watch(branchFilter, (val) => {
  rootSearchQuery.value = val
})

provide('rootSearchQuery', rootSearchQuery)
provide('rootExpandedPaths', rootExpandedPaths)
provide('rootSelectedPath', rootSelectedPath)
provide('rootHandleSelect', rootHandleSelect)
provide('rootHandleToggle', handleToggle)
provide('rootHandleContextMenu', handleContextMenu)

function handleToggle(branch) {
    console.log('toggle', branch)
}

function handleContextMenu(event, branch) {
    console.log('context menu', branch)
}

defineExpose({
  callExpandAll,
  callCollapseAll,
})
</script>
