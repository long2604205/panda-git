<template>
  <aside
    ref="sidebarEl"
    class="flex-shrink-0 bg-[var(--bg-side)] border-r border-[var(--border-color)] flex flex-col select-none z-10"
    :style="{ width: sidebarWidth + 'px' }"
  >
    <div :style="{ height: paneHeight + 'px' }" class="overflow-hidden flex flex-col">
      <side-bar-repositories
        :groups="groups"
        :repositories="repositories"
        :selected-repo-id="selectedRepo?.id"
        :is-menu-open="isMenuOpen && activeMenuType === 'main'"
        @select-repo="selectRepo"
        @toggle-group="toggleGroup"
        @drag-start="onDragStartRepo"
        @drop-repo="onDropRepo"
        @group-context="openGroupMenu"
        @repo-context="openRepositoryMenu"
        @open-menu="(e) => toggleMenu(e, 'main')"
      />
    </div>

    <div
      class="resizer-left-inner resizer-h h-1 cursor-row-resize bg-transparent"
      @mousedown.prevent="startRowResize"
    />

    <div
      class="flex-1 flex flex-col border-t border-[var(--border-color)] bg-[var(--bg-side)] overflow-hidden"
    >
      <side-bar-branches
        ref="sidebarBranchesRef"
        :current-branch="currentBranch"
        :branches="selectedRepo?.branches"
        :is-menu-open="isMenuOpen && activeMenuType === 'branch'"
        @select-branch="onBranchSelect"
        @open-menu="(e) => toggleMenu(e, 'branch')"
        @branch-context="openBranchMenu"
      />
    </div>
  </aside>

  <div
    class="resizer-left-sidebar resizer-v w-1 cursor-col-resize bg-transparent"
    @mousedown.prevent="startColResize"
  />

  <group-context-menu ref="groupContextMenuRef" @action-click="handleGroupAction" />
  <repository-context-menu ref="repositoryContextMenuRef" @action-click="handleRepositoryAction" />
  <branch-context-menu ref="branchContextMenuRef" @action-click="handleBranchAction" />

  <teleport-menu
    :is-open="isMenuOpen"
    :menu-style="menuStyle"
    :actions="activeMenuActions"
    @action="handleMenuAction"
  />

  <teleport-menu
    :is-open="isMenuOpen"
    :menu-style="menuStyle"
    :actions="activeMenuActions"
    @action="handleMenuAction"
  />
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import mitter from '@/plugins/mitter.js'
import {
  deleteGroup,
  loadGroups,
  loadRepos,
  saveGroups,
  saveRepos,
  updateGroup
} from '@/plugins/PandaDB.js'
import commonApi from '@/services/api/common.js'

// Import Components đã tách
import GroupContextMenu from '@/components/repository-workspace/components/GroupContextMenu.vue'
import RepositoryContextMenu from '@/components/repository-workspace/components/RepositoryContextMenu.vue'
import TeleportMenu from '@/components/common/TeleportMenu.vue'
import { useSideBarResize } from '@/composables/use-side-bar-resize.js'
import SideBarBranches from '@/components/repository-workspace/components/SideBarBranches.vue'
import SideBarRepositories from '@/components/repository-workspace/components/SideBarRepositories.vue'
import {
  addGroup,
  createBranch,
  openRepository,
  renameGroup,
  renameRepository
} from '@/composables/repositories-manager.js'
import notify from '@/plugins/notify.js'
import {useRepositoryStore} from "@/stores/repositoryStore.js";
import BranchContextMenu from '@/components/repository-workspace/components/BranchContextMenu.vue'

// --- 1. RESIZE LOGIC (Từ Composable) ---
const { paneHeight, sidebarWidth, startRowResize, startColResize } = useSideBarResize()

// --- 2. DATA STATE ---
const groups = ref([])
const repositories = ref([])
const selectedRepo = ref(null)
const draggingRepo = ref(null)
const currentBranch = computed(() => selectedRepo.value?.currentBranch ?? '')
const sidebarBranchesRef = ref(null)
const repositoriesStore = useRepositoryStore()

// --- 3. REPOSITORY ACTIONS ---
async function selectRepo(repo) {
  // const loadingId = notify.loading('Đang tải dữ liệu...')
  try {
    const response = await commonApi.open({ repo_path: repo.path })
    const result = response.data
    if (!result) return

    // Logic giữ GroupId
    const existing = repositories.value.find((r) => r.path === repo.path)
    result.groupId = existing ? existing.groupId : (repo.groupId || null)

    // Update active
    repositories.value.forEach((r) => (r.active = false))
    result.active = true

    // Update List
    const index = repositories.value.findIndex((r) => r.path === repo.path)
    if (index !== -1) repositories.value.splice(index, 1, result)
    else repositories.value.push(result)

    selectedRepo.value = result
    repositoriesStore.setActiveRepo(result)
    await saveRepos(repositories.value)
    return { success: true, data: result }
    // notify.remove(loadingId)
    // notify.info('Active successfully')
  } catch (error) {
    return { success: false, error }
    // notify.remove(loadingId)
    // notify.error(`Failed: ${error.message}`)
  }
}

