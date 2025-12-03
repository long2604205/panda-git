import { showPageInModal } from '@/services/modals.js'
import { defineAsyncComponent } from 'vue'

const openForm = defineAsyncComponent(() => import('@/components/common/OpenRepositoryForm.vue'))
const groupForm = defineAsyncComponent(() => import('@/components/common/GroupForm.vue'))

export function addGroup () {
  showPageInModal(groupForm, {}, { width: '20%' })
}

export function renameGroup (groupId) {
  showPageInModal(groupForm, {params: {id: groupId}}, { width: '20%' })
}

export function openRepository () {
  showPageInModal(openForm, {}, {width: '30%'})
}
