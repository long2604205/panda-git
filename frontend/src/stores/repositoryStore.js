import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRepositoryStore = defineStore('repository', () => {
  const activeRepo = ref(null)

  function setActiveRepo(repo) {
    activeRepo.value = {
      id: repo.id,
      name: repo.name,
      currentBranch: repo.currentBranch,
      path: repo.path,
      groupId: repo.groupId || null,
    }
  }

  function setBranch(branchName) {
    if (activeRepo.value) activeRepo.value.currentBranch = branchName
  }

  const repoName = computed(() => activeRepo.value?.name || '')
  const branchName = computed(() => activeRepo.value?.currentBranch || '')
  const repoPath = computed(() => activeRepo.value?.path || '')

  return {
    activeRepo,
    setActiveRepo,
    setBranch,
    repoName,
    branchName,
    repoPath
  }
})
