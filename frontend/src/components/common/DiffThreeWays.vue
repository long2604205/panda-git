<template>
  <div
    class="merge-editor-wrapper"
    :class="themeStore.theme === 'dark' ? 'dark-theme' : 'light-theme'"
  >
    <div class="header">
      <div class="header-col flex-1 border-r">
        Local Changes
      </div>
      <div class="header-col gap-header border-r" />
      <div class="header-col header-center border-r">
        Result (Working tree)
      </div>
      <div class="header-col gap-header border-r" />
      <div class="header-col flex-1">
        Remote Changes
      </div>
    </div>

    <div
      id="main-container"
      ref="mainContainerRef"
    >
      <svg
        id="svg-layer"
        ref="svgLayerRef"
      />

      <div
        ref="containerLeftRef"
        class="editor-container flex-1 border-r"
      />
      <div class="gap-col" />
      <div
        ref="containerCenterRef"
        class="editor-container editor-center border-r"
      />
      <div class="gap-col" />
      <div
        ref="containerRightRef"
        class="editor-container flex-1"
      />

      <div
        ref="actionsOverlayRef"
        class="action-overlay"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount, nextTick, watch} from 'vue'
// --- IMPORT PACKAGES ---
import * as monaco from 'monaco-editor'
import DiffMatchPatch from 'diff-match-patch'

// --- CẤU HÌNH WORKER (VITE) ---
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'
import {useThemeStore} from '@/stores/theme.store.js'

self.MonacoEnvironment = {
  getWorker(_, label) {
    if (label === 'json') return new jsonWorker()
    if (label === 'css' || label === 'scss' || label === 'less')
      return new cssWorker()
    if (label === 'html' || label === 'handlebars' || label === 'razor')
      return new htmlWorker()
    if (label === 'typescript' || label === 'javascript') return new tsWorker()
    return new editorWorker()
  },
}

// --- PROPS ---
const props = defineProps({
  mergeSegments: {
    type: Array,
    required: false,
    default: () => [],
  },
  navMode: {
    type: String,
    default: 'changes' // 'changes' | 'conflict'
  }
})

const themeStore = useThemeStore()

watch(
  () => themeStore.theme,
  (t) => {
    monaco.editor.setTheme(t === 'dark' ? 'vs-dark' : 'vs')
  },
  { immediate: true }
)
// --- STATE ---
const canNavPrev = ref(false)
const canNavNext = ref(false)

const totalConflicts = ref(0)
const totalChanges = ref(0)

// DOM Refs
const mainContainerRef = ref(null)
const containerLeftRef = ref(null)
const containerCenterRef = ref(null)
const containerRightRef = ref(null)
const svgLayerRef = ref(null)
const actionsOverlayRef = ref(null)

// Logic variables
let editorLeft, editorCenter, editorRight
let decorationsLeft = [],
  decorationsCenter = [],
  decorationsRight = []
let LEFT_LINES = [],
  CENTER_LINES_INIT = [],
  RIGHT_LINES = [],
  DIFF_MAPPING = []
let currentChangeIndex = -1
let resizeObserver = null
const resolvedStateHistory = new Map()

// --- CORE LOGIC ---

