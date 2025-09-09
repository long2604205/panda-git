<template>
  <base-form
    ref="openCloneRepositoryForm"
    v-model="visible"
    title="Open Repository">
    <template #content>
      <div class="mb-3">
        <label for="clone-url" class="form-label">Repository URL</label>
        <input
          v-model="repoUrl"
          type="text"
          class="form-control"
          placeholder="url">
      </div>
      <div class="mb-3">
        <label for="clone-path" class="form-label">Local Path</label>
        <div class="input-group">
          <input
            v-model="localPath"
            type="text"
            class="form-control"
            placeholder="Local directory path">
          <button
            class="btn btn-open-local"
            type="button"
            @click="chooseFolder">
            <i class="fas fa-folder-open"></i>
          </button>
        </div>
      </div>
    </template>
    <template #footer>
      <button
        type="button"
        class="btn btn-cancel"
        data-bs-dismiss="modal">
        <span>Cancel</span>
      </button>
      <button
        type="button"
        class="btn btn-clone"
        @click="cloneRepository">
        <span>Clone</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import BaseForm from '@/components/modals/BaseForm.vue'
import { ref } from 'vue'
import api from '@/plugins/api.js'
import mitter from '@/plugins/mitter.js'
import { useLoadingStore } from '@/stores/loadingStore.js'

const openCloneRepositoryForm = ref(null)
const visible = ref(false)
const repoUrl = ref('')
const localPath = ref('')
const loading = useLoadingStore()

const chooseFolder = async () => {
  const selected = await window.electronAPI?.selectFolder()
  if (selected) {
    localPath.value = selected
  }
}

function cloneRepository (){
  handleCloneRepo(repoUrl.value, localPath.value)
  openCloneRepositoryForm.value?.close()
}

async function handleCloneRepo(repoPath, localPath) {
  try {
    loading.show('Cloning...')
    const response = await api.post('/clone', {
      repo_url: repoPath,
      destination: localPath
    });

    const result = response.data.data

    if (result) {
      mitter.emit('open-repository', result)
      mitter.emit('alert', {
        message: 'Clone successfully!',
        type: 'success'
      })
    } else {
      mitter.emit('alert', {
        message: 'Failed to open repository: No data returned',
        type: 'error'
      })
    }

  } catch (error) {
    mitter.emit('alert', {
      message: `Error opening repository: ${error.message}`,
      type: 'error'
    })
  } finally {
    loading.hide()
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

.btn-open-local {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: var(--bg-tertiary);
  font-size: 14px;
  font-weight: 500;
}

.btn-open-local:hover {
  background: var(--bg-tertiary);
}
</style>
