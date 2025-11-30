<template>
  <aside
    ref="sidebarEl"
    class="flex-shrink-0 bg-[var(--bg-side)] border-r border-[var(--border-color)] flex flex-col select-none z-10"
    :style="{ width: sidebarWidth + 'px' }"
  >
    <div :style="{ height: paneHeight + 'px' }" class="overflow-hidden flex flex-col">
      <SidebarRepositories
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
      <SidebarBranches
        ref="sidebarBranchesRef"
        :current-branch="currentBranch"
        :branches="selectedRepo?.branches"
        :is-menu-open="isMenuOpen && activeMenuType === 'branch'"
        @select-branch="onBranchSelect"
        @open-menu="(e) => toggleMenu(e, 'branch')"
      />
    </div>
  </aside>

  <div
    class="resizer-left-sidebar resizer-v w-1 cursor-col-resize bg-transparent"
    @mousedown.prevent="startColResize"
  />

  <group-context-menu ref="groupContextMenuRef" @action-click="handleGroupAction" />
  <repository-context-menu ref="repositoryContextMenuRef" @action-click="handleRepositoryAction" />

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
import { loadGroups, loadRepos, saveGroups, saveRepos, updateGroup } from '@/plugins/PandaDB.js'
import commonApi from '@/services/api/common.js'
import notify from '@/plugins/notify.js'

// Import Components đã tách
import GroupContextMenu from '@/components/repository-workspace/components/GroupContextMenu.vue'
import RepositoryContextMenu from '@/components/repository-workspace/components/RepositoryContextMenu.vue'
import TeleportMenu from '@/components/common/TeleportMenu.vue'
import { useSidebarResize } from '@/composables/useSidebarResize.js'
import SidebarBranches from '@/components/repository-workspace/components/SidebarBranches.vue'
import SidebarRepositories from '@/components/repository-workspace/components/SidebarRepositories.vue'
import { addGroup, openRepository } from '@/composables/repositories-manager.js'

// --- 1. RESIZE LOGIC (Từ Composable) ---
const { paneHeight, sidebarWidth, startRowResize, startColResize } = useSidebarResize()

// --- 2. DATA STATE ---
const groups = ref([])
const repositories = ref([])
const selectedRepo = ref(null)
const draggingRepo = ref(null)
const currentBranch = computed(() => selectedRepo.value?.currentBranch ?? '')
const sidebarBranchesRef = ref(null)

// --- 3. REPOSITORY ACTIONS ---
async function selectRepo(repo) {
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
    await saveRepos(repositories.value)
  } catch (error) {
    notify.error(`Failed: ${error.message}`)
  }
}

