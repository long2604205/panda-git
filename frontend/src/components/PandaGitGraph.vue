<template>
  <div class="git-graph-wrapper">
    <!-- Graph Viewport -->
    <div ref="viewport" class="graph-viewport">
      <!-- Sticky Header BÊN TRONG viewport -->
      <div
        class="column-header"
        :style="{ right: '350px' }"
      >
        <div class="header-col flex-1">Graph & Subject</div>
        <div class="header-col w-author">Author</div>
        <div class="header-col w-date">Date</div>
      </div>

      <div class="graph-content-wrapper">
        <svg
          ref="svg"
          class="graph-svg"
          :style="{ height: `${totalHeight}px` }"
        ></svg>

        <div
          ref="content"
          class="graph-content"
          :style="{ height: `${totalHeight}px` }"
        >
          <div
            v-for="(commit, idx) in processedCommits"
            :key="commit.id"
            class="commit-row"
            :style="{
              top: `${idx * rowHeight}px`,
              height: `${rowHeight}px`
            }"
            @mouseenter="highlightNode(commit.id, true)"
            @mouseleave="highlightNode(commit.id, false)"
            @click="selectCommit(commit)"
          >
            <div class="commit-row-content">
              <!-- Graph & Subject -->
              <div
                class="commit-col flex-1"
                :style="{ paddingLeft: `${graphWidth}px` }"
              >
                <span class="commit-hash">{{ commit.id }}</span>
                <div class="commit-message-wrapper">
                  <span class="commit-message">{{ commit.message }}</span>
                  <span v-if="commit.type === 'merge'" class="merge-badge">
                    Merge
                  </span>
                </div>
              </div>

              <!-- Author -->
              <div class="commit-col w-author">
                <div class="author-info">
                  <div class="author-avatar">{{ commit.author.initials }}</div>
                  <span class="author-name">{{ commit.author.name }}</span>
                </div>
              </div>

              <!-- Date -->
              <div class="commit-col w-date commit-date">
                {{ formatDate(commit.date) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

const props = defineProps({
  commits: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['select-commit']);

// Constants
const ROW_HEIGHT = 36;
const COL_WIDTH = 22;
const X_OFFSET = 20;
const Y_OFFSET = 18;
const PALETTE = [
  '#22d3ee', '#e879f9', '#f472b6', '#4ade80', '#fbbf24',
  '#38bdf8', '#a78bfa', '#fb923c', '#f87171', '#818cf8'
];

// Refs
const viewport = ref(null);
const svg = ref(null);
const content = ref(null);
const processedCommits = ref([]);
const graphWidth = ref(0);
const rowHeight = ROW_HEIGHT;

// Computed
const totalHeight = computed(() => props.commits.length * ROW_HEIGHT + 40);

// Methods
const layoutCommits = () => {
  const branchToCol = { main: 0, master: 0 };
  let nextCol = 1;

  processedCommits.value = props.commits.map((commit, index) => {
    let col;
    if (branchToCol[commit.branch] !== undefined) {
      col = branchToCol[commit.branch];
    } else {
      col = nextCol;
      nextCol = (nextCol + 1) % 10;
      if (nextCol === 0) nextCol = 1;
      branchToCol[commit.branch] = col;
    }

    let color = PALETTE[col % PALETTE.length];
    if (commit.branch === 'main' || commit.branch === 'master') {
      color = '#3b82f6';
    }

    return {
      ...commit,
      x: X_OFFSET + col * COL_WIDTH,
      y: Y_OFFSET + index * ROW_HEIGHT,
      color: color,
      colIndex: col
    };
  });

  const maxCol = Math.max(...processedCommits.value.map(c => c.colIndex));
  graphWidth.value = X_OFFSET + maxCol * COL_WIDTH + 30;
};

const drawGraph = () => {
  if (!svg.value) return;

  svg.value.innerHTML = '';

  // Draw paths
  processedCommits.value.forEach(commit => {
    commit.parents.forEach(parentId => {
      const parent = processedCommits.value.find(c => c.id === parentId);
      if (parent) {
        const path = createPath(
          commit.x, commit.y,
          parent.x, parent.y,
          commit.color,
          commit.colIndex !== parent.colIndex
        );
        svg.value.appendChild(path);
      }
    });
  });

  // Draw nodes
  processedCommits.value.forEach(commit => {
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', commit.x);
    circle.setAttribute('cy', commit.y);
    circle.setAttribute('r', '6');
    circle.setAttribute('fill', commit.color);
    circle.setAttribute('stroke', 'var(--bg-main)');
    circle.setAttribute('stroke-width', '2');
    circle.setAttribute('class', 'commit-node');
    circle.dataset.id = commit.id;
    circle.onclick = () => selectCommit(commit);
    svg.value.appendChild(circle);
  });
};

const createPath = (x1, y1, x2, y2, color, isMerge) => {
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  const d = `M ${x1} ${y1} L ${x2} ${y2}`;

  path.setAttribute('d', d);
  path.setAttribute('stroke', color);
  path.setAttribute('stroke-width', '2');
  path.setAttribute('fill', 'none');
  path.setAttribute('class', 'branch-path opacity-80');

  if (isMerge) {
    path.setAttribute('stroke-dasharray', '4 2');
    path.setAttribute('opacity', '0.5');
  }

  return path;
};

const highlightNode = (id, isActive) => {
  if (!svg.value) return;
  const node = svg.value.querySelector(`circle[data-id="${id}"]`);
  if (node) {
    node.classList.toggle('is-hovered', isActive);
  }
};

const selectCommit = (commit) => {
  emit('select-commit', commit);
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString();
};

// Lifecycle
onMounted(() => {
  layoutCommits();
  drawGraph();
});

watch(() => props.commits, () => {
  layoutCommits();
  drawGraph();
}, { deep: true });
</script>

<style scoped>
.git-graph-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.graph-viewport {
  flex: 1;
  overflow: auto;
  position: relative;
  background-size: 100% 36px;
  background-position: 0 35px;
}

.column-header {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  height: 36px;
  background-color: var(--bg-main);
  border-bottom: 1px solid var(--border-color);
  z-index: 30;
  display: flex;
  text-transform: uppercase;
  font-size: 10px;
  font-weight: 700;
  color: var(--p-text-dim);
  letter-spacing: 0.05em;
  transition: right 0.3s;
}

.header-col {
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-right: 1px solid var(--border-color);
}

.header-col.flex-1 {
  flex: 1;
  min-width: 0;
}

.w-author {
  width: 180px;
  flex-shrink: 0;
}

.w-date {
  width: 140px;
  flex-shrink: 0;
  justify-content: flex-end;
}

.graph-content-wrapper {
  position: relative;
  min-width: 100%;
}

.graph-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  pointer-events: none;
  z-index: 10;
}

.graph-content {
  position: relative;
  z-index: 20;
  min-height: 100%;
}

.commit-row {
  position: absolute;
  left: 0;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.05s ease;
}

.commit-row:hover {
  background-color: var(--p-selection);
}

.commit-row-content {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  font-size: 13px;
}

.commit-col {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 16px;
  border-right: 1px solid var(--border-color);
  overflow: hidden;
}

.commit-col.flex-1 {
  flex: 1;
  min-width: 0;
}

.commit-hash {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--p-text-muted);
  opacity: 0.5;
  width: 56px;
  flex-shrink: 0;
}

.commit-message-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.commit-message {
  color: var(--text-color);
  font-weight: 250;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.merge-badge {
  padding: 2px 6px;
  border-radius: 2px;
  font-size: 9px;
  background-color: var(--p-selection);
  color: var(--accent-color);
  border: 1px solid var(--border-color);
  line-height: 1;
  flex-shrink: 0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  overflow: hidden;
}

.author-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: var(--p-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: var(--text-color);
  font-weight: 700;
  flex-shrink: 0;
}

.author-name {
  color: var(--p-text-muted);
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.commit-date {
  justify-content: flex-end;
  font-size: 12px;
  color: var(--p-text-dim);
  font-family: 'JetBrains Mono', monospace;
}

/* Graph Styles */
:deep(.commit-node) {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-origin: center;
  cursor: pointer;
  filter: drop-shadow(0 0 3px rgba(0, 0, 0, 0.6));
}

:deep(.commit-node:hover),
:deep(.commit-node.is-hovered) {
  r: 8;
  stroke-width: 3px;
  filter: drop-shadow(0 0 6px currentColor);
}

:deep(.branch-path) {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: opacity 0.3s ease;
  pointer-events: auto;
}

:deep(.branch-path:hover) {
  stroke-width: 4px !important;
  opacity: 1 !important;
  filter: drop-shadow(0 0 4px currentColor);
}
</style>
