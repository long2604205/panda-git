<template>
  <main class="flex-1 flex flex-col bg-[var(--bg-main)] min-w-0 relative" style="min-width: 300px">
    <!-- TOP PANE: WORKING COPY -->
<!--    <div ref="paneWorking" style="height: 300px"-->
<!--         class="flex bg-[var(&#45;&#45;bg-main)] shrink-0 border-b border-[var(&#45;&#45;border-color)]">-->
<!--      &lt;!&ndash; Left: File Tree (Staging) &ndash;&gt;-->
<!--      <div ref="paneStaging" style="width: 50%" class="flex flex-col border-r border-[var(&#45;&#45;border-color)]">-->
<!--        <div-->
<!--          class="h-8 px-4 flex items-center justify-between border-b border-[var(&#45;&#45;border-color)] text-xs font-bold text-[var(&#45;&#45;p-text-muted)] uppercase tracking-wider bg-[var(&#45;&#45;bg-side)]">-->
<!--          <div class="flex items-center gap-2">-->
<!--            <input type="checkbox" class="tree-checkbox" checked />-->
<!--            <span>Changes-->
<!--                <span-->
<!--                  class="ml-1 px-1.5 py-0.5 rounded bg-[var(&#45;&#45;p-hover)] text-[var(&#45;&#45;text-color)] opacity-80 font-mono">-->
<!--                  4 files-->
<!--                </span>-->
<!--              </span>-->
<!--          </div>-->
<!--          <div class="flex gap-3 text-[var(&#45;&#45;text-color)] opacity-70">-->
<!--            <i class="fa-solid fa-layer-group cursor-pointer hover:text-[var(&#45;&#45;accent-color)]"></i><i-->
<!--            class="fa-solid fa-expand cursor-pointer hover:text-[var(&#45;&#45;accent-color)]"></i>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div class="flex-1 overflow-y-auto p-1" id="working-tree-container">-->
<!--          &lt;!&ndash; Tree &ndash;&gt;-->
<!--        </div>-->
<!--      </div>-->

<!--      &lt;!&ndash; SPLITTER: WORKING HORIZONTAL &ndash;&gt;-->
<!--      <div ref="resizerWorkingInner" class="resizer-v bg-[var(&#45;&#45;border-color)]"></div>-->

<!--      &lt;!&ndash; Right: Commit Message &ndash;&gt;-->
<!--      <div class="flex-1 flex flex-col min-w-0">-->
<!--        <div-->
<!--          class="h-8 px-4 flex items-center border-b border-[var(&#45;&#45;border-color)] text-xs font-bold text-[var(&#45;&#45;p-text-muted)] uppercase tracking-wider bg-[var(&#45;&#45;bg-side)]">-->
<!--          <span>Commit</span>-->
<!--          <div class="ml-auto flex gap-2 text-[var(&#45;&#45;text-color)]">-->
<!--            <i class="fa-solid fa-clock-rotate-left cursor-pointer hover:text-[var(&#45;&#45;accent-color)]"-->
<!--               title="History"></i>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div class="flex-1 p-3 flex flex-col gap-2">-->
<!--          <div class="flex items-center gap-2 select-none">-->
<!--            <input type="checkbox" id="amend-check" class="tree-checkbox" /><label for="amend-check"-->
<!--                                                                                   class="text-xs text-[var(&#45;&#45;text-color)] cursor-pointer">Amend</label>-->
<!--          </div>-->
<!--          <textarea-->
<!--            class="w-full h-full bg-transparent border border-[var(&#45;&#45;border-color)] outline-none text-sm text-[var(&#45;&#45;text-color)] font-mono resize-none p-2 rounded hover:border-[var(&#45;&#45;p-text-muted)] focus:border-[var(&#45;&#45;accent-color)] transition-colors placeholder-[var(&#45;&#45;p-text-dim)]"-->
<!--            placeholder="Commit Message"></textarea>-->
<!--        </div>-->
<!--        <div-->
<!--          class="h-12 border-t border-[var(&#45;&#45;border-color)] flex items-center justify-between px-4 bg-[var(&#45;&#45;bg-side)]">-->
<!--          <div class="flex gap-2">-->
<!--            <button class="btn btn-primary text-xs">Commit</button><button-->
<!--            class="btn btn-secondary text-xs">-->
<!--            Commit and Push...-->
<!--          </button>-->
<!--          </div>-->
<!--          <i-->
<!--            class="fa-solid fa-ellipsis-vertical text-[var(&#45;&#45;p-text-dim)] hover:text-[var(&#45;&#45;text-color)] cursor-pointer px-2"></i>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->

    <!-- SPLITTER: MAIN VERTICAL -->
