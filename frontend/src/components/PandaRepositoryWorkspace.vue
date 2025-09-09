<template>
  <div class="horizontal-resize-wrapper" :style="{ width: containerWidth + 'px' }">
    <div class="workspace-container" :class="{ collapsed: isWorkspaceCollapsed }">
      <div class="workspace-panel workspace-split">
        <div class="repositories-workspace" :style="{ height: reposHeight + 'px' }">
          <!-- Header -->
          <div class="workspace-header">
            <h6 class="mb-0">Repositories</h6>
            <div class="workspace-toggle">
              <button
                class="btn btn-sm workspace-action"
                v-if="showActions"
                @click="openRepository"
              >
                <i class="fa-solid fa-plus"></i>
              </button>
              <button
                class="btn btn-sm workspace-action search"
                v-if="showActions"
                @click="showSearchRepository = !showSearchRepository"
              >
                <i class="fa-solid fa-magnifying-glass"></i>
              </button>
              <button
                class="btn btn-sm workspace-action"
                v-if="showActions"
              >
                <i class="fa-solid fa-ellipsis-vertical"></i>
              </button>
              <button class="btn btn-sm workspace-action" @click="toggleWorkspacePanel">
                <i :class="['fas', isWorkspaceCollapsed ? 'fa-solid fa-layer-group' : 'fa-solid fa-minus']"></i>
              </button>
            </div>
          </div>
          <transition name="fade-search">
            <div class="search-workspace" v-if="showSearchRepository">
              <div class="symbol-search">
                <i class="fa-solid fa-magnifying-glass"></i>
              </div>
              <input
                ref="repositorySearchInput"
                class="search-branch"
                placeholder="search repository"
                v-model="repositoryKeyword"
              />
            </div>
          </transition>

          <!-- repository list -->
          <div class="workspace-content">
            <div class="workspace-repos">
              <template v-if="repositories.length === 0">
                <div class="no-repos-message text-center py-4">
                  <i class="fas fa-folder-open fa-2x mb-2"></i>
                  <p>No repositories open</p>
                  <small>Open repositories to manage them here</small>
                </div>
              </template>

              <template v-else>
                <div
                  v-for="repo in filteredRepositories"
                  :key="repo.id"
                  class="repo-item"
                  :class="{ active: activeRepository && activeRepository.id === repo.id }"
                  @click="setActiveRepository(repo)"
                >
                  <div class="repo-icon">
                    <i class="fas fa-folder text-warning"></i>
                  </div>
                  <div class="repo-info">
                    <div class="repo-name">{{ repo.name }}</div>
                    <div class="repo-path">{{ repo.path }}</div>
                  </div>
                  <div class="repo-status">
                    <i
                      class="fas"
                      :class="[getStatusIcon(repo.status), getStatusColor(repo.status)]"
                      :title="repo.status"
                    ></i>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <div class="resizer" @mousedown="startResizing"></div>

        <div class="branch-workspace" :style="{ height: 'calc(100% - ' + reposHeight + 'px - 5px)' }">
          <div class="branch-workspace-header">
            <h6 class="mb-0">Branches</h6>
            <div class="workspace-toggle">
              <button
                class="btn btn-sm workspace-action"
                v-if="showActions"
              >
                <i class="fa-solid fa-plus"></i>
              </button>
              <button
                class="btn btn-sm workspace-action search"
                v-if="showActions"
                @click="showSearchBranch = !showSearchBranch"
              >
                <i class="fa-solid fa-magnifying-glass"></i>
              </button>
              <button
                class="btn btn-sm workspace-action"
                v-if="showActions"
              >
                <i class="fa-solid fa-ellipsis-vertical"></i>
              </button>
            </div>
          </div>
          <transition name="fade-search">
            <div class="search-workspace" v-if="showSearchBranch">
              <div class="symbol-search">
                <i class="fa-solid fa-magnifying-glass"></i>
              </div>
              <input
                ref="branchSearchInput"
                class="search-branch"
                placeholder="search branch"
                v-model="branchKeyword"
              />
            </div>
          </transition>
          <div class="workspace-content branch-tree-scroll">
            <div class="branch-tree" id="branch-tree">
              <div v-if="!activeRepository" class="no-repo-message text-center py-4">
                <i class="fas fa-code-branch fa-2x mb-2"></i>
                <p>No repository selected</p>
                <small>Open a repository to view branches</small>
              </div>

              <template v-else>
                <!-- HEAD -->
                <div class="tree-item tree-header">
                  <i class="fas fa-laptop text-info me-1"></i>
                  <span>HEAD (Current Branch)</span>
                </div>
                <div class="tree-item nested active">
                  <i class="fas fa-star text-warning me-1"></i>
                  <span>{{ activeRepository.currentBranch }}</span>
                </div>

                <!-- Local -->
                <div class="tree-item tree-header"
                     @click="toggle('local')">
                  <i
                    class="fas fa-chevron-down tree-toggle"
                    :class="{ collapsed: collapsedTree.local }"
                  />
                  <i class="fas fa-folder text-warning me-1"></i>
                  <span>Local</span>
                </div>
                <template v-if="!collapsedTree.local || branchKeyword">
                  <div
                    class="tree-item nested"
                    v-for="branch in filteredLocalBranches"
                    :key="'local-' + branch.raw"
                    :class="{ active: branch.raw === activeRepository.currentBranch }"
                    @contextmenu="openContextMenuLocal($event, branch)"
                  >
                    <i class="fas fa-code-branch text-success me-1"></i>
                    <span v-html="branch.highlighted"></span>
                  </div>
                </template>

                <div class="tree-item tree-header"
                     @click="toggle('remote')">
                  <i
                    class="fas fa-chevron-down tree-toggle"
                    :class="{ collapsed: collapsedTree.remote }"
                  />
                  <i class="fas fa-cloud text-primary me-1"></i>
                  <span>Remote</span>
                </div>
                <template v-if="!collapsedTree.remote || branchKeyword">
                  <div
                    class="tree-item nested"
                    v-for="branch in filteredRemoteBranches"
                    :key="'remote-' + branch.raw"
                    @contextmenu="contextMenu?.open($event, branch.raw)"
                  >
                    <i class="fas fa-server text-primary me-1"></i>
                    <span v-html="branch.highlighted"></span>
                  </div>
                </template>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="resizer-horizontal" @mousedown="startResizeContainer" v-if="!isWorkspaceCollapsed"></div>
  </div>
  <!--  Modal-->
  <panda-open-repository-form ref="openModal"/>
  <branch-context-menu ref="contextMenu" @action="handleContextAction"/>
