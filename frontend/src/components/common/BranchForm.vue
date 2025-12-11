<template>
  <base-form
    ref="openForm"
    v-model="visible"
    :title="isEdit ? 'rename branch' : 'create branch'"
    @opened="onOpened"
  >
    <template #content>
      <label class="block text-xs text-[var(--p-text-muted)] mb-2">Branch name</label>
      <div class="flex gap-2 mb-4">
        <input
          ref="branchInput"
          v-model="branchName"
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
import {ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'

defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})

const visible = ref(false)
const openForm = ref(null)
const branchName = ref('')
const isEdit = ref(false)

const close = () => {
  openForm.value.close()
  branchName.value = ''
}

const save = async () => {
  close()
}

const branchInput = ref(null)

const onOpened = () => {
  branchInput.value?.focus()
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
