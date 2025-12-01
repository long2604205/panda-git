import mitter from '@/plugins/mitter.js'

const notify = {
  success(message, options = {}) {
    mitter.emit("toast", {
      type: "success",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      closable: options.closable !== false,
      ...options
    })
  },

  error(message, options = {}) {
    mitter.emit("toast", {
      type: "error",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      closable: options.closable !== false,
      ...options
    })
  },

  warning(message, options = {}) {
    mitter.emit("toast", {
      type: "warning",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      closable: options.closable !== false,
      ...options
    })
  },

  info(message, options = {}) {
    mitter.emit("toast", {
      type: "info",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      closable: options.closable !== false,
      ...options
    })
  },

  loading(message, options = {}) {
    const id = Date.now() + Math.floor(Math.random() * 1000)
    mitter.emit("toast", {
      type: "loading",
      message,
      closable: false,
      duration: 0,
      id,
      ...options
    })

    return id
  },

  remove(id) {
    mitter.emit("toast-remove", id)
  },

  on: mitter.on
}

export default notify
