import { showPageInModal } from '@/services/modals.js'
import { defineAsyncComponent } from 'vue'

const openForm = defineAsyncComponent(() => import('@/components/common/OpenRepositoryForm.vue'))
const addGroupForm = defineAsyncComponent(() => import('@/components/common/GroupForm.vue'))

export function openRepository () {
  showPageInModal(openForm, {}, {width: '30%'})
}

export function addGroup () {
  showPageInModal(addGroupForm, {}, { width: '15%' })
}
