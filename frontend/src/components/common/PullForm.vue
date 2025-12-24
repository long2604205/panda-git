<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="pull changes"
    @opened="onOpened"
  >
    <template #content>
      <div class="w-full p-4 flex flex-col gap-2">
        <div>
          <label class="input-group-label">Branch to merge</label>
          <div class="flex gap-2">
            <div class="w-[30%]">
              <input
                disabled
                value="origin"
                type="text"
                class="search-input w-full bg-[var(--input-bg)] border border-[var(--border-color)] text-[var(--text-color)] text-xs rounded px-3 py-1.5 outline-none focus:border-[var(--accent-color)] transition-colors disabled:opacity-70"
              >
            </div>

            <div class="flex-1">
              <panda-select-search
                v-model="selectedBranch"
                style="width: 100%; height: 100%"
                :options="getLocalBranches(repositoryStore.localBranches)"
                value="id"
                text="label"
                value-default="changes"
              />
            </div>
          </div>
        </div>

        <div>
          <label class="input-group-label">Strategy</label>
          <div class="segmented-control">
            <label class="flex-1">
              <input
                v-model="selectedStrategy"
                type="radio"
                name="strategy"
                value="merge"
                class="segmented-input hidden"
                checked
              >
              <div class="segmented-item">
                <i class="fa-solid fa-code-merge text-[10px]" /> Merge
              </div>
            </label>
            <label class="flex-1">
              <input
                v-model="selectedStrategy"
                type="radio"
                name="strategy"
                value="rebase"
                class="segmented-input hidden"
              >
              <div class="segmented-item">
                <i class="fa-solid fa-list-ol text-[10px]" /> Rebase
              </div>
            </label>
          </div>
          <p
            class="text-[10px] text-[var(--p-text-dim)] mt-2 italic"
          >
            {{ strategy[selectedStrategy] }}
          </p>
        </div>

        <div
          v-if="hasCheckedOptions"
          class="flex flex-wrap gap-2 animate-fade-in"
        >
          <div
            v-for="opt in pullOptions"
            v-show="opt.checked"
            :key="'tag-' + opt.id"
            class="tag-item"
          >
            <span class="tag-text">{{ opt.flag }}</span>
            <button
              class="tag-close-btn"
              @click="opt.checked = false"
            >
              <i class="fa-solid fa-xmark" />
            </button>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex w-full items-center justify-between">
        <div
          ref="dropdownContainer"
          class="relative"
        >
          <button
            class="flex items-center gap-1.5 text-[11px] font-medium text-[#e67e22] hover:text-[#d35400] transition-colors outline-none select-none"
            @click.stop="toggleDropdown"
          >
            <i class="fa-regular fa-circle-question" />
            Modify options
            <i
              class="fa-solid fa-chevron-down text-[9px] opacity-70 transition-transform duration-200"
              :class="{'rotate-180': showOptions}"
            />
          </button>

          <div
            v-if="showOptions"
            class="options-dropdown"
          >
            <div class="dropdown-header">
              Add Pull Options
            </div>

            <div class="flex flex-col py-1">
              <label
                v-for="option in pullOptions"
                :key="option.id"
                class="dropdown-item"
                :class="{ 'disabled-option': option.disabled }"
                @click.stop
              >
                <input
                  v-model="option.checked"
                  type="checkbox"
                  class="hidden"
                  :disabled="option.disabled"
                >
                <div class="flex-1 flex justify-between items-center">
                  <span
                    class="text-[11px]"
                    :class="option.checked ? 'text-[var(--accent-color)] font-medium' : 'text-[var(--text-color)]'"
                  >
                    {{ option.label }}
                  </span>
                  <span class="text-[10px] text-[var(--p-text-dim)] font-mono ml-3">
                    {{ option.flag }}
                  </span>
                </div>
                <div class="w-4 flex justify-end">
                  <i
                    v-if="option.checked"
                    class="fa-solid fa-check text-[10px] text-[var(--accent-color)]"
                  />
                </div>
              </label>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            class="btn btn-primary"
            @click="save"
          >
            Pull
          </button>
          <button
            class="btn btn-secondary"
            @click="close"
          >
            Cancel
          </button>
        </div>
      </div>
    </template>
  </base-form>
</template>

<script setup>
import {onMounted, onUnmounted, ref, watch, computed} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import mitter from '@/plugins/mitter.js'
import {editGroup, findGroup} from '@/plugins/PandaDB.js'
import PandaSelectSearch from '@/components/common/PandaSelectSearch.vue'
import { useRepositoryStore } from '@/stores/repositoryStore.js'

const props = defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})

// --- DATA ---
const visible = ref(false)
const openForm = ref(null)
const groupName = ref('')
const isEdit = ref(false)
const groupInput = ref(null)
const selectedStrategy = ref('merge')
const showOptions = ref(false) // Toggle dropdown
const dropdownContainer = ref(null)
const repositoryStore = useRepositoryStore()
// --- OPTIONS CONFIG ---
const strategy = {
  merge: 'Create a merge commit to combine changes.',
  rebase: 'Replay local commits on top of incoming changes.'
}
const selectedBranch = ref(repositoryStore.branchName)
const pullOptions = ref([
  {
    id: 'ffonly',
    label: 'Merge only if it can be fast-forwarded',
    flag: '--ff-only',
    checked: false,
    disabled: false
  },
  {
    id: 'noff',
    label: 'Merge only if it can be fast-forwarded',
    flag: '--no-ff',
    checked: false,
    disabled: false
  },
  {
    id: 'squash',
    label: 'Create a single commit for all pulled changes',
    flag: '--squash',
    checked: false,
    disabled: false
  },
  {
    id: 'nocommit',
    label: 'Merge, but do not commit the result',
    flag: '--no-commit',
    checked: false,
    disabled: false
  },
  {
    id: 'noverify',
    label: 'Bypass the pre-merge and commit message hooks',
    flag: '--no-verify',
    checked: false,
    disabled: false
  }
])