<!--    <div ref="resizerMainVert" class="resizer-h bg-[var(&#45;&#45;border-color)]"></div>-->

      <div class="sidebar-section-title border-b border-[var(--border-color)]">
        <span>Working Space</span>
      </div>
    <!-- BOTTOM PANE: TABS -->
    <div ref="paneGraph" class="flex-1 flex flex-col min-h-0">

      <!-- TAB BAR -->
      <div class="h-9 flex items-center bg-[var(--bg-header)] border-b border-[var(--border-color)] shrink-0">
        <!-- TAB: GIT GRAPH -->
        <div
          @click="activeTab = 'graph'"
          :class="[
            'h-full px-4 flex items-center gap-2 text-xs border-r border-[var(--border-color)] cursor-pointer',
            activeTab === 'graph'
              ? 'bg-[var(--p-selection)] text-[var(--accent-color)]'
              : 'text-[var(--p-text-dim)] hover:bg-[var(--bg-side)]'
          ]"
        >
          <i class="fa-solid fa-code-commit"></i>
          <span>History Graph</span>
        </div>
        <!-- TAB: TERMINAL -->
        <div
          @click="activeTab = 'terminal'"
          :class="[
            'h-full px-4 flex items-center gap-2 text-xs border-r border-[var(--border-color)] cursor-pointer',
            activeTab === 'terminal'
              ? 'bg-[var(--p-selection)] text-[var(--accent-color)]'
              : 'text-[var(--p-text-dim)] hover:bg-[var(--bg-side)]'
          ]"
        >
          <i class="fa-solid fa-terminal"></i>
          <span>Terminal</span>
        </div>
      </div>

      <!-- TAB CONTENT -->
      <div class="flex-1 min-h-0 relative">
        <!-- GIT GRAPH -->
        <div
          v-show="activeTab === 'graph'"
          class="w-full h-full graph-container"
          id="graph-scroll-area"
        >
          <!-- B. NEW FILTER BAR (FIXED UI) -->
            <div class="h-10 flex-shrink-0 flex items-center px-4 gap-2 bg-[var(--bg-header)] border-b border-[var(--border-color)] z-30 relative">

                <!-- Search Box -->
                <div class="relative w-64 group">
                    <i class="fa-solid fa-magnifying-glass absolute left-2.5 top-1/2 transform -translate-y-1/2 text-[11px] text-[var(--p-text-dim)] group-focus-within:text-[var(--accent-color)]"></i>
                    <input type="text" id="filterSearch" class="filter-input" placeholder="Search message or hash..." />
                </div>

                <div class="h-4 w-px bg-[var(--border-color)] mx-2"></div>

                <!-- Custom Filters -->
                <div class="flex items-center gap-2">

                    <!-- Branch Filter -->
                    <div class="custom-select-container" id="filterBranchContainer">
                        <div class="custom-select-trigger" data-value="all">
                            <span>All Branches</span>
                            <i class="fa-solid fa-chevron-down"></i>
                        </div>
                        <div class="custom-select-menu">
                            <div class="custom-option selected" data-value="all">All Branches</div>
                            <!-- Dynamic items here -->
                        </div>
                    </div>

                    <!-- Author Filter -->
                    <div class="custom-select-container" id="filterAuthorContainer">
                        <div class="custom-select-trigger" data-value="all">
                            <span>All Authors</span>
                            <i class="fa-solid fa-chevron-down"></i>
                        </div>
                        <div class="custom-select-menu">
                            <div class="custom-option selected" data-value="all">All Authors</div>
                            <!-- Dynamic items here -->
                        </div>
                    </div>

                    <!-- Date Filter -->
                    <div class="custom-select-container" id="filterDateContainer" style="min-width: 100px;">
                        <div class="custom-select-trigger" data-value="all">
                            <span>Any Time</span>
                            <i class="fa-solid fa-chevron-down"></i>
                        </div>
                        <div class="custom-select-menu">
                            <div class="custom-option selected" data-value="all">Any Time</div>
                            <div class="custom-option" data-value="24h">Last 24 Hours</div>
                            <div class="custom-option" data-value="7d">Last 7 Days</div>
                            <div class="custom-option" data-value="30d">Last 30 Days</div>
                        </div>
                    </div>

                </div>

                <!-- Reset Button -->
                <button onclick="resetFilters()" id="resetBtn" class="ml-auto text-[10px] text-[var(--p-text-muted)] hover:text-[var(--accent-color)] hidden transition-colors px-2 py-1 rounded hover:bg-[var(--p-hover)]">
                    <i class="fa-solid fa-rotate-left mr-1"></i> Reset
                </button>
            </div>
            <panda-git-graph
              :commits="filteredCommits"
              @select-commit="handleSelectCommit"
            />
        </div>

        <!-- TERMINAL -->
        <div
          v-show="activeTab === 'terminal'"
          class="w-full h-full p-2 text-sm font-mono text-[var(--text-color)] overflow-auto"
        >
          <div class="border border-[var(--border-color)] rounded p-2 h-full bg-black text-green-400">
            <!-- Bạn nhúng terminal vào đây -->
            <p>Terminal here...</p>
          </div>
        </div>
      </div>
    </div>

  </main>
