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
                class="btn btn-sm workspace-action search"
                v-if="showActions"
                @click="showSearchRepository = !showSearchRepository"
              >
                <i class="fa-solid fa-magnifying-glass"></i>
              </button>
              <button class="btn btn-sm workspace-action" @click="toggleWorkspacePanel">
                <i :class="['fas', isWorkspaceCollapsed ? 'fa-solid fa-layer-group' : 'fa-solid fa-layer-group']"></i>
              </button>
            </div>
          </div>
          <div class="toolbar-line"/>

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
              <div v-if="!activeRepository" class="no-repos-message text-center py-4">
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
  <branch-context-menu ref="contextMenu" @action="handleContextAction"/>
  <repository-context-menu ref="repoContextMenu" @action="handleReposContextAction"/>
</template>
<script setup>
// Props
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import BranchContextMenu from '@/components/modals/BranchContextMenu.vue'
import mitter from '@/plugins/mitter.js'
import api from '@/plugins/api.js'
import { useLoadingStore } from '@/stores/loadingStore.js'
import RepositoryContextMenu from '@/components/modals/RepositoryContextMenu.vue'

/*----Data----*/
const showActions = ref(true);
const showSearchRepository = ref(false);
const showSearchBranch = ref(false);
const reposHeight = ref(0);
const containerHeight = ref(0);
const containerWidth = ref(325);
const previousWidth = ref(300)
let isResizing = false;
let isResizingContainer = false;
const contextMenu = ref(null)
const repoContextMenu = ref(null)
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
const repositories = ref([])
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
    const existing = repositories.value.find(r => r.path === repo.path);

    if (existing) {
      activeRepository.value = existing;

      mitter.emit('alert', {
        message: `📁 Repository "${repo.name}" is already open`,
        type: 'success'
      });
      return;
    }

    // Nếu chưa có -> push mới và active
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
    showSearchRepository.value = false
    showSearchBranch.value = false
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

function handleReposContextAction (action, url) {
  if (action === 'checkout') {
    console.log('checkout', url)
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
<style scoped src="@/assets/styles/PandaRepositoryWorkspace.css">
</style>
