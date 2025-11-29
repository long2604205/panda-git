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
      <div
        class="h-9 flex items-center bg-[var(--bg-header)] border-b border-[var(--border-color)] shrink-0"
      >
        <!-- TAB: GIT GRAPH -->
        <div
          @click="activeTab = 'graph'"
          :class="[
            'h-full px-4 flex items-center gap-2 text-xs border-r border-[var(--border-color)] cursor-pointer',
            activeTab === 'graph'
              ? 'bg-[var(--p-selection)] text-[var(--accent-color)]'
              : 'text-[var(--p-text-dim)] hover:bg-[var(--bg-side)]',
          ]"
        >
          <i class="fa-solid fa-diagram-project" />
          <span>History Graph</span>
        </div>
        <!-- TAB: TERMINAL -->
        <div
          @click="activeTab = 'terminal'"
          :class="[
            'h-full px-4 flex items-center gap-2 text-xs border-r border-[var(--border-color)] cursor-pointer',
            activeTab === 'terminal'
              ? 'bg-[var(--p-selection)] text-[var(--accent-color)]'
              : 'text-[var(--p-text-dim)] hover:bg-[var(--bg-side)]',
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
          <div
            class="h-10 flex-shrink-0 flex items-center gap-2 bg-[var(--bg-main)] border-b border-[var(--border-color)] z-30 relative"
          >
            <!-- Search Box -->
            <div
              class="relative flex-1 max-w-md flex items-center bg-[var(--bg-main)] border border-[var(--border-color)] rounded h-8 focus-within:border-[var(--accent-color)] transition-colors"
            >
              <i class="fa-solid fa-search ml-3 text-[10px] text-[var(--p-text-dim)]"></i>
              <input
                v-model="searchTerm"
                type="text"
                class="flex-1 bg-transparent border-none outline-none text-[11px] text-[var(--text-color)] px-2 h-full placeholder-[var(--p-text-dim)]"
                placeholder="Search..."
              />

              <!-- Search Options -->
              <div class="flex gap-1 pr-1">
                <div
                  id="btnMatchCase"
                  class="search-option-btn"
                  :class="{ active: searchOptions.matchCase }"
                  @click="toggleOption('matchCase')"
                  title="Match Case (Alt+C)"
                >
                  <span class="font-mono text-[10px] font-bold">Aa</span>
                </div>

                <div
                  id="btnWords"
                  class="search-option-btn"
                  :class="{ active: searchOptions.matchWord }"
                  @click="toggleOption('matchWord')"
                  title="Match Whole Word (Alt+W)"
                >
                  <span class="font-mono text-[10px] font-bold">
                    <i class="fa-solid fa-w fa-sm"></i>
                  </span>
                </div>

                <div
                  id="btnRegex"
                  class="search-option-btn"
                  :class="{ active: searchOptions.useRegex }"
                  @click="toggleOption('useRegex')"
                  title="Use Regular Expression (Alt+R)"
                >
                  <span class="font-mono text-[10px] font-bold">.*</span>
                </div>
              </div>
            </div>

            <div class="h-4 w-px bg-[var(--border-color)] mx-2"></div>

            <!-- Custom Filters -->
            <div class="flex items-center gap-2">
              <!-- Branch Filter -->
              <panda-select-search
                style="width: 200px"
                v-model="selectedBranch"
                :options="branchList"
                value="id"
                text="label"
                value-default="all"
              />

              <!-- Author Filter -->
              <panda-select-search
                style="width: 200px"
                v-model="selectedAuthor"
                :options="authorList"
                value="email"
                text="name"
                value-default="all"
              />

              <!-- Date Filter -->
              <panda-range-date-picker
                v-model="selectedDateRange"
              />
            </div>
          </div>
          <panda-git-graph
            v-model="selectedDateRange"
            :commits="commits"
            :search-query="searchTerm"
            :search-options="searchOptions"
            @select-commit="handleSelectCommit"
            :filter-branch="selectedBranch"
            :filter-author="selectedAuthor"
            :filter-date="selectedDateRange"
          />
        </div>

        <!-- TERMINAL -->
        <div
          v-show="activeTab === 'terminal'"
          class="w-full h-full p-2 text-sm font-mono text-[var(--text-color)] overflow-auto"
        >
          <div
            class="border border-[var(--border-color)] rounded p-2 h-full bg-black text-green-400"
          >
            <!-- Bạn nhúng terminal vào đây -->
            <p>Terminal here...</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import PandaGitGraph from '@/components/PandaGitGraph.vue'
