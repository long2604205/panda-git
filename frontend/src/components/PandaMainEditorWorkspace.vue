<template>
  <main class="flex-1 flex flex-col bg-[var(--bg-main)] min-w-0 relative" style="min-width: 300px">
    <!-- TOP PANE: WORKING COPY -->
    <div ref="paneWorking" style="height: 300px"
         class="flex bg-[var(--bg-main)] shrink-0 border-b border-[var(--border-color)]">
      <!-- Left: File Tree (Staging) -->
      <div ref="paneStaging" style="width: 50%" class="flex flex-col border-r border-[var(--border-color)]">
        <div
          class="h-8 px-4 flex items-center justify-between border-b border-[var(--border-color)] text-xs font-bold text-[var(--p-text-muted)] uppercase tracking-wider bg-[var(--bg-side)]">
          <div class="flex items-center gap-2">
            <input type="checkbox" class="tree-checkbox" checked />
            <span>Changes
                <span
                  class="ml-1 px-1.5 py-0.5 rounded bg-[var(--p-hover)] text-[var(--text-color)] opacity-80 font-mono">
                  4 files
                </span>
              </span>
          </div>
          <div class="flex gap-3 text-[var(--text-color)] opacity-70">
            <i class="fa-solid fa-layer-group cursor-pointer hover:text-[var(--accent-color)]"></i><i
            class="fa-solid fa-expand cursor-pointer hover:text-[var(--accent-color)]"></i>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto p-1" id="working-tree-container">
          <!-- Tree -->
        </div>
      </div>

      <!-- SPLITTER: WORKING HORIZONTAL -->
      <div ref="resizerWorkingInner" class="resizer-v bg-[var(--border-color)]"></div>

      <!-- Right: Commit Message -->
      <div class="flex-1 flex flex-col min-w-0">
        <div
          class="h-8 px-4 flex items-center border-b border-[var(--border-color)] text-xs font-bold text-[var(--p-text-muted)] uppercase tracking-wider bg-[var(--bg-side)]">
          <span>Commit</span>
          <div class="ml-auto flex gap-2 text-[var(--text-color)]">
            <i class="fa-solid fa-clock-rotate-left cursor-pointer hover:text-[var(--accent-color)]"
               title="History"></i>
          </div>
        </div>
        <div class="flex-1 p-3 flex flex-col gap-2">
          <div class="flex items-center gap-2 select-none">
            <input type="checkbox" id="amend-check" class="tree-checkbox" /><label for="amend-check"
                                                                                   class="text-xs text-[var(--text-color)] cursor-pointer">Amend</label>
          </div>
          <textarea
            class="w-full h-full bg-transparent border border-[var(--border-color)] outline-none text-sm text-[var(--text-color)] font-mono resize-none p-2 rounded hover:border-[var(--p-text-muted)] focus:border-[var(--accent-color)] transition-colors placeholder-[var(--p-text-dim)]"
            placeholder="Commit Message"></textarea>
        </div>
        <div
          class="h-12 border-t border-[var(--border-color)] flex items-center justify-between px-4 bg-[var(--bg-side)]">
          <div class="flex gap-2">
            <button class="btn btn-primary text-xs">Commit</button><button
            class="btn btn-secondary text-xs">
            Commit and Push...
          </button>
          </div>
          <i
            class="fa-solid fa-ellipsis-vertical text-[var(--p-text-dim)] hover:text-[var(--text-color)] cursor-pointer px-2"></i>
        </div>
      </div>
    </div>

    <!-- SPLITTER: MAIN VERTICAL -->
    <div ref="resizerMainVert" class="resizer-h bg-[var(--border-color)]"></div>

    <!-- BOTTOM PANE: GIT GRAPH -->
    <div ref="paneGraph" class="flex-1 flex flex-col min-h-0">
      <div class="h-9 flex items-center bg-[var(--bg-header)] border-b border-[var(--border-color)] shrink-0">
        <div
          class="h-full px-4 flex items-center gap-2 text-xs bg-[var(--bg-main)] border-t-2 border-t-[var(--accent-color)] text-[var(--text-color)] border-r border-r-[var(--border-color)]">
          <i class="fa-solid fa-code-commit text-[var(--accent-color)]"></i><span>History Graph</span>
        </div>
        <div class="ml-2 flex items-center">
          <div class="relative">
            <i
              class="fa-solid fa-filter absolute left-2 top-1/2 transform -translate-y-1/2 text-[10px] text-[var(--p-text-dim)]"></i><input
            type="text" id="commit-search-input"
            class="search-input w-64 pl-6 pr-2 py-0.5 rounded-full" placeholder="Search commits..." />
          </div>
        </div>
      </div>
      <div class="graph-container" id="graph-scroll-area">
        <svg id="graph-svg" class="graph-svg-layer" width="200" height="0"></svg>
        <div id="graph-rows" class="w-full z-10 relative">
          <!-- Rows -->
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { ref, onMounted } from "vue";

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
</script>

<style scoped></style>
