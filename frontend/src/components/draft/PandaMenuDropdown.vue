<template>
  <div class="nav-item dropdown">
    <a class="nav-link dropdown-toggle px-2" href="#" data-bs-toggle="dropdown">{{ label }}</a>
    <ul class="dropdown-menu dropdown-menu-dark mt-0">
      <template v-for="(item, index) in items" :key="index">
        <li v-if="item === 'divider'"><hr class="dropdown-divider" /></li>
        <li v-else>
          <a class="dropdown-item"
             href="#"
             :data-action="item.action"
             @click.prevent="emit('action', item.action)">
            <i :class="[item.icon, 'me-2']"></i>{{ item.label }}
          </a>
        </li>
      </template>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Dropdown } from 'bootstrap'

defineProps({
  label: String,
  items: Array
})

const emit = defineEmits(['action'])

onMounted(() => {
  document.querySelectorAll('.dropdown-toggle').forEach(el => {
    new Dropdown(el)
  })
})
</script>
<style scoped>
.nav-item .nav-link {
  color: var(--text-secondary);
  font-size: 14px;
  padding: 6px 12px;
}

.nav-link.active {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.dropdown-toggle::after {
  display: none;
}

.dropdown-menu-dark {
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.dropdown-menu-dark .dropdown-item {
  color: var(--text-secondary);
  font-size: 14px;
  padding: 6px 12px;
}

.dropdown-menu-dark .dropdown-item:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.dropdown-divider {
  border-color: var(--border-color);
}
</style>
