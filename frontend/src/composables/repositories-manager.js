import { showPageInModal } from '@/services/modals.js'
import { defineAsyncComponent } from 'vue'

const openForm = defineAsyncComponent(() => import('@/components/common/OpenRepositoryForm.vue'))
const groupForm = defineAsyncComponent(() => import('@/components/common/GroupForm.vue'))
const branchForm = defineAsyncComponent(() => import('@/components/common/BranchForm.vue'))
const repositoryForm = defineAsyncComponent(() => import('@/components/common/RepositoryForm.vue'))
const openPullForm = defineAsyncComponent(() => import('@/components/common/PullForm.vue'))

export function addGroup () {
  showPageInModal(groupForm, {}, { width: '20%' })
}

export function renameGroup (groupId) {
  showPageInModal(groupForm, {params: {id: groupId}}, { width: '20%' })
}

export function openRepository () {
  showPageInModal(openForm, {}, {width: '30%'})
}

export function createBranch () {
  showPageInModal(branchForm, {}, {width: '20%'})
}

export function renameRepository (repo) {
  showPageInModal(repositoryForm, {params: {data: repo}}, {width: '30%'})
}

export function pullRepository () {
  showPageInModal(openPullForm, {}, {width: '25%'})
}