import mitter from '@/plugins/mitter.js'
import { commitSapmle } from '@/data/commitSapmle.js'
import PandaSelectSearch from '@/components/common/PandaSelectSearch.vue'
import PandaRangeDatePicker from '@/components/common/PandaRangeDatePicker.vue'

const activeTab = ref('graph')

// DOM refs
const paneStaging = ref(null) // left in top pane
const resizerWorkingInner = ref(null)

const paneWorking = ref(null) // top pane (working copy)
const paneGraph = ref(null) // bottom pane (graph)
const resizerMainVert = ref(null)

// generic resize initializer
function initResize(resizerEl, prevEl, nextEl, isVertical) {
  if (!resizerEl || !prevEl) return

  let startX, startY, startW, startH
  let nextStartW, nextStartH

  const onMouseDown = (e) => {
    startX = e.clientX
    startY = e.clientY

    const prevRect = prevEl.getBoundingClientRect()
    startW = prevRect.width
    startH = prevRect.height

    if (nextEl) {
      const nextRect = nextEl.getBoundingClientRect()
      nextStartW = nextRect.width
      nextStartH = nextRect.height
    }

    document.addEventListener('mousemove', onMouseMove)
    document.addEventListener('mouseup', onMouseUp)

    document.body.classList.add(isVertical ? 'resizing-col' : 'resizing-row')
  }

  const onMouseMove = (e) => {
    if (isVertical) {
      const dx = e.clientX - startX
      prevEl.style.width = `${startW + dx}px`
      if (nextEl) nextEl.style.width = `${nextStartW - dx}px`
    } else {
      const dy = e.clientY - startY
      prevEl.style.height = `${startH + dy}px`
      if (nextEl) nextEl.style.height = `${nextStartH - dy}px`
    }
  }

  const onMouseUp = () => {
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)

    document.body.classList.remove('resizing-col')
    document.body.classList.remove('resizing-row')
  }

  resizerEl.addEventListener('mousedown', onMouseDown)
}

onMounted(() => {
  // 1) Horizontal split: staging (left) <-> commit (right)
  initResize(
    resizerWorkingInner.value, // splitter
    paneStaging.value, // left pane
    null, // right auto flex -> không cần set
    true, // horizontal movement (resize width)
  )

  // 2) Vertical split: working (top) <-> graph (bottom)
  initResize(
    resizerMainVert.value, // splitter
    paneWorking.value, // top pane
    paneGraph.value, // bottom pane (giãn ngược)
    false, // vertical movement (resize height)
  )
})

class DataGenerator {
  constructor() {
    this.users = [
      { name: 'Lion Wilson', email: 'lionwilson@gmail.com', initials: 'LW' },
      { name: 'Sarah Chen', email: 'sarah@tech.co', initials: 'SC' },
      { name: 'Mike Ross', email: 'mike@tech.co', initials: 'MR' },
      { name: 'Bot CI/CD', email: 'bot@ci.com', initials: 'BT' },
    ]

    this.features = [
      'ui-refresh',
      'dark-mode',
      'api-opt',
      'sidebar',
      'auth-flow',
      'chart-fix',
      'export-csv',
    ]

    this.files = [
      'src/App.tsx',
      'package.json',
      'src/components/Header.tsx',
      'src/utils/api.ts',
      'README.md',
      'src/styles.css',
    ]
  }

  getSHA() {
    return Math.random().toString(16).substring(2, 9)
  }

  getRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)]
  }

  getChanges() {
    const count = Math.floor(Math.random() * 4) + 1
    const changes = []
    for (let i = 0; i < count; i++) {
      const status = Math.random() > 0.8 ? (Math.random() > 0.5 ? 'A' : 'D') : 'M'
      changes.push({
        file: this.getRandom(this.files),
        status: status,
      })
    }
    return changes
  }

  generate(count = 150) {
    const commits = []
    let branches = { main: null }
    let activeFeatures = {}
    const rootId = this.getSHA()

    // Initial commit
    commits.push(
      this.createCommit(rootId, [], 'main', 'Initial commit', this.users[0], count, 'commit', []),
    )
    branches['main'] = rootId

    for (let i = 1; i < count; i++) {
      const rand = Math.random()
      let activeBranch = 'main'
      let parents = []
      let message = ''
      let type = 'commit'

      // Create feature branch
      if (rand < 0.2 && Object.keys(activeFeatures).length < 5) {
        const featName = `feat/${this.getRandom(this.features)}-${i}`
        if (!activeFeatures[featName]) {
          activeBranch = featName
          parents = [branches['main']]
          activeFeatures[featName] = null
          message = `Start ${featName}`
        }
      }
      // Merge branch
      else if (rand < 0.35 && Object.keys(activeFeatures).length > 0) {
        const feats = Object.keys(activeFeatures)
        const source = feats[0]
        if (branches[source]) {
          activeBranch = 'main'
          parents = [branches['main'], branches[source]]
          type = 'merge'
          message = `Merge ${source}`
          delete activeFeatures[source]
        }
      }
      // Regular commit
      else {
        const candidates = ['main', ...Object.keys(activeFeatures)]
        const valid = candidates.filter((b) => branches[b] || activeFeatures[b])
        activeBranch = valid[Math.floor(Math.random() * valid.length)]
        parents = [branches[activeBranch] || branches['main']]
        message = `Update logic in ${activeBranch}`
      }

      const newId = this.getSHA()
      const author = this.getRandom(this.users)
      commits.push(
        this.createCommit(
          newId,
          parents,
          activeBranch,
          message,
          author,
          count - i,
          type,
          this.getChanges(),
        ),
      )

      branches[activeBranch] = newId
      if (activeFeatures[activeBranch] !== undefined) {
        activeFeatures[activeBranch] = newId
      }
    }

    return commits.reverse()
  }

  createCommit(id, parents, branch, message, author, timeOffset, type, changes) {
    return {
      id,
      parents: parents.filter((p) => p),
      branch,
      message,
      author,
      date: new Date(Date.now() - timeOffset * 3600000).toISOString(),
      type,
      changes,
    }
  }
}

// State
const generator = new DataGenerator()
const commits = ref(generator.generate(150));
// const commits = ref(commitSapmle)
const searchTerm = ref('')

// Methods
const handleSelectCommit = (commit) => {
  mitter.emit('select-commit', commit)
}

// --- STATE SEARCH OPTIONS ---
const searchOptions = reactive({
  matchCase: false, // Aa
  matchWord: false, // \w
  useRegex: false, // .*
})

// Hàm toggle cho gọn
const toggleOption = (key) => {
  searchOptions[key] = !searchOptions[key]
}

const branch = ref(null)
const author = ref(null)

