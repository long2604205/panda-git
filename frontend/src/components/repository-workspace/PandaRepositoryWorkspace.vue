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
                <i
                  :class="[
                    'fas',
                    isWorkspaceCollapsed ? 'fa-solid fa-layer-group' : 'fa-solid fa-layer-group',
                  ]"
                ></i>
              </button>
            </div>
          </div>
          <div class="toolbar-line" />

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
                  class="repo-item no-select"
                  :class="{ active: activeRepository && activeRepository.id === repo.id }"
                  @dblclick="setActiveRepository(repo)"
                  @contextmenu.prevent="repoContextMenu.open($event, repo)"
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
          <h1>Branches</h1>
        </div>
      </div>
    </div>
    <div
      class="resizer-horizontal"
      @mousedown="startResizeContainer"
      v-if="!isWorkspaceCollapsed"
    ></div>
  </div>
  <repository-context-menu ref="repoContextMenu" @action="onRepoAction" />
</template>
<script setup>
// Props
import {
  computed,
  defineAsyncComponent,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'
import mitter from '@/plugins/mitter.js'
import { useLoadingStore } from '@/stores/loadingStore.js'
import { saveRepos, loadRepos } from '@/plugins/indexedDB.js'
import RepositoryContextMenu from '@/components/repository-workspace/RepositoryContextMenu.vue'
import { useRepositoryStore } from '@/stores/repositoryStore.js'
import { showPageInModal } from '@/services/modals.js'
import commonApi from '@/services/api/common.js'
import notify from '@/plugins/notify.js'
import { getStatusColor, getStatusIcon } from '@/composable/attributes.js'

/*----Data----*/
let isResizingContainer = false
let isResizing = false;
const reposHeight = ref(0)
const containerHeight = ref(0)
const containerWidth = ref(325)
const previousWidth = ref(300)
const isWorkspaceCollapsed = ref(false)
const repoContextMenu = ref(null)
const showActions = ref(true)
const showSearchRepository = ref(false)
const repositoryKeyword = ref('')
const repositorySearchInput = ref(null)
const activeRepository = ref(null)
const repositories = ref([])
const loading = useLoadingStore()
const isLoadingRepos = ref(true)
const repositoryStore = useRepositoryStore()
const renameForm = defineAsyncComponent(() => import('@/components/repository-workspace/RenameForm.vue'),)
const confirmDialog = defineAsyncComponent(() => import('@/components/common/ConfirmDialog.vue'))

/*----Mounted----*/
onMounted(() => {
  const container = document.querySelector('.workspace-split')
  if (container) {
    containerHeight.value = container.clientHeight
    reposHeight.value = containerHeight.value / 2
  }
})

onMounted(() => {
  if (repositories.value.length > 0 && !activeRepository.value) {
    setActiveRepository(repositories.value[0])
  }

  mitter.on('open-repository', (repo) => {
    const existing = repositories.value.find((r) => r.path === repo.path)

    repositories.value.forEach((r) => (r.active = false))
    if (existing) {
      existing.active = true
      activeRepository.value = existing
      return
    }

    repo.active = true
    repositories.value.push(repo)
    activeRepository.value = repo
  })
})

onMounted(async () => {
  isLoadingRepos.value = true
  try {
    const savedRepos = await loadRepos()
    repositories.value = savedRepos

    const active = savedRepos.find((r) => r.active)

    if (active) {
      await setActiveRepository(active)
      return
    }

    if (savedRepos.length) {
      await setActiveRepository(savedRepos[0])
    }
  } finally {
    isLoadingRepos.value = false
  }
})

onBeforeUnmount(() => {
  mitter.off('open-repository')
})

/*----Computed----*/
const filteredRepositories = computed(() => {
  if (!activeRepository.value) return []
  return repositories.value.filter((repo) =>
    repo.name.toLowerCase().includes(repositoryKeyword.value.toLowerCase()),
  )
})

/*----Watch----*/
watch(() => isWorkspaceCollapsed.value, (newVal) => {
    if (!newVal) {
      showActions.value = true
      containerWidth.value = previousWidth.value
    } else {
      showActions.value = false
      previousWidth.value = containerWidth.value
      containerWidth.value = 55
      showSearchRepository.value = false
    }
  },
)

watch(showSearchRepository, (newVal) => {
  if (newVal) {
    nextTick(() => {
      repositorySearchInput.value?.focus()
    })
  }
})

watch(repositories, async (newVal) => {
    const basicRepos = newVal.map((r) => ({
      id: r.id,
      path: r.path,
      name: r.name,
      status: r.status || 'clean',
      active: r.active || false,
    }))
    await saveRepos(basicRepos)
  },
  { deep: true },
)

/*----Method----*/
const startResizeContainer = () => {
  if (isWorkspaceCollapsed.value) return
  isResizingContainer = true
  window.addEventListener('mousemove', resizeContainer)
  window.addEventListener('mouseup', stopResizeContainer)
}

const resizeContainer = (e) => {
  if (!isResizingContainer) return
  const wrapperLeft = document
    .querySelector('.horizontal-resize-wrapper')
    .getBoundingClientRect().left
  let newWidth = e.clientX - wrapperLeft
  newWidth = Math.min(Math.max(newWidth, 250), 500)
  containerWidth.value = newWidth
}

const stopResizeContainer = () => {
  isResizingContainer = false
  window.removeEventListener('mousemove', resizeContainer)
  window.removeEventListener('mouseup', stopResizeContainer)
}

function toggleWorkspacePanel() {
  isWorkspaceCollapsed.value = !isWorkspaceCollapsed.value
}

function onRepoAction({ action, repo }) {
  switch (action) {
    case 'open':
      setActiveRepository(repo)
      break
    case 'open-in-explorer':
      window.electronAPI.openInExplorer(repo.path)
      break
    case 'open-terminal':
      window.electronAPI.openTerminal(repo.path)
      break
    case 'pull-repository':
      pullRepository(repo.path)
      break
    case 'push-repository':
      pushRepository(repo.path)
      break
    case 'refresh-repository':
      refreshRepository(repo)
      break
    case 'rename': {
      openRenameForm(repo)
      break
    }
    case 'delete':
      showPageInModal(confirmDialog, {
        title: 'Confirm delete',
        message: `Are you sure you want to delete ${repo.name}?`,
        onConfirm() {
          const index = repositories.value.findIndex((r) => r.id === repo.id)
          if (index !== -1) repositories.value.splice(index, 1)
          if (activeRepository.value?.id === repo.id) {
            activeRepository.value = repositories.value[0] || null
          }
        },
      })
      break
  }
}

async function setActiveRepository(repo) {
  try {
    loading.show(`Fetching repository "${repo.name}"...`)

    const response = await commonApi.open({ repo_path: repo.path })
    const result = response.data
    if (!result) return
    // set active false for all repos
    repositories.value.forEach((r) => (r.active = false))
    result.active = true
    //Replace/update in list
    const index = repositories.value.findIndex((r) => r.path === repo.path)
    if (index !== -1) repositories.value.splice(index, 1, result)
    else repositories.value.push(result)
    // 3. Set active repo in store
    activeRepository.value = result
    repositoryStore.setActiveRepo(result)

    mitter.emit('set-active-repository', result)
    notify.success(`Activated repository "${repo.name}"`)
  } catch (error) {
    notify.error(`Failed: ${error.message}`)
  } finally {
    loading.hide()
  }
}

async function pushRepository(repoPath) {
  try {
    loading.show('Pushing...')
    const data = {
      repo_path: repoPath,
    }
    await commonApi.push(data)
    notify.info('Everything is up to date')
  } catch (error) {
    notify.error(`Push failed: ${error.message}`)
  } finally {
    loading.hide()
  }
}

async function pullRepository(repoPath) {
  try {
    loading.show('Pulling...')
    const data = {
      repo_path: repoPath,
    }
    await commonApi.pull(data)
    notify.info('All files are up to date')
  } catch (error) {
    notify.error(`Pull failed: ${error.message}`)
    console.error(error)
  } finally {
    loading.hide()
  }
}

async function refreshRepository(repo) {
  try {
    loading.show(`Refreshing "${repo.name}"...`)

    const data = {
      repo_path: repo.path,
    }

    // 1. Load repo từ backend
    const response = await commonApi.open(data)
    const result = response.data
    if (!result) return

    // 2. Replace/update in list

    const index = repositories.value.findIndex((r) => r.id === repo.id)
    if (index !== -1) {
      repositories.value[index] = {
        ...repositories.value[index],
        branches: result.branches,
        changes: result.changes,
        currentBranch: result.currentBranch,
        status: result.status,
      }
    }

    // 3. Set active
    activeRepository.value = result
    repositoryStore.setActiveRepo(result)

    notify.success(`Repository "${repo.name}" refreshed!`)
  } catch (err) {
    notify.error('Refresh failed')
    console.error(err)
  } finally {
    loading.hide()
  }
}

function openRenameForm(repo) {
  showPageInModal(renameForm, { data: repo }, { width: '20%' })
}

const startResizing = () => {
  const container = document.querySelector('.workspace-split');
  if (!container) return;

  containerHeight.value = container.clientHeight;
  isResizing = true;

  window.addEventListener('mousemove', resizePanel);
  window.addEventListener('mouseup', stopResizing);
};

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
</script>
<style scoped src="@/assets/styles/PandaRepositoryWorkspace.css"></style>
