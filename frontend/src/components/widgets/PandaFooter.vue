<template>
  <footer
    class="h-6 bg-[var(--bg-status)] text-[var(--status-fg)] flex items-center justify-between px-2 text-[11px] select-none"
  >
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1 px-2 py-0.5 rounded hover:bg-white/10 cursor-pointer">
        <i class="fa-solid fa-code-branch text-[10px]"></i>
        <span class="font-bold">{{ selectedBranch }}</span>
      </div>

      <div class="flex items-center gap-1 px-1 opacity-80">
        <i class="fa-solid fa-cloud-arrow-up text-[10px]"></i>
        <span>0</span>
        <i class="fa-solid fa-cloud-arrow-down text-[10px] ml-1"></i>
        <span>1</span>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <div class="flex bg-black/20 rounded cursor-pointer overflow-hidden">
        <div @click="$emit('change-theme', 'light')" class="px-2 hover:bg-white/20 transition-colors">
          <i class="fa-solid fa-sun text-[10px]"></i>
        </div>
        <div @click="$emit('change-theme', 'dark')" class="px-2 hover:bg-white/20 transition-colors">
          <i class="fa-solid fa-moon text-[10px]"></i>
        </div>
      </div>
      <span class="px-1">Panda Git v2.4</span>
    </div>
  </footer>
</template>

<script setup>
defineProps({
  selectedBranch: String,
})

defineEmits(["change-theme"])
</script>
