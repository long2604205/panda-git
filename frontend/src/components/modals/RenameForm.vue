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

const props = defineProps({
  data: Object
})

const openForm = ref(null)
const visible = ref(false)
const newName = ref(props.data.name)

function refactorRepository(repo) {
  if (newName.value && newName.value !== repo.name) {
    window.electronAPI
      .renameRepository(repo.path, newName.value)
      .then((newPath) => {
        repo.name = newName.value
        repo.path = newPath

        // Update IndexDB
        updateRepoInDB(repo)
          .then(() => {
            // Thông báo thành công bằng alert component
            mitter.emit('alert', {
              message: `Repository renamed to "${repo.name}" successfully!`,
              type: 'success',
            })
          })
          .catch(err => {
            console.error('Failed to update IndexedDB', err)
            mitter.emit('alert', {
              message: `Repository renamed but failed to update DB: ${err}`,
              type: 'warning',
            })
          })
      })
      .catch((err) => {
        mitter.emit('alert', {
          message: `Rename failed: ${err}`,
          type: 'danger',
        })
      })
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
