<template>
  <teleport to="body">
    <div v-if="isOpen" class="custom-dropdown" :style="menuStyle" @click.stop>
      <template v-for="(action, index) in actions" :key="index">
        <div v-if="action.type === 'separator'" class="dropdown-separator"></div>
        <div v-else class="dropdown-item" :class="action.class" @click="handleAction(action)">
          <div class="dropdown-left">
            <i :class="action.icon + ' w-3'"></i>
            <span>{{ action.label }}</span>
          </div>
          <span v-if="action.shortcut" class="dropdown-shortcut" :style="action.shortcutStyle">
            {{ action.shortcut }}
          </span>
        </div>
      </template>
    </div>
  </teleport>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// Props
defineProps({
  isOpen: {
    type: Boolean,
    required: true,
    default: false
  },
  menuStyle: {
    type: Object,
    required: true,
    default: () => ({ top: '0px', left: '0px' })
  },
  actions: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Emits
const emit = defineEmits(['action']);

// Methods
const handleAction = (action) => {
  if (action.value) {
    emit('action', action.value);
  }
};
</script>

<style scoped>
/* --- DROPDOWN MENU (Fixed Position) --- */
.custom-dropdown {
  position: fixed;
  background-color: var(--menu-bg);
  border: 1px solid var(--border-color);
  min-width: 220px;
  box-shadow: 0 4px 12px var(--ctx-shadow);
  border-radius: 6px;
  padding: 4px 0;
  z-index: 9999;
  animation: fadeIn 0.1s ease-out;
}

.dropdown-item {
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 400;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  white-space: nowrap;
}

.dropdown-item:hover {
  background-color: var(--p-selection);
  color: var(--accent-color);
}

.dropdown-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dropdown-shortcut {
  color: var(--p-text-dim);
  font-size: 10px;
  margin-left: 16px;
  font-family: inherit;
}

.dropdown-item:hover .dropdown-shortcut {
  color: var(--accent-color);
  opacity: 0.8;
}

.dropdown-separator {
  height: 1px;
  background-color: var(--border-color);
  margin: 4px 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

<!--
==================== CÁCH SỬ DỤNG ====================

1. IMPORT COMPONENT:
   import DropdownMenu from './components/DropdownMenu.vue';

2. REGISTER COMPONENT:
   components: { DropdownMenu }

3. SETUP DATA:
   import { ref, onMounted, onUnmounted } from 'vue';

   const isMenuOpen = ref(false);
   const menuStyle = ref({ top: '0px', left: '0px' });
   const menuActions = ref([
     {
       value: 'add_repo',
       label: 'Add Repository...',
       icon: 'fa-solid fa-plus',
       shortcut: 'Alt+A'
     },
     {
       value: 'add_group',
       label: 'Add Group...',
       icon: 'fa-regular fa-folder',
       shortcut: 'Alt+G'
     },
     {
       type: 'separator'  // Separator line
     },
     {
       value: 'expand_all',
       label: 'Expand All',
       icon: 'fa-solid fa-angles-down',
       shortcut: 'Shift+E'
     },
     {
       value: 'delete',
       label: 'Delete',
       icon: 'fa-solid fa-trash',
       class: 'text-red-400 hover:text-red-300',
       shortcut: 'Del',
       shortcutStyle: 'color: inherit; opacity: 0.7;'
     }
   ]);

4. TÍNH VỊ TRÍ MENU:
   const calculatePosition = (event) => {
     const rect = event.currentTarget.getBoundingClientRect();
     return {
       top: `${rect.top}px`,
       left: `${rect.right + 4}px`
     };
   };

5. MỞ MENU:
   const openMenu = (event) => {
     menuStyle.value = calculatePosition(event);
     isMenuOpen.value = true;
   };

6. XỬ LÝ ACTION:
   const handleMenuAction = (actionValue) => {
     isMenuOpen.value = false;

     switch(actionValue) {
       case 'add_repo':
         console.log('Add repository');
         break;
       case 'add_group':
         console.log('Add group');
         break;
       case 'expand_all':
         console.log('Expand all');
         break;
       case 'delete':
         console.log('Delete item');
         break;
     }
   };

7. ĐÓNG MENU KHI CLICK BÊN NGOÀI:
   const handleGlobalClick = () => {
     isMenuOpen.value = false;
   };

   onMounted(() => window.addEventListener('click', handleGlobalClick));
   onUnmounted(() => window.removeEventListener('click', handleGlobalClick));

8. TEMPLATE:
   <DropdownMenu
     :is-open="isMenuOpen"
     :menu-style="menuStyle"
     :actions="menuActions"
     @action="handleMenuAction"
   />

9. BUTTON MỞ MENU:
   <button @click.stop="openMenu($event)">
     <i class="fa-solid fa-ellipsis"></i>
   </button>

==================== CẤU TRÚC ACTION OBJECT ====================

{
  value: string,           // Giá trị emit khi click (required nếu không phải separator)
  label: string,           // Text hiển thị (required nếu không phải separator)
  icon: string,            // Font Awesome class (required nếu không phải separator)
  shortcut: string,        // Phím tắt hiển thị (optional)
  class: string,           // Custom CSS class (optional)
  shortcutStyle: string,   // Custom inline style cho shortcut (optional)
  type: 'separator'        // Để tạo separator, bỏ qua các field khác
}

==================== VÍ DỤ ĐẦY ĐỦ ====================

<template>
  <div>
    <button @click.stop="openMenu($event)" class="menu-button">
      <i class="fa-solid fa-ellipsis"></i>
    </button>

    <DropdownMenu
      :is-open="isMenuOpen"
      :menu-style="menuStyle"
      :actions="menuActions"
      @action="handleMenuAction"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import DropdownMenu from './components/DropdownMenu.vue';

const isMenuOpen = ref(false);
const menuStyle = ref({ top: '0px', left: '0px' });

const menuActions = ref([
  {
    value: 'add_repo',
    label: 'Add Repository...',
    icon: 'fa-solid fa-plus',
    shortcut: 'Alt+A'
  },
  {
    value: 'add_group',
    label: 'Add Group...',
    icon: 'fa-regular fa-folder',
    shortcut: 'Alt+G'
  },
  { type: 'separator' },
  {
    value: 'expand_all',
    label: 'Expand All',
    icon: 'fa-solid fa-angles-down',
    shortcut: 'Shift+E'
  },
  {
    value: 'collapse_all',
    label: 'Collapse All',
    icon: 'fa-solid fa-angles-right',
    shortcut: 'Shift+C'
  }
]);

const calculatePosition = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  return {
    top: `${rect.top}px`,
    left: `${rect.right + 4}px`
  };
};

const openMenu = (event) => {
  menuStyle.value = calculatePosition(event);
  isMenuOpen.value = true;
};

const handleMenuAction = (actionValue) => {
  isMenuOpen.value = false;
  console.log('Action triggered:', actionValue);
};

const handleGlobalClick = () => {
  isMenuOpen.value = false;
};

onMounted(() => window.addEventListener('click', handleGlobalClick));
onUnmounted(() => window.removeEventListener('click', handleGlobalClick));
</script>
-->
