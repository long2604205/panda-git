// src/plugins/indexedDB.js
const DB_NAME = 'gitUI';
const STORE_NAME = 'repositories';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id' });
      }
    };

    request.onsuccess = (event) => resolve(event.target.result);
    request.onerror = (event) => reject(event.target.error);
  });
}

// Lưu danh sách repo (id, path, name, status)
export async function saveRepos(repos) {
  const db = await openDB();
  const tx = db.transaction(STORE_NAME, 'readwrite');
  const store = tx.objectStore(STORE_NAME);

  store.clear(); // xóa hết trước khi lưu mới
  for (const repo of repos) {
    store.put({
      id: repo.id,
      path: repo.path,
      name: repo.name,
      status: repo.status || 'clean',
      active: repo.active || false
    });
  }

  return tx.complete;
}

// Load danh sách repo đã lưu
export async function loadRepos() {
  const db = await openDB();
  const tx = db.transaction(STORE_NAME, 'readonly');
  const store = tx.objectStore(STORE_NAME);

  return new Promise((resolve, reject) => {
    const request = store.getAll();
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

// Cập nhật repo trong IndexedDB
export async function updateRepoInDB(repo) {
  const db = await openDB();
  const tx = db.transaction(STORE_NAME, 'readwrite');
  const store = tx.objectStore(STORE_NAME);

  return new Promise((resolve, reject) => {
    const request = store.put({
      id: repo.id,
      name: repo.name,
      path: repo.path,
      status: repo.status || 'clean',
      active: repo.active || false
    });

    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error);
  });
}

