<template>
  <footer
    class="h-8 bg-[var(--bg-status)] text-[var(--status-fg)] flex items-center justify-between px-2 text-[11px] select-none"
  >
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1 px-2 py-0.5 rounded hover:bg-white/10 cursor-pointer">
        <i class="fa-solid fa-code-branch text-[10px]" />
        <span class="font-bold">{{ repositoryStore.branchName }}</span>
      </div>

      <div class="flex items-center gap-1 px-1 opacity-80">
        <i class="fa-solid fa-cloud-arrow-up text-[10px]" />
        <span>0</span>
        <i class="fa-solid fa-cloud-arrow-down text-[10px] ml-1" />
        <span>1</span>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <theme-switch
        v-model="isDarkTheme"
        @change-theme="handleThemeChange"
      />
      <span class="px-1">Panda Git v2.4</span>
    </div>
  </footer>
</template>

<script setup>
import ThemeSwitch from '@/components/common/ThemeSwitch.vue'
import { onMounted, ref } from 'vue'
import { useThemeStore } from '@/stores/theme.store.js'
import { useRepositoryStore } from '@/stores/repositoryStore.js'

const repositoryStore = useRepositoryStore()
const themeStore = useThemeStore()

const isDarkTheme = ref(false)

// Chuyển sự kiện đổi theme từ Switch lên cấp cha (App.vue?)
const handleThemeChange = (newTheme) => {
    isDarkTheme.value = (newTheme === 'dark') // Cập nhật trạng thái checkbox
    themeStore.setTheme(newTheme)
}

onMounted(() => {
  // 1. Lấy giá trị theme từ store
  const currentTheme = themeStore.theme

  // 2. Chuyển đổi giá trị string ('light'/'dark') sang boolean (true/false)
  // Checkbox sẽ được CHECKED (true) nếu theme là 'dark'.
  isDarkTheme.value = currentTheme === 'dark'

  // Console log để kiểm tra:
  console.log(`Store Theme: ${currentTheme}, isDarkTheme: ${isDarkTheme.value}`)
})
</script>