async function toggleGroup(groupReceived) {
  // 1. Tìm object GỐC trong danh sách groups (nguồn sự thật - source of truth)
  const targetGroup = groups.value.find(g => g.id === groupReceived.id)

  if (targetGroup) {
    // 2. Cập nhật trên object GỐC.
    // Việc này sẽ kích hoạt Vue Reactivity -> Props truyền xuống con sẽ thay đổi -> UI cập nhật.
    targetGroup.collapsed = !targetGroup.collapsed

    // 3. Gọi API lưu lại
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
const isMenuOpen = ref(false)
const menuStyle = ref({ top: '0px', left: '0px' })
const activeMenuType = ref('main')

// Define Actions cho từng loại Menu
const menuActionsMain = [
  {
    value: 'add_repository',
    label: 'Add Repository...',
    icon: 'fa-solid fa-plus',
    shortcut: 'Alt+A'
  },
  {
    value: 'add_group',
    label: 'Add Group...',
    icon: 'fa-regular fa-folder',
    shortcut: 'Alt+G'
  },
  {
    type: 'separator'
  },
  {
    value: 'expand_all',
    label: 'Expand All',
    icon: 'fa-solid fa-up-right-and-down-left-from-center',
    shortcut: 'Shift+E'
  },
  {
    value: 'collapse_all',
    label: 'Collapse All',
    icon: 'fa-solid fa-down-left-and-up-right-to-center',
    shortcut: 'Shift+C'
  }
]

const menuActionsBranch = [
  {
    value: 'add_branch',
    label: 'Add new branch...',
    icon: 'fa-solid fa-plus',
    shortcut: 'Alt+A'
  },
  {
    type: 'separator'
  },
  {
    value: 'expand_all',
    label: 'Expand All',
    icon: 'fa-solid fa-up-right-and-down-left-from-center',
    shortcut: 'Shift+E'
  },
  {
    value: 'collapse_all',
    label: 'Collapse All',
    icon: 'fa-solid fa-down-left-and-up-right-to-center',
    shortcut: 'Shift+C'
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
function toggleMenu(event, type) {
    // 1. Kiểm tra xem ĐÚNG cái menu này có đang mở không
    // Phải khớp cả trạng thái mở lẫn loại menu (main hay branch)
    const isThisMenuOpen = isMenuOpen.value && activeMenuType.value === type;

    // 2. Đóng tất cả menu trước (để reset trạng thái)
    closeAllMenus();

    // 3. Nếu menu này CHƯA mở thì mới mở nó ra
    // (Nếu nó đang mở rồi thì bước 2 đã đóng nó lại -> hành vi toggle)
    if (!isThisMenuOpen) {
        activeMenuType.value = type; // Set type mới (main hoặc branch)

        // Tính toán vị trí
        const rect = event.currentTarget.getBoundingClientRect();
        menuStyle.value = {
            top: `${rect.top}px`,
            left: `${rect.right + 1}px`
        };

        // Mở menu
        isMenuOpen.value = true;
    }
}
function closeAllMenus() {
  isMenuOpen.value = false
  groupContextMenuRef.value?.close?.()
  repositoryContextMenuRef.value?.close?.()
}
const handleGlobalClick = () => closeAllMenus()
const handleGroupAction = ({ action, data }) => console.log(action, data)
const handleRepositoryAction = ({ action, data }) => console.log(action, data)
const handleMenuAction = (action) => {
    // 1. Đóng menu
    closeAllMenus()

    // 2. Phân loại xử lý dựa trên loại menu đang mở
    if (activeMenuType.value === 'branch') {
        // --- LOGIC CHO BRANCH ---
        if (action === 'expand_all') {
            sidebarBranchesRef.value?.callExpandAll()
        } else if (action === 'collapse_all') {
            sidebarBranchesRef.value?.callCollapseAll()
        }
        else if (action === 'add_repo') {
            // Logic add repo (nếu dùng chung)
             console.log('Add repo clicked from branch menu')
        }
    }
    else {
      switch (action) {
        case 'add_repository':
          openRepository()
          break
        case 'add_group':
          addGroup()
          break
        case 'expand_all':
          groups.value.forEach(g => g.collapsed = false)
          saveGroups(groups.value)
          break
        case 'collapse_all':
          groups.value.forEach(g => g.collapsed = true)
          saveGroups(groups.value)
          break
      }
    }
}

const sidebarEl = ref(null)
// --- 6. LIFECYCLE ---
onMounted(async () => {
  // --- FIX LỖI HEIGHT 50-50 Ở ĐÂY ---
  if (sidebarEl.value) {
    // Lấy chiều cao tổng của sidebar hiện tại
    const totalHeight = sidebarEl.value.clientHeight
    // Set chiều cao paneRepo bằng 50%
    if (totalHeight > 0) {
      paneHeight.value = totalHeight / 2
    }
  }

  groups.value = await loadGroups()
  repositories.value = await loadRepos()
  const activeRepo = repositories.value.find((r) => r.active)
  if(activeRepo) await selectRepo(activeRepo)

  mitter.on('add-group', (g) => { groups.value.push(g); saveGroups(groups.value) })
  mitter.on('open-repository', (r) => {
      const newRepo = reactive({ groupId: null, ...r })
      repositories.value.push(newRepo)
      saveRepos(repositories.value)
      selectRepo(newRepo)
  })
  window.addEventListener('click', handleGlobalClick)
})

onBeforeUnmount(() => {
  mitter.off('add-group')
  mitter.off('open-repository')
  window.removeEventListener('click', handleGlobalClick)
})
</script>
