<script setup>
import PandaNavigation from '@/components/widgets/PandaNavigation.vue'
import PandaDefaultContent from '@/components/widgets/PandaDefaultContent.vue'
import PandaFooter from '@/components/widgets/PandaFooter.vue'
import { onMounted, ref } from 'vue'
import { loadRepos } from '@/plugins/indexedDB.js'
import FullLoadingPage from '@/components/FullLoadingPage.vue'

const isLoadingPage = ref(true)

onMounted(async () => {
  // Load dữ liệu repo từ IndexedDB trước khi render workspace

  window.__savedRepos = await loadRepos() // lưu tạm global để các component dùng

  // Khoảng delay giả lập backend load
  await new Promise((resolve) => setTimeout(resolve, 2000))

  isLoadingPage.value = false
})
</script>

<template>
  <full-loading-page :is-loading="isLoadingPage"/>
  <!-- Top Navbar with Dropdown Menus -->
  <panda-navigation />

  <!-- Content -->
  <panda-default-content />

  <!-- Footer -->
  <panda-footer />
</template>

<style scoped>
</style>
