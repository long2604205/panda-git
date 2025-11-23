<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="Open Repository"
    @opened="onOpened"
  >
    <template #content>
      <label class="block text-xs text-[var(--p-text-muted)] mb-2">Repository path</label>
      <div class="flex gap-2 mb-4">
        <input
          ref="pathInput"
          v-model="pathRepository"
          type="text"
          class="search-input w-full px-3 py-2 rounded border border-[var(--border-color)]"
          @keyup.enter="openRepository"
          @keyup.esc="close"
        />
        <button class="btn btn-secondary">
          <i class="fa-regular fa-folder-open"/>
        </button>
      </div>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="close">Close</button>
      <button class="btn btn-primary" @click="openRepository">Open</button>
    </template>
  </base-form>
</template>

<script setup>
import { ref } from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import commonApi from '@/services/api/common.js'
import notify from '@/plugins/notify.js'
import { useLoadingStore } from '@/stores/loadingStore.js'
import mitter from '@/plugins/mitter.js'
const visible = ref(false);
const openForm = ref(null);
const pathRepository = ref('');
const loading = useLoadingStore()
const pathInput = ref(null)

const close = () => {
  openForm.value.close()
}

function openRepository() {
  handleOpenRepo(pathRepository.value)
  close()
  // mitter.emit('open-repository', pathRepositories.value)
}
async function handleOpenRepo(pathRepository) {
  try {
    loading.show('Opening repository')

    const response = await commonApi.open({ repo_path: pathRepository })

    const result = response.data

    if (result) {
      // repositoryStore.setActiveRepo(result)

      mitter.emit('open-repository', result)

      notify.success('Open repository successfully')

    } else {
      notify.error(`Can not open repository for ${pathRepository}`)
    }
  } catch (error) {
    notify.error(`Error: ${error.message}`)
  } finally {
    loading.hide()
  }
}

const onOpened = () => {
  pathInput.value?.focus()
}
</script>

<style scoped></style>
