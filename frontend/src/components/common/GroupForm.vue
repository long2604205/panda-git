<template>
  <base-form
    ref="openForm"
    v-model="visible"
    :title="isEdit ? 'Rename group' : 'Add group'"
    @opened="onOpened"
  >
    <template #content>
      <label class="block text-xs text-[var(--p-text-muted)] mb-2">Group name</label>
      <div class="flex gap-2 mb-4">
        <input
          ref="groupInput"
          v-model="groupName"
          type="text"
          class="search-input w-full px-3 py-2 rounded border border-[var(--border-color)]"
          @keyup.enter="save"
          @keyup.esc="close"
        />
      </div>
    </template>
    <template #footer>
      <button class="btn btn-secondary" @click="close">Close</button>
      <button class="btn btn-primary" @click="save">Save</button>
    </template>
  </base-form>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import mitter from '@/plugins/mitter.js'
import {editGroup, findGroup} from "@/plugins/PandaDB.js";

const props = defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})

onMounted(async () => {
  if (props.params.id) {
    isEdit.value = true
    const group = await findGroup(props.params.id)
    if (group) groupName.value = group.name
  }
})

const visible = ref(false)
const openForm = ref(null)
const groupName = ref('')
const isEdit = ref(false)

const close = () => {
  openForm.value.close()
  groupName.value = ''
}

const save = async () => {
  if (!groupName.value.trim()) return

  if (isEdit.value) {
    const group = await editGroup(props.params.id, {name: groupName.value})
    mitter.emit('rename-group', {
      id: group.id,
      name: group.name,
      collapsed: group.collapsed,
    })
  }
  else {
    mitter.emit('add-group', {
      id: `group-${Date.now()}`,
      name: groupName.value,
      collapsed: true,
    })
  }

  close()
}

const groupInput = ref(null)

const onOpened = () => {
  groupInput.value?.focus()
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
