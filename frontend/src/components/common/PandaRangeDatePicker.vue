<template>
  <div class="date-picker-container" ref="containerRef">
    <div
      class="date-picker-trigger"
      :class="{ active: open }"
      @click="toggle"
    >
      <div class="trigger-content">
        <i class="fa-regular fa-calendar text-[10px] mr-1.5 opacity-70"></i>
        <span>{{ displayLabel }}</span>
      </div>
      <i class="fa-solid fa-chevron-down arrow-icon"></i>
    </div>

    <div class="date-picker-menu" :class="{ open: open }" @click.stop>

      <div v-if="currentView === 'main'" class="view-main">
        <div class="presets-list">
          <div
            v-for="preset in presets"
            :key="preset.key"
            class="preset-item"
            :class="{ active: currentPreset === preset.key }"
            @click="selectPreset(preset)"
          >
            <span>{{ preset.label }}</span>
            <i v-if="currentPreset === preset.key" class="fa-solid fa-check check-icon"></i>
          </div>
        </div>

        <div class="separator"></div>

        <div class="custom-range-inputs">
          <div class="input-group">
            <label>FROM</label>
            <div
              class="fake-input"
              :class="{ active: picking === 'from' }"
              @click="openCalendar('from')"
            >
              {{ formatDate(tempRange.from) || 'mm/dd/yyyy' }}
              <i class="fa-regular fa-calendar icon"></i>
            </div>
          </div>
          <div class="input-group">
            <label>TO</label>
            <div
              class="fake-input"
              :class="{ active: picking === 'to' }"
              @click="openCalendar('to')"
            >
               {{ formatDate(tempRange.to) || 'mm/dd/yyyy' }}
               <i class="fa-regular fa-calendar icon"></i>
            </div>
          </div>
        </div>

        <div class="picker-footer">
          <button class="btn-cancel" @click="close">Cancel</button>
          <button class="btn-apply" @click="apply">Apply</button>
        </div>
      </div>

      <div v-else class="view-calendar">
        <div class="cal-header">
          <div class="cal-nav-btn" @click="changeMonth(-1)">
            <i class="fa-solid fa-chevron-left"></i>
          </div>
          <div class="cal-title">
            {{ monthNames[calMonth] }} {{ calYear }}
          </div>
          <div class="cal-nav-btn" @click="changeMonth(1)">
            <i class="fa-solid fa-chevron-right"></i>
          </div>
        </div>

        <div class="cal-grid">
          <div v-for="day in weekDays" :key="day" class="cal-cell weekday">{{ day }}</div>

          <div v-for="n in firstDayOfMonth" :key="'empty-'+n" class="cal-cell empty"></div>

          <div
            v-for="date in daysInMonth"
            :key="date"
            class="cal-cell day"
            :class="{
              'selected': isSelected(date),
              'today': isToday(date),
              'disabled': isDisabled(date)
            }"
            @click="selectDate(date)"
          >
            {{ date }}
          </div>
        </div>

        <div class="cal-footer">
            <span class="back-btn" @click="currentView = 'main'">
                <i class="fa-solid fa-arrow-left"></i> Back
            </span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

const props = defineProps({
  modelValue: { type: Object, default: () => ({ from: null, to: null }) },
});

const emit = defineEmits(["update:modelValue"]);

// --- STATE ---
const open = ref(false);
const containerRef = ref(null);
const currentView = ref('main');
const picking = ref(null);
const currentPreset = ref('all');
const tempRange = ref({ from: null, to: null });

// Calendar Init
const today = new Date();
const calYear = ref(today.getFullYear());
const calMonth = ref(today.getMonth());

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const weekDays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
const presets = [
  { label: 'All Time', key: 'all', days: null },
  { label: 'Today', key: 'today', days: 0 },
  { label: 'Last 7 Days', key: '7d', days: 7 },
  { label: 'Last 30 Days', key: '30d', days: 30 },
];

// --- LOGIC ---
const daysInMonth = computed(() => new Date(calYear.value, calMonth.value + 1, 0).getDate());
const firstDayOfMonth = computed(() => new Date(calYear.value, calMonth.value, 1).getDay());