// 1. Data Processing
const processSegments = () => {
  LEFT_LINES = []
  CENTER_LINES_INIT = []
  RIGHT_LINES = []
  DIFF_MAPPING = []
  let leftIdx = 0,
    centerIdx = 0,
    rightIdx = 0,
    conflictId = 1

  props.mergeSegments.forEach((seg) => {
    if (seg.type === 'common') {
      seg.text.forEach((l) => {
        LEFT_LINES.push(l)
        CENTER_LINES_INIT.push(l)
        RIGHT_LINES.push(l)
      })
      leftIdx += seg.text.length
      centerIdx += seg.text.length
      rightIdx += seg.text.length
    } else if (seg.type === 'conflict') {
      seg.local.forEach((l) => LEFT_LINES.push(l))
      seg.remote.forEach((l) => RIGHT_LINES.push(l))

      const startC = centerIdx
      CENTER_LINES_INIT.push('<<<<<<< HEAD')
      seg.local.forEach((l) => CENTER_LINES_INIT.push(l))
      CENTER_LINES_INIT.push('=======')
      seg.remote.forEach((l) => CENTER_LINES_INIT.push(l))
      CENTER_LINES_INIT.push('>>>>>>> feature/branch')

      const lenC = 1 + seg.local.length + 1 + seg.remote.length + 1

      DIFF_MAPPING.push({
        id: conflictId++,
        type: 'conflict',
        left: { start: leftIdx, end: leftIdx + seg.local.length - 1 },
        center: { start: startC, end: startC + lenC - 1 },
        right: { start: rightIdx, end: rightIdx + seg.remote.length - 1 },
        color: 'rgba(255, 100, 100, 0.25)',
        bgClass: 'diff-conflict',
        resolvedSide: null,
        finalized: false,
        leftDiffers: true,
        rightDiffers: true,
      })
      leftIdx += seg.local.length
      rightIdx += seg.remote.length
      centerIdx += lenC
    } else if (seg.type === 'auto-merge-right') {
      seg.text.forEach((l) => {
        RIGHT_LINES.push(l)
        CENTER_LINES_INIT.push(l)
      })
      DIFF_MAPPING.push({
        id: conflictId++,
        type: 'auto-merge',
        left: null,
        center: { start: centerIdx, end: centerIdx + seg.text.length - 1 },
        right: { start: rightIdx, end: rightIdx + seg.text.length - 1 },
        color: 'rgba(50, 150, 255, 0.2)',
        bgClass: 'diff-auto-merge-blue',
        resolvedSide: 'auto',
        rejected: false,
      })
      rightIdx += seg.text.length
      centerIdx += seg.text.length
    } else if (seg.type === 'edit-left') {
      seg.local.forEach((l) => LEFT_LINES.push(l))
      seg.remote.forEach((l) => {
        RIGHT_LINES.push(l)
        CENTER_LINES_INIT.push(l)
      })
      DIFF_MAPPING.push({
        id: conflictId++,
        type: 'edit',
        source: 'left',
        left: { start: leftIdx, end: leftIdx + seg.local.length - 1 },
        center: { start: centerIdx, end: centerIdx + seg.remote.length - 1 },
        right: { start: rightIdx, end: rightIdx + seg.remote.length - 1 },
        color: 'rgba(155, 89, 182, 0.25)',
        bgClass: 'diff-edit-purple',
        resolvedSide: null,
        rejected: false,
      })
      leftIdx += seg.local.length
      rightIdx += seg.remote.length
      centerIdx += seg.remote.length
    } else if (seg.type === 'edit-right') {
      seg.local.forEach((l) => {
        LEFT_LINES.push(l)
        CENTER_LINES_INIT.push(l)
      })
      seg.remote.forEach((l) => RIGHT_LINES.push(l))
      DIFF_MAPPING.push({
        id: conflictId++,
        type: 'edit',
        source: 'right',
        left: { start: leftIdx, end: leftIdx + seg.local.length - 1 },
        center: { start: centerIdx, end: centerIdx + seg.local.length - 1 },
        right: { start: rightIdx, end: rightIdx + seg.remote.length - 1 },
        color: 'rgba(155, 89, 182, 0.25)',
        bgClass: 'diff-edit-purple',
        resolvedSide: null,
        rejected: false,
      })
      leftIdx += seg.local.length
      rightIdx += seg.remote.length
      centerIdx += seg.local.length
    }
  })
}

// 2. Diff Logic & UI Helpers
const computeCharLevelDiffs = (
  centerText,
  sideText,
  centerStartLine,
  sideStartLine,
  isConflict = false
) => {
  const dmp = new DiffMatchPatch()
  const diffs = dmp.diff_main(centerText, sideText)
  dmp.diff_cleanupSemantic(diffs)

  const decosCenter = []
  const decosSide = []
  const clsAdd = isConflict ? 'diff-char-diff' : 'diff-char-add'
  const clsDel = isConflict ? 'diff-char-diff' : 'diff-char-del'

  let cLine = centerStartLine + 1,
    cCol = 1
  let sLine = sideStartLine + 1,
    sCol = 1

  diffs.forEach(([op, text]) => {
    const lines = text.split('\n')
    const lineCount = lines.length
    const processText = (startL, startC, targetArray, className) => {
      let curL = startL,
        curC = startC
      lines.forEach((lineContent, i) => {
        const len = lineContent.length
        if (len > 0 && className) {
          targetArray.push({
            range: new monaco.Range(curL, curC, curL, curC + len),
            options: { inlineClassName: className },
          })
        }
        if (i < lineCount - 1) {
          curL++
          curC = 1
        } else {
          curC += len
        }
      })
      return { l: curL, c: curC }
    }

    if (op === 0) {
      const resC = processText(cLine, cCol, [], null)
      cLine = resC.l
      cCol = resC.c
      const resS = processText(sLine, sCol, [], null)
      sLine = resS.l
      sCol = resS.c
    } else if (op === -1) {
      const res = processText(cLine, cCol, decosCenter, clsDel)
      cLine = res.l
      cCol = res.c
    } else if (op === 1) {
      const res = processText(sLine, sCol, decosSide, clsAdd)
      cLine = res.l
      cCol = res.c
    }
  })
  return { center: decosCenter, side: decosSide }
}

const hasMarkersInContent = (diff, model) => {
  const lineCount = model.getLineCount()
  const start = Math.max(1, diff.center.start + 1)
  const end = Math.min(lineCount, diff.center.end + 1)
  if (start > end) return false
  const rangeContent = model.getValueInRange(
    new monaco.Range(start, 1, end, 9999)
  )
  return rangeContent.includes('<<<<<<<') && rangeContent.includes('>>>>>>>')
}

const captureResolvedState = (versionId) => {
  const state = {}
  DIFF_MAPPING.forEach((d) => {
    const s = {}
    if (d.resolvedSide) s.resolvedSide = d.resolvedSide
    if (d.rejected) s.rejected = true
    if (d.finalized) s.finalized = true
    if (Object.keys(s).length > 0) state[d.id] = s
  })
  resolvedStateHistory.set(versionId, state)
}

