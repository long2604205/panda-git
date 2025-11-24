const DB_NAME = 'panda-git';
const STORE_NAME = 'data';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      if (db.objectStoreNames.contains(STORE_NAME)) {
        db.deleteObjectStore(STORE_NAME);
      }

      db.createObjectStore(STORE_NAME, { keyPath: 'id' });
    };

    request.onsuccess = (event) => resolve(event.target.result);
    request.onerror = (event) => reject(event.target.error);
  });
}

export async function saveGroups(groups) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);

    const record = {
      id: 'groups',
      data: JSON.parse(JSON.stringify(groups))
    };

    const request = store.put(record);

    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error);
  });
}

export async function loadGroups() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const store = tx.objectStore(STORE_NAME);

    const request = store.get('groups');

    request.onsuccess = () => resolve(request.result?.data || []);
    request.onerror = () => reject(request.error);
  });
}

export async function updateGroup(groupId, newData) {
  const currentGroups = await loadGroups();

  const updated = currentGroups.map(group => {
    if (group.id === groupId) {
      return {
        ...group,
        ...newData
      };
    }
    return group;
  });

  return await saveGroups(updated);
}

export async function saveRepos(repos) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);

    const deleteRequest = store.delete('repositories');
    deleteRequest.onsuccess = () => {
      const dataToSave = repos.map(r => ({
        id: r.id,
        path: r.path,
        name: r.name,
        groupId: r.groupId || null,
        active: r.active || false
      }));

      const record = {
        id: 'repositories',
        data: dataToSave
      };

      const putRequest = store.put(record);

      putRequest.onsuccess = () => resolve(true);
      putRequest.onerror = () => reject(putRequest.error);
    };

    deleteRequest.onerror = () => reject(deleteRequest.error);
  });
}

export async function loadRepos() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const store = tx.objectStore(STORE_NAME);

    const request = store.get('repositories');

    request.onsuccess = () => {
      const data = request.result?.data || [];
      resolve(data);
    };

    request.onerror = () => reject(request.error);
  });
}

