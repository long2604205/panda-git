<template>
  <div class="flex flex-col h-full bg-[var(--bg-side)] overflow-hidden">
    <div class="sidebar-section-title flex items-center justify-between">
      <span id="selected-repo-name" class="truncate max-w-[150px] text-[var(--accent-color)]">
        BRANCHES
      </span>
      <div class="flex gap-2">
        <div
          class="cursor-pointer hover:text-[var(--p-text-main)] px-1 rounded hover:bg-[var(--p-hover)] transition-colors"
          :class="{'text-[var(--p-text-main)] bg-[var(--p-hover)]': isMenuOpen}"
          @click.stop="$emit('open-menu', $event)"
        >
          <i class="w-4 fa-solid fa-ellipsis fa-lg hover:text-[var(--text-color)] cursor-pointer items-center text-center" />
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
      <div v-if="currentBranch" class="branch-item active-branch">
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
      />

      <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-2">
        remotes
      </div>
      <git-branch-tree
        ref="treeRemoteRef"
        :branches="filteredBranches.remote"
        :search-query="branchFilter"
        @select="$emit('select-branch', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import GitBranchTree from '@/components/repository-workspace/components/GitBranchTree.vue'

const props = defineProps(['branches', 'currentBranch', 'isMenuOpen'])
defineEmits(['select-branch', 'open-menu'])

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
    local: (props.branches.local || []).filter(b => b.toLowerCase().includes(filter)),
    remote: (props.branches.remote || []).filter(b => b.toLowerCase().includes(filter))
  }
})

defineExpose({
  callExpandAll,
  callCollapseAll
})
</script>