const restoreResolvedState = (versionId) => {
  const state = resolvedStateHistory.get(versionId) || {}
  DIFF_MAPPING.forEach((d) => {
    const s = state[d.id] || {}
    d.resolvedSide = s.resolvedSide || null
    d.rejected = !!s.rejected
    d.finalized = !!s.finalized
  })
}

// --- VISUAL UPDATES ---

const updateDecorations = () => {
  if (!editorCenter) return
  const createDeco = (range, className) => ({
    range: new monaco.Range(range.start + 1, 1, range.end + 1, 1),
    options: { isWholeLine: true, className },
  })
  const model = editorCenter.getModel()
  const txt = model.getValue().split('\n')
  const LC = model.getLineCount()
  let dl = [],
    dc = [],
    dr = []

  DIFF_MAPPING.forEach((d) => {
    if (d.rejected || d.finalized) return
    if (
      d.center.start < 0 ||
      d.center.end >= LC ||
      d.center.start > d.center.end
    )
      return

    if (d.type === 'auto-merge') {
      const blueClass = 'diff-auto-merge-blue'
      dc.push(createDeco(d.center, blueClass))
      if (d.right) dr.push(createDeco(d.right, blueClass))
    } else if (d.type === 'edit') {
      if (d.resolvedSide) return
      const purpleClass = 'diff-edit-purple'
      if (d.source === 'left') {
        dl.push(createDeco(d.left, purpleClass))
        dc.push(createDeco(d.center, purpleClass))
      } else {
        dr.push(createDeco(d.right, purpleClass))
        dc.push(createDeco(d.center, purpleClass))
      }
      const centerRange = new monaco.Range(
        d.center.start + 1,
        1,
        d.center.end + 1,
        9999
      )
      const centerText = model.getValueInRange(centerRange)
      let sideText = '',
        sideStartLine = 0
      if (d.source === 'left') {
        sideStartLine = d.left.start
        sideText = LEFT_LINES.slice(d.left.start, d.left.end + 1).join('\n')
      } else {
        sideStartLine = d.right.start
        sideText = RIGHT_LINES.slice(d.right.start, d.right.end + 1).join('\n')
      }
      const charDiffs = computeCharLevelDiffs(
        centerText,
        sideText,
        d.center.start,
        sideStartLine,
        false
      )
      dc.push(...charDiffs.center)
      if (d.source === 'left') dl.push(...charDiffs.side)
      else dr.push(...charDiffs.side)
    } else if (d.type === 'conflict') {
      const markersExist = hasMarkersInContent(d, model)
      const centerRange = new monaco.Range(
        d.center.start + 1,
        1,
        d.center.end + 1,
        9999
      )
      const centerText = model.getValueInRange(centerRange)

      // Left compare
      const leftText = LEFT_LINES.slice(d.left.start, d.left.end + 1).join(
        '\n'
      )
      if (leftText !== centerText || markersExist) {
        d.leftDiffers = true
        const baseClass = markersExist ? 'diff-conflict' : 'diff-block-base'
        dl.push(createDeco(d.left, baseClass))
        if (!markersExist) {
          dc.push(createDeco(d.center, 'diff-block-base'))
          const chars = computeCharLevelDiffs(
            centerText,
            leftText,
            d.center.start,
            d.left.start,
            true
          )
          dc.push(...chars.center)
          dl.push(...chars.side)
        } else dc.push(createDeco(d.center, 'diff-conflict'))
      } else d.leftDiffers = false

      // Right compare
      const rightText = RIGHT_LINES.slice(d.right.start, d.right.end + 1).join(
        '\n'
      )
      if (rightText !== centerText || markersExist) {
        d.rightDiffers = true
        const baseClass = markersExist ? 'diff-conflict' : 'diff-block-base'
        dr.push(createDeco(d.right, baseClass))
        if (!markersExist) {
          if (!d.leftDiffers) dc.push(createDeco(d.center, 'diff-block-base'))
          const chars = computeCharLevelDiffs(
            centerText,
            rightText,
            d.center.start,
            d.right.start,
            true
          )
          dc.push(...chars.center)
          dr.push(...chars.side)
        } else if (!d.leftDiffers)
          dc.push(createDeco(d.center, 'diff-conflict'))
      } else d.rightDiffers = false

      if (markersExist) {
        const end = Math.min(d.center.end, txt.length - 1)
        for (let i = d.center.start; i <= end; i++) {
          if ((txt[i] || '').match(/^(<<<<<<<|=======|>>>>>>>)/)) {
            dc.push({
              range: new monaco.Range(i + 1, 1, i + 1, 1),
              options: { isWholeLine: true, className: 'diff-marker' },
            })
          }
        }
      }
    }
  })

  decorationsLeft = editorLeft.deltaDecorations(decorationsLeft, dl)
  decorationsCenter = editorCenter.deltaDecorations(decorationsCenter, dc)
  decorationsRight = editorRight.deltaDecorations(decorationsRight, dr)
  updateNavState()
}