</template>
<script setup>
import {ref, onMounted, computed} from "vue";
import PandaGitGraph from "@/components/PandaGitGraph.vue";
import mitter from "@/plugins/mitter.js";
import {commitSapmle} from "@/data/commitSapmle.js";

const activeTab = ref('graph');

// DOM refs
const paneStaging = ref(null);        // left in top pane
const resizerWorkingInner = ref(null);

const paneWorking = ref(null);        // top pane (working copy)
const paneGraph = ref(null);          // bottom pane (graph)
const resizerMainVert = ref(null);

// generic resize initializer
function initResize(resizerEl, prevEl, nextEl, isVertical) {
  if (!resizerEl || !prevEl) return;

  let startX, startY, startW, startH;
  let nextStartW, nextStartH;

  const onMouseDown = (e) => {
    startX = e.clientX;
    startY = e.clientY;

    const prevRect = prevEl.getBoundingClientRect();
    startW = prevRect.width;
    startH = prevRect.height;

    if (nextEl) {
      const nextRect = nextEl.getBoundingClientRect();
      nextStartW = nextRect.width;
      nextStartH = nextRect.height;
    }

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);

    document.body.classList.add(isVertical ? "resizing-col" : "resizing-row");
  };

  const onMouseMove = (e) => {
    if (isVertical) {
      const dx = e.clientX - startX;
      prevEl.style.width = `${startW + dx}px`;
      if (nextEl) nextEl.style.width = `${nextStartW - dx}px`;
    } else {
      const dy = e.clientY - startY;
      prevEl.style.height = `${startH + dy}px`;
      if (nextEl) nextEl.style.height = `${nextStartH - dy}px`;
    }
  };

  const onMouseUp = () => {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);

    document.body.classList.remove("resizing-col");
    document.body.classList.remove("resizing-row");
  };

  resizerEl.addEventListener("mousedown", onMouseDown);
}

