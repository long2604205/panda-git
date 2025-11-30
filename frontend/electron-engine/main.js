import { app, BrowserWindow, dialog, ipcMain, shell } from 'electron'
import path, { dirname, join } from 'path'
import { fileURLToPath } from 'url'
import { spawn } from 'child_process'
import os from 'os'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

let win, splash

function createWindow() {

  splash = new BrowserWindow({
    width: 680,
    height: 420,
    frame: false,
    alwaysOnTop: true,
    transparent: true,
    resizable: false,
    center: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    icon: join(__dirname, 'assets/panda-logo.ico'),
  })
  splash.loadFile(join(__dirname, 'splash.html'))

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
  win.loadFile(join(__dirname, '../dist/index.html'))

  win.once('ready-to-show', () => {})
  ipcMain.on('splash-finished', () => {
      if (splash && !splash.isDestroyed()) {
        splash.destroy();
      }
      if (win && !win.isDestroyed()) {
        win.maximize();
        win.show();
      }
  });

  win.on('restore', () => {
    if (!win.isMaximized()) {
      win.setSize(1200, 800)
    }
  })


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

ipcMain.handle('open-in-explorer', async (event, folderPath) => {
  try {
    await shell.openPath(folderPath);
    return { success: true };
  } catch (err) {
    console.error('Failed to open folder:', err);
    return { success: false, error: err.message };
  }
});

ipcMain.handle('open-terminal', async (event, folderPath) => {
  try {
    const platform = os.platform();

    if (platform === 'win32') {
      // Windows Terminal
      spawn('wt', ['-d', folderPath], { detached: true });

      // Nếu máy không có Windows Terminal thì fallback CMD
      // spawn('cmd.exe', ['/K', `cd /d "${folderPath}"`], { detached: true });
    }
    else if (platform === 'darwin') {
      // macOS - mở Terminal và cd vào
      spawn('open', ['-a', 'Terminal', folderPath]);
    }
    else {
      // Linux - mở terminal mặc định
      spawn('x-terminal-emulator', ['--working-directory', folderPath], {
        detached: true
      });
    }

    return { success: true };
  } catch (err) {
    console.error(err);
    return { success: false, error: err.message };
  }
});

ipcMain.handle('open-devtools', () => {
  if (win) {
    win.webContents.openDevTools()
    return true
  }
  return false
})

app.whenReady().then(createWindow)