</template>
<script setup>
// Props
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import PandaOpenRepositoryForm from '@/components/modals/PandaOpenRepositoryForm.vue'
import BranchContextMenu from '@/components/modals/BranchContextMenu.vue'
import mitter from '@/plugins/mitter.js'
import api from '@/plugins/api.js'
import { useLoadingStore } from '@/stores/loadingStore.js'

/*----Data----*/
const showActions = ref(true);
const showSearchRepository = ref(false);
const showSearchBranch = ref(false);
const reposHeight = ref(0);
const containerHeight = ref(0);
const containerWidth = ref(300);
const previousWidth = ref(300)
let isResizing = false;
let isResizingContainer = false;
const openModal = ref(null);
const contextMenu = ref(null)
const branchKeyword = ref('')
const repositoryKeyword = ref('')
const collapsedTree = ref({
  local: false,
  remote: false
})
const isWorkspaceCollapsed = ref(false)
const branchSearchInput = ref(null)
const repositorySearchInput = ref(null)
const activeRepository = ref(null)
const repositories = ref([
  {
    id: 'repo1',
    name: 'Core API',
    path: 'C:/Users/zhilo/OneDrive/Documents/Project/Training/auto_verse',
    status: 'clean',
    currentBranch: 'main',
    branches: {
      local: ['main', 'dev', 'release/v1.0', 'feature/auth-module', 'bugfix/token-refresh', 'hotfix/login-timeout'],
      remote: ['origin/main', 'origin/dev', 'origin/release/v1.0', 'origin/feature/auth-module']
    },
    changes: [
      {
        id: 1,
        name: 'base.css',
        path: 'src\\assets',
        type: 'css'
      },
      {
        id: 2,
        name: 'PandaDefaultContent.vue',
        path: 'src\\components',
        type: 'vue'
      }
    ]
  },
  {
    id: 'repo2',
    name: 'Admin Dashboard',
    path: '/projects/admin-dashboard',
    status: 'dirty',
    currentBranch: 'dev',
    branches: {
      local: ['main', 'dev', 'feature/user-management', 'feature/role-settings', 'bugfix/sidebar-collapse', 'refactor/table-component'],
      remote: ['origin/main', 'origin/dev', 'origin/feature/user-management']
    },
    changes: [
      {
        id: 1,
        name: 'main.css',
        path: 'src\\assets',
        type: 'css',
        selected: false
      },
      {
        id: 2,
        name: 'UserController.php',
        path: 'src\\components',
        type: 'vue',
        selected: false
      }
    ]
  }
])
const loading = useLoadingStore()
/*----Mounted----*/
onMounted(() => {
  const container = document.querySelector('.workspace-split')
  if (container) {
    containerHeight.value = container.clientHeight;
    reposHeight.value = containerHeight.value / 2
  }

  if (repositories.value.length > 0 && !activeRepository.value) {
    setActiveRepository(repositories.value[0])
  }

  mitter.on('open-repository', (repo) => {
    repositories.value.push(repo);
    activeRepository.value = repo;
  })
});

