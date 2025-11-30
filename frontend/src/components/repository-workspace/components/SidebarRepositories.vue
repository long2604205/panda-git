<template>
  <div class="flex flex-col h-full overflow-hidden">
    <div class="sidebar-section-title border-b border-[var(--border-color)] flex items-center justify-between">
      <span>Repositories</span>
      <div class="flex gap-2">
        <div
          class="cursor-pointer hover:text-[var(--p-text-main)] px-1 rounded hover:bg-[var(--p-hover)] transition-colors"
          :class="{'text-[var(--p-text-main)] bg-[var(--p-hover)]': isMenuOpen}"
          @click.stop="$emit('open-menu', $event)"
        >
          <i class="w-4 fa-solid fa-ellipsis fa-lg hover:text-[var(--text-color)] cursor-pointer items-center text-center" />
        </div>
      </div>
    </div>

    <div class="px-3 py-2 border-b border-[var(--border-color)] border-opacity-30">
      <div class="relative">
        <i class="fa-solid fa-search absolute left-2 top-1/2 transform -translate-y-1/2 text-[10px] text-[var(--p-text-dim)]" />
        <input
          type="text"
          v-model="repoFilter"
          class="search-input w-full pl-6 pr-2 py-1 rounded"
          placeholder="Filter repositories..."
        />
      </div>
    </div>

    <div v-if="filteredView.groups.length > 0 || filteredView.standalone.length > 0" class="flex-1 overflow-y-auto py-1">
      <div v-for="group in filteredView.groups" :key="group.id" class="group-item">
        <div
          class="group-header"
          @click="$emit('toggle-group', group)"
          @dragover.prevent
          @drop="$emit('drop-repo', group)"
          @contextmenu.prevent="$emit('group-context', $event, group)"
        >
          <i
            class="fa-solid fa-chevron-down arrow"
            :class="{
              '-rotate-90': !isGroupExpanded(group),
              invisible: !group.matchedRepos || group.matchedRepos.length === 0,
            }"
          />
          <i
            class="fa-regular"
            :class="[
              !group.matchedRepos || group.matchedRepos.length === 0 ? 'fa-folder' : !isGroupExpanded(group) ? 'fa-folder' : 'fa-folder-open',
              'mr-2 group-icon',
            ]"
            :style="{
              color: !group.matchedRepos || group.matchedRepos.length === 0 ? 'var(--p-text-dim)' : !isGroupExpanded(group) ? 'var(--p-text-dim)' : 'var(--accent-color)',
            }"
          />
          <span>{{ group.name }}</span>
        </div>

        <div class="group-content" v-show="isGroupExpanded(group)">
          <div
            v-for="repo in group.matchedRepos"
            :key="repo.id"
            class="repo-item"
            :class="{ active: selectedRepoId === repo.id }"
            @dblclick="$emit('select-repo', repo)"
            draggable="true"
            @dragstart="$emit('drag-start', repo)"
            @contextmenu.prevent="$emit('repo-context', $event, repo)"
          >
            <i class="fa-solid fa-bars-progress mr-2" />
            <span>{{ repo.name }}</span>
          </div>
        </div>
      </div>

      <div class="drop-standalone min-h-10" @dragover.prevent @drop="$emit('drop-repo', null)">
        <div
          v-for="repo in filteredView.standalone"
          :key="repo.id"
          class="repo-item mt-1"
          :class="{ active: selectedRepoId === repo.id }"
          style="padding-left: 12px"
          @dblclick="$emit('select-repo', repo)"
          draggable="true"
          @dragstart="$emit('drag-start', repo)"
          @contextmenu.prevent="$emit('repo-context', $event, repo)"
        >
          <i class="fa-solid fa-book mr-2" />
          <span>{{ repo.name }}</span>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-gray-500 mt-4 italic">
      <span class="text-[12px]">No repositories found</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps(['groups', 'repositories', 'selectedRepoId', 'isMenuOpen'])

defineEmits(['select-repo', 'toggle-group', 'drag-start', 'drop-repo', 'group-context', 'repo-context', 'open-menu'])

const repoFilter = ref('')

const filteredView = computed(() => {
  const filter = repoFilter.value?.toLowerCase().trim() ?? ''

  // 1. Map lại dữ liệu
  const mappedGroups = props.groups.map(group => {
    // Lấy tất cả repo thuộc group này
    const allReposInGroup = props.repositories.filter(r => (r?.groupId ?? null) === group.id)

    // Kiểm tra xem Tên Group có khớp từ khóa search không?
    const isGroupNameMatch = group.name.toLowerCase().includes(filter)

    // LOGIC QUAN TRỌNG:
    // - Nếu tên Group khớp: Lấy TOÀN BỘ repo (để người dùng xem được nội dung bên trong).
    // - Nếu tên Group KHÔNG khớp: Chỉ lấy những repo khớp từ khóa.
    let matched = []
    if (filter && isGroupNameMatch) {
      matched = allReposInGroup
    } else {
      matched = allReposInGroup.filter(r => r?.name?.toLowerCase().includes(filter))
    }

    return {
      ...group,
      matchedRepos: matched,
      isNameMatch: isGroupNameMatch // Lưu lại cờ này để dùng cho hàm expand
    }
  })

  // 2. Lọc danh sách Group để hiển thị
  const filteredGroups = mappedGroups.filter(g => {
    if (!filter) return true
    // Hiển thị nếu: Có repo con khớp HOẶC tên group khớp
    return g.matchedRepos.length > 0 || g.isNameMatch
  })

  // 3. Standalone repos (Repo lẻ)
  const standalone = props.repositories
    .filter(r => (r?.groupId ?? null) === null)
    .filter(r => r?.name?.toLowerCase().includes(filter))

  return { groups: filteredGroups, standalone }
})

// --- SỬA LOGIC EXPAND ---
function isGroupExpanded(group) {
  const filter = repoFilter.value?.trim()

  // Nếu đang không search thì dùng trạng thái collapsed của DB
  if (!filter) return !group.collapsed

  // Nếu ĐANG SEARCH:
  // Luôn mở group nếu có repo bên trong (matchedRepos > 0)
  // hoặc chính tên group khớp (isNameMatch)
  if (group.matchedRepos.length > 0 || group.isNameMatch) {
    return true
  }

  return !group.collapsed
}
</script>
