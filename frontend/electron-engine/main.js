import { app, BrowserWindow, ipcMain, dialog } from 'electron'
import { dirname, join } from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

let win

function createWindow() {
  win = new BrowserWindow({
    width: 1200,
    height: 800,
    frame: false,
    show: false,
    icon: join(__dirname, 'assets/panda-logo.ico'),
    webPreferences: {
      preload: join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  win.once('ready-to-show', () => {
    win.maximize()
    win.show()
  })

  win.on('restore', () => {
    if (!win.isMaximized()) {
      win.setSize(1200, 800)
    }
  })

  win.loadFile(join(__dirname, '../dist/index.html'))
  // win.webContents.openDevTools()

  ipcMain.on('close-app', () => win.close())
  ipcMain.on('minimize', () => win.minimize())
  ipcMain.on('maximize', () => win.maximize())
  ipcMain.on('unmaximize', () => win.unmaximize())

  ipcMain.on('toggle-maximize', () => {
    if (win.isMaximized()) {
      win.unmaximize()
    } else {
      win.maximize()
    }
  })

  ipcMain.handle('get-memory-info', async () => {
    // eslint-disable-next-line no-undef
    const memoryInfo = await process.getProcessMemoryInfo()
    return {
      ramKB: memoryInfo.residentSet
    }
  })

  ipcMain.handle('dialog:select-folder', async () => {
    const result = await dialog.showOpenDialog(win, {
      properties: ['openDirectory']
    })

    if (result.canceled) return null
    return result.filePaths[0]
  })

  win.on('maximize', () => {
    win.webContents.send('is-maximized')
  })

  win.on('unmaximize', () => {
    win.webContents.send('is-unmaximized')
  })
}

app.whenReady().then(createWindow)
