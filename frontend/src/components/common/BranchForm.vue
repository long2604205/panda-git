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
        >
      </div>
      <div class="flex gap-2 mb-4">
        <panda-checkbox
          v-model="isCheckout"
          label="Checkout branch"
          class="mb-3"
        />
        <panda-checkbox
          v-model="isOverwrite"
          label="Overwrite existing branch"
          class="mb-3"
        />
      </div>
    </template>
    <template #footer>
      <button
        class="btn btn-primary"
        @click="save"
      >
        <span>Save</span>
      </button>
      <button
        class="btn btn-secondary"
        @click="close"
      >
        <span>Close</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import {ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import PandaCheckbox from '@/components/common/PandaCheckbox.vue'

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
// Tách state checkbox
const isCheckout = ref(true)
const isOverwrite = ref(false)

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
</style>
