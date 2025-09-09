// modalService.js
import { createApp, h, reactive } from 'vue'

let modalInstance = null

export function showPageInModal(component, props = {}, modalProps = {}) {
  if (modalInstance) return

  const container = document.createElement('div')
  document.body.appendChild(container)

  const state = reactive({ visible: true })

  const app = createApp({
    render() {
      return h(component, {
        ...props,
        modelValue: state.visible,
        'onUpdate:modelValue': (val) => {
          state.visible = val
          if (!val) close()
        },
        onClose: close,
        ...modalProps, // ✅ truyền thêm width, title, id, ...
      })
    }
  })

  function close() {
    state.visible = false
    setTimeout(() => {
      app.unmount()
      container.remove()
      modalInstance = null
    }, 300)
  }

  modalInstance = app
  app.mount(container)
}
