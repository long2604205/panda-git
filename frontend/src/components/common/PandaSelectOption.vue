<template>
  <div class="custom-select-container" ref="containerRef">
    <!-- Trigger -->
    <div
      class="custom-select-trigger"
      :class="{ active: open }"
      @click="toggle"
      :data-value="modelValue"
    >
      <span>{{ selectedLabel }}</span>
      <i class="fa-solid fa-chevron-down"></i>
    </div>

    <!-- Menu -->
    <div
      class="custom-select-menu"
      :class="{ open: open }"
    >
      <div
        v-for="item in options"
        :key="item[value]"
        class="custom-option"
        :class="{ selected: item[value] === modelValue }"
        :data-value="item[value]"
        @click="choose(item)"
      >
        {{ item[text] }}
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, watch, onMounted, onUnmounted} from "vue";

const props = defineProps({
  modelValue: [String, Number, null],
  options: { type: Array, required: true },
  /** field name để lấy value */
  value: { type: String, default: "value" },

  /** field name để lấy label */
  text: { type: String, default: "text" },

  /** giá trị mặc định nếu chưa chọn */
  valueDefault: { type: [String, Number, null], default: null }
});
// -- REF --
const containerRef = ref(null);

const emit = defineEmits(["update:modelValue"]);

const open = ref(false);

const toggle = () => (open.value = !open.value);

const choose = (item) => {
  emit("update:modelValue", item[props.value]);
  open.value = false;
};

// -- CLICK OUTSIDE (Để đóng menu khi click ra ngoài) --
const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    open.value = false;
  }
};

onMounted(() => { document.addEventListener('click', handleClickOutside); });
onUnmounted(() => { document.removeEventListener('click', handleClickOutside); });

/** Tự gán valueDefault nếu modelValue chưa có */
watch(
  () => props.options,
  () => {
    if (props.modelValue == null && props.valueDefault != null) {
      emit("update:modelValue", props.valueDefault);
    }
  },
  { immediate: true }
);

const selectedLabel = computed(() => {
  const found = props.options.find(o => o[props.value] === props.modelValue);
  return found ? found[props.text] : "";
});
</script>

<style lang="scss" scoped>
/* CUSTOM DROPDOWN CSS (FIXED) */
.custom-select-container {
  position: relative;
  min-width: 130px; /* Width tối thiểu của input */
  max-width: 100%;  /* Để nó không bị tràn ra ngoài cha */
  height: 26px;
}
.custom-select-trigger {
  background-color: var(--input-bg);
  border: 1px solid var(--border-color);
  color: var(--p-text-muted);
  font-size: 11px;
  padding: 0 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
  height: 100%;
  overflow: hidden;
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

/* Span chứa text trong Trigger */
.custom-select-trigger span {
  /* 3 dòng này tạo dấu ... */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  flex: 1; /* Chiếm hết chỗ trống còn lại */
  margin-right: 4px; /* Cách icon ra 1 chút */
}

.custom-select-trigger i {
  transition: transform 0.2s ease;
  margin-left: 8px;
  font-size: 10px;
}

.custom-select-trigger.active i {
  transform: rotate(180deg);
}

/* FIXED MENU STYLES */
.custom-select-menu {
  position: absolute;
  top: 100%;
  left: 0;
  /* width: 100%; Ensure menu fits trigger width */
  width: 100%; /* Can be wider if content needs it */

  /* IMPORTANT FIXES FOR OVERFLOW */
  max-height: 250px; /* Fix height issue */
  overflow-y: auto; /* Add scrollbar */

  background-color: var(--menu-bg); /* Solid background */
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6); /* Stronger shadow */
  z-index: 1000; /* High Z-index to sit on top */

  /* Animation States */
  opacity: 0;
  visibility: hidden;
  transform: translateY(-5px);
  transition: all 0.1s ease-in-out;
  pointer-events: none;
  /* Đảm bảo padding không làm phình width */
  box-sizing: border-box;
}

.custom-select-menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

.custom-option {
  padding: 6px 12px;
  font-size: 11px;
  color: var(--text-color);
  cursor: pointer;
  transition: background 0.1s;
  align-items: center;

  /* QUAN TRỌNG: Xử lý dấu ... */
  white-space: nowrap;      /* Không xuống dòng */
  overflow: hidden;         /* Ẩn phần thừa */
  text-overflow: ellipsis;  /* Thêm dấu ... */

  display: block; /* Đổi về block để text-overflow hoạt động tốt hơn flex trong trường hợp này */
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
</style>
