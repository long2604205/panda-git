<template>
  <div class="flex flex-col h-screen overflow-hidden" :data-theme="theme">
    <panda-navigation/>
    <panda-toolbar
      :current-repo="currentRepo"
      :current-branch="currentBranch"
      :repositories="repositories"
      :branches="branches"
      :show-pull-badge="showPullBadge"
      :sidebar-visible="sidebarVisible"
      :detail-visible="detailVisible"
      @fetch="handleFetch"
      @pull="handlePull"
      @push="handlePush"
      @stash="handleStash"
      @pop="handlePop"
      @select-repo="handleRepoChange"
      @select-branch="handleBranchChange"
      @open-terminal="handleOpenTerminal"
      @open-settings="handleOpenSettings"
      @toggle-sidebar="toggleSidebar"
      @toggle-detail="toggleDetail"
    />
    <panda-workspace />
    <panda-footer :selected-branch="selectedBranch" @change-theme="setTheme" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import PandaFooter from '@/components/widgets/PandaFooter.vue'
import PandaWorkspace from '@/components/PandaWorkspace.vue'
import PandaNavigation from "@/components/widgets/PandaNavigation.vue";
import PandaToolbar from "@/components/widgets/PandaToolbar.vue";

const theme = ref('dark')
function setTheme(t) {
  theme.value = t
}
const selectedBranch = ref('main')
onMounted(() => {
  document.documentElement.setAttribute('data-theme', theme.value)
})
watch(theme, (newTheme) => {
  document.documentElement.setAttribute('data-theme', newTheme)
})




const currentRepo = ref('shop-ui-core');
const currentBranch = ref('main');
const showPullBadge = ref(false);
const sidebarVisible = ref(true);
const detailVisible = ref(true);

// Danh sách repositories
const repositories = ref([
  { id: 'shop-ui-core', name: 'shop-ui-core' },
  { id: 'shop-api', name: 'shop-api' },
  { id: 'auth-service', name: 'auth-service' },
  { id: 'payment-gateway', name: 'payment-gateway' },
  { id: 'admin-dashboard', name: 'admin-dashboard' }
]);

// Danh sách branches
const branches = ref([
  { id: 'main', name: 'main' },
  { id: 'develop', name: 'develop' },
  { id: 'feat/new-login', name: 'feat/new-login' },
  { id: 'feat/dark-mode', name: 'feat/dark-mode' },
  { id: 'fix/bug-102', name: 'fix/bug-102' },
  { id: 'fix/responsive', name: 'fix/responsive' }
]);

// ==================== EVENT HANDLERS (LOG ONLY) ====================
const handleFetch = () => {
  console.log('🔄 FETCH: Fetching from remote...');
};

const handlePull = () => {
  console.log('⬇️ PULL: Pulling changes from remote...');
};

const handlePush = () => {
  console.log('⬆️ PUSH: Pushing changes to remote...');
};

const handleStash = () => {
  console.log('📦 STASH: Stashing current changes...');
};

const handlePop = () => {
  console.log('📤 POP: Popping stash...');
};

const handleRepoChange = (repoId) => {
  console.log('📁 SELECT REPO:', repoId);
  currentRepo.value = repoId;
};

const handleBranchChange = (branchId) => {
  console.log('🌿 SELECT BRANCH:', branchId);
  currentBranch.value = branchId;
};

const handleOpenTerminal = () => {
  console.log('💻 OPEN TERMINAL: Opening integrated terminal...');
};

const handleOpenSettings = () => {
  console.log('⚙️ OPEN SETTINGS: Opening settings panel...');
};

const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
  console.log('📂 TOGGLE SIDEBAR:', sidebarVisible.value ? 'SHOW' : 'HIDE');
};

const toggleDetail = () => {
  detailVisible.value = !detailVisible.value;
  console.log('📋 TOGGLE DETAIL:', detailVisible.value ? 'SHOW' : 'HIDE');
};
</script>
<!--https://heroicons.com/solid-->
<style></style>
