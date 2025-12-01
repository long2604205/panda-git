import { ref, onBeforeUnmount } from 'vue'

export function useSideBarResize() {
  // 1. Resize Chiều cao (Giữa Repo và Branch)
  const paneHeight = ref(200)
  let startY = 0
  let startHeight = 0

  const onRowMouseMove = (e) => {
    paneHeight.value = startHeight + (e.clientY - startY)
  }

  const onRowMouseUp = () => {
    document.removeEventListener('mousemove', onRowMouseMove)
    document.removeEventListener('mouseup', onRowMouseUp)
    document.body.classList.remove('resizing-row')
  }

  const startRowResize = (e) => {
    startY = e.clientY
    startHeight = paneHeight.value
    document.addEventListener('mousemove', onRowMouseMove)
    document.addEventListener('mouseup', onRowMouseUp)
    document.body.classList.add('resizing-row')
  }

  // 2. Resize Chiều rộng Sidebar (Trái qua phải)
  const sidebarWidth = ref(288) // w-72 ~ 288px
  let startX = 0
  let startW = 0

  const onColMouseMove = (e) => {
    sidebarWidth.value = startW + (e.clientX - startX)
    if (window.diffEditor) window.diffEditor.layout()
  }

  const onColMouseUp = () => {
    document.removeEventListener('mousemove', onColMouseMove)
    document.removeEventListener('mouseup', onColMouseUp)
    document.body.classList.remove('resizing-col')
  }

  const startColResize = (e) => {
    startX = e.clientX
    startW = sidebarWidth.value
    document.addEventListener('mousemove', onColMouseMove)
    document.addEventListener('mouseup', onColMouseUp)
    document.body.classList.add('resizing-col')
  }

  onBeforeUnmount(() => {
    document.removeEventListener('mousemove', onRowMouseMove)
    document.removeEventListener('mouseup', onRowMouseUp)
    document.removeEventListener('mousemove', onColMouseMove)
    document.removeEventListener('mouseup', onColMouseUp)
  })

  return { paneHeight, sidebarWidth, startRowResize, startColResize }
}
