import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
  const isLoading = ref(false)
  const message = ref('')

  function show(msg = '') {
    isLoading.value = true
    message.value = msg
  }

  function hide() {
    isLoading.value = false
    message.value = ''
  }

  return { isLoading, message, show, hide }
})