// --- COMPUTED ---
const hasCheckedOptions = computed(() => {
  return pullOptions.value.some(opt => opt.checked)
})

// --- METHODS ---
function getLocalBranches(arr) {
  return arr.map(item => ({
    id: item,
    label: item
  }))
}

// Xử lý đóng Dropdown khi click ra ngoài
const handleClickOutside = (event) => {
  if (dropdownContainer.value && !dropdownContainer.value.contains(event.target)) {
    showOptions.value = false
  }
}

const toggleDropdown = () => {
  showOptions.value = !showOptions.value
}

const onOpened = () => {
  groupInput.value?.focus()
  // Reset trạng thái dropdown khi mở form
  showOptions.value = false
}

const close = () => {
  openForm.value.close()
  groupName.value = ''
  showOptions.value = false
}

// Logic Save/Pull (Mô phỏng)
const save = async () => {
  if (!groupName.value.trim() && isEdit.value) return // Check tạm

  // Gom các flag đã chọn
  const activeFlags = pullOptions.value
      .filter(opt => opt.checked)
      .map(opt => opt.flag)

  console.log('Pulling with strategy:', selectedStrategy.value)
  console.log('Options:', activeFlags)

  // ... (Logic backend cũ của bạn) ...
  if (isEdit.value) {
    const group = await editGroup(props.params.id, {name: groupName.value})
    mitter.emit('rename-group', { id: group.id, name: group.name, collapsed: group.collapsed })
  } else {
    mitter.emit('add-group', { id: `group-${Date.now()}`, name: groupName.value || 'New Group', collapsed: true })
  }
  close()
}

// --- LIFECYCLE ---
onMounted(async () => {
  if (props.params.id) {
    isEdit.value = true
    const group = await findGroup(props.params.id)
    if (group) groupName.value = group.name
  }
  // Lắng nghe click outside để đóng dropdown
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// --- WATCHERS ---
// Logic Rebase vs Merge (Disable các options không tương thích)
watch(selectedStrategy, (newStrategy) => {
  if (newStrategy === 'rebase') {
    pullOptions.value.forEach(opt => {
      // Chỉ cho phép --no-verify khi rebase (theo logic cũ)
      if (opt.id !== 'noverify') {
        opt.disabled = true
        opt.checked = false
      }
    })
  } else {
    pullOptions.value.forEach(opt => {
      opt.disabled = false
    })
  }
})
</script>

<style scoped>
:deep(.modal-body) {
  padding: 0 !important;
}

/* --- FORM TEXT & INPUTS --- */
.input-group-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--p-text-dim);
    margin-bottom: 4px;
    display: block;
}

.custom-select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 8px center;
    background-size: 12px;
}

/* --- SEGMENTED CONTROL --- */
.segmented-control {
    display: flex;
    background-color: var(--input-bg);
    padding: 3px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
}

.segmented-item {
    flex: 1;
    text-align: center;
    padding: 5px 0;
    font-size: 12px;
    font-weight: 500;
    color: var(--p-text-muted);
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.segmented-item:hover {
    color: var(--text-color);
}

.segmented-input:checked + .segmented-item {
    background-color: var(--p-hover);
    color: var(--accent-color);
    font-weight: 600;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

/* --- TAGS (CHIPS) STYLE --- */
.tag-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background-color: var(--input-bg);
    border: 1px solid var(--border-color);
    color: var(--text-color);
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 10px;
    font-family: "JetBrains Mono", monospace;
    user-select: none;
    transition: all 0.2s;
}

.tag-item:hover {
    border-color: var(--p-text-dim);
}

.tag-close-btn {
    border: none;
    background: transparent;
    cursor: pointer;
    padding: 0;
    font-size: 10px;
    color: var(--p-text-dim);
    display: flex;
    align-items: center;
    transition: color 0.2s;
}

.tag-close-btn:hover {
    color: #e74c3c; /* Màu đỏ khi hover nút xóa */
}

/* --- DROPDOWN MENU STYLE --- */
.options-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    margin-top: 6px;
    width: 400px; /* Rộng vừa phải */
    background-color: var(--bg-side); /* Hoặc màu nền đậm #1e1e1e */
    border: 1px solid var(--border-color);
    border-radius: 6px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    z-index: 50;
    overflow: hidden;
    animation: fadeIn 0.1s ease-out;
}

.dropdown-header {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--p-text-dim);
    padding: 8px 12px;
    border-bottom: 1px solid var(--border-color);
    background-color: rgba(0,0,0,0.1);
}

.dropdown-item {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    cursor: pointer;
    transition: background 0.15s;
    user-select: none;
}

.dropdown-item:hover {
    background-color: var(--p-hover);
}

.disabled-option {
    opacity: 0.4;
    pointer-events: none;
    cursor: not-allowed;
    background-color: transparent !important;
}

/* --- UTILS --- */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
    animation: fadeIn 0.2s ease-out;
}
</style>
