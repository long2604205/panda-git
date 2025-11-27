<template>
  <!-- Empty State -->
  <div v-if="!commit" class="empty-state">
      <p class="empty-text">Select commit to view changes</p>
    </div>
  <!-- Commit Content -->
  <div v-else class="detail-content">
    <!-- Branch & Hash -->
    <div class="detail-section">
      <div class="badge-row">
        <span
          class="branch-badge"
          :style="{
            color: commit.color,
            borderColor: commit.color,
            backgroundColor: commit.color + '10'
          }"
        >
          {{ commit.branch }}
        </span>
        <span class="hash-badge">{{ commit.id }}</span>
      </div>
      <h2 class="commit-title">{{ commit.message }}</h2>
    </div>
  <!-- Author Info -->
    <div class="author-card">
      <div class="avatar">{{ commit.author.initials }}</div>
      <div class="author-details">
        <span class="author-name">{{ commit.author.name }}</span>
        <span class="author-email">{{ commit.author.email }}</span>
      </div>
    </div>
      <!-- Metadata -->
    <div class="detail-section">
      <div class="metadata-item">
        <span class="metadata-label">Date</span>
        <span class="metadata-value">{{ formatDate(commit.date) }}</span>
      </div>
      <div class="metadata-item">
        <span class="metadata-label">Commit Type</span>
        <span class="metadata-value">{{ commit.type }}</span>
      </div>
      <div class="metadata-item">
        <span class="metadata-label">Parents</span>
        <span class="metadata-value">
          {{ commit.parents.length > 0 ? commit.parents.join(', ') : 'None' }}
        </span>
      </div>
    </div>

      <!-- Changed Files -->
    <div class="detail-section">
      <h3 class="section-title">Changed Files</h3>
      <div v-if="commit.changes && commit.changes.length > 0" class="file-list">
        <div
          v-for="(file, idx) in commit.changes"
          :key="idx"
          class="file-item"
        >
          <span class="file-status" :class="`status-${file.status.toLowerCase()}`">
            {{ file.status }}
          </span>
          <span class="file-path">{{ file.file }}</span>
        </div>
      </div>
      <div v-else class="no-changes">
        <span>No changes recorded</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from "vue";
import mitter from "@/plugins/mitter.js";

const commit = ref(null)
onMounted(() => {
  mitter.on('select-commit', (data) => {
    commit.value = data;
  });
});

onBeforeUnmount(() => {
  mitter.off('select-commit')
})
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--p-text-muted);
  padding: 32px;
  text-align: center;
  opacity: 0.6;
}

.empty-text {
  font-size: 12px;
  font-weight: 200;
}

.detail-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.branch-badge {
  padding: 4px 8px;
  border-radius: 2px;
  font-size: 10px;
  border: 1px solid;
  font-family: 'JetBrains Mono', monospace;
  opacity: 0.7;
}

.hash-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--p-text-muted);
  background-color: var(--p-hover);
  padding: 4px 6px;
  border-radius: 2px;
}

.commit-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-color);
  line-height: 1.4;
}

.author-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: var(--bg-main);
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--p-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: var(--text-color);
  font-weight: 700;
  flex-shrink: 0;
}

.author-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
}

.author-name {
  font-size: 12px;
  color: var(--text-color);
  font-weight: 500;
}

.author-email {
  font-size: 10px;
  color: var(--p-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.metadata-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid var(--border-color);
  border-opacity: 0.3;
}

.metadata-item:last-child {
  border-bottom: none;
}

.metadata-label {
  font-size: 11px;
  color: var(--p-text-dim);
  font-weight: 500;
}

.metadata-value {
  font-size: 11px;
  color: var(--text-color);
  font-family: 'JetBrains Mono', monospace;
  text-align: right;
}

.section-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--p-text-dim);
  margin-bottom: 4px;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  color: var(--p-text-muted);
  border-radius: 2px;
  transition: background-color 0.15s;
  cursor: pointer;
}

.file-item:hover {
  background-color: var(--p-hover);
}

.file-status {
  width: 12px;
  font-weight: 700;
  flex-shrink: 0;
  text-align: center;
}

.file-status.status-m {
  color: #fbbf24;
}

.file-status.status-a {
  color: #4ade80;
}

.file-status.status-d {
  color: #f87171;
}

.file-path {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-changes {
  padding: 8px;
  color: var(--p-text-dim);
  font-style: italic;
  font-size: 11px;
}
</style>
