import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRepositoryStore = defineStore('repository', () => {
  const activeRepo = ref(null)

  function setActiveRepo(repo) {
    activeRepo.value = {
      id: repo.id,
      name: repo.name,
      branch: repo.branch || 'main',
      status: repo.status || 'clean',
      path: repo.path,
    }
  }

  function setBranch(branchName) {
    if (activeRepo.value) activeRepo.value.branch = branchName
  }

  function setStatus(status) {
    if (activeRepo.value) activeRepo.value.status = status
  }

  const repoName = computed(() => activeRepo.value?.name || '')
  const branchName = computed(() => activeRepo.value?.branch || '')
  const repoStatus = computed(() => activeRepo.value?.status || '')

  return {
    activeRepo,
    setActiveRepo,
    setBranch,
    setStatus,
    repoName,
    branchName,
    repoStatus,
  }
})
