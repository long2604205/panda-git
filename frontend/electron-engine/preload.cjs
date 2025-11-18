// eslint-disable-next-line no-undef
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  closeApp: () => ipcRenderer.send('close-app'),
  minimize: () => ipcRenderer.send('minimize'),
  maximize: () => ipcRenderer.send('maximize'),
  unmaximize: () => ipcRenderer.send('unmaximize'),
  toggleMaximize: () => ipcRenderer.send('toggle-maximize'),
  onMaximize: (cb) => ipcRenderer.on('is-maximized', cb),
  onUnmaximize: (cb) => ipcRenderer.on('is-unmaximized', cb),
  getMemoryInfo: () => ipcRenderer.invoke('get-memory-info'),
  selectFolder: () => ipcRenderer.invoke('dialog:select-folder'),
  openInExplorer: (folderPath) => ipcRenderer.invoke('open-in-explorer', folderPath),
  openTerminal: (folderPath) => ipcRenderer.invoke('open-terminal', folderPath),
  openDevtools: () => ipcRenderer.invoke('open-devtools'),


})
