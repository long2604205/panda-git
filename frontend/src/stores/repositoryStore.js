import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRepositoryStore = defineStore('repository', () => {
  const activeRepo = ref(null)

  function setActiveRepo(repo) {
    activeRepo.value = {
      id: repo.id,
      name: repo.name,
      branch: repo.branch || 'main',
      path: repo.path,
      status: repo.status || 'clean',
      groupId: repo.groupId || null,
    }
  }

  function setBranch(branchName) {
    if (activeRepo.value) activeRepo.value.branch = branchName
  }

  const repoName = computed(() => activeRepo.value?.name || '')
  const branchName = computed(() => activeRepo.value?.branch || '')

  return {
    activeRepo,
    setActiveRepo,
    setBranch,
    repoName,
    branchName,
  }
})