const branchList = [
  { id: 'all', label: 'All Branches' },
  { id: 'main', label: 'main' },
  { id: 'dev', label: 'dev' },
  { id: 'feature/login', label: 'Feature Login' },
  { id: 'feature/signup', label: 'Feature Signup' },
  { id: 'feature/dashboard-ui', label: 'Dashboard UI' },
  { id: 'hotfix/typo', label: 'Hotfix Typo' },
  { id: 'bugfix/crash-on-load', label: 'Bugfix Crash on Load' },
  { id: 'release/v1.0.0', label: 'Release v1.0.0' },
  { id: 'release/v1.0.1', label: 'Release v1.0.1' },
  { id: 'experiment/new-idea', label: 'Experiment New Idea' },
  { id: 'feature/profile-page', label: 'Profile Page' },
  { id: 'feature/settings-panel', label: 'Settings Panel' },
  { id: 'bugfix/login-error', label: 'Login Error' },
  { id: 'feature/chat-system', label: 'Chat System' },
  { id: 'feature/notifications', label: 'Notifications' },
  { id: 'hotfix/ui-glitch', label: 'UI Glitch' },
  { id: 'feature/payment-integration', label: 'Payment Integration' },
  { id: 'feature/shopping-cart', label: 'Shopping Cart' },
  { id: 'feature/search-function', label: 'Search Function' },
  { id: 'feature/reporting', label: 'Reporting' },
  { id: 'feature/admin-dashboard', label: 'Admin Dashboard' },
  { id: 'bugfix/missing-avatar', label: 'Missing Avatar' },
  { id: 'feature/multi-language', label: 'Multi Language' },
  { id: 'feature/theme-switcher', label: 'Theme Switcher' },
  { id: 'hotfix/logout-issue', label: 'Logout Issue' },
  { id: 'feature/analytics-page', label: 'Analytics Page' },
  { id: 'feature/email-notifications', label: 'Email Notifications' },
  { id: 'feature/password-reset', label: 'Password Reset' },
  { id: 'feature/social-login', label: 'Social Login' },
  { id: 'feature/drag-drop', label: 'Drag & Drop' },
  { id: 'feature/mobile-ui', label: 'Mobile UI' },
  { id: 'bugfix/crash-on-logout', label: 'Crash on Logout' },
  { id: 'feature/seo-optimization', label: 'SEO Optimization' },
  { id: 'feature/inventory-management', label: 'Inventory Management' },
  { id: 'feature/shipping-integration', label: 'Shipping Integration' },
  { id: 'feature/order-tracking', label: 'Order Tracking' },
  { id: 'feature/coupon-system', label: 'Coupon System' },
  { id: 'hotfix/payment-error', label: 'Payment Error' },
  { id: 'feature/review-system', label: 'Review System' },
  { id: 'feature/wishlist', label: 'Wishlist' },
  { id: 'feature/recommendation-engine', label: 'Recommendation Engine' },
]

const dateRange = ref({
  from: null,
  to: null,
})
const selectedDateRange = ref({ from: null, to: null });

// Watch để filter data khi chọn ngày xong
watch(selectedDateRange, (newRange) => {
  if (!newRange.from || !newRange.to) {
    console.log('Show All Time')
  } else {
    console.log(`Filter từ ${newRange.from} đến ${newRange.to}`)
    // Gọi hàm filterCommitsByDate(newRange)
  }
})

const authorList = [
  { email: "all", name: "All Author" },
  { email: "lionwilson@gmail.com", name: "Lion Wilson" },
  { email: "ameliahunt@gmail.com", name: "Amelia Hunt" },
  { email: "jacksonford@gmail.com", name: "Jackson Ford" },
  { email: "natalierose@gmail.com", name: "Natalie Rose" },
  { email: "ethanblake@gmail.com", name: "Ethan Blake" },
  { email: "sophiabrooks@gmail.com", name: "Sophia Brooks" },
  { email: "owenclark@gmail.com", name: "Owen Clark" },
  { email: "miagriffin@gmail.com", name: "Mia Griffin" },
  { email: "lucascarter@gmail.com", name: "Lucas Carter" },
  { email: "bellawarren@gmail.com", name: "Bella Warren" },
  { email: "henryadams@gmail.com", name: "Henry Adams" },
  { email: "charlottegray@gmail.com", name: "Charlotte Gray" },
  { email: "levimorgan@gmail.com", name: "Levi Morgan" },
  { email: "ellalawson@gmail.com", name: "Ella Lawson" },
  { email: "calebturner@gmail.com", name: "Caleb Turner" },
  { email: "laylawest@gmail.com", name: "Layla West" },
  { email: "graysonmiller@gmail.com", name: "Grayson Miller" },
  { email: "zoeyhall@gmail.com", name: "Zoey Hall" },
  { email: "julianprice@gmail.com", name: "Julian Price" },
  { email: "scarlettjenkins@gmail.com", name: "Scarlett Jenkins" },
];

const selectedBranch = ref(null)
const selectedAuthor = ref(null)

</script>

<style scoped>
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
  overflow-y: auto; /* Add scrollbar */

  background-color: var(--menu-bg); /* Solid background */
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6); /* Stronger shadow */
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

/* --- SEARCH INPUT EXTRA --- */
.search-option-btn {
  padding: 2px 4px;
  border-radius: 3px;
  cursor: pointer;
  color: var(--p-text-muted);
  transition: all 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-option-btn:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.search-option-btn.active {
  background-color: var(--p-hover);
  color: var(--text-color);
}
</style>
