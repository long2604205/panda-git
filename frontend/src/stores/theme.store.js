import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const THEME_KEY = 'app-theme'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem(THEME_KEY) || 'dark')

  function setTheme(t) {
    theme.value = t
  }

  watch(
    theme,
    (t) => {
      localStorage.setItem(THEME_KEY, t)
      document.documentElement.setAttribute('data-theme', t)
    },
    { immediate: true }
  )

  return { theme, setTheme }
})
