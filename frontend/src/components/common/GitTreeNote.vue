<script setup>
import { ref, computed, provide, inject, toRef } from 'vue';

defineOptions({
  name: 'GitBranchTree'
});

const props = defineProps({
  // Dành cho Root: Mảng dữ liệu đầu vào
  branches: {
    type: Array,
    default: null
  },
  // Dành cho Root: Search Query được truyền từ cha vào
  searchQuery: {
    type: String,
    default: ''
  },
  // Dành cho Node con: Object node hiện tại
  node: {
    type: Object,
    default: null
  },
  // Độ sâu
  depth: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['select']);

// ==========================================
// 1. LOGIC DÀNH CHO ROOT (Quản lý State)
// ==========================================
const isRoot = computed(() => Array.isArray(props.branches));

// State nội bộ của Tree (Expanded Set & Selected Path)
const _expandedPaths = isRoot.value ? ref(new Set()) : null;
const _selectedPath = isRoot.value ? ref(null) : null;

// Provide state xuống các cấp con
if (isRoot.value) {
  // QUAN TRỌNG: Provide prop searchQuery (dạng ref) để con reactive theo cha
  provide('rootSearchQuery', toRef(props, 'searchQuery'));
  provide('rootExpandedPaths', _expandedPaths);
  provide('rootSelectedPath', _selectedPath);

  const handleSelect = (path) => {
    _selectedPath.value = path;
    emit('select', path);
  };
  provide('rootHandleSelect', handleSelect);

  const handleToggle = (path) => {
    if (_expandedPaths.value.has(path)) {
      _expandedPaths.value.delete(path);
    } else {
      _expandedPaths.value.add(path);
    }
    _expandedPaths.value = new Set(_expandedPaths.value);
  };
  provide('rootHandleToggle', handleToggle);
}

// Inject state (Nhận lại từ chính mình nếu là Root, hoặc từ cha nếu là Node con)
const injectedSearchQuery = inject('rootSearchQuery');
const expandedPaths = inject('rootExpandedPaths');
const selectedPath = inject('rootSelectedPath');
const onSelect = inject('rootHandleSelect');
const onToggle = inject('rootHandleToggle');

// ==========================================
// 2. XỬ LÝ DATA & PUBLIC METHODS (Cho cha gọi)
// ==========================================

// Hàm Build Tree (Chỉ chạy ở Root)
const rootTreeData = computed(() => {
  if (!isRoot.value || !props.branches) return [];

  const root = {};
  props.branches.forEach(path => {
    const parts = path.split('/');
    let current = root;
    let currentPathAccumulator = "";

    parts.forEach((part, index) => {
      currentPathAccumulator = currentPathAccumulator ? `${currentPathAccumulator}/${part}` : part;
      if (!current[part]) {
        current[part] = {
          name: part,
          path: currentPathAccumulator,
          children: {},
          fullPath: null
        };
      }
      if (index === parts.length - 1) {
        current[part].fullPath = path;
      }
      current = current[part].children;
    });
  });
  return Object.values(root).sort((a, b) => a.name.localeCompare(b.name));
});

// Các hàm utility để component Cha gọi thông qua ref template
const expandAll = () => {
  if (!isRoot.value) return;
  const allPaths = new Set();
  const traverse = (nodes) => {
    nodes.forEach(node => {
      allPaths.add(node.path);
      if (node.children) traverse(Object.values(node.children));
    });
  };
  traverse(rootTreeData.value);
  _expandedPaths.value = allPaths;
};

const collapseAll = () => {
  if (!isRoot.value) return;
  _expandedPaths.value = new Set();
};

// Expose ra ngoài để cha dùng được: treeRef.value.expandAll()
defineExpose({
  expandAll,
  collapseAll
});

// ==========================================
// 3. LOGIC HIỂN THỊ NODE
// ==========================================

const hasChildren = computed(() => {
  return props.node && props.node.children && Object.keys(props.node.children).length > 0;
});

const sortedChildren = computed(() => {
  if (!hasChildren.value) return [];
  return Object.values(props.node.children).sort((a, b) => a.name.localeCompare(b.name));
});

// Logic Search Đệ quy
const matchesSearch = computed(() => {
  if (!injectedSearchQuery.value) return true;
  const q = injectedSearchQuery.value.toLowerCase();

  if (props.node.name.toLowerCase().includes(q)) return true;
  if (props.node.path && props.node.path.toLowerCase().includes(q)) return true;
  return checkChildrenMatch(props.node, q);
});

function checkChildrenMatch(node, query) {
  if (!node.children) return false;
  return Object.values(node.children).some(child => {
    const selfMatch = child.name.toLowerCase().includes(query) || (child.path && child.path.toLowerCase().includes(query));
    if (selfMatch) return true;
    return checkChildrenMatch(child, query);
  });
}

const isOpen = computed(() => {
  if (injectedSearchQuery.value) return true; // Auto expand khi search
  return expandedPaths.value.has(props.node.path);
});

const highlightedName = computed(() => {
  const text = props.node.name;
  if (!injectedSearchQuery.value) return text;
  const safeQuery = injectedSearchQuery.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${safeQuery})`, 'gi');
  return text.replace(regex, '<span class="bg-[#ac6802] text-white rounded-[2px] font-normal">$1</span>');
});

const handleClick = () => {
  if (props.node.fullPath) {
    onSelect(props.node.fullPath);
  } else if (hasChildren.value) {
    onToggle(props.node.path);
  }
};

const handleToggleIcon = (e) => {
  e.stopPropagation();
  if (hasChildren.value) onToggle(props.node.path);
};

</script>

<template>
  <!-- TRƯỜNG HỢP 1: LÀ ROOT (CHỈ RENDER LIST, KHÔNG RENDER TOOLBAR) -->
  <div v-if="isRoot" class="h-full overflow-y-auto select-none custom-scrollbar p-2">
    <GitBranchTree
      v-for="childNode in rootTreeData"
      :key="childNode.path"
      :node="childNode"
      :depth="0"
    />
    <div v-if="rootTreeData.length === 0" class="text-center text-gray-500 mt-4 italic">
      No branches found
    </div>
  </div>

  <!-- TRƯỜNG HỢP 2: LÀ NODE CON -->
  <div v-else-if="matchesSearch">
    <!-- Node Row -->
    <div
      class="flex items-center py-1 cursor-pointer rounded-sm whitespace-nowrap group select-none transition-colors duration-100"
      :class="[
        node.fullPath === selectedPath
          ? 'bg-[#2c3e50] text-white'
          : 'hover:bg-[#2b2d30] text-[#bcbec4]'
      ]"
      :style="{ paddingLeft: `${depth * 16}px` }"
      @click.stop="handleClick"
      @dblclick.stop="handleToggleIcon"
    >
      <!-- 1. Chevron -->
      <span class="w-5 flex justify-center items-center cursor-pointer hover:text-white shrink-0" @click.stop="handleToggleIcon">
        <template v-if="hasChildren">
          <svg v-if="isOpen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3 text-gray-500"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3 text-gray-500"><path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" /></svg>
        </template>
      </span>

      <!-- 2. Icon -->
      <span class="mr-2 shrink-0 flex items-center">
        <template v-if="hasChildren">
          <svg v-if="isOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-gray-400"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h4.375L12 6h7.5a2.25 2.25 0 012.25 2.25v1.528" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-gray-400"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" /></svg>
        </template>
        <template v-else>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5 text-green-500"><path fill-rule="evenodd" d="M12.208 2.274a.75.75 0 01.52.95l-.75 2.723a3.003 3.003 0 011.082 3.193l.66 2.404a3 3 0 01.385 4.606.75.75 0 01-1.06-1.06 1.5 1.5 0 00-.734-2.268l-.756-2.756a1.503 1.503 0 00-1.776-1.063l-1.393.383a.75.75 0 01-.4-1.455l1.393-.383a3.003 3.003 0 013.628 1.95l.66-2.403a1.503 1.503 0 00-.638-1.748l.942-3.42a.75.75 0 01.936-.532z" clip-rule="evenodd" /><path fill-rule="evenodd" d="M6.5 9a1.5 1.5 0 100-3 1.5 1.5 0 000 3zM5 14a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z" clip-rule="evenodd" /></svg>
        </template>
      </span>

      <!-- 3. Name -->
      <span
        class="truncate text-sm"
        :class="{ 'text-blue-300': node.fullPath && hasChildren && node.fullPath !== selectedPath }"
        v-html="highlightedName"
      ></span>
    </div>

    <!-- Recursive Children -->
    <div v-if="isOpen && hasChildren">
      <git-tree-note
        v-for="child in sortedChildren"
        :key="child.path"
        :node="child"
        :depth="depth + 1"
      />
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 8px; height: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #2b2d30; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #777; }
</style>
