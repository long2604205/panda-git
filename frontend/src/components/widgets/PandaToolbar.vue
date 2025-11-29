<template>
  <div class="git-toolbar">
    <!-- MAIN LEFT GROUP (Repo Info + Actions) -->
    <div class="toolbar-left">

      <!-- --- 1. REPO & BRANCH --- -->
      <div class="info-group">
        <!-- Repo Dropdown Trigger -->
        <div class="dropdown-wrapper w-72">
          <div
            @click="toggleDropdown('repo')"
            class="info-trigger"
          >
            <div class="repo-avatar">
              {{ repoInitials }}
            </div>
            <div class="info-content">
              <span class="info-label">Repository</span>
              <div class="info-value">
                <span class="value-text">{{ currentRepo }}</span>
                <i class="fa-solid fa-chevron-down chevron-icon"/>
              </div>
            </div>
          </div>
          <!-- Repo Dropdown Content -->
          <div
            v-show="activeDropdown === 'repo'"
            class="toolbar-dropdown"
          >
            <div
              v-for="repo in repositories"
              :key="repo.id"
              :class="['dropdown-item', { active: repo.id === currentRepo }]"
              @click="selectRepo(repo.id)"
            >
              <i class="fa-solid fa-folder-open text-xs"/> {{ repo.name }}
            </div>
          </div>
        </div>

        <!-- Vertical Separator -->
        <div class="vertical-separator"/>

        <!-- Branch Dropdown Trigger -->
        <div class="dropdown-wrapper w-56">
          <div
            @click="toggleDropdown('branch')"
            class="info-trigger"
          >
            <div class="branch-avatar">
              <i class="fa-solid fa-code-branch text-sm"/>
            </div>
            <div class="info-content">
              <span class="info-label">Current Branch</span>
              <div class="info-value">
                <span class="value-text">{{ currentBranch }}</span>
                <i class="fa-solid fa-chevron-down chevron-icon"/>
              </div>
            </div>
          </div>
          <!-- Branch Dropdown Content -->
          <div
            v-show="activeDropdown === 'branch'"
            class="toolbar-dropdown"
          >
            <div class="dropdown-section-title">
              Local Branches
            </div>
            <div
              v-for="branch in branches"
              :key="branch.id"
              :class="['dropdown-item', { active: branch.id === currentBranch }]"
              @click="selectBranch(branch.id)"
            >
              <i class="fa-solid fa-code-branch text-xs"/> {{ branch.name }}
            </div>
          </div>
        </div>
      </div>

      <!-- Vertical Separator between Info and Actions -->
      <div class="section-separator"/>

      <!-- --- 2. ACTIONS --- -->
      <div class="actions-group">
        <div class="control-group-transparent">
          <button
            class="control-btn"
            @click="$emit('fetch')"
            title="Fetch from origin"
          >
<!--            <i class="fa-solid fa-clone"/>-->
            <i class="fa-solid fa-cloud-arrow-down"/>
            <span>Clone</span>
          </button>
          <div class="toolbar-divider"/>
          <button
            class="control-btn"
            @click="$emit('pull')"
            title="Pull 1 commit from origin"
          >
            <i class="fa-solid fa-arrow-down-long"/>
            <span>Pull</span>
          </button>
          <div class="toolbar-divider"/>
          <button
            class="control-btn"
            @click="$emit('push')"
            title="Push to origin"
          >
            <i class="fa-solid fa-arrow-up-long"/>
            <span>Push</span>
          </button>
          <div class="toolbar-divider"/>
          <button
            class="control-btn"
            @click="$emit('fetch')"
            title="Fetch from origin"
          >
            <i class="fa-solid fa-retweet"/>
            <span>Fetch</span>
          </button>
        </div>
      </div>
    </div>

    <!-- RIGHT: Tools & Layout -->
    <div class="toolbar-right">
      <!-- Tools Group -->
      <div class="tools-group">
        <button
          class="icon-only-btn"
          @click="$emit('open-settings')"
          title="Settings"
        >
          <i class="fa-solid fa-gear text-sm"/>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// Props
const props = defineProps({
  currentRepo: {
    type: String,
    default: 'shop-ui-core'
  },
  currentBranch: {
    type: String,
    default: 'main'
  },
  repositories: {
    type: Array,
    default: () => [
      { id: 'shop-ui-core', name: 'shop-ui-core' },
      { id: 'shop-api', name: 'shop-api' },
      { id: 'auth-service', name: 'auth-service' }
    ]
  },
  branches: {
    type: Array,
    default: () => [
      { id: 'main', name: 'main' },
      { id: 'develop', name: 'develop' },
      { id: 'feat/new-login', name: 'feat/new-login' },
      { id: 'fix/bug-102', name: 'fix/bug-102' }
    ]
  },
  showPullBadge: {
    type: Boolean,
    default: false
  },
  sidebarVisible: {
    type: Boolean,
    default: true
  },
  detailVisible: {
    type: Boolean,
    default: true
  }
});

