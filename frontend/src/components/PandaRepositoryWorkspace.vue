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
      </div>
    </div>
    <div class="resizer-horizontal" @mousedown="startResizeContainer" v-if="!isWorkspaceCollapsed"></div>
  </div>
  <repository-context-menu ref="repoContextMenu" @action="onRepoAction"/>
</template>
<script setup>
// Props
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import mitter from '@/plugins/mitter.js'
import api from '@/plugins/api.js'
import { useLoadingStore } from '@/stores/loadingStore.js'
import { saveRepos, loadRepos } from '@/plugins/indexedDB.js'
import RepositoryContextMenu from '@/components/modals/RepositoryContextMenu.vue'

/*----Data----*/
const repoContextMenu = ref(null)
const showActions = ref(true);
const showSearchRepository = ref(false);
const reposHeight = ref(0);
const containerHeight = ref(0);
const containerWidth = ref(325);
const previousWidth = ref(300)
let isResizingContainer = false;
const repositoryKeyword = ref('')
const isWorkspaceCollapsed = ref(false)
const repositorySearchInput = ref(null)
const activeRepository = ref(null)
const repositories = ref([])
const loading = useLoadingStore()
const isLoadingRepos = ref(true)

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
      return;
    }

    // Nếu chưa có -> push mới và active
    repositories.value.push(repo);
    activeRepository.value = repo;
  })
});

onMounted(async () => {
  isLoadingRepos.value = true
  try {
    const savedRepos = await loadRepos()
    repositories.value = savedRepos

    // 1) Có repo có active = true -> active repo đó
    const active = savedRepos.find(r => r.active)

    if (active) {
      await setActiveRepository(active)
      return
    }

    // 2) Không có active -> active repo đầu tiên
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
  }
});

watch(showSearchRepository, (newVal) => {
  if (newVal) {
    nextTick(() => {
      repositorySearchInput.value?.focus()
    })
  }
})

// Watch repositories để tự động lưu khi có thay đổi
watch(repositories, async (newVal) => {
  const basicRepos = newVal.map(r => ({
    id: r.id,
    path: r.path,
    name: r.name,
    status: r.status || 'clean',
    active: r.active || false
  }));
  await saveRepos(basicRepos);
}, { deep: true });

/*----Method----*/
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

async function setActiveRepository(repo) {
  try {
    loading.show(`Fetching repository "${repo.name}"...`)

    // 1. Load repo từ backend
    const response = await api.post('/open-repository', {
      repo_path: repo.path,
    })
    const result = response.data.data
    if (!result) return

    // === SET ACTIVE ===
    repositories.value.forEach(r => r.active = false)
    result.active = true

    // 2. Replace/update in list
    const index = repositories.value.findIndex(r => r.path === repo.path)
    if (index !== -1) repositories.value.splice(index, 1, result)
    else repositories.value.push(result)

    // 3. Set active
    activeRepository.value = result

    // 4. Emit
    mitter.emit('set-active-repository', result)
    mitter.emit('push-repository', result.path)

    mitter.emit('alert', {
      message: `Open repository for ${repo.name}`,
      type: 'success',
    })

  } catch (error) {
    mitter.emit('alert', {
      message: `❌ Failed: ${error.message}`,
      type: 'error',
    })
  } finally {
    loading.hide()
  }
}

function toggleWorkspacePanel() {
  isWorkspaceCollapsed.value = !isWorkspaceCollapsed.value
}

function onRepoAction({ action, repo }) {
  switch(action) {
    case 'open':
      setActiveRepository(repo)
      break
    case 'rename':
      { const newName = prompt('Enter new repo name', repo.name)
      if(newName) repo.name = newName
      break }
    case 'delete':
      if(confirm(`Delete repo ${repo.name}?`)) {
        const index = repositories.value.findIndex(r => r.id === repo.id)
        if(index !== -1) repositories.value.splice(index, 1)
        if(activeRepository.value?.id === repo.id) {
          activeRepository.value = repositories.value[0] || null
        }
      }
      break
    case 'open-terminal':
      mitter.emit('open-terminal', repo.path)
      break
  }
}
</script>
<style scoped src="@/assets/styles/PandaRepositoryWorkspace.css"></style>