const changeMonth = (step) => {
  let m = calMonth.value + step;
  if (m > 11) { m = 0; calYear.value++; }
  else if (m < 0) { m = 11; calYear.value--; }
  calMonth.value = m;
};

const openCalendar = (type) => {
  picking.value = type;
  currentView.value = 'calendar';

  let targetDateStr = type === 'from' ? tempRange.value.from : tempRange.value.to;
  if (type === 'to' && !targetDateStr && tempRange.value.from) {
    targetDateStr = tempRange.value.from;
  }

  if (targetDateStr) {
      const d = new Date(targetDateStr);
      calYear.value = d.getFullYear();
      calMonth.value = d.getMonth();
  } else {
      const now = new Date();
      calYear.value = now.getFullYear();
      calMonth.value = now.getMonth();
  }
};

const isDisabled = (day) => {
  if (picking.value === 'to' && tempRange.value.from) {
    const cellDate = new Date(calYear.value, calMonth.value, day);
    cellDate.setHours(0, 0, 0, 0);
    const fromDate = new Date(tempRange.value.from);
    fromDate.setHours(0, 0, 0, 0);
    return cellDate < fromDate;
  }
  return false;
};

const selectDate = (day) => {
  if (isDisabled(day)) return;

  const y = calYear.value;
  const m = String(calMonth.value + 1).padStart(2, '0');
  const d = String(day).padStart(2, '0');
  const isoDate = `${y}-${m}-${d}`;

  if (picking.value === 'from') {
    tempRange.value.from = isoDate;
    if (tempRange.value.to && tempRange.value.to < isoDate) {
        tempRange.value.to = null;
    }
  } else {
    tempRange.value.to = isoDate;
  }

  currentView.value = 'main';
  currentPreset.value = 'custom';
};

const isSelected = (day) => {
  if (!picking.value) return false;
  const target = picking.value === 'from' ? tempRange.value.from : tempRange.value.to;
  if (!target) return false;

  const d = new Date(target);
  return d.getDate() === day && d.getMonth() === calMonth.value && d.getFullYear() === calYear.value;
};

const isToday = (day) => {
    const now = new Date();
    return day === now.getDate() && calMonth.value === now.getMonth() && calYear.value === now.getFullYear();
}