// Emits
const emit = defineEmits([
  'fetch',
  'pull',
  'push',
  'stash',
  'pop',
  'select-repo',
  'select-branch',
  'open-terminal',
  'open-settings',
  'toggle-sidebar',
  'toggle-detail'
]);

// State
const activeDropdown = ref(null);

// Computed
const repoInitials = computed(() => {
  const words = props.currentRepo.split('-');
  return words.map(w => w[0].toUpperCase()).join('').slice(0, 2);
});

// Methods
const toggleDropdown = (type) => {
  activeDropdown.value = activeDropdown.value === type ? null : type;
};

const selectRepo = (repoId) => {
  emit('select-repo', repoId);
  activeDropdown.value = null;
};

const selectBranch = (branchId) => {
  emit('select-branch', branchId);
  activeDropdown.value = null;
};

const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown-wrapper')) {
    activeDropdown.value = null;
  }
};

// Lifecycle
onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* --- MAIN TOOLBAR CONTAINER --- */
.git-toolbar {
  height: 56px;
  background-color: var(--bg-header);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  user-select: none;
  position: relative;
}

/* --- LEFT SECTION --- */
.toolbar-left {
  display: flex;
  align-items: center;
  margin-right: auto;
}

.info-group {
  display: flex;
  align-items: center;
}

.vertical-separator {
  width: 1px;
  height: 32px;
  background-color: var(--border-color);
}

.section-separator {
  width: 1px;
  height: 24px;
  background-color: var(--border-color);
  margin: 0 8px;
}

/* --- DROPDOWN WRAPPER --- */
.dropdown-wrapper {
  position: relative;
}

.info-trigger {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 6px 6px 6px 16px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.info-trigger:hover {
  background-color: var(--p-hover);
}

.repo-avatar {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  background: linear-gradient(135deg, #f97316 0%, #eab308 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.branch-avatar {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-color);
  background-color: var(--p-selection);
}

.info-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.info-label {
  font-size: 10px;
  color: var(--p-text-muted);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  line-height: 1;
  margin-bottom: 4px;
  transition: color 0.2s;
}

.info-trigger:hover .info-label {
  color: var(--text-color);
}

.info-value {
  display: flex;
  align-items: center;
  gap: 4px;
}

.value-text {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-color);
  line-height: 1;
}

.chevron-icon {
  font-size: 10px;
  color: var(--p-text-dim);
}

/* --- TOOLBAR DROPDOWN --- */
.toolbar-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  margin-left: 16px;
  background-color: var(--bg-side);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  min-width: 200px;
  overflow: hidden;
  animation: fadeIn 0.1s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-section-title {
  padding: 8px 12px;
  font-size: 10px;
  color: var(--p-text-dim);
  text-transform: uppercase;
  font-weight: 700;
  border-bottom: 1px solid var(--border-color);
}

.dropdown-item {
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 12px;
  color: var(--p-text-muted);
  transition: background-color 0.1s;
}

.dropdown-item:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.dropdown-item.active {
  color: var(--accent-color);
  background-color: var(--p-selection);
}

/* --- ACTIONS GROUP --- */
.actions-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.control-group-transparent {
  display: flex;
  align-items: center;
  gap: 0;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  height: 42px;
  border-radius: 6px;
  cursor: pointer;
  color: var(--p-text-muted);
  transition: all 0.2s;
  min-width: 64px;
  position: relative;
  background: none;
  border: none;
}

.control-btn:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.control-btn:active {
  transform: scale(0.98);
  background-color: var(--p-selection);
}

.control-btn i {
  font-size: 16px;
  margin-bottom: 2px;
}

.control-btn span {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background-color: var(--border-color);
  margin: 0 4px;
  opacity: 0.5;
}

.badge-dot {
  position: absolute;
  top: 6px;
  right: 18px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--accent-color);
  box-shadow: 0 0 5px var(--accent-color);
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0% {
    opacity: 0.6;
    box-shadow: 0 0 2px var(--accent-color);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 8px var(--accent-color);
  }
  100% {
    opacity: 0.6;
    box-shadow: 0 0 2px var(--accent-color);
  }
}

.action-spacer {
  width: 16px;
}

/* --- RIGHT SECTION --- */
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.tools-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-only-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  color: var(--p-text-muted);
  cursor: pointer;
  transition: all 0.2s;
  background: none;
  border: none;
}

.icon-only-btn:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.icon-only-btn.active {
  background-color: var(--p-selection);
  color: var(--accent-color);
}
</style>
