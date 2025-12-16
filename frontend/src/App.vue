<template>
  <div
    class="flex flex-col h-screen overflow-hidden"
    :data-theme="themeStore.theme"
  >
    <panda-navigation />
    <panda-toolbar
      @fetch="handleFetch"
      @pull="handlePull"
      @push="handlePush"
      @open-settings="handleOpenSettings"
    />
    <panda-workspace />
    <panda-footer />
  </div>
</template>

<script setup>
import PandaFooter from '@/components/widgets/PandaFooter.vue'
import PandaWorkspace from '@/components/PandaWorkspace.vue'
import PandaNavigation from '@/components/widgets/PandaNavigation.vue'
import PandaToolbar from '@/components/widgets/PandaToolbar.vue'
import {useThemeStore} from '@/stores/theme.store.js'

const themeStore = useThemeStore()

// ==================== EVENT HANDLERS (LOG ONLY) ====================
const handleFetch = () => {
  console.log('🔄 FETCH: Fetching from remote...')
}

const handlePull = () => {
  console.log('⬇️ PULL: Pulling changes from remote...')
}

const handlePush = () => {
  console.log('⬆️ PUSH: Pushing changes to remote...')
}

const handleOpenSettings = () => {
  console.log('⚙️ OPEN SETTINGS: Opening settings panel...')
}

</script>
<!--https://heroicons.com/solid-->
<style></style>
