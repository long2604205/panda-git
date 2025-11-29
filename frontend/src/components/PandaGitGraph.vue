<template>
  <div class="git-graph-wrapper">
    <!-- Graph Viewport -->
    <div ref="viewport" class="graph-viewport">
      <!-- Sticky Header BÊN TRONG viewport -->
      <div class="column-header" :style="{ right: '350px' }">
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
              height: `${rowHeight}px`,
            }"
            :data-id="commit.id"
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
import { ref, computed, onMounted, watch, nextTick } from "vue";

const props = defineProps({
  commits: {
    type: Array,
    required: true,
  },
  // --- SEARCH PROPS (Highlight) ---
  searchQuery: {
    type: String,
    default: "",
  },
  searchOptions: {
    type: Object,
    default: () => ({ matchCase: false, matchWord: false, useRegex: false }),
  },

  // --- FILTER PROPS (Ẩn hiện data) ---
  filterBranch: {
    type: String,
    default: 'all'
  },
  filterAuthor: {
    type: String, // Email hoặc Name tùy data của bạn
    default: 'all'
  },
  filterDate: {
    type: Object,
    default: () => ({ from: null, to: null })
  }
});

const emit = defineEmits(["select-commit"]);

// Constants
const ROW_HEIGHT = 36;
const COL_WIDTH = 22;
const X_OFFSET = 20;
const Y_OFFSET = 18;
const PALETTE = [
  "#22d3ee", "#e879f9", "#f472b6", "#4ade80", "#fbbf24",
  "#38bdf8", "#a78bfa", "#fb923c", "#f87171", "#818cf8",
];

// Refs
const viewport = ref(null);
const svg = ref(null);
const content = ref(null);
const processedCommits = ref([]); // Danh sách đã tính toán tọa độ (x, y)
const graphWidth = ref(0);
const rowHeight = ROW_HEIGHT;

// --- 1. COMPUTED FILTER LOGIC ---
// Lọc dữ liệu thô trước khi tính toán layout
const filteredRawCommits = computed(() => {
  return props.commits.filter(commit => {
    // 1. Filter Branch
    if (props.filterBranch !== 'all' && commit.branch !== props.filterBranch) {
      return false;
    }

    // 2. Filter Author
    if (props.filterAuthor !== 'all') {
      if (commit.author.email !== props.filterAuthor) return false;
    }

    // 3. Filter Date (SỬA LỖI TẠI ĐÂY)
    // Thêm điều kiện: props.filterDate && ... để chắc chắn nó không null
    if (props.filterDate && (props.filterDate.from || props.filterDate.to)) {
      const commitDate = new Date(commit.date).setHours(0, 0, 0, 0);

      if (props.filterDate.from) {
        const fromDate = new Date(props.filterDate.from).setHours(0, 0, 0, 0);
        if (commitDate < fromDate) return false;
      }

      if (props.filterDate.to) {
        const toDate = new Date(props.filterDate.to).setHours(0, 0, 0, 0);
        if (commitDate > toDate) return false;
      }
    }

    return true;
  });
});
// Tính tổng chiều cao dựa trên danh sách ĐÃ LỌC
const totalHeight = computed(() => filteredRawCommits.value.length * ROW_HEIGHT + 40);

// --- 2. LAYOUT LOGIC ---
const layoutCommits = () => {
  const branchToCol = { main: 0, master: 0 };
  let nextCol = 1;

  // Sử dụng filteredRawCommits thay vì props.commits
  processedCommits.value = filteredRawCommits.value.map((commit, index) => {
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
    if (commit.branch === "main" || commit.branch === "master") {
      color = "#3b82f6";
    }

    return {
      ...commit,
      x: X_OFFSET + col * COL_WIDTH,
      y: Y_OFFSET + index * ROW_HEIGHT,
      color: color,
      colIndex: col,
    };
  });

  // Tính lại độ rộng graph để đẩy text sang phải
  const maxCol = processedCommits.value.length > 0
    ? Math.max(...processedCommits.value.map((c) => c.colIndex))
    : 0;
  graphWidth.value = X_OFFSET + maxCol * COL_WIDTH + 30;
};

// --- DRAWING LOGIC ---
const drawGraph = () => {
  if (!svg.value) return;

  svg.value.innerHTML = "";

  // Helper tìm node cha trong danh sách hiện tại
  // Lưu ý: Khi filter, cha của node có thể bị ẩn đi -> Đường nối sẽ không vẽ được hoặc phải vẽ nối tắt (phức tạp).
  // Ở đây ta dùng logic đơn giản: Chỉ vẽ nếu cha cũng đang hiển thị.
  const findParent = (id) => processedCommits.value.find(c => c.id === id);

  // Draw paths
  processedCommits.value.forEach((commit) => {
    commit.parents.forEach((parentId) => {
      const parent = findParent(parentId);
      if (parent) {
        const path = createPath(
          commit.x,
          commit.y,
          parent.x,
          parent.y,
          commit.color,
          commit.colIndex !== parent.colIndex
        );
        svg.value.appendChild(path);
      }
    });
  });

  // Draw nodes
  processedCommits.value.forEach((commit) => {
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", commit.x);
    circle.setAttribute("cy", commit.y);
    circle.setAttribute("r", "6");
    circle.setAttribute("fill", commit.color);
    circle.setAttribute("stroke", "var(--bg-main)");
    circle.setAttribute("stroke-width", "2");
    circle.setAttribute("class", "commit-node");
    circle.dataset.id = commit.id;
    circle.onclick = () => selectCommit(commit);
    svg.value.appendChild(circle);
  });

  // Sau khi vẽ xong, chạy lại Search Text (Highlight) nếu đang có query
  if (props.searchQuery) {
    handleSearch();
  }
};

