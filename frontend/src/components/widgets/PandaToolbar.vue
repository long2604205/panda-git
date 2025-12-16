<template>
  <div class="git-toolbar">
    <!-- MAIN LEFT GROUP (Repo Info + Actions) -->
    <div class="toolbar-left">

      <!-- --- 1. REPO & BRANCH --- -->
      <div class="info-group">
        <!-- Repo Dropdown Trigger -->
        <div class="dropdown-wrapper w-72">
          <div class="info-trigger">
            <div class="repo-avatar">
              {{ repoInitials }}
            </div>
            <div class="info-content">
              <span class="info-label">Repository</span>
              <div class="info-value">
                <span class="value-text">{{ repositoryStore.repoName }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Vertical Separator -->
        <div class="vertical-separator"/>

        <!-- Branch Dropdown Trigger -->
        <div class="dropdown-wrapper w-56">
          <div class="info-trigger group relative">
            <div class="branch-avatar">
              <i class="fa-solid fa-code-branch text-sm"/>
            </div>
            <div class="info-content">
              <span class="info-label">Current Branch</span>
              <div class="info-value">
                <span class="value-text">{{ repositoryStore.branchName }}</span>
              </div>
            </div>
            <div class="tooltip-arrow-box">{{ repositoryStore.branchName }}</div>
          </div>
        </div>
      </div>

      <!-- Vertical Separator between Info and Actions -->
      <div class="section-separator"/>

      <!-- --- 2. ACTIONS --- -->
      <!-- Main Actions -->
      <button class="toolbar-btn" title="Fetch from origin">
        <i class="fa-solid fa-cloud-arrow-down text-[var(--p-text-muted)]"/>
        <span>Clone</span>
      </button>
      <div class="section-separator"/>
      <button class="toolbar-btn" title="Pull changes">
        <i class="fa-solid fa-arrow-down text-[#22d3ee]"></i>
        <span>Pull</span>
      </button>
      <button class="toolbar-btn" title="Push changes">
        <i class="fa-solid fa-arrow-up text-[#34d399]"></i>
        <span>Push</span>
      </button>
      <button class="toolbar-btn" title="Fetch from origin">
        <i class="fa-solid fa-retweet text-[var(--p-text-muted)]"/>
        <span>Fetch</span>
      </button>
      <div class="section-separator"/>
      <button class="toolbar-btn" title="Fetch from origin" @click="openConflict">
        <i class="fa-solid fa-retweet text-[var(--p-text-muted)]"/>
        <span>Conflict</span>
      </button>
    </div>

    <!-- RIGHT: Tools & Layout -->
    <div class="toolbar-right">
      <!-- Tools Group -->
      <div class="tools-group">
        <button
          class="icon-only-btn"
          @click="$emit('open-settings')"
        >
          <i class="fa-solid fa-gear text-sm"/>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent } from 'vue';
import {useRepositoryStore} from "@/stores/repositoryStore.js";
import { showPageInModal } from '@/services/modals.js'

const conflictForm = defineAsyncComponent(() => import('@/components/common/DiffForm.vue'))
const repositoryStore = useRepositoryStore()

const repoInitials = computed(() => {
  const name = repositoryStore.repoName;
  if (!name) return '';

  let cleanName = name.replace(/[-_]/g, ' ');
  cleanName = cleanName.replace(/([a-z])([A-Z])/g, '$1 $2');
  const words = cleanName.trim().split(/\s+/);

  const firstInitial = words[0].charAt(0).toUpperCase();

  if (words.length === 1) {
    return firstInitial;
  }

  const lastWord = words[words.length - 1];
  const lastWordInitial = lastWord.charAt(0).toUpperCase();

  if (firstInitial !== lastWordInitial) {
    return firstInitial + lastWordInitial;
  }

  for (let i = lastWord.length - 1; i > 0; i--) {
    const char = lastWord.charAt(i).toUpperCase();

    if (char !== firstInitial) {
      return firstInitial + char;
    }
  }

  return firstInitial;
});

// Emits
const emit = defineEmits([
  'fetch',
  'pull',
  'push',
  'open-settings',
]);

function openConflict () {
  showPageInModal(conflictForm, {}, {width: '90%'})
}
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
.info-trigger {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 6px 6px 16px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.repo-avatar {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  background: linear-gradient(135deg, #22d3ee 0%, #831843 100%);

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


.info-value {
  display: flex;
  align-items: center;
  gap: 4px;
}

.value-text {
  font-size: 10px;
  font-weight: 700;
  color: var(--text-color);
  line-height: 1;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
  display: inline-block;
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
.tooltip-arrow-box {
  @apply absolute top-full mt-1 left-1/2 -translate-x-1/2 z-50
         whitespace-nowrap rounded-md px-3 py-1.5 text-[11px] font-semibold
         opacity-0 group-hover:opacity-100 transition-all duration-200 ease-out
         -translate-y-1 group-hover:translate-y-0 pointer-events-none;

  background-color: var(--bg-header);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.tooltip-arrow-box::before {
  content: "";
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 9px;
  height: 9px;
  background-color: var(--bg-header);
  border-top: 1px solid var(--border-color);
  border-left: 1px solid var(--border-color);
  z-index: 10;
}

/* --- TOOLBAR STYLES (NEW) --- */
        .toolbar-btn {
            height: 32px;
            padding: 0 12px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-color);
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        .toolbar-btn:hover {
            background-color: var(--p-hover);
        }
        .toolbar-btn:active {
            background-color: var(--p-selection);
            border-color: var(--accent-color);
        }
        .toolbar-btn.icon-only {
            padding: 0;
            width: 32px;
            justify-content: center;
        }
        .toolbar-btn.disabled {
            opacity: 0.5;
            cursor: default;
        }
        .toolbar-btn.disabled:hover {
            background-color: transparent;
        }
</style>