async function toggleGroup(groupReceived) {
  const targetGroup = groups.value.find(g => g.id === groupReceived.id)
  if (targetGroup) {
    targetGroup.collapsed = !targetGroup.collapsed
    await updateGroup(targetGroup.id, { collapsed: targetGroup.collapsed })
  }
}

// Drag & Drop
function onDragStartRepo(repo) { draggingRepo.value = repo }

async function onDropRepo(group) {
  if (!draggingRepo.value) return
  draggingRepo.value.groupId = group ? group.id : null
  await saveRepos(repositories.value)
  draggingRepo.value = null
}

// --- 4. BRANCH ACTIONS ---
const onBranchSelect = (path) => {
  console.log('Selected Branch:', path);
  // Logic checkout branch...
};

// --- 5. MENUS (Context & Teleport) ---
const groupContextMenuRef = ref(null)
const repositoryContextMenuRef = ref(null)
const branchContextMenuRef = ref(null)
const isMenuOpen = ref(false)
const menuStyle = ref({ top: '0px', left: '0px' })
const activeMenuType = ref('main')
const sidebarEl = ref(null)

const menuActionsMain = [
  {
    value: 'add-repository',
    label: 'Add Repository...',
    icon: 'fa-solid fa-plus',
  },
  {
    value: 'add-group',
    label: 'Add Group...',
    icon: 'fa-solid fa-folder-plus',
  },
  {
    type: 'separator'
  },
  {
    value: 'expand-all',
    label: 'Expand All',
    icon: 'fa-solid fa-up-right-and-down-left-from-center',
  },
  {
    value: 'collapse-all',
    label: 'Collapse All',
    icon: 'fa-solid fa-down-left-and-up-right-to-center',
  }
]

const menuActionsBranch = [
  {
    value: 'add-branch',
    label: 'Add new branch...',
    icon: 'fa-solid fa-plus',
  },
  {
    type: 'separator'
  },
  {
    value: 'expand-all',
    label: 'Expand All',
    icon: 'fa-solid fa-up-right-and-down-left-from-center',
  },
  {
    value: 'collapse-all',
    label: 'Collapse All',
    icon: 'fa-solid fa-down-left-and-up-right-to-center',
  }
]

const activeMenuActions = computed(() => {
    return activeMenuType.value === 'branch' ? menuActionsBranch : menuActionsMain
})

function openGroupMenu(event, group) {
  closeAllMenus()
  groupContextMenuRef.value.open(event, group)
}
function openRepositoryMenu(event, repo) {
  closeAllMenus()
  repositoryContextMenuRef.value.open(event, repo)
}
function openBranchMenu(event, branch) {
  closeAllMenus()
  branchContextMenuRef.value.open(event, branch)
}
function toggleMenu(event, type) {
    const isThisMenuOpen = isMenuOpen.value && activeMenuType.value === type;
    closeAllMenus();
    if (!isThisMenuOpen) {
        activeMenuType.value = type
        const rect = event.currentTarget.getBoundingClientRect()
        menuStyle.value = {
            top: `${rect.top}px`,
            left: `${rect.right + 1}px`
        }
        isMenuOpen.value = true;
    }
}
function closeAllMenus() {
  isMenuOpen.value = false
  groupContextMenuRef.value?.close?.()
  repositoryContextMenuRef.value?.close?.()
  branchContextMenuRef.value?.close?.()
}
const handleGlobalClick = () => closeAllMenus()
const handleGroupAction = ({ action, data }) => {
  switch (action) {
      case 'add-group':
        addGroup()
        break
      case 'rename-group':
        renameGroup(data.id)
        break
      case 'delete-group':
        handleDeleteGroup(data.id)
        break
  }
}
const handleRepositoryAction = ({ action, data }) => {
  let context
  if (action.includes('move-repository')) {
    context = splitMoveToGroup(action)
    action = context.action
  }
  switch (action) {
    case 'open-repository':
      handleActiveRepository(data)
      break
    case 'open-in-terminal':
      window.electronAPI.openTerminal(data.path)
      break
    case 'open-in-explorer':
      window.electronAPI.openInExplorer(data.path)
      break
    case 'copy-path':
      navigator.clipboard.writeText(data.path)
      break
    case 'move-repository':
      changeRepoGroup(data, context)
      break
    case 'move-into-no-group':
      changeRepoGroup(data)
      break
    case 'rename-repository':
      renameRepository(data)
      break
    case 'delete-repository':
      handleDeleteRepository(data.path)
      break
    case 'refresh-repository':
      handleRefreshRepository(data)
      break
    case 'git-fetch':
      handleFetchRepository(data)
      break
    case 'git-pull':
      handlePullRepository(data)
      break
  }
}

