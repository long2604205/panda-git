<template>
  <!-- SPLITTER: MAIN RIGHT -->
  <div ref="resizerRightSidebar" class="resizer-right-sidebar resizer-v bg-transparent -mr-[2px]"></div>

  <!-- RIGHT SIDEBAR -->
  <aside ref="sidebarRight" style="width: 300px"
         class="flex-shrink-0 bg-[var(--bg-side)] border-l border-[var(--border-color)] flex flex-col select-none z-10">
    <div ref="paneCommitInfo" style="height: 40%"
         class="flex-col min-h-0 border-b border-[var(--border-color)] flex">
      <div class="sidebar-section-title border-b border-[var(--border-color)]">
        <span>Commit Details</span>
        <div class="flex gap-2">
          <i class="fa-regular fa-copy hover:text-[var(--text-color)] cursor-pointer"></i>
        </div>
      </div>
      <div class="p-4 overflow-y-auto" id="commit-detail-info">
        <div class="text-center text-[var(--p-text-dim)] mt-10 text-xs">
          Select a commit to view details
        </div>
      </div>
    </div>

    <!-- SPLITTER: RIGHT VERTICAL -->
    <div ref="resizerRightInner" class="resizer-h bg-[var(--border-color)]"></div>

    <div class="flex-1 flex flex-col min-h-0">
      <div class="sidebar-section-title border-b border-[var(--border-color)] flex justify-between">
        <span>Changed Files</span><span
        class="text-[var(--accent-color)] text-[9px] border border-[var(--accent-color)] px-1 rounded"
        id="commit-file-count">0</span>
      </div>
      <div class="flex-1 overflow-y-auto p-1" id="commit-file-tree">
        <!-- Tree -->
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from "vue";

// refs cho DOM element
const resizerRightSidebar = ref(null);
const sidebarRight = ref(null);

const resizerRightInner = ref(null);
const paneCommitInfo = ref(null);

// ---- logic resize chung (giống bản gốc) ----
function initResize(resizerEl, prevEl, isVert) {
  if (!resizerEl || !prevEl) return;

  let startX, startY, startW, startH;

  const onMouseDown = (e) => {
    startX = e.clientX;
    startY = e.clientY;

    const rect = prevEl.getBoundingClientRect();
    startW = rect.width;
    startH = rect.height;

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);

    document.body.classList.add(isVert ? "resizing-col" : "resizing-row");
  };

  const onMouseMove = (e) => {
    if (isVert) {
      const dx = e.clientX - startX;
      prevEl.style.width = `${startW + dx}px`;
    } else {
      const dy = e.clientY - startY;
      prevEl.style.height = `${startH + dy}px`;
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

// ---- RIGHT SIDEBAR WIDTH (kéo ngang) ----
function initRightSidebarResize() {
  const resizer = resizerRightSidebar.value;
  const pane = sidebarRight.value;

  if (!resizer || !pane) return;

  let startX, startW;

  resizer.addEventListener("mousedown", (e) => {
    startX = e.clientX;
    startW = pane.getBoundingClientRect().width;

    const mm = (e) => {
      pane.style.width = `${startW - (e.clientX - startX)}px`;
    };

    const mu = () => {
      document.removeEventListener("mousemove", mm);
      document.removeEventListener("mouseup", mu);
    };

    document.addEventListener("mousemove", mm);
    document.addEventListener("mouseup", mu);
  });
}

// Mount
onMounted(() => {
  initRightSidebarResize();

  initResize(resizerRightInner.value, paneCommitInfo.value, false);
});
</script>

<style scoped></style>
