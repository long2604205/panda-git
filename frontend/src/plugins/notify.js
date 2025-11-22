import mitter from '@/plugins/mitter.js'

const notify = {
  success(message, options = {}) {
    mitter.emit("alert", {
      type: "success",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      ...options
    })
  },

  error(message, options = {}) {
    mitter.emit("alert", {
      type: "danger",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      ...options
    })
  },

  info(message, options = {}) {
    mitter.emit("alert", {
      type: "info",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      ...options
    })
  },

  warning(message, options = {}) {
    mitter.emit("alert", {
      type: "warning",
      message,
      title: options.title || null,
      duration: options.duration || 5000,
      ...options
    })
  },

  on: mitter.on
}

export default notify
