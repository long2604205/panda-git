<template>
  <div
    ref="containerRef"
    class="custom-select-container"
  >
    <div
      class="custom-select-trigger"
      :class="{ active: open }"
      :data-value="modelValue"
      @click="toggle"
    >
      <span :title="selectedLabel">{{ selectedLabel }}</span>
      <i class="fa-solid fa-chevron-down" />
    </div>

    <div
      class="custom-select-menu"
      :class="{ open: open }"
    >
      <div class="search-box">
        <div class="search-icon">
          <i class="fa-solid fa-search" />
        </div>
        <input
          ref="searchInputRef"
          v-model="searchQuery"
          type="text"
          placeholder="Search..."
          @click.stop
        >
      </div>

      <div class="options-wrapper">
        <div
          v-for="item in filteredOptions"
          :key="item[value]"
          class="custom-option"
          :class="{ selected: item[value] === modelValue }"
          :data-value="item[value]"
          @click="choose(item)"
        >
          {{ item[text] }}
        </div>

        <div
          v-if="filteredOptions.length === 0"
          class="empty-state"
        >
          No results found
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: [String, Number, null],
  options: { type: Array, required: true },
  value: { type: String, default: 'value' },
  text: { type: String, default: 'text' },
  valueDefault: { type: [String, Number, null], default: null }
})

const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const searchQuery = ref('')
const searchInputRef = ref(null)
const containerRef = ref(null)

// -- LOGIC TOGGLE & FOCUS --
const toggle = async () => {
  open.value = !open.value

  if (open.value) {
    // Reset search khi mở lại
    searchQuery.value = ''
    // Đợi DOM render xong thì focus vào ô input
    await nextTick()
    searchInputRef.value?.focus()
  }
}

const choose = (item) => {
  emit('update:modelValue', item[props.value])
  open.value = false
  searchQuery.value = ''
}

// -- CLICK OUTSIDE (Để đóng menu khi click ra ngoài) --
const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    open.value = false
  }
}

onMounted(() => { document.addEventListener('click', handleClickOutside) })
onUnmounted(() => { document.removeEventListener('click', handleClickOutside) })

// -- AUTO DEFAULT VALUE --
watch(
  () => props.options,
  () => {
    if (props.modelValue == null && props.valueDefault != null) {
      emit('update:modelValue', props.valueDefault)
    }
  },
  { immediate: true }
)

// -- COMPUTED --
const selectedLabel = computed(() => {
  const found = props.options.find(o => o[props.value] === props.modelValue)
  return found ? found[props.text] : 'Select...'
})

// Logic Search
const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options
  const query = searchQuery.value.toLowerCase()
  return props.options.filter(item =>
    String(item[props.text]).toLowerCase().includes(query)
  )
})
</script>

<style lang="scss" scoped>
/* --- CONTAINER --- */
.custom-select-container {
  position: relative;
  /* width: 100% để nó luôn nằm gọn trong thẻ cha, không tự ý phình to */
  width: 100%;
  min-width: 130px;
  height: 26px;
}

/* --- TRIGGER (Dùng GRID để trị dứt điểm lỗi tràn text) --- */
.custom-select-trigger {
  background-color: var(--input-bg);
  border: 1px solid var(--border-color);
  color: var(--p-text-muted);
  font-size: 11px;
  padding: 0 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;

  /* LAYOUT GRID: Cột 1 (text) co giãn - Cột 2 (icon) tự động */
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 6px; /* Khoảng cách an toàn giữa text và icon */

  width: 100%;
  height: 100%;
  box-sizing: border-box; /* Tính cả border vào width */
  user-select: none;
}

.custom-select-trigger:hover {
  border-color: var(--p-text-dim);
  color: var(--text-color);
  background-color: var(--p-hover);
}

.custom-select-trigger.active {
  border-color: var(--accent-color);
  color: var(--text-color);
}

/* --- TEXT LABEL --- */
.custom-select-trigger span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  /* BẮT BUỘC: Để Grid hiểu là cột này có thể co nhỏ hơn nội dung của nó */
  min-width: 0;
  display: block; /* Đảm bảo hành vi block chuẩn */
}

/* --- ICON CHEVRON --- */
.custom-select-trigger i {
  transition: transform 0.2s ease;
  font-size: 10px;
  display: flex; /* Căn chỉnh icon chuẩn */
  align-items: center;
}

.custom-select-trigger.active i {
  transform: rotate(180deg);
}

/* --- MENU DROPDOWN --- */
.custom-select-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%; /* Bằng với container */

  display: flex;
  flex-direction: column;

  max-height: 250px;

  background-color: var(--menu-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
  z-index: 1000;

  opacity: 0;
  visibility: hidden;
  transform: translateY(-5px);
  transition: all 0.1s ease-in-out;
  pointer-events: none;
  box-sizing: border-box;
}

.custom-select-menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

/* --- SEARCH BOX --- */
.search-box {
  padding: 4px 6px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--menu-bg);
  position: sticky;
  top: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  z-index: 10;
}

.search-icon {
  font-size: 10px;
  color: var(--p-text-muted);
  display: flex; /* Căn giữa icon search */
}

.search-box input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-color);
  font-size: 11px;
  padding: 2px 0;
  min-width: 0; /* An toàn cho input flex */

  &::placeholder {
    color: var(--p-text-dim);
  }
}

/* --- OPTIONS LIST --- */
.options-wrapper {
  overflow-y: auto;
  flex: 1;
  padding: 4px 0;

  &::-webkit-scrollbar {
    width: 4px;
  }
  &::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 2px;
  }
}

/* --- OPTION ITEM --- */
.custom-option {
  padding: 6px 12px;
  font-size: 11px;
  color: var(--text-color);
  cursor: pointer;
  transition: background 0.1s;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.custom-option:hover {
  background-color: var(--p-selection);
  color: var(--accent-color);
}

.custom-option.selected {
  background-color: var(--p-hover);
  color: var(--accent-color);
  font-weight: 600;
  position: relative;
}

.custom-option.selected::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--accent-color);
}

.empty-state {
  padding: 8px 12px;
  font-size: 10px;
  color: var(--p-text-muted);
  text-align: center;
  font-style: italic;
}
</style>