const selectPreset = (preset) => {
  currentPreset.value = preset.key;
  if (preset.key === 'all') {
    tempRange.value = { from: null, to: null };
  } else {
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - preset.days);
    const format = (d) => {
        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${y}-${m}-${day}`;
    };
    tempRange.value = { from: format(start), to: format(end) };
  }
};

const formatDate = (isoStr) => {
    if(!isoStr) return '';
    const [y, m, d] = isoStr.split('-');
    return `${m}/${d}/${y}`;
};

const displayLabel = computed(() => {
  if (currentPreset.value === 'all') return 'All Time';
  if (props.modelValue.from && props.modelValue.to) {
    return `${formatDate(props.modelValue.from)} - ${formatDate(props.modelValue.to)}`;
  }
  return 'Select Date';
});

const toggle = () => {
  open.value = !open.value;
  if (open.value) {
    tempRange.value = { ...props.modelValue };
    currentView.value = 'main';
  }
};

const close = () => { open.value = false; };
const apply = () => { emit("update:modelValue", { ...tempRange.value }); close(); };

// --- CLICK OUTSIDE LOGIC ---
// Trigger không còn @click.stop, nên click vào Trigger sẽ lan ra document.
// Các menu khác sẽ bắt được sự kiện này và tự đóng lại thông qua logic này:
const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    close();
  }
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onUnmounted(() => document.removeEventListener('click', handleClickOutside));
</script>

<style scoped>
/* --- CONTAINER --- */
.date-picker-container {
  position: relative;
  /* QUAN TRỌNG: Tăng min-width lên để Input to bằng cái Lịch (Lịch cần ~260px) */
  min-width: 260px;
  height: 26px;
}

/* --- TRIGGER --- */
.date-picker-trigger {
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
}
.date-picker-trigger:hover {
  border-color: var(--p-text-dim);
  color: var(--text-color);
  background-color: var(--p-hover);
}
.date-picker-trigger.active {
  border-color: var(--accent-color);
  color: var(--text-color);
  z-index: 1002;
}
.trigger-content {
  display: flex;
  align-items: center;
  white-space: nowrap;
  overflow: hidden;
}
.arrow-icon {
  font-size: 10px;
  transition: transform 0.2s;
  margin-left: 6px;
}
.date-picker-trigger.active .arrow-icon {
  transform: rotate(180deg);
}

/* --- DROPDOWN MENU --- */
.date-picker-menu {
  position: absolute;
  top: 100%;
  margin-top: 0;
  left: 0;

  /* QUAN TRỌNG: Menu luôn bằng Input */
  width: 100%;

  background-color: var(--menu-bg);
  border: 1px solid var(--border-color);
  border-radius: 0 0 4px 4px; /* Chỉ bo góc dưới */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
  z-index: 1001;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-5px);
  transition: all 0.1s ease-in-out;
}
.date-picker-menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* --- VIEW MAIN --- */
.view-main {
  padding: 6px;
  display: flex;
  flex-direction: column;
}
.presets-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.preset-item {
  padding: 6px 8px;
  font-size: 11px;
  color: var(--text-color);
  cursor: pointer;
  border-radius: 3px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.preset-item:hover {
  background-color: var(--p-hover);
}
.preset-item.active {
  background-color: var(--p-selection);
  color: var(--accent-color);
  font-weight: 600;
}
.check-icon {
  font-size: 10px;
}
.separator {
  height: 1px;
  background-color: var(--border-color);
  margin: 8px 0;
  opacity: 0.5;
}

/* Fake Inputs */
.custom-range-inputs {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
.input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.input-group label {
  font-size: 9px;
  color: var(--p-text-dim);
  font-weight: 700;
  text-transform: uppercase;
}
.fake-input {
  height: 28px;
  background-color: var(--input-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  color: var(--text-color);
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px;
  cursor: pointer;
  font-family: "JetBrains Mono", monospace;
  transition: border 0.2s;
}
.fake-input:hover {
  border-color: var(--p-text-dim);
}
.fake-input.active {
  border-color: var(--accent-color);
  color: var(--accent-color);
  box-shadow: 0 0 0 1px var(--accent-color);
}
.fake-input .icon {
  font-size: 10px;
  opacity: 0.5;
}

/* --- VIEW CALENDAR --- */
.view-calendar {
  padding: 8px;
  background-color: var(--menu-bg);
}
.cal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  color: var(--text-color);
}
.cal-title {
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}
.cal-nav-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  cursor: pointer;
  font-size: 10px;
  color: var(--p-text-muted);
}
.cal-nav-btn:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

/* GRID LỊCH: Dùng fr để tự co giãn theo width 100% của cha */
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  margin-bottom: 8px;
}
.cal-cell {
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  border-radius: 4px;
  cursor: pointer;
  color: var(--text-color);
  user-select: none;
}
.weekday {
  font-size: 9px;
  color: var(--p-text-dim);
  font-weight: 700;
  cursor: default;
}
.day:hover {
  background-color: var(--p-hover);
}
.day.selected {
  background-color: var(--accent-color);
  color: #09090b;
  font-weight: 700;
  box-shadow: 0 0 4px var(--accent-color);
}
.day.today {
  border: 1px solid var(--p-text-dim);
}
.day.empty {
  pointer-events: none;
}

/* DISABLED STATE */
.day.disabled {
  opacity: 0.2;
  pointer-events: none;
  cursor: not-allowed;
  background-color: transparent !important;
  text-decoration: line-through;
}

.cal-footer {
  border-top: 1px solid var(--border-color);
  padding-top: 6px;
}
.back-btn {
  font-size: 10px;
  color: var(--p-text-dim);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}
.back-btn:hover {
  color: var(--text-color);
}

/* --- FOOTER --- */
.picker-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 6px;
  border-top: 1px solid var(--border-color);
}
.picker-footer button {
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 500;
}
.btn-cancel {
  background: transparent;
  color: var(--p-text-muted);
  border: 1px solid transparent;
}
.btn-cancel:hover {
  color: var(--text-color);
  background-color: var(--p-hover);
}
.btn-apply {
  background-color: var(--accent-color);
  color: #09090b;
  border: none;
  font-weight: 600;
}
.btn-apply:hover {
  filter: brightness(1.1);
}
</style>
