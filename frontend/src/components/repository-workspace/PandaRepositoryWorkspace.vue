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
                <i class="fa-solid fa-magnifying-glass"/>
              </button>
              <button class="btn btn-sm workspace-action" @click="toggleWorkspacePanel">
                <i
                  :class="[
                    'fas',
                    isWorkspaceCollapsed ? 'fa-solid fa-layer-group' : 'fa-solid fa-layer-group',
                  ]"
                />
              </button>
            </div>
          </div>

          <transition name="fade-search">
            <div class="search-workspace" v-if="showSearchRepository">
              <div class="symbol-search">
                <i class="fa-solid fa-magnifying-glass"/>
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
                  <i class="fas fa-folder-open fa-2x mb-2"/>
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
                    <i class="fas fa-folder text-warning"/>
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
                    />
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <div class="resizer" @mousedown="startResizing"></div>

        <div
          class="branch-workspace"
          :style="{ height: 'calc(100% - ' + reposHeight + 'px - 5px)' }"
        >
          <div class="branch-workspace-header">
            <h6 class="mb-0">Branches</h6>
            <div class="workspace-toggle">
              <button
                class="btn btn-sm workspace-action search"
                v-if="showActions"
                @click="showSearchBranch = !showSearchBranch"
              >
                <i class="fa-solid fa-magnifying-glass"/>
              </button>
              <button class="btn btn-sm workspace-action" v-if="showActions">
                <i class="fa-solid fa-ellipsis-vertical"/>
              </button>
            </div>
          </div>
          <transition name="fade-search">
            <div class="search-workspace" v-if="showSearchBranch">
              <div class="symbol-search">
                <i class="fa-solid fa-magnifying-glass"/>
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
                <i class="fas fa-code-branch fa-2x mb-2"/>
                <p>No repository selected</p>
                <small>Open a repository to view branches</small>
              </div>

              <template v-else>
                <!-- HEAD -->
                <div class="tree-item tree-header">
                  <i class="fas fa-laptop text-info me-1"/>
                  <span>HEAD (Current Branch)</span>
                </div>
                <div class="tree-item nested">
                  <i class="fas fa-solid fa-tag text-info me-1"/>
                  <span>{{ getDisplayHeadBranchName(activeRepository.currentBranch)}}</span>
                </div>

                <!-- Local -->
                <div class="tree-item tree-header" @click="toggle('local')">
                  <i
                    class="fas fa-chevron-down tree-toggle branch-toggle"
                    :class="{ collapsed: collapsedTree.local }"
                  />
                  <i class="fas fa-folder branch-folder me-1"/>
                  <span>Local</span>
                </div>
                <template v-if="!collapsedTree.local || branchKeyword">
                  <branch-tree-node
                    :node="localBranchTree"
                    path=""
                    :collapsed-groups="collapsedGroups"
                    :toggle-group="toggleGroup"
                    :open-context-menu="openContextMenu"
                    :search-term="branchKeyword"
                    :level="1"
                  />
                </template>

                <!-- Remote -->
                <div class="tree-item tree-header"
                     @click="toggle('remote')">
                  <i
                    class="fas fa-chevron-down tree-toggle branch-toggle"
                    :class="{ collapsed: collapsedTree.remote }"
                  />
                  <i class="fas fa-cloud branch-folder me-1"/>
                  <span>Remote</span>
                </div>
                <template v-if="!collapsedTree.remote || branchKeyword">
                  <branch-tree-node
                    :node="remoteBranchTree"
                    path=""
                    :collapsed-groups="collapsedGroups"
                    :toggle-group="toggleGroup"
                    :open-context-menu="openContextMenu"
                    :search-term="branchKeyword"
                    :level="1"
                  />
                </template>
              </template>
            </div>
          </div>
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
  <branch-context-menu ref="branchContextActionMenu" @action="onBranchAction"/>
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
  watchEffect,
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
import BranchTreeNode from '@/components/repository-workspace/BranchTreeNode.vue'
import BranchContextMenu from '@/components/repository-workspace/BranchContextMenu.vue'

/*----Data----*/
let isResizingContainer = false
let isResizing = false
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
const renameForm = defineAsyncComponent(
  () => import('@/components/repository-workspace/RenameForm.vue'),
)
const confirmDialog = defineAsyncComponent(() => import('@/components/common/ConfirmDialog.vue'))

const showSearchBranch = ref(false)
const branchKeyword = ref('')
const collapsedTree = ref({
  local: false,
  remote: false,
})
const branchContextActionMenu = ref(null)
const collapsedGroups = ref({})

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

const localBranchTree = computed(() => {
  const repo = activeRepository.value
  if (!repo || !repo.branches || !repo.branches.local) return
  let localBranches = activeRepository.value.branches.local
  if (!repo || !repo.branches || !repo.branches.local) return {}
  if (!branchKeyword.value) return buildTree(localBranches)
  const normalizedTerm = branchKeyword.value.toLowerCase()
  const filtered = localBranches.filter((b) => b.toLowerCase().includes(normalizedTerm))
  return buildTree(filtered)
})

