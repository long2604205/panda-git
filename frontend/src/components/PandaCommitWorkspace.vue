<template>
  <!-- SPLITTER: MAIN RIGHT -->
  <div
    ref="resizerRightSidebar"
    class="resizer-right-sidebar resizer-v bg-transparent -mr-[2px]"
  ></div>

  <!-- RIGHT SIDEBAR -->
  <aside
    ref="sidebarRight"
    style="width: 300px"
    class="flex-shrink-0 bg-[var(--bg-side)] border-l border-[var(--border-color)] flex flex-col select-none z-10"
  >
    <!-- Header -->
    <div class="sidebar-section-title border-b border-[var(--border-color)]">
      <span>Commit Workspace</span>
      <div class="flex gap-2">
        <i class="fa-regular fa-copy hover:text-[var(--text-color)] cursor-pointer"></i>
      </div>
    </div>
    <!-- TAB HEADER -->
    <div
      class="h-9 flex items-center border-b border-[var(--border-color)] bg-[var(--bg-header)] select-none flex-shrink-0"
    >
      <button
        :class="['panel-tab-btn', { active: activeTab === 'details' }]"
        @click="switchTab('details')"
      >
        Commit Details
      </button>
      <div class="w-[1px] h-8 bg-[var(--border-color)]"/>
      <button
        :class="['panel-tab-btn', { active: activeTab === 'changes' }]"
        @click="switchTab('changes')"
      >
        <span>Changes</span>
        <span
          class="px-1.5 py-0.5 rounded bg-[var(--p-highlight)] text-[var(--bg-main)] text-[9px] ml-2"
        >
          {{ totalChanges }}
        </span>
      </button>
    </div>

    <!--=======CONTENT========-->
    <div class="flex-1 overflow-hidden relative flex flex-col">
      <panda-commit-detail-workspace v-show="activeTab === 'details'"/>
      <panda-commit-form v-if="activeTab === 'changes'"/>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import PandaCommitDetailWorkspace from '@/components/PandaCommitDetailWorkspace.vue'
import PandaCommitForm from '@/components/PandaCommitForm.vue'

onMounted(() => {
  initRightSidebarResize()
})

// refs cho DOM element
const resizerRightSidebar = ref(null)
const sidebarRight = ref(null)

// ---- RIGHT SIDEBAR WIDTH (kéo ngang) ----
function initRightSidebarResize() {
  const resizer = resizerRightSidebar.value
  const pane = sidebarRight.value

  if (!resizer || !pane) return

  let startX, startW

  resizer.addEventListener('mousedown', (e) => {
    startX = e.clientX
    startW = pane.getBoundingClientRect().width

    const mm = (e) => {
      pane.style.width = `${startW - (e.clientX - startX)}px`
    }

    const mu = () => {
      document.removeEventListener('mousemove', mm)
      document.removeEventListener('mouseup', mu)
    }

    document.addEventListener('mousemove', mm)
    document.addEventListener('mouseup', mu)
  })
}

// =================TAB LOGIC=============

const activeTab = ref('details')
const switchTab = (tab) => {
  activeTab.value = tab
}
const totalChanges = computed(() => {
  return 10
})
</script>

<style scoped>
.panel-tab-btn {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--p-text-dim);
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.panel-tab-btn:hover {
  color: var(--text-color);
  background-color: rgba(255, 255, 255, 0.02);
}

.panel-tab-btn.active {
  color: var(--accent-color);
  border-bottom-color: var(--accent-color);
  background-color: var(--p-selection);
}
</style>