onMounted(() => {
  // 1) Horizontal split: staging (left) <-> commit (right)
  initResize(
    resizerWorkingInner.value,   // splitter
    paneStaging.value,           // left pane
    null,                        // right auto flex -> không cần set
    true                         // horizontal movement (resize width)
  );

  // 2) Vertical split: working (top) <-> graph (bottom)
  initResize(
    resizerMainVert.value,       // splitter
    paneWorking.value,           // top pane
    paneGraph.value,             // bottom pane (giãn ngược)
    false                        // vertical movement (resize height)
  );
});


class DataGenerator {
  constructor() {
    this.users = [
      { name: 'Lion Wilson', email: 'lion@panda.com', initials: 'LW' },
      { name: 'Sarah Chen', email: 'sarah@tech.co', initials: 'SC' },
      { name: 'Mike Ross', email: 'mike@tech.co', initials: 'MR' },
      { name: 'Bot CI/CD', email: 'bot@ci.com', initials: 'BT' }
    ];

    this.features = [
      'ui-refresh', 'dark-mode', 'api-opt', 'sidebar',
      'auth-flow', 'chart-fix', 'export-csv'
    ];

    this.files = [
      'src/App.tsx', 'package.json', 'src/components/Header.tsx',
      'src/utils/api.ts', 'README.md', 'src/styles.css'
    ];
  }

  getSHA() {
    return Math.random().toString(16).substring(2, 9);
  }

  getRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  getChanges() {
    const count = Math.floor(Math.random() * 4) + 1;
    const changes = [];
    for (let i = 0; i < count; i++) {
      const status = Math.random() > 0.8
        ? (Math.random() > 0.5 ? 'A' : 'D')
        : 'M';
      changes.push({
        file: this.getRandom(this.files),
        status: status
      });
    }
    return changes;
  }

  generate(count = 150) {
    const commits = [];
    let branches = { main: null };
    let activeFeatures = {};
    const rootId = this.getSHA();

    // Initial commit
    commits.push(this.createCommit(
      rootId, [], 'main', 'Initial commit',
      this.users[0], count, 'commit', []
    ));
    branches['main'] = rootId;

    for (let i = 1; i < count; i++) {
      const rand = Math.random();
      let activeBranch = 'main';
      let parents = [];
      let message = '';
      let type = 'commit';

      // Create feature branch
      if (rand < 0.2 && Object.keys(activeFeatures).length < 5) {
        const featName = `feat/${this.getRandom(this.features)}-${i}`;
        if (!activeFeatures[featName]) {
          activeBranch = featName;
          parents = [branches['main']];
          activeFeatures[featName] = null;
          message = `Start ${featName}`;
        }
      }
      // Merge branch
      else if (rand < 0.35 && Object.keys(activeFeatures).length > 0) {
        const feats = Object.keys(activeFeatures);
        const source = feats[0];
        if (branches[source]) {
          activeBranch = 'main';
          parents = [branches['main'], branches[source]];
          type = 'merge';
          message = `Merge ${source}`;
          delete activeFeatures[source];
        }
      }
      // Regular commit
      else {
        const candidates = ['main', ...Object.keys(activeFeatures)];
        const valid = candidates.filter(b => branches[b] || activeFeatures[b]);
        activeBranch = valid[Math.floor(Math.random() * valid.length)];
        parents = [branches[activeBranch] || branches['main']];
        message = `Update logic in ${activeBranch}`;
      }

      const newId = this.getSHA();
      const author = this.getRandom(this.users);
      commits.push(this.createCommit(
        newId, parents, activeBranch, message,
        author, count - i, type, this.getChanges()
      ));

      branches[activeBranch] = newId;
      if (activeFeatures[activeBranch] !== undefined) {
        activeFeatures[activeBranch] = newId;
      }
    }

    return commits.reverse();
  }

