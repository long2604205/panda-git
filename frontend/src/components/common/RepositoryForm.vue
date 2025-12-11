<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="Rename repository"
    @opened="onOpened"
  >
    <template #content>
      <label class="block text-xs text-[var(--p-text-muted)] mb-2">Name</label>
      <div class="flex gap-2 mb-4">
        <input
          ref="repositoryInput"
          v-model="repositoryName"
          type="text"
          class="search-input w-full px-3 py-2 rounded border border-[var(--border-color)]"
          @keyup.enter="save"
          @keyup.esc="close"
        />
      </div>
    </template>
    <template #footer>
      <button
        class="btn btn-secondary"
        @click="close"
      >
        <span>Close</span>
      </button>
      <button
        class="btn btn-primary"
        @click="save"
      >
        <span>Save</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import mitter from '@/plugins/mitter.js'
import {findRepos} from '@/plugins/PandaDB.js'
import notify from '@/plugins/notify.js'
import commonApi from '@/services/api/common.js'

const props = defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})

onMounted(async () => {
  if (props.params.data) {
    const repo = await findRepos(props.params.data.path)
    if (repo) repositoryName.value = repo.name
  }
})

const visible = ref(false)
const openForm = ref(null)
const repositoryName = ref('')

const close = () => {
  openForm.value.close()
  repositoryName.value = ''
}

const repositoryInput = ref(null)

const onOpened = () => {
  repositoryInput.value?.focus()
}

async function save() {
  const loadingId = notify.loading('Đang tải dữ liệu...')
  try {
    const response = await commonApi.rename({
      repo_path: props.params.data.path,
      new_name: repositoryName.value
    })
    const result = response.data
    if (!result) return

    mitter.emit('repository-renamed', {
      oldPath: props.params.data.path,
      name: result.name,
      path: result.path
    })
    notify.remove(loadingId)
    notify.info('Active successfully')
  } catch (error) {
    notify.remove(loadingId)
    notify.error(`Failed: ${error.message}`)
  }
  close()
}
</script>

<style scoped>
.btn {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-secondary {
  background-color: transparent;
  border-color: var(--p-text-muted);
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: var(--bg-side);
}

.btn-primary {
  background-color: var(--accent-color);
  color: #000;
  font-weight: 600;
}

.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 10px var(--p-selection);
}
</style>
