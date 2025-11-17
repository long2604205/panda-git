<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="Rename">
    <template #content>
      <div class="mb-3">
        <label for="clone-url" class="form-label">
          Rename repository
          <strong>{{ props.data.name }}</strong>
          and its usages to:
        </label>
        <input
          v-model="newName"
          type="text"
          class="form-control"
          />
      </div>
    </template>
    <template #footer>
      <button
        type="button"
        class="btn btn-clone"
        @click="refactorRepository(props.data)"
      >
        <span>Refactor</span>
      </button>
      <button
        type="button"
        class="btn btn-cancel"
        data-bs-dismiss="modal"
        @click="close"
      >
        <span>Cancel</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import BaseForm from '@/components/common/BaseForm.vue'
import { ref } from 'vue'
import { updateRepoInDB } from '@/plugins/indexedDB.js'
import mitter from '@/plugins/mitter.js'
import api from '@/plugins/api.js'
import { useLoadingStore } from '@/stores/loadingStore.js'

const props = defineProps({
  data: Object
})

const openForm = ref(null)
const visible = ref(false)
const newName = ref(props.data.name)
const loading = useLoadingStore()

async function refactorRepository(repo) {
  if (newName.value && newName.value !== repo.name) {
    try {
      loading.show(`Renaming "${repo.name}"...`)

      // Gọi backend rename
      const res = await api.post('/rename', {
        repo_path: repo.path,
        new_name: newName.value
      })

      if (res?.data?.data) {
        repo.name = res.data.data.name
        repo.path = res.data.data.path
        await updateRepoInDB(repo)
      }

      mitter.emit('alert', {
        message: res?.data?.message || 'Rename failed!',
        type: 'info',
      })

      openForm.value?.close()
    } catch (err) {
      openForm.value?.close()
      mitter.emit('alert', {
        message: err.res?.data?.message || err.message || 'Rename failed!',
        type: 'danger',
      })
      console.error(err)
      throw err
    } finally {
      openForm.value?.close()
      loading.hide()
    }
  }
}
</script>
<style scoped>
*{
  font-size: 14px;
}

.btn-cancel, .btn-clone, .btn-clone:disabled {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: var(--bg-tertiary);
  font-size: 14px;
  font-weight: 500;
}
.btn-clone:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.btn-cancel:hover {
  background: var(--bs-red);
  color: var(--text-primary);
}

input {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 14px;
  resize: none;
  min-height: 80%;
}

input::placeholder {
  color: var(--text-muted);
}

input:focus {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  box-shadow: none;
}

input:focus-visible {
  outline: none;
  border: 1px solid var(--border-color);
}
</style>