  createCommit(id, parents, branch, message, author, timeOffset, type, changes) {
    return {
      id,
      parents: parents.filter(p => p),
      branch,
      message,
      author,
      date: new Date(Date.now() - timeOffset * 3600000).toISOString(),
      type,
      changes
    };
  }
}

// State
const generator = new DataGenerator();
// const commits = ref(generator.generate(150));
const commits = ref(commitSapmle)
const searchTerm = ref('');

// Computed
const filteredCommits = computed(() => {
  if (!searchTerm.value) return commits.value;

  const term = searchTerm.value.toLowerCase();
  return commits.value.filter(commit => {
    return (
      commit.message.toLowerCase().includes(term) ||
      commit.author.name.toLowerCase().includes(term) ||
      commit.branch.toLowerCase().includes(term) ||
      commit.id.includes(term)
    );
  });
});

// Methods
const handleSelectCommit = (commit) => {
  mitter.emit('select-commit', commit);
};
</script>

<style scoped>
        /* --- FILTER BAR STYLES (FIXED) --- */
        .filter-input {
            background: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            outline: none;
            font-size: 11px;
            transition: border-color 0.2s;
            padding: 5px 8px 5px 30px; /* More left padding for icon */
            border-radius: 4px;
            width: 100%;
            height: 26px;
        }

        .filter-input:focus {
            border-color: var(--accent-color);
        }

        /* CUSTOM DROPDOWN CSS (FIXED) */
        .custom-select-container {
            position: relative;
            min-width: 130px;
            height: 26px;
        }

        .custom-select-trigger {
            background-color: var(--input-bg);
            border: 1px solid var(--border-color);
            color: var(--p-text-muted);
            font-size: 11px;
            padding: 0 8px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: space-between;
            user-select: none;
            height: 100%;
            white-space: nowrap;
        }

        .custom-select-trigger:hover {
            border-color: var(--p-text-dim);
            color: var(--text-color);
            background-color: var(--p-hover);
        }

        .custom-select-trigger.active {
            border-color: var(--accent-color);
            color: var(--text-color);
        }

        .custom-select-trigger i {
            transition: transform 0.2s ease;
            margin-left: 8px;
            font-size: 10px;
        }

        .custom-select-trigger.active i {
            transform: rotate(180deg);
        }

        /* FIXED MENU STYLES */
        .custom-select-menu {
            position: absolute;
            top: calc(100% + 4px);
            left: 0;
            /* width: 100%; Ensure menu fits trigger width */
            min-width: 100%; /* Can be wider if content needs it */
            max-width: 250px; /* Don't get too wide */

            /* IMPORTANT FIXES FOR OVERFLOW */
            max-height: 250px; /* Fix height issue */
            overflow-y: auto;  /* Add scrollbar */

            background-color: var(--menu-bg); /* Solid background */
            border: 1px solid var(--border-color);
            border-radius: 4px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.6); /* Stronger shadow */
            z-index: 1000; /* High Z-index to sit on top */

            /* Animation States */
            opacity: 0;
            visibility: hidden;
            transform: translateY(-5px);
            transition: all 0.1s ease-in-out;
            pointer-events: none;
        }

        .custom-select-menu.open {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
            pointer-events: auto;
        }

        .custom-option {
            padding: 6px 12px;
            font-size: 11px;
            color: var(--text-color);
            cursor: pointer;
            transition: background 0.1s;
            display: flex;
            align-items: center;
            white-space: nowrap;
        }

        .custom-option:hover {
            background-color: var(--p-selection);
            color: var(--accent-color);
        }

        .custom-option.selected {
            background-color: var(--p-hover);
            color: var(--accent-color);
            font-weight: 600;
            position: relative;
        }

        .custom-option.selected::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: var(--accent-color);
        }
</style>