onBeforeUnmount(() => {
  mitter.off('open-repository')
})

/*----Computed----*/
const filteredLocalBranches = computed(() => {
  if (!activeRepository.value) return []
  return activeRepository.value.branches.local
    .filter(b => b.toLowerCase().includes(branchKeyword.value.toLowerCase()))
    .map(b => ({
      raw: b,
      highlighted: highlightMatch(b, branchKeyword.value)
    }))
})

const filteredRemoteBranches = computed(() => {
  if (!activeRepository.value) return []
  return activeRepository.value.branches.remote
    .filter(b => b.toLowerCase().includes(branchKeyword.value.toLowerCase()))
    .map(b => ({
      raw: b,
      highlighted: highlightMatch(b, branchKeyword.value)
    }))
})

const filteredRepositories = computed(() => {
  if (!activeRepository.value) return []
  return repositories.value
    .filter(repo => repo.name.toLowerCase().includes(repositoryKeyword.value.toLowerCase()))
})

/*----Watch----*/
watch(() => isWorkspaceCollapsed.value, (newVal) => {
  if (!newVal) {
    showActions.value = true;
    containerWidth.value = previousWidth.value;
  } else {
    showActions.value = false;
    previousWidth.value = containerWidth.value;
    containerWidth.value = 55;
  }
});

watch(showSearchBranch, (newVal) => {
  if (newVal) {
    nextTick(() => {
      branchSearchInput.value?.focus()
    })
  }
})

watch(showSearchRepository, (newVal) => {
  if (newVal) {
    nextTick(() => {
      repositorySearchInput.value?.focus()
    })
  }
})

/*----Method----*/
const resizePanel = (e) => {
  if (!isResizing) return;

  const container = document.querySelector('.workspace-split');
  const containerTop = container.getBoundingClientRect().top;
  const newHeight = e.clientY - containerTop;

  const minHeight = containerHeight.value * 0.2;
  const maxHeight = containerHeight.value * 0.8;

  reposHeight.value = Math.min(Math.max(newHeight, minHeight), maxHeight)
};

const stopResizing = () => {
  isResizing = false;
  window.removeEventListener('mousemove', resizePanel)
  window.removeEventListener('mouseup', stopResizing)
};

const startResizeContainer = () => {
  if (isWorkspaceCollapsed.value) return;
  isResizingContainer = true;
  window.addEventListener('mousemove', resizeContainer);
  window.addEventListener('mouseup', stopResizeContainer);
};

const resizeContainer = (e) => {
  if (!isResizingContainer) return;
  const wrapperLeft = document.querySelector('.horizontal-resize-wrapper').getBoundingClientRect().left;
  let newWidth = e.clientX - wrapperLeft;
  newWidth = Math.min(Math.max(newWidth, 250), 500);
  containerWidth.value = newWidth;
};

const stopResizeContainer = () => {
  isResizingContainer = false;
  window.removeEventListener('mousemove', resizeContainer);
  window.removeEventListener('mouseup', stopResizeContainer);
};

const openRepository = () => {
  openModal.value?.openModal()
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'clean': return 'fa-check-circle'
    case 'dirty': return 'fa-exclamation-circle'
    case 'untracked': return 'fa-question-circle'
    default: return 'fa-circle'
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'clean': return 'text-success'
    case 'dirty': return 'text-warning'
    case 'untracked': return 'text-secondary'
    default: return 'text-muted'
  }
}

