<template>
  <base-form ref="openRepositoryForm" v-model="visible" title="Open Repository">
    <template #content>
      <div class="mb-3">
        <label for="clone-path" class="form-label">Repository Path</label>
        <div class="input-group">
          <input
            v-model="pathRepositories"
            type="text"
            class="form-control"
            id="clone-path"
            placeholder="Local directory path"
          />
          <button class="btn btn-open-local" type="button" id="browse-clone" @click="chooseFolder">
            <i class="fas fa-folder-open"></i>
          </button>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-cancel" data-bs-dismiss="modal">
        <span>Cancel</span>
      </button>
      <button type="button" class="btn btn-clone" id="clone-repo-confirm" @click="openRepository">
        <span>Open</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import { ref } from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import api from '@/plugins/api.js'
import mitter from '@/plugins/mitter.js'
import { useLoadingStore } from '@/stores/loadingStore.js'
import { useRepositoryStore } from '@/stores/repositoryStore.js'
import commonApi from '@/services/api/common.js'
import notify from '@/plugins/notify.js'

const openRepositoryForm = ref(null)
const visible = ref(false)
const pathRepositories = ref('')
const loading = useLoadingStore()
const repositoryStore = useRepositoryStore()
const chooseFolder = async () => {
  const selected = await window.electronAPI?.selectFolder()
  if (selected) {
    pathRepositories.value = selected
  }
}

function openRepository() {
  handleOpenRepo(pathRepositories.value)
  openRepositoryForm.value?.close()
  // mitter.emit('open-repository', pathRepositories.value)
}
async function handleOpenRepo(repoPath) {
  try {
    loading.show('Opening repository')

    const response = await commonApi.open({ repo_path: repoPath })

    const result = response.data

    if (result) {
      repositoryStore.setActiveRepo(result)

      mitter.emit('open-repository', result)

      notify.success('Open repository successfully')

    } else {
      notify.error(`Can not open repository for ${repoPath}`)
    }
  } catch (error) {
    notify.error(`Error: ${error.message}`)
  } finally {
    loading.hide()
  }
}
</script>
<style scoped>
* {
  font-size: 14px;
}
.btn-cancel,
.btn-clone,
.btn-clone:disabled {
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
