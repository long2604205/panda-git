<template>
  <div class="git-log-panel">
    <div class="log-header">
      <div class="log-tabs">
        <button class="btn btn-sm log-tab active" data-tab="git">
          <i class="fas fa-code-branch me-1"></i>Git
        </button>
        <button class="btn btn-sm log-tab" data-tab="log">
          <i class="fas fa-list me-1"></i>Log
        </button>
        <button class="btn btn-sm log-tab" data-tab="console">
          <i class="fas fa-terminal me-1"></i>Console
        </button>
      </div>

      <div class="log-controls">
        <div class="search-box">
          <input type="text" class="form-control form-control-sm"
                 placeholder="Search commits..." id="log-search">
          <button class="btn btn-sm search-btn">
            <i class="fas fa-search"></i>
          </button>
        </div>

        <div class="filter-controls">
          <select class="form-select form-select-sm" id="branch-filter">
            <option value="">All Branches</option>
          </select>
          <select class="form-select form-select-sm" id="author-filter">
            <option value="">All Authors</option>
          </select>
          <select class="form-select form-select-sm" id="date-filter">
            <option value="">All Dates</option>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          <input type="text" class="form-control form-control-sm"
                 placeholder="Path filter" id="path-filter">
        </div>
      </div>
    </div>

    <div class="log-content">
      <div class="commit-graph" id="commit-graph">
        <div class="no-commits-message text-center py-4">
          <i class="fas fa-history fa-2x mb-2"></i>
          <p>No commits</p>
          <small>Select a repository to view commit history</small>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>

</script>
<style scoped>
.git-log-panel {
  flex: 1;
  background-color: var(--bg-secondary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.log-header {
  background-color: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.log-tabs {
  display: flex;
  gap: 4px;
}

.log-tab {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.log-tab.active,
.log-tab:hover {
  background-color: var(--accent-primary);
  color: var(--bg-primary);
  border-color: var(--accent-primary);
}

.log-controls {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  display: flex;
}

.search-box input {
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 12px;
  width: 150px;
  border-radius: 4px 0 0 4px;
}

.search-btn {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-left: none;
  color: var(--text-secondary);
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 0 4px 4px 0;
  transition: all 0.2s ease;
}

.search-btn:hover {
  color: var(--text-primary);
  background-color: var(--bg-hover);
}

.filter-controls {
  display: flex;
  gap: 4px;
}

.filter-controls select,
.filter-controls input {
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 12px;
  width: 100px;
  border-radius: 4px;
}

.log-content {
  flex: 1;
  overflow: auto;
  position: relative;
}

/* Commit Graph */
.commit-graph {
  padding: 8px;
}

.commit-row {
  display: flex;
  align-items: center;
  padding: 2px 0;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  min-height: 24px;
  border-radius: 2px;
}

.commit-row:hover {
  background-color: var(--bg-hover);
}

.commit-row.selected {
  background-color: var(--accent-primary);
  color: var(--bg-primary);
}

.commit-graph-line {
  width: 120px;
  height: 24px;
  position: relative;
  margin-right: 8px;
  flex-shrink: 0;
}

.graph-node {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  border: 2px solid var(--bg-secondary);
}

.graph-line {
  position: absolute;
  width: 2px;
  height: 100%;
  top: 0;
}

.commit-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.commit-message {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
}

.commit-author {
  width: 120px;
  color: var(--text-secondary);
  font-size: 11px;
  flex-shrink: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.commit-time {
  width: 100px;
  color: var(--text-secondary);
  font-size: 11px;
  text-align: right;
  flex-shrink: 0;
}

.commit-tags {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.commit-tag {
  background-color: var(--accent-secondary);
  color: var(--bg-primary);
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  white-space: nowrap;
}

.commit-hash {
  font-family: "Courier New", monospace;
  color: var(--text-muted);
  font-size: 10px;
  margin-left: 8px;
}

</style>