const startResizing = () => {
  const container = document.querySelector('.workspace-split');
  if (!container) return;

  containerHeight.value = container.clientHeight;
  isResizing = true;

  window.addEventListener('mousemove', resizePanel);
  window.addEventListener('mouseup', stopResizing);
};

function highlightMatch(text, keyword) {
  const index = text.toLowerCase().indexOf(keyword.toLowerCase())
  if (index === -1 || !keyword) return text

  const before = text.substring(0, index)
  const match = text.substring(index, index + keyword.length)
  const after = text.substring(index + keyword.length)

  return `${before}<span class="highlight">${match}</span>${after}`
}

function openContextMenuLocal(event, branch)
{
  mitter.emit('merge-information', activeRepository.value.currentBranch)
  contextMenu.value?.open(event, branch.raw)
}

function handleContextAction({ action, branch }) {
  if (action === 'checkout') {
    switchBranch(branch)
  }
  if (action === 'merge-branch') {
    mergeBranch(branch)
  }
}

async function mergeBranch(branch) {
  try {
    loading.show('Merging branch...');
    const res = await api.post('/merge', {
      repo_path: activeRepository.value.path,
      source_branch: branch
    });
    mitter.emit('alert', {
      message: res.data.message || 'Merge thành công!',
      type: 'success',
    })
  } catch (error) {
    mitter.emit('alert', {
      message: error.response?.data?.message || 'Lỗi Merge!',
      type: 'error',
    })
    console.error(error)
  } finally {
    loading.hide()
  }
}

function switchBranch(branchName) {
  if (branchName.includes("origin/")) {
    branchName = branchName.replace("origin/", "");
  }
  if (activeRepository.value) {
    checkoutBranch(activeRepository.value, branchName)
  }
}

async function checkoutBranch(repoPath, branchName) {
  try {
    loading.show(`Switching to branch "${branchName}"...`)

    const response = await api.post('/checkout-branch', {
      repo_path: activeRepository.value.path,
      branch_name: branchName
    });

    const result = response.data.data

    if (result) {
      activeRepository.value.currentBranch = result.currentBranch
      if (!activeRepository.value.branches.local.includes(result.currentBranch)) {
        activeRepository.value.branches.local.push(result.currentBranch)
      }
      mitter.emit('alert', {
        message: `✅ Switched to branch "${result.currentBranch}"`,
        type: 'success'
      })
    } else {
      mitter.emit('alert', {
        message: '❌ Failed to open repository: No data returned',
        type: 'error'
      })
    }

  } catch (error) {
    mitter.emit('alert', {
      message: `Checkout error: ${error.message}`,
      type: 'error'
    })
  } finally {
    loading.hide()
  }
}

function toggle(section) {
  collapsedTree.value[section] = !collapsedTree.value[section]
}

// function setActiveRepository(repo) {
//   activeRepository.value = repo
//   mitter.emit('set-active-repository', repo)
//   mitter.emit('push-repository', repo.path)
//   window.__activeRepository = repo
// }

async function setActiveRepository(repo) {
  try {
    loading.show(`Fetching repository "${repo.name}"...`)

    // 1. Gọi API mở repository mới
    const response = await api.post('/open-repository', {
      repo_path: repo.path,
    })

    const result = response.data.data

    if (!result) {
      mitter.emit('alert', {
        message: '⚠️ Failed to open repository',
        type: 'error',
      })
      return
    }

    // 2. Tìm index repo cũ trùng path (nếu có)
    const existingIndex = repositories.value.findIndex(r => r.path === repo.path)

    if (existingIndex !== -1) {
      // Xoá repo cũ
      repositories.value.splice(existingIndex, 1)

      // Thêm lại repo mới vào đúng vị trí cũ
      repositories.value.splice(existingIndex, 0, result)
    } else {
      // Nếu chưa có, thêm vào cuối
      repositories.value.push(result)
    }

    // 3. Gán làm repo active (dùng bản mới)
    activeRepository.value = result

    // 4. Emit các sự kiện liên quan (dùng result)
    mitter.emit('set-active-repository', result)
    mitter.emit('push-repository', result.path)

    // 5. Gán global
    window.__activeRepository = result

    // 6. Thông báo
    mitter.emit('alert', {
      message: `✅ Opened repository: ${result.name || result.path}`,
      type: 'success',
    })

  } catch (error) {
    mitter.emit('alert', {
      message: `❌ Failed to open repository: ${error.message}`,
      type: 'error',
    })
  } finally {
    loading.hide()
  }
}