const drawLayerElements = () => {
  if (!editorLeft || !svgLayerRef.value) return
  const getH = (e) => e.getOption(monaco.editor.EditorOption.lineHeight)

  // Use container refs for dimensions
  const rL = containerLeftRef.value.getBoundingClientRect()
  const rC = containerCenterRef.value.getBoundingClientRect()
  const rR = containerRightRef.value.getBoundingClientRect()
  const rMain = mainContainerRef.value.getBoundingClientRect()

  const xL_end = rL.width
  const xC_start = rC.left - rMain.left
  const xC_end = xC_start + rC.width
  const xR_start = rR.left - rMain.left

  let svg = ''
  const model = editorCenter.getModel()
  const LC = model.getLineCount()
  const cssStyle = getComputedStyle(document.body)
  const autoMergeColor =
    cssStyle.getPropertyValue('--color-auto-merge').trim() ||
    'rgba(50, 150, 255, 0.2)'
  const editColor =
    cssStyle.getPropertyValue('--color-edit').trim() ||
    'rgba(155, 89, 182, 0.15)'
  const conflictColor =
    cssStyle.getPropertyValue('--color-conflict-block').trim() ||
    'rgba(255, 100, 100, 0.1)'

  DIFF_MAPPING.forEach((d) => {
    if (d.rejected || d.finalized) return
    const getY = (ed, idx) =>
      ed.getTopForLineNumber(idx + 1) - ed.getScrollTop()
    if (
      d.center.start < 0 ||
      d.center.end >= LC ||
      d.center.start > d.center.end
    )
      return

    const yc1 = getY(editorCenter, d.center.start)
    const yc2 = getY(editorCenter, d.center.end) + getH(editorCenter)
    const mkFillPath = (x1, y1a, y1b, x2, y2a, y2b, fill) => {
      const cp = (x2 - x1) * 0.5
      return `<path d="M ${x1} ${y1a} C ${x1 + cp} ${y1a}, ${
        x2 - cp
      } ${y2a}, ${x2} ${y2a} L ${x2} ${y2b} C ${x2 - cp} ${y2b}, ${
        x1 + cp
      } ${y1b}, ${x1} ${y1b} Z" fill="${fill}" />`
    }

    if (d.type === 'auto-merge' && d.right) {
      const yr1 = getY(editorRight, d.right.start)
      const yr2 = getY(editorRight, d.right.end) + getH(editorRight)
      svg += mkFillPath(xC_end, yc1, yc2, xR_start, yr1, yr2, autoMergeColor)
    } else if (d.type === 'edit' && !d.resolvedSide) {
      if (d.source === 'left') {
        const yl1 = getY(editorLeft, d.left.start)
        const yl2 = getY(editorLeft, d.left.end) + getH(editorLeft)
        svg += mkFillPath(xL_end, yl1, yl2, xC_start, yc1, yc2, editColor)
      } else {
        const yr1 = getY(editorRight, d.right.start)
        const yr2 = getY(editorRight, d.right.end) + getH(editorRight)
        svg += mkFillPath(xC_end, yc1, yc2, xR_start, yr1, yr2, editColor)
      }
    } else if (d.type === 'conflict') {
      if (d.leftDiffers) {
        const yl1 = getY(editorLeft, d.left.start)
        const yl2 = getY(editorLeft, d.left.end) + getH(editorLeft)
        svg += mkFillPath(xL_end, yl1, yl2, xC_start, yc1, yc2, conflictColor)
      }
      if (d.rightDiffers) {
        const yr1 = getY(editorRight, d.right.start)
        const yr2 = getY(editorRight, d.right.end) + getH(editorRight)
        svg += mkFillPath(xC_end, yc1, yc2, xR_start, yr1, yr2, conflictColor)
      }
    }
  })
  svgLayerRef.value.innerHTML = svg
}

// --- BUTTONS OVERLAY ---