async function handleRefreshRepository(repo) {
  const loadingId = notify.loading("Refreshing...")
  const res = await selectRepo(repo)

  notify.remove(loadingId)

  if (res.success) notify.success("Refresh successfully")
  else notify.error("Refresh failed: " + res.error)
}

async function handlePullRepository(repo) {
  const loadingId = notify.loading("Pulling...")
  try {
    const data = { repo_path: repo.path }
    await commonApi.pull(data)

    notify.remove(loadingId)
    notify.info('All files are up to date')
  } catch (error) {
    notify.remove(loadingId)
    notify.error(`Pull failed: ${error.message}`)
    console.error(error)
  }
}

async function handleFetchRepository(repo) {
  const loadingId = notify.loading("Fetching...")
  try {
    const data = { repo_path: repo.path }
    await commonApi.fetch(data)
    await selectRepo(repo)
    notify.remove(loadingId)
    notify.success("Fetch successfully")
  } catch (error) {
    notify.remove(loadingId)
    notify.error(`Fetch failed: ${error.message}`)
    console.error(error)
  }
}

async function handleOpenRepository(repo) {
  const loadingId = notify.loading("Opening...")
  const res = await selectRepo(repo)

  notify.remove(loadingId)
  if (res.success) notify.success("Open successfully")
  else notify.error("Open failed: " + res.error)
}


async function handleDeleteRepository(repoPath) {
  const index = repositories.value.findIndex(r => r.path === repoPath);
  if (index !== -1) {
    repositories.value.splice(index, 1);
    await saveRepos(repositories.value);
  }
}

async function changeRepoGroup(data, context = { group_id: null }) {
  const index = repositories.value.findIndex(r => r.path === data.path);
  repositories.value[index] = {
    ...repositories.value[index],
    groupId: context.group_id
  };
  await saveRepos(repositories.value);
}

const handleMenuAction = (action) => {
    closeAllMenus()
    if (activeMenuType.value === 'branch') {
      switch (action) {
        case 'add-branch':
          createBranch()
          break
        case 'expand-all':
          sidebarBranchesRef.value?.callExpandAll()
          break
        case 'collapse-all':
          sidebarBranchesRef.value?.callCollapseAll()
          break
        }
    }
    else {
      switch (action) {
        case 'add-repository':
          openRepository()
          break
        case 'add-group':
          addGroup()
          break
        case 'expand-all':
          groups.value.forEach(g => g.collapsed = false)
          saveGroups(groups.value)
          break
        case 'collapse-all':
          groups.value.forEach(g => g.collapsed = true)
          saveGroups(groups.value)
          break
      }
    }
}

const handleBranchAction = ({ action, data }) => {
  console.log(action, data)
}

async function handleDeleteGroup(groupId) {
  const { groups: newGroups, repos: newRepos } = await deleteGroup(groupId);
  groups.value = newGroups;
  repositories.value = newRepos;
}

function splitMoveToGroup(str) {
  const SEP = "-group-";
  const idx = str.indexOf(SEP);

  if (idx === -1) {
    return { action: str, group_id: null };
  }

  return {
    action: str.slice(0, idx),
    group_id: str.slice(idx + 1)
  };
}

async function handleActiveRepository(repo) {
  const loadingId = notify.loading("Active...")
  const res = await selectRepo(repo)

  notify.remove(loadingId)
  if (res.success) notify.success("Active successfully")
  else notify.error("Active failed: " + res.error)
}

// --- 6. LIFECYCLE ---
onMounted(async () => {
  if (sidebarEl.value) {
    const totalHeight = sidebarEl.value.clientHeight
    if (totalHeight > 0) {
      paneHeight.value = totalHeight / 2
    }
  }

  groups.value = await loadGroups()
  repositories.value = await loadRepos()
  const activeRepo = repositories.value.find((r) => r.active)
  if(activeRepo) await handleOpenRepository(activeRepo)

  mitter.on('add-group', (g) => { groups.value.push(g); saveGroups(groups.value) })
  mitter.on('rename-group', (g) => {
    const index = groups.value.findIndex((group) => group.id === g.id)
    if (index !== -1) {
      groups.value[index] = g
    }
  })
  mitter.on('open-repository', (r) => {
      const newRepo = reactive({ groupId: null, ...r })
      handleOpenRepository(newRepo)
  })

  mitter.on('repository-renamed', (r) => {
    const index = repositories.value.findIndex((repo) => repo.path === r.oldPath)
    if (index !== -1) {
      repositories.value[index] = {
        ...repositories.value[index],
        path: r.path,
        name: r.name
      }
    }
    saveRepos(repositories.value)
  })
  window.addEventListener('click', handleGlobalClick)
})

onBeforeUnmount(() => {
  mitter.off('add-group')
  mitter.off('open-repository')
  mitter.off('repository-renamed')
  window.removeEventListener('click', handleGlobalClick)
})
</script>