function toggleWorkspacePanel() {
  isWorkspaceCollapsed.value = !isWorkspaceCollapsed.value
}
</script>
<style scoped>
.horizontal-resize-wrapper {
  display: flex;
  flex-direction: row;
  width: 300px;
  min-width: 60px;
  max-width: 500px;
  height: 100%;
  overflow: hidden;
  position: relative;
  padding-right: 0;
}

.resizer-horizontal {
  width: 5px;
  background-color: var(--border-color);
  cursor: col-resize;
  user-select: none;
}

.workspace-container {
  width: 100%;
  height: 100%;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  overflow: hidden;
  padding-right: 0;
}

.workspace-container.collapsed {
  width: 0;
  overflow: hidden;
}

.workspace-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.workspace-header {
  position: relative;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  min-height: 36px;
}

.workspace-header h6 {
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

.workspace-toggle {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  font-size: 14px;
  z-index: 10;
}

.workspace-toggle:hover {
  color: var(--text-primary);
}

.workspace-content {
  flex: 1;
  overflow-y: auto;
}

.workspace-repos {
  padding: 8px;
}

.workspace-container.collapsed {
  width: 50px;
}

.workspace-container.collapsed .workspace-toggle {
  right: 50%;
  transform: translate(50%, -50%);
}

.workspace-container.collapsed .workspace-header h6,
.workspace-container.collapsed .workspace-content {
  opacity: 0;
  visibility: hidden;
  height: 0;
  pointer-events: none;
}

.workspace-container.collapsed .branch-workspace-header{
  opacity: 0;
  visibility: hidden;
  height: 0;
  pointer-events: none;
}

.workspace-action {
  margin: 0;
  background: transparent;
  border: none;
  color: var(--text-secondary);
}
.repositories-workspace {
  height: 50%;
  min-height: 20%;
  max-height: 80%;
  display: flex;
  flex-direction: column;
}
.branch-workspace{
  height: 50%;
  min-height: 20%;
  max-height: 80%;
}

.branch-workspace-header{
  position: relative;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  min-height: 36px;
}

.branch-workspace-header h6{
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}
/* Utility Classes */
.no-repos-message{
  text-align: center;
  color: var(--text-muted);
  padding: 32px 16px;
}

.no-repos-message i{
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}

.repo-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 4px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid transparent;
}

.repo-item:hover {
  background-color: var(--bg-hover);
  border-radius: 10px;
}

.repo-item.active {
  background-color: var(--bg-hover);
  border-radius: 10px;
}

.repo-icon {
  width: 20px;
  margin-right: 8px;
  text-align: center;
}

.repo-info {
  flex: 1;
  min-width: 0;
}

.repo-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.repo-path {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-workspace{
  position: sticky;
  top: 0;
  padding: 8px;
  margin: 5px;
  display: flex;
  align-items: center;
  border-radius: 8px;
  border: solid 1px var(--border-color);
  font-size: 12px;
  background-color: var(--bg-secondary);
}

.search-branch {
  width: 100%;
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  border: none;
}

.search-branch:focus-visible {
  outline: none;
}

.symbol-search {
  margin-right: 5px;
  color: var(--text-secondary);
}

.workspace-split {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.resizer {
  height: 5px;
  background-color: var(--bg-secondary);
  cursor: row-resize;
  user-select: none;
}

.fade-search-enter-active, .fade-search-leave-active {
  transition: all 0.3s ease;
}
.fade-search-enter-from, .fade-search-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-search-enter-to, .fade-search-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Branch Tree */
.workspace-content.branch-tree-scroll {
  max-height: 100%;
  overflow-y: scroll;
}

.branch-tree {
  margin: 10px;
}

.tree-item {
  display: flex;
  align-items: center;
  padding: 4px 0;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-radius: 5px;
  user-select: none;
}

.tree-item:hover {
  background-color: var(--bg-hover);
}

.tree-item.active {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.tree-item.nested {
  padding-left: 20px;
}

.tree-item.nested-2 {
  padding-left: 40px;
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

.tree-toggle.collapsed {
  transform: rotate(-90deg);
}

.tree-header {
  cursor: pointer;
}

.tree-item.tree-header:hover {
  background-color: transparent;
}

::v-deep(.highlight) {
  background-color: #ff9700;
  color: black;
}
</style>