const remoteBranchTree = computed(() => {
  const repo = activeRepository.value
  if (!repo || !repo.branches || !repo.branches.remote) return
  let remoteBranches = activeRepository.value.branches.remote
  if (!repo || !repo.branches || !repo.branches.remote) return {}
  if (!branchKeyword.value) return buildTree(remoteBranches)
  const normalizedTerm = branchKeyword.value.toLowerCase()
  const filtered = remoteBranches.filter((b) => b.toLowerCase().includes(normalizedTerm))
  return buildTree(filtered)
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
  }, { deep: true })

watchEffect(() => {
  const newCollapsedGroups = {}
  const initCollapsed = (subTree, pathPrefix = '') => {
    for (const key in subTree) {
      const fullPathKey = pathPrefix + key
      if (hasChildren(subTree[key])) {
        newCollapsedGroups[fullPathKey] = true
        initCollapsed(subTree[key], fullPathKey + '/')
      }
    }
  }

  initCollapsed(localBranchTree.value)
  initCollapsed(remoteBranchTree.value)

  // Expand match khi search
  if (branchKeyword.value) {
    toggleCollapseForMatches(localBranchTree.value, '', newCollapsedGroups)
    toggleCollapseForMatches(remoteBranchTree.value, '', newCollapsedGroups)
  }

  collapsedGroups.value = newCollapsedGroups
})

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
  const container = document.querySelector('.workspace-split')
  if (!container) return

  containerHeight.value = container.clientHeight
  isResizing = true

  window.addEventListener('mousemove', resizePanel)
  window.addEventListener('mouseup', stopResizing)
}

const resizePanel = (e) => {
  if (!isResizing) return

  const container = document.querySelector('.workspace-split')
  const containerTop = container.getBoundingClientRect().top
  const newHeight = e.clientY - containerTop

  const minHeight = containerHeight.value * 0.2
  const maxHeight = containerHeight.value * 0.8

  reposHeight.value = Math.min(Math.max(newHeight, minHeight), maxHeight)
}

const stopResizing = () => {
  isResizing = false
  window.removeEventListener('mousemove', resizePanel)
  window.removeEventListener('mouseup', stopResizing)
}

function toggle(section) {
  collapsedTree.value[section] = !collapsedTree.value[section]
}

const getDisplayHeadBranchName = (branch) => {
  const parts = branch.split('/');
  if (parts.length === 1) return parts[0];

  const last = parts[parts.length - 1];
  if (last === 'main' || last === 'master') {
    return parts[parts.length - 2];
  }
  return last;
};

/*----Build branch tree----*/
const buildTree = (branches) => {
  const tree = {}
  branches.forEach((branch) => {
    const parts = branch.split('/')
    let current = tree
    parts.forEach((part, index) => {
      if (!current[part]) current[part] = index === parts.length - 1 ? null : {}
      current = current[part] ?? {}
    })
  })
  return tree
}

const hasChildren = (node) =>
  node !== null && node !== undefined && Object.keys(node || {}).length > 0

const toggleGroup = (path) => {
  collapsedGroups.value[path] = !collapsedGroups.value[path]
}

const openContextMenu = (branchName, event) => {
  branchContextActionMenu.value.open(event, branchName)
}
const toggleCollapseForMatches = (treeNode, pathPrefix = '', currentCollapsedGroups) => {
  const normalizedTerm = branchKeyword.value.toLowerCase()
  for (const key in treeNode) {
    const fullPathKey = pathPrefix + key
    const isMatch =
      branchKeyword.value &&
      (key.toLowerCase().includes(normalizedTerm) ||
        fullPathKey.toLowerCase().includes(normalizedTerm))
    if (hasChildren(treeNode[key]))
      toggleCollapseForMatches(treeNode[key], fullPathKey + '/', currentCollapsedGroups)
    if (isMatch) {
      const parts = fullPathKey.split('/')
      let ancestorPath = ''
      for (let i = 0; i < parts.length - 1; i++) {
        ancestorPath += (i > 0 ? '/' : '') + parts[i]
        currentCollapsedGroups[ancestorPath] = false
      }
      if (hasChildren(treeNode[key])) currentCollapsedGroups[fullPathKey] = false
    }
  }
}

function onBranchAction({ action, branch}) {
  switch (action) {
    case 'checkout':
      switchBranch(branch)
      break
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

    const data = {
      repo_path: activeRepository.value.path,
      branch_name: branchName
    }

    const response = await commonApi.checkout(data)

    const result = response.data

    if (result) {
      activeRepository.value.currentBranch = result.currentBranch
      if (!activeRepository.value.branches.local.includes(result.currentBranch)) {
        activeRepository.value.branches.local.push(result.currentBranch)
      }
      notify.success(`Switched to branch "${result.currentBranch}"`)
    }
  } catch (error) {
    notify.error(error.message)
  } finally {
    loading.hide()
  }
}
</script>
<style scoped src="@/assets/styles/PandaRepositoryWorkspace.css"></style>
