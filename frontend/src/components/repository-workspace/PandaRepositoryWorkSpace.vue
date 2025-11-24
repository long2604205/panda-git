<template>
  <aside
    ref="sidebarLeft"
    class="w-72 flex-shrink-0 bg-[var(--bg-side)] border-r border-[var(--border-color)] flex flex-col select-none z-10"
  >
    <!-- TOP PANE: REPOSITORIES -->
    <div
      ref="paneRepo"
      class="overflow-hidden flex flex-col"
      :style="{ height: paneHeight + 'px' }"
    >
      <div class="sidebar-section-title border-b border-[var(--border-color)]">
        <span>Repositories</span>
        <div class="flex gap-2">
          <i
            class="fa-solid fa-plus hover:text-[var(--text-color)] cursor-pointer"
            @click="openFormAddGroup"
          />
          <i class="fa-solid fa-ellipsis hover:text-[var(--text-color)] cursor-pointer" />
        </div>
      </div>

      <!-- Repo Search -->
      <div class="px-3 py-2 border-b border-[var(--border-color)] border-opacity-30">
        <div class="relative">
          <i
            class="fa-solid fa-search absolute left-2 top-1/2 transform -translate-y-1/2 text-[10px] text-[var(--p-text-dim)]"
          ></i>
          <input
            type="text"
            v-model="repoFilter"
            class="search-input w-full pl-6 pr-2 py-1 rounded"
            placeholder="Filter repositories..."
          />
        </div>
      </div>

      <div class="flex-1 overflow-y-auto py-1">
        <div v-for="group in filteredReposByGroup.groups" :key="group.id" class="group-item">
          <div
            class="group-header"
            @click="toggleGroup(group)"
            @dragover.prevent
            @drop="onDropRepo(group)"
            @contextmenu.prevent="openMenu($event, group)"
          >
            <i
              class="fa-solid fa-chevron-down arrow"
              :class="{
                '-rotate-90': !isGroupExpanded(group),
                invisible: !group.matchedRepos || group.matchedRepos.length === 0,
              }"
            />
            <i
              class="fa-regular"
              :class="[
                !group.matchedRepos || group.matchedRepos.length === 0
                  ? 'fa-folder'
                  : !isGroupExpanded(group)
                    ? 'fa-folder'
                    : 'fa-folder-open',
                'mr-2 group-icon',
              ]"
              :style="{
                color:
                  !group.matchedRepos || group.matchedRepos.length === 0
                    ? 'var(--p-text-dim)'
                    : !isGroupExpanded(group)
                      ? 'var(--p-text-dim)'
                      : 'var(--accent-color)',
              }"
            />
            <span>{{ group.name }}</span>
          </div>

          <div class="group-content" v-show="isGroupExpanded(group)">
            <div
              v-for="repo in group.matchedRepos"
              :key="repo.id"
              class="repo-item"
              :class="{ active: selectedRepo && selectedRepo.id === repo.id }"
              @dblclick="selectRepo(repo)"
              draggable="true"
              @dragstart="onDragStartRepo(repo)"
            >
              <i class="fa-solid fa-bars-progress mr-2"/>
              <span>{{ repo.name }}</span>
            </div>
          </div>
        </div>

        <!-- Standalone repos -->
        <div class="drop-standalone min-h-10" @dragover.prevent @drop="onDropRepo(null)">
          <div
            v-for="repo in filteredReposByGroup.standalone"
            :key="repo.id"
            class="repo-item mt-1"
            :class="{ active: selectedRepo && selectedRepo.id === repo.id }"
            style="padding-left: 12px"
            @dblclick="selectRepo(repo)"
            draggable="true"
            @dragstart="onDragStartRepo(repo)"
          >
            <i class="fa-solid fa-book mr-2"></i>
            <span>{{ repo.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SPLITTER: LEFT VERTICAL -->
    <div
      ref="resizer"
      class="resizer-left-inner resizer-h h-1 cursor-row-resize bg-transparent"
      @mousedown.prevent="onMouseDown"
    />

    <!-- BOTTOM PANE: BRANCHES -->
    <div
      class="flex-1 flex flex-col border-t border-[var(--border-color)] bg-[var(--bg-side)] overflow-hidden"
    >
      <div class="sidebar-section-title flex items-center justify-between">
        <span id="selected-repo-name" class="truncate max-w-[150px] text-[var(--accent-color)]">
          BRANCHES
        </span>
        <div class="flex gap-2">
          <i class="fa-solid fa-code-branch text-[var(--p-text-dim)]"></i>
          <i class="fa-solid fa-filter hover:text-[var(--text-color)] cursor-pointer"></i>
        </div>
      </div>

      <!-- Branch Search -->
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
        <div class="branch-item active-branch">
          <i class="fa-solid fa-check w-4 text-center mr-1 text-[10px]"/>
          <span class="truncate">{{ currentBranch }}</span>
          <span class="ml-auto text-[9px] border border-[var(--border-color)] px-1 rounded">
            HEAD
          </span>
        </div>
        <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-1">
          Local
        </div>
        <panda-tree-git
          ref="treeRef"
          :branches="filteredBranches.local"
          :search-query="branchFilter"
          @select="onBranchSelect"
        />

        <div class="px-3 py-1 text-[10px] font-bold text-[var(--p-text-dim)] uppercase mt-2">
          remotes
        </div>
        <panda-tree-git
          ref="treeRef"
          :branches="filteredBranches.remote"
          :search-query="branchFilter"
          @select="onBranchSelect"
        />
      </div>
    </div>
  </aside>
  <div
    ref="resizerLeftSidebar"
    class="resizer-left-sidebar resizer-v w-1 cursor-col-resize bg-transparent"
  />
  <draft-context-menu ref="groupContextMenuRef" @action-click="handleAction"/>
</template>

<script setup>
import { computed, defineAsyncComponent, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { showPageInModal } from '@/services/modals.js'
import mitter from '@/plugins/mitter.js'
import { loadGroups, loadRepos, saveGroups, saveRepos, updateGroup } from '@/plugins/PandaDB.js'
import commonApi from '@/services/api/common.js'
import notify from '@/plugins/notify.js'
import PandaTreeGit from '@/components/common/PandaTreeGit.vue'
import DraftContextMenu from "@/components/repository-workspace/DraftContextMenu.vue";
const addGroupForm = defineAsyncComponent(() => import('@/components/common/GroupForm.vue'))

const repoFilter = ref('')
const branchFilter = ref('')

const groups = ref([])

const repositories = ref([])
const currentBranch = computed(() => {
  return selectedRepo.value?.currentBranch ?? ''
})

const selectedRepo = ref(null)

async function toggleGroup(group) {
  group.collapsed = !group.collapsed
  await updateGroup(group.id, { collapsed: group.collapsed })
}

async function selectRepo(repo) {
  try {
    // loading.show(`Fetching repository "${repo.name}"...`)
    const response = await commonApi.open({ repo_path: repo.path })
    const result = response.data
    if (!result) return

    // ---- IMPORTANT FIX ----
    const existing = repositories.value.find((r) => r.path === repo.path)
    result.groupId = existing ? existing.groupId : null

    // set active false for all repos
    repositories.value.forEach((r) => (r.active = false))
    result.active = true
    //Replace/update in list
    const index = repositories.value.findIndex((r) => r.path === repo.path)
    if (index !== -1) repositories.value.splice(index, 1, result)
    else repositories.value.push(result)
    // 3. Set active repo in store
    selectedRepo.value = result
    await saveRepos(repositories.value)
    notify.success(`Activated repository "${repo.name}"`)
  } catch (error) {
    notify.error(`Failed: ${error.message}`)
  } finally {
    // loading.hide()
  }
}

const filteredReposByGroup = computed(() => {
  const filter = repoFilter.value?.toLowerCase() ?? ''

  groups.value.forEach((group) => {
    // thêm thuộc tính matchedRepos trực tiếp vào object gốc
    group.matchedRepos = (repositories.value ?? [])
      .filter((r) => (r?.groupId ?? null) === group.id)
      .filter((r) => r?.name?.toLowerCase().includes(filter))
  })

  const filteredGroups = groups.value.filter((g) => {
    if (!filter) return true
    if (g.matchedRepos?.length > 0) return true
    return g.name?.toLowerCase().includes(filter)
  })

  const standalone = (repositories.value ?? [])
    .filter((r) => (r?.groupId ?? null) === null)
    .filter((r) => r?.name?.toLowerCase().includes(filter))

  return { groups: filteredGroups, standalone }
})

const filteredBranches = computed(() => {
  if (!selectedRepo.value) return { local: [], remote: [] }

  const filter = branchFilter.value?.toLowerCase() ?? ''

  const local = selectedRepo.value.branches.local.filter((b) => b.toLowerCase().includes(filter))

  const remote = selectedRepo.value.branches.remote.filter((b) => b.toLowerCase().includes(filter))

  return { local, remote }
})

const paneRepo = ref(null)
const resizer = ref(null)
const paneHeight = ref(200)

let startY = 0
let startHeight = 0

onMounted(() => {
  const container = paneRepo.value?.parentElement
  if (container) {
    paneHeight.value = container.clientHeight / 2
  }
})

const onMouseMove = (e) => {
  const dy = e.clientY - startY
  paneHeight.value = startHeight + dy
}

const onMouseUp = () => {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
  document.body.classList.remove('resizing-row')
}

const onMouseDown = (e) => {
  startY = e.clientY
  startHeight = paneHeight.value

  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
  document.body.classList.add('resizing-row')
}

onBeforeUnmount(() => {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
})

// Resize ngang
const sidebarLeft = ref(null)
const resizerLeftSidebar = ref(null)
let startX = 0
let startW = 0

const onMouseMoveSidebar = (e) => {
  const dx = e.clientX - startX
  sidebarLeft.value.style.width = `${startW + dx}px`
  if (window.diffEditor) window.diffEditor.layout()
}

const onMouseUpSidebar = () => {
  document.removeEventListener('mousemove', onMouseMoveSidebar)
  document.removeEventListener('mouseup', onMouseUpSidebar)
  document.body.classList.remove('resizing-col')
}

const onMouseDownSidebar = (e) => {
  startX = e.clientX
  startW = sidebarLeft.value.getBoundingClientRect().width
  document.addEventListener('mousemove', onMouseMoveSidebar)
  document.addEventListener('mouseup', onMouseUpSidebar)
  document.body.classList.add('resizing-col')
}

onMounted(() => {
  if (resizerLeftSidebar.value && sidebarLeft.value) {
    resizerLeftSidebar.value.addEventListener('mousedown', onMouseDownSidebar)
  }
})

onBeforeUnmount(() => {
  if (resizerLeftSidebar.value) {
    resizerLeftSidebar.value.removeEventListener('mousedown', onMouseDownSidebar)
  }
})

function openFormAddGroup() {
  showPageInModal(addGroupForm, {}, { width: '15%' })
}

onMounted(() => {
  mitter.on('add-group', (newGroup) => {
    groups.value.push(newGroup)
    saveGroups(groups.value)
  })

  mitter.on('open-repository', (repo) => {
    const newRepo = reactive({
      groupId: null,
      ...repo,
    })
    repositories.value.push(newRepo)

    saveRepos(repositories.value)

    selectRepo(newRepo)
  })
})

onBeforeUnmount(() => {
  mitter.off('add-group')
  mitter.off('open-repository')
})

const draggingRepo = ref(null)

function onDragStartRepo(repo) {
  draggingRepo.value = repo
}

async function onDropRepo(group) {
  if (!draggingRepo.value) return
  draggingRepo.value.groupId = group ? group.id : null
  await saveRepos(repositories.value)
  draggingRepo.value = null
}

onMounted(async () => {
  groups.value = await loadGroups()
  repositories.value = await loadRepos()

  const activeRepo = repositories.value.find((r) => r.active)
  await selectRepo(activeRepo)
})

function isGroupExpanded(group) {
  const isSearching = repoFilter.value && repoFilter.value.trim() !== ''
  const hasMatches = group.matchedRepos && group.matchedRepos.length > 0

  if (isSearching && hasMatches) {
    return true
  }
  return !group.collapsed
}

const onBranchSelect = (path) => {
  console.log('Selected Branch:', path);
};

const groupContextMenuRef = ref(null);
const handleAction = ({ action, data }) => {
  console.log('Action:', action, 'Data:', data);
};

function openMenu(event, group) {
  groupContextMenuRef.value.open(event, group);
}
</script>

<style scoped></style>
