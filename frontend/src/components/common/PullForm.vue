<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="pull changes"
    @opened="onOpened"
  >
    <template #content>
      <div class="flex">
        <!-- LEFT COLUMN: MAIN CONFIG (55%) -->
        <!-- GIẢM PADDING: p-5 -> p-4 -->
        <div class="w-[55%] p-4 flex flex-col gap-5 border-r border-[var(--border-color)]">
          <!-- Remote Selection -->
          <div>
            <label class="input-group-label">Remote</label>
            <select class="custom-select w-full bg-[var(--input-bg)] border border-[var(--border-color)] text-[var(--text-color)] text-xs rounded px-3 py-1.5 outline-none focus:border-[var(--accent-color)] transition-colors">
              <option value="origin">
                origin
              </option>
              <option value="upstream">
                upstream
              </option>
            </select>
          </div>

          <!-- Branch Selection -->
          <div>
            <label class="input-group-label">Branch to merge</label>
            <select class="custom-select w-full bg-[var(--input-bg)] border border-[var(--border-color)] text-[var(--text-color)] text-xs rounded px-3 py-1.5 outline-none focus:border-[var(--accent-color)] transition-colors font-mono">
              <option value="main">
                main
              </option>
              <option value="develop">
                develop
              </option>
              <option value="feature/new-ui">
                feature/new-ui
              </option>
            </select>
          </div>

          <!-- Strategy: Segmented Control -->
          <div>
            <label class="input-group-label mb-2">Strategy</label>
            <div class="segmented-control">
              <label class="flex-1">
                <input
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
              id="strategy-desc"
              class="text-[10px] text-[var(--p-text-dim)] mt-2 italic"
            >
              Create a merge commit to combine changes.
            </p>
          </div>
        </div>

        <!-- RIGHT COLUMN: OPTIONS (45%) -->
        <!-- GIẢM PADDING: p-5 -> p-4 -->
        <div class="w-[45%] bg-[var(--bg-side)] p-4 flex flex-col">
          <label class="input-group-label mb-2">Options</label>

          <div class="flex flex-col gap-0.5">
            <label class="option-item">
              <input
                type="checkbox"
                class="option-checkbox"
                checked
              >
              <div class="option-content">
                <span class="option-text">Prune remote</span>
                <span class="option-subtext">--prune</span>
              </div>
            </label>

            <label class="option-item">
              <input
                type="checkbox"
                class="option-checkbox"
              >
              <div class="option-content">
                <span class="option-text">Auto stash</span>
                <span class="option-subtext">--auto stash</span>
              </div>
            </label>

            <label class="option-item">
              <input
                type="checkbox"
                class="option-checkbox"
              >
              <div class="option-content">
                <span class="option-text">Fast-forward only</span>
                <span class="option-subtext">--ff-only</span>
              </div>
            </label>

            <label class="option-item">
              <input
                type="checkbox"
                class="option-checkbox"
              >
              <div class="option-content">
                <span class="option-text">Squash commits</span>
                <span class="option-subtext">--squash</span>
              </div>
            </label>

            <label class="option-item">
              <input
                type="checkbox"
                class="option-checkbox"
              >
              <div class="option-content">
                <span class="option-text">No commit</span>
                <span class="option-subtext">--no-commit</span>
              </div>
            </label>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
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
    </template>
  </base-form>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import mitter from '@/plugins/mitter.js'
import {editGroup, findGroup} from '@/plugins/PandaDB.js'

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

const descs = ref({
        merge: 'Create a merge commit to combine changes.',
        rebase: 'Replay local commits on top of incoming changes.'
    })
</script>

<style scoped>
:deep(.modal-body) {
  padding: 0 !important;
}
/* --- FORM ELEMENTS --- */
.input-group-label {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--p-text-dim);
            margin-bottom: 6px;
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
            padding: 5px 0; /* Giảm padding */
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

        /* --- CHECKBOXES --- */
        .option-checkbox {
            appearance: none;
            width: 14px;
            height: 14px;
            border: 1px solid var(--p-text-dim);
            border-radius: 3px;
            background-color: var(--input-bg);
            cursor: pointer;
            position: relative;
            flex-shrink: 0;
            transition: all 0.2s;
            margin-top: 0; /* Bỏ margin-top để căn giữa chuẩn hơn khi cùng dòng */
        }

        .option-checkbox:checked {
            background-color: var(--accent-color);
            border-color: var(--accent-color);
        }

        .option-checkbox:checked::after {
            content: '✓';
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: #000;
            font-weight: bold;
        }

        .option-item {
            display: flex;
            align-items: center; /* Căn giữa theo chiều dọc */
            gap: 10px;
            padding: 6px 8px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .option-item:hover {
            background-color: var(--p-hover);
        }

        .option-content {
            display: flex;
            flex-direction: row; /* Chuyển thành hàng ngang */
            flex: 1; /* Lấp đầy khoảng trống còn lại */
            justify-content: space-between; /* Đẩy Text sang trái, Flag sang phải */
            align-items: baseline; /* Căn chân chữ cho đẹp */
        }

        .option-text {
            font-size: 11px;
            color: var(--p-text-muted);
            line-height: 1.2;
            white-space: nowrap; /* Đảm bảo không bị xuống dòng */
        }

        .option-subtext {
            font-size: 10px; /* Tăng nhẹ size lên chút cho dễ đọc */
            color: var(--p-text-dim);
            font-family: "JetBrains Mono", monospace;
        }
</style>