const createActionBtn = (top, left, d, type, icon, extraClass = '') => {
  const btn = document.createElement('div')
  btn.className = `action-btn ${extraClass}`
  btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${icon}</svg>`
  btn.style.top = top + 'px'
  btn.style.left = left + 'px'

  btn.onclick = (e) => {
    e.stopPropagation()
    if (type === 'reject-auto') rejectAutoMerge(d.id)
    else if (type === 'finalize') finalizeConflict(d.id)
    else resolveConflict(d.id, type)
  }
  return btn
}

const updateActionButtons = () => {
  if (!actionsOverlayRef.value || !editorLeft) return
  actionsOverlayRef.value.innerHTML = ''

  const rL = containerLeftRef.value.getBoundingClientRect()
  const rC = containerCenterRef.value.getBoundingClientRect()
  const rR = containerRightRef.value.getBoundingClientRect()
  const rMain = mainContainerRef.value.getBoundingClientRect()
  const btnSz = 24,
    padding = -3
  const model = editorCenter.getModel()
  const LC = model.getLineCount()

  const getYCenter = (s, e) =>
    editorCenter.getTopForLineNumber(s + 1) -
    editorCenter.getScrollTop() +
    ((e - s + 1) *
      editorCenter.getOption(monaco.editor.EditorOption.lineHeight)) /
      2 -
    btnSz / 2
  const getYSource = (ed, s, e) =>
    ed.getTopForLineNumber(s + 1) +
    ((e - s + 1) * ed.getOption(monaco.editor.EditorOption.lineHeight)) / 2 -
    btnSz / 2 -
    ed.getScrollTop()

  const gapLeftX = rC.left - rMain.left - btnSz - padding
  const gapRightX = rC.right - rMain.left + padding

  DIFF_MAPPING.forEach((d) => {
    if (d.rejected || d.finalized) return
    if (d.center.start < 0 || d.center.end >= LC) return

    if (d.type === 'auto-merge') {
      const top = getYCenter(d.center.start, d.center.end)
      if (top > -btnSz && top < rMain.height) {
        actionsOverlayRef.value.appendChild(
          createActionBtn(
            top,
            rC.right - rMain.left,
            d,
            'reject-auto',
            '<path d="M18 6L6 18M6 6l12 12"></path>',
            'reject-btn'
          )
        )
      }
    } else if (d.type === 'edit' && !d.resolvedSide) {
      const top = getYCenter(d.center.start, d.center.end)
      if (top < -btnSz || top > rMain.height) return
      if (d.source === 'left') {
        actionsOverlayRef.value.appendChild(
          createActionBtn(
            top,
            gapLeftX,
            d,
            'left',
            '<path d="M13 17l5-5-5-5M6 17l5-5-5-5"></path>',
            'edit-btn'
          )
        )
      } else {
        actionsOverlayRef.value.appendChild(
          createActionBtn(
            top,
            gapRightX,
            d,
            'right',
            '<path d="M11 17l-5-5 5-5M18 17l-5-5 5-5"></path>',
            'edit-btn'
          )
        )
      }
    } else if (d.type === 'conflict') {
      const markersExist = hasMarkersInContent(d, model)
      if (d.left && d.leftDiffers) {
        const top = getYSource(editorLeft, d.left.start, d.left.end)
        if (top > -btnSz && top < rMain.height) {
          const arrowX = rL.right - rMain.left + padding
          actionsOverlayRef.value.appendChild(
            createActionBtn(
              top,
              arrowX,
              d,
              'left',
              '<path d="M13 17l5-5-5-5M6 17l5-5-5-5"></path>'
            )
          )
          if (!markersExist)
            actionsOverlayRef.value.appendChild(
              createActionBtn(
                top,
                arrowX + btnSz,
                d,
                'finalize',
                '<path d="M18 6L6 18M6 6l12 12"></path>',
                'finalize-btn'
              )
            )
        }
      }
      if (d.right && d.rightDiffers) {
        const top = getYSource(editorRight, d.right.start, d.right.end)
        if (top > -btnSz && top < rMain.height) {
          const arrowX = rR.left - rMain.left - btnSz - padding
          actionsOverlayRef.value.appendChild(
            createActionBtn(
              top,
              arrowX,
              d,
              'right',
              '<path d="M11 17l-5-5 5-5M18 17l-5-5 5-5"></path>'
            )
          )
          if (!markersExist)
            actionsOverlayRef.value.appendChild(
              createActionBtn(
                top,
                arrowX - btnSz - 2,
                d,
                'finalize',
                '<path d="M18 6L6 18M6 6l12 12"></path>',
                'finalize-btn'
              )
            )
        }
      }
    }
  })
}

// --- ACTIONS & EVENTS ---

const resolveConflict = (id, side) => {
  const idx = DIFF_MAPPING.findIndex((d) => d.id === id)
  if (idx === -1) return
  const d = DIFF_MAPPING[idx]
  d.resolvedSide = side

  const txt = (
    side === 'left'
      ? LEFT_LINES.slice(d.left.start, d.left.end + 1)
      : RIGHT_LINES.slice(d.right.start, d.right.end + 1)
  ).join('\n')
  const range = new monaco.Range(d.center.start + 1, 1, d.center.end + 1, 9999)

  editorCenter.pushUndoStop()
  editorCenter.executeEdits('merge', [
    { range, text: txt, forceMoveMarkers: true },
  ])
  editorCenter.pushUndoStop()

  captureResolvedState(editorCenter.getModel().getAlternativeVersionId())
  refreshUI()
  // ĐÃ XÓA: goToChange("next", false); -> Để con trỏ đứng yên
}

const rejectAutoMerge = (id) => {
  const idx = DIFF_MAPPING.findIndex((d) => d.id === id)
  if (idx === -1) return
  DIFF_MAPPING[idx].rejected = true

  const d = DIFF_MAPPING[idx]
  const range = new monaco.Range(d.center.start + 1, 1, d.center.end + 1, 9999)
  editorCenter.pushUndoStop()
  editorCenter.executeEdits('reject', [
    { range, text: '', forceMoveMarkers: true },
  ])
  editorCenter.pushUndoStop()

  captureResolvedState(editorCenter.getModel().getAlternativeVersionId())
  refreshUI()
  // ĐÃ XÓA: goToChange("next", false);
}

const finalizeConflict = (id) => {
  const idx = DIFF_MAPPING.findIndex((d) => d.id === id)
  if (idx !== -1) {
    DIFF_MAPPING[idx].finalized = true
    captureResolvedState(editorCenter.getModel().getAlternativeVersionId())
    refreshUI()
    // ĐÃ XÓA: goToChange("next", false);
  }
}

const acceptAllConflicts = (side) => {
  editorCenter.pushUndoStop()
  const edits = []
  DIFF_MAPPING.filter(
    (d) => d.type === 'conflict' && !d.finalized && !d.resolvedSide
  ).forEach((d) => {
    d.resolvedSide = side
    const txt =
      side === 'left'
        ? LEFT_LINES.slice(d.left.start, d.left.end + 1).join('\n')
        : RIGHT_LINES.slice(d.right.start, d.right.end + 1).join('\n')
    edits.push({
      range: new monaco.Range(d.center.start + 1, 1, d.center.end + 1, 9999),
      text: txt,
      forceMoveMarkers: true,
    })
  })
  editorCenter.executeEdits('merge-all', edits)
  editorCenter.pushUndoStop()
  captureResolvedState(editorCenter.getModel().getAlternativeVersionId())
  refreshUI()
}

// --- NAVIGATION ---

const getActiveChangeBlocks = () => {
  // Lọc ra CÁC BLOCK CHƯA FINALIZED (chưa nhấn nút X), bất kể resolvedSide có giá trị hay không.
  let active = DIFF_MAPPING.filter(
    (d) =>
      // Chỉ loại trừ nếu đã finalized (hoặc bị rejected nếu là auto-merge)
      !(d.finalized || d.rejected)
  ).sort((a, b) => a.center.start - b.center.start)

  // Áp dụng filter theo navMode như cũ
  if (props.navMode === 'conflict') {
    active = active.filter(d => d.type === 'conflict')
  }

  return active // Mảng này chứa A, B, C (dù A đã resolveSide, miễn là chưa finalized)
}

const calculateCounts = () => {
  let conflictCount = 0
  let totalActiveChangeCount = 0

  DIFF_MAPPING.forEach((d) => {

    // 1. LOGIC ĐẾM CONFLICTS (Conflicts CÒN CHƯA RESOLVE)
    // Conflict được coi là ĐÃ RESOLVE (Xong) nếu:
    // a) Đã Finalized (d.finalized = true)
    // b) Hoặc đã chọn bên (d.resolvedSide có giá trị)
    if (d.type === 'conflict' && !d.finalized && !d.resolvedSide) {
      conflictCount++
    }

    // 2. LOGIC ĐẾM TỔNG CHANGES (Active Blocks)

    let isChangeActive = false

    if (d.type === 'conflict') {
      // Conflict vẫn active cho đến khi FINALIZED
      if (!d.finalized) {
        isChangeActive = true
      }
    } else if (d.type === 'edit') {
      // Edit (left/right): Active cho đến khi RESOLVED (đã chọn 1 bên) hoặc FINALIZED (nếu có nút X)
      // Dựa trên cấu trúc code của bạn: Edit không có nút X, chỉ có nút Accept (resolve).
      // Coi như đã xong nếu d.resolvedSide có giá trị (người dùng đã hành động).
      if (!d.resolvedSide) {
         isChangeActive = true
      }

      // *** CẢNH BÁO: Nếu bạn muốn nút Next/Prev dừng lại ở Edit ngay cả khi đã chọn bên,
      //     thì hãy dùng điều kiện !d.finalized (và bạn cần thêm cơ chế finalize cho Edit block).
      //     Hiện tại, tôi giả định Edit block được đánh dấu là "xử lý xong" ngay khi RESOLVED.

    } else if (d.type === 'auto-merge') {
      // Auto-Merge: Active cho đến khi REJECTED (Chỉ có nút X/Reject cho Auto-Merge)
      if (!d.rejected) {
        isChangeActive = true
      }
    }

    if (isChangeActive) {
      totalActiveChangeCount++
    }
  })

  totalConflicts.value = conflictCount
  totalChanges.value = totalActiveChangeCount
}

watch(
  () => props.navMode,
  () => {
    currentChangeIndex = -1
    updateNavState()
  }
)

const updateNavState = () => {
  const active = getActiveChangeBlocks()
  canNavPrev.value = active.length > 0
  canNavNext.value = active.length > 0
}

const goToChange = (direction, initial = false) => {
  const activeBlocks = getActiveChangeBlocks()
  if (activeBlocks.length === 0) {
    currentChangeIndex = -1
    return
  }

  let newIndex = currentChangeIndex
  if (initial) newIndex = 0
  else if (direction === 'next')
    newIndex = newIndex + 1 >= activeBlocks.length ? 0 : newIndex + 1
  else if (direction === 'prev')
    newIndex = newIndex - 1 < 0 ? activeBlocks.length - 1 : newIndex - 1

  currentChangeIndex = newIndex
  if (activeBlocks[newIndex]) {
    const line = activeBlocks[newIndex].center.start + 1
    editorCenter.revealLineInCenter(line)
    editorCenter.setPosition({ lineNumber: line, column: 1 })
    editorCenter.focus()
  }
}

const refreshUI = () => {
  updateDecorations()
  drawLayerElements()
  updateActionButtons()
  calculateCounts()
}

const acceptAllBoth = () => {
  // 1. Kiểm tra xem editor đã được khởi tạo chưa
  if (!editorCenter) return

  editorCenter.pushUndoStop()
  const edits = []

  // 2. Lọc các block là 'conflict' và chưa được xử lý (finalized/resolved)
  DIFF_MAPPING.filter(
    (d) => d.type === 'conflict' && !d.finalized && !d.resolvedSide
  ).forEach((d) => {
    // Đánh dấu trạng thái là đã resolve
    d.resolvedSide = 'both'

    // 3. Lấy text từ cả 2 bên Local và Remote
    const leftTxt = LEFT_LINES.slice(d.left.start, d.left.end + 1).join('\n')
    const rightTxt = RIGHT_LINES.slice(d.right.start, d.right.end + 1).join('\n')

    // Nối code (thường Local trên, Remote dưới)
    const combinedTxt = leftTxt + (leftTxt && rightTxt ? '\n' : '') + rightTxt

    // 4. Tạo edit operation cho Monaco
    edits.push({
      range: new monaco.Range(d.center.start + 1, 1, d.center.end + 1, 9999),
      text: combinedTxt,
      forceMoveMarkers: true,
    })
  })

  // 5. Thực thi tất cả các thay đổi cùng một lúc (Atomic Update)
  if (edits.length > 0) {
    editorCenter.executeEdits('merge-all-both', edits)
    editorCenter.pushUndoStop()

    // Cập nhật lại lịch sử để hỗ trợ Undo/Redo
    captureResolvedState(editorCenter.getModel().getAlternativeVersionId())

    // Làm mới UI (vẽ lại SVG, cập nhật đếm số lượng)
    refreshUI()
  }
}
// --- LIFECYCLE ---

onMounted(() => {
  processSegments()

  const commonOpts = {
    language: 'java',
    theme: themeStore.theme === 'dark' ? 'vs-dark' : 'vs',
    scrollBeyondLastLine: false,
    minimap: { enabled: false },
    lineNumbers: 'on',
    renderLineHighlight: 'none',
    scrollbar: { vertical: 'auto', horizontal: 'auto' },
    readOnly: true,
    folding: false,
    quickSuggestions: false,
  }

  editorLeft = monaco.editor.create(containerLeftRef.value, {
    value: LEFT_LINES.join('\n'),
    ...commonOpts,
  })
  editorCenter = monaco.editor.create(containerCenterRef.value, {
    value: CENTER_LINES_INIT.join('\n'),
    ...commonOpts,
    readOnly: false,
  })
  editorRight = monaco.editor.create(containerRightRef.value, {
    value: RIGHT_LINES.join('\n'),
    ...commonOpts,
  })

// Event Listeners
  editorCenter.onDidChangeModelContent((e) => {
    const versionId = editorCenter.getModel().getAlternativeVersionId()
    e.changes.forEach((change) => {
      const linesAdded = (change.text.match(/\n/g) || []).length
      const linesRemoved =
        change.range.endLineNumber - change.range.startLineNumber
      const delta = linesAdded - linesRemoved
      if (delta !== 0) {
        DIFF_MAPPING.forEach((d) => {
          const diffStartLine = d.center.start + 1
          const diffEndLine = d.center.end + 1
          if (change.range.endLineNumber < diffStartLine) {
            d.center.start += delta
            d.center.end += delta
          } else if (change.range.endLineNumber <= diffEndLine) {
            d.center.end += delta
          }
        })
      }
    })
    if (e.isUndoing || e.isRedoing) restoreResolvedState(versionId)
    else captureResolvedState(versionId)
    refreshUI()
  })

  // Sync Scrolling
  let isSyncing = false
    const sync = (src) => {
      if (!isSyncing) {
        isSyncing = true

        // 1. Lấy vị trí cả dọc (Top) và ngang (Left)
        const top = src.getScrollTop()
        const left = src.getScrollLeft();

        [editorLeft, editorCenter, editorRight].forEach((e) => {
          if (e !== src) {
            // 2. Set lại cho các editor khác
            e.setScrollTop(top)
            e.setScrollLeft(left)
          }
        })

        drawLayerElements()
        updateActionButtons()
        isSyncing = false
      }
    };

    // Đăng ký sự kiện
    [editorLeft, editorCenter, editorRight].forEach((e) =>
      e.onDidScrollChange(() => sync(e))
    )

  // Resize
  resizeObserver = new ResizeObserver(() => {
    [editorLeft, editorCenter, editorRight].forEach((e) => e && e.layout())
    refreshUI()
  })
  resizeObserver.observe(mainContainerRef.value)

  // Init state
  captureResolvedState(editorCenter.getModel().getAlternativeVersionId())

  refreshUI()
  nextTick(() => {
    [editorLeft, editorCenter, editorRight].forEach((e) => e.layout())
    refreshUI()
  })

  setTimeout(() => {
    [editorLeft, editorCenter, editorRight].forEach((e) => e.layout())
    refreshUI()
    goToChange('next', true)
  }, 300)
})

onBeforeUnmount(() => {
  if (editorLeft) editorLeft.dispose()
  if (editorCenter) editorCenter.dispose()
  if (editorRight) editorRight.dispose()
  if (resizeObserver) resizeObserver.disconnect()
})

defineExpose({
  goNext: () => goToChange('next'),
  goPrev: () => goToChange('prev'),
  acceptLocal: () => acceptAllConflicts('left'),
  acceptRemote: () => acceptAllConflicts('right'),
  acceptAllBoth: () => acceptAllBoth(),
  // (Optional) Expose biến state để Cha biết đường disable nút
  canNavNext,
  canNavPrev,
  totalConflicts, // Gửi ra ngoài
  totalChanges    // Gửi ra ngoài
})
</script>

<style scoped>
/* CSS Variables Scope */
.merge-editor-wrapper {
  --bg-body: #ededed;
  --border-light: #d1d1d1;
  --border-medium: #c0c0c0;
  --bg-gap: #f0f0f0;
  --bg-header: #e8e8e8;
  --bg-editor: white;
  --bg-center-header: #fff9c4;
  --text-color: #666;

  /* Light Theme Highlights */
  --color-auto-merge: rgba(50, 150, 255, 0.2);
  --color-edit: rgba(155, 89, 182, 0.15);
  --color-edit-char: rgba(142, 36, 170, 0.3);
  --color-conflict-block: rgba(255, 100, 100, 0.1);
  --color-conflict-marker: rgba(255, 0, 0, 0.4);
  --color-conflict-char-bg: rgba(255, 165, 0, 0.4);
  --color-conflict-char-border: #e65100;

  height: 80vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;
  background-color: var(--bg-body);
}

.merge-editor-wrapper.dark-theme {
  --bg-body: #1e1e1e;
  --border-light: #3c3c3c;
  --border-medium: #4e4e4e;
  --bg-gap: #252526;
  --bg-header: #2c2c2c;
  --bg-editor: #1e1e1e;
  --bg-center-header: #474700;
  --text-color: #ccc;

  --color-auto-merge: rgba(50, 150, 255, 0.3);
  --color-edit: rgba(186, 104, 200, 0.3);
  --color-edit-char: rgba(186, 104, 200, 0.5);
  --color-conflict-block: rgba(255, 120, 120, 0.2);
  --color-conflict-marker: rgba(255, 80, 80, 0.5);
  --color-conflict-char-bg: rgba(255, 180, 50, 0.5);
  --color-conflict-char-border: #ffcc00;
}

/* Layout */
.flex {
  display: flex;
}
.flex-1 {
  flex: 1;
}
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
.border-r {
  border-right: 1px solid var(--border-light);
}

.header {
  height: 28px;
  background-color: var(--bg-header);
  border-bottom: 1px solid var(--border-medium);
  display: flex;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-color);
  z-index: 20;
}
.header-col {
  padding: 0 8px;
  display: flex;
  align-items: center;
}
.header-center {
  background-color: var(--bg-center-header);
  justify-content: center;
  flex: 1.2; /* QUAN TRỌNG: Phải khớp với .editor-center */
}

.gap-header {
  width: 80px;
  background: var(--bg-gap);
  flex-shrink: 0; /* QUAN TRỌNG: Chống bị co lại khi màn hình nhỏ */
}

/* Main Container */
#main-container {
  flex: 1;
  display: flex;
  position: relative;
  background-color: var(--bg-gap);
  min-height: 0;
}
.editor-container {
  background-color: var(--bg-editor);
  position: relative;
  overflow: hidden;
}
.editor-center {
  flex: 1.2;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}

.gap-col {
  width: 80px;
  background-color: var(--bg-gap);
  border-left: 1px solid var(--border-light);
  border-right: 1px solid var(--border-light);
  flex-shrink: 0;
  position: relative;
}
#svg-layer,
.action-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
#svg-layer {
  z-index: 10;
}
.action-overlay {
  z-index: 50;
}

/* Buttons */
.nav-btn,
.accept-all-btn,
.theme-toggle {
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid var(--border-medium);
  background: var(--bg-editor);
  color: var(--text-color);
  margin: 0 4px;
  font-size: 12px;
  font-weight: 600;
}
.nav-btn:hover,
.theme-toggle:hover {
  background: var(--bg-header);
}
.nav-btn:disabled {
  color: #aaa;
  cursor: not-allowed;
  opacity: 0.6;
}

.accept-all-btn {
  color: #4caf50;
  border-color: #4caf50;
}
.accept-all-btn:hover {
  background: #e8f5e9;
  color: #388e3c;
}
.dark-theme .accept-all-btn {
  color: #66bb6a;
  border-color: #66bb6a;
  background: var(--bg-editor);
}
.dark-theme .accept-all-btn:hover {
  background: #383838;
  color: #81c784;
}

.legend-group span {
  margin-left: 10px;
  font-size: 11px;
  font-weight: bold;
}

/* Deep selectors for Monaco & Dynamic Elements */
:deep(.action-btn) {
  position: absolute;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-color);
  pointer-events: auto;
  background: transparent;
  z-index: 60;
}

/* Dynamic Monaco Classes */
:deep(.diff-conflict) {
  background-color: var(--color-conflict-block) !important;
}
:deep(.diff-marker) {
  background-color: var(--color-conflict-marker);
  font-weight: bold;
  color: var(--text-color);
}
:deep(.diff-auto-merge-blue) {
  background-color: var(--color-auto-merge) !important;
}
:deep(.diff-edit-purple) {
  background-color: var(--color-edit) !important;
}
:deep(.diff-block-base) {
  background-color: var(--color-conflict-block);
}
:deep(.diff-char-add),
:deep(.diff-char-del) {
  background-color: var(--color-edit-char);
}
:deep(.diff-char-diff) {
  background-color: var(--color-conflict-char-bg);
  border-bottom: 1px solid var(--color-conflict-char-border);
}
</style>