const createPath = (x1, y1, x2, y2, color, isMerge) => {
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  const d = `M ${x1} ${y1} L ${x2} ${y2}`;
  path.setAttribute("d", d);
  path.setAttribute("stroke", color);
  path.setAttribute("stroke-width", "2");
  path.setAttribute("fill", "none");
  path.setAttribute("class", "branch-path opacity-80");

  if (isMerge) {
    path.setAttribute("stroke-dasharray", "4 2");
    path.setAttribute("opacity", "0.5");
  }
  return path;
};

// --- SEARCH / HIGHLIGHT LOGIC (Giữ nguyên logic highlight của bạn) ---
const highlightNode = (id, isActive) => {
  if (!svg.value) return;
  const node = svg.value.querySelector(`circle[data-id="${id}"]`);
  if (node) {
    if (!props.searchQuery || node.classList.contains("search-match")) {
      node.classList.toggle("is-hovered", isActive);
    }
  }
};

const buildSearchRegex = (query, options) => {
  if (!query) return null;
  let pattern = query;
  let flags = options.matchCase ? "g" : "gi";
  if (!options.useRegex) {
    pattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
  if (options.matchWord) {
    pattern = `\\b${pattern}\\b`;
  }
  try {
    return new RegExp(pattern, flags);
  } catch (e) {
    return null;
  }
};

const handleSearch = () => {
  if (!svg.value || !content.value) return;

  const query = props.searchQuery.trim();
  const options = props.searchOptions;
  const hasQuery = query.length > 0;
  const regex = hasQuery ? buildSearchRegex(query, options) : null;
  let firstMatchElement = null;

  // Xử lý Rows
  const rows = content.value.querySelectorAll(".commit-row");
  rows.forEach((row) => {
    const textContent = row.innerText;
    const isMatch = regex ? regex.test(textContent) : false;

    if (hasQuery && regex) {
      if (isMatch) {
        row.classList.add("search-match");
        row.classList.remove("search-dimmed");
        if (!firstMatchElement) firstMatchElement = row;
      } else {
        row.classList.add("search-dimmed");
        row.classList.remove("search-match");
      }
    } else {
      row.classList.remove("search-match", "search-dimmed");
    }
  });

  // Xử lý Nodes
  processedCommits.value.forEach((commit) => {
    const node = svg.value.querySelector(`circle[data-id="${commit.id}"]`);
    if (!node) return;
    const searchTarget = `${commit.id} ${commit.message} ${commit.author.name}`;
    const isMatch = regex ? regex.test(searchTarget) : false;

    if (hasQuery && regex) {
      if (isMatch) {
        node.classList.add("search-match");
        node.classList.remove("search-dimmed");
      } else {
        node.classList.add("search-dimmed");
        node.classList.remove("search-match");
      }
    } else {
      node.classList.remove("search-match", "search-dimmed");
    }
  });

  // Xử lý Paths
  const paths = svg.value.querySelectorAll("path");
  paths.forEach((path) => {
    if (hasQuery && regex) {
      path.classList.add("search-dimmed-path");
    } else {
      path.classList.remove("search-dimmed-path");
    }
  });

  // 4. SCROLL TỚI KẾT QUẢ (Logic mới thêm)
  if (firstMatchElement && viewport.value) {
    // scrollIntoView là API native mượt mà nhất
    firstMatchElement.scrollIntoView({
      behavior: "smooth", // Cuộn mượt
      block: "center", // Đưa kết quả vào giữa màn hình cho dễ nhìn
    });
  } else if (!hasQuery && viewport.value) {
    // (Tùy chọn) Nếu xóa search, cuộn về đầu trang
    viewport.value.scrollTo({ top: 0, behavior: "smooth" });
  }
};

const selectCommit = (commit) => {
  emit("select-commit", commit);
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString();
};

// --- LIFECYCLE & WATCHERS ---
onMounted(() => {
  layoutCommits();
  drawGraph();
});

// Watch sự thay đổi của Filters -> Layout lại toàn bộ graph
watch(
  [
    () => props.commits,
    () => props.filterBranch,
    () => props.filterAuthor,
    () => props.filterDate
  ],
  () => {
    layoutCommits();
    drawGraph();
    // Sau khi layout lại, nếu đang có search text thì apply highlight
    nextTick(() => {
      handleSearch();
    });
  },
  { deep: true }
);

// Watch sự thay đổi của Search Text -> Chỉ highlight/dim, KHÔNG layout lại
watch(
  [() => props.searchQuery, () => props.searchOptions],
  () => {
    handleSearch();
  },
  { deep: true }
);
</script>

<style scoped>
.git-graph-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1;
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
  font-family: "JetBrains Mono", monospace;
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
  font-family: "JetBrains Mono", monospace;
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

/* --- SEARCH ANIMATION STYLES --- */

/* Trạng thái bị làm mờ (Dimmed) */
:deep(.search-dimmed) {
  opacity: 0.1 !important;
  filter: grayscale(100%);
  transition: opacity 0.3s ease, filter 0.3s ease;
}

:deep(.search-dimmed-path) {
  opacity: 0.05 !important;
  transition: opacity 0.3s ease;
}

/* Giữ hover effect hoạt động mượt mà */
.commit-row {
  transition: background-color 0.2s ease, opacity 0.3s ease;
}
</style>
