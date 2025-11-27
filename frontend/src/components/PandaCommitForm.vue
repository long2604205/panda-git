<template>
  <!-- TOP: COMMIT FORM -->
  <div class="commit-box flex-shrink-0 border-b border-[var(--border-color)]">
    <!-- Commit Options Popup -->
    <div
      v-show="showCommitOptions"
      class="commit-options-popup active"
      @click.stop
    >
      <div class="co-section">
        <div class="flex items-center gap-2 mb-2">
          <label class="co-label">Author:</label>
          <input
            type="text"
            v-model="authorInput"
            class="bg-[var(--p-bg-sidebar)] border border-[var(--border-color)] rounded px-1.5 py-0.5 text-[var(--text-color)] outline-none w-36 text-[11px]"
            placeholder="Name <email>"
          />
        </div>
        <div class="co-item" @click="toggleOption('signOff')">
          <div
            :class="[
              'custom-checkbox',
              'option-check',
              { checked: commitOptions.signOff },
            ]"
          >
            <i class="fa-solid fa-check"></i>
          </div>
          <span>Sign-off commit</span>
        </div>
      </div>
      <div class="co-section">
        <div class="co-title">Commit Checks</div>
        <div class="co-item" @click="toggleOption('reformat')">
          <div
            :class="[
              'custom-checkbox',
              'option-check',
              { checked: commitOptions.reformat },
            ]"
          >
            <i class="fa-solid fa-check"></i>
          </div>
          <span>Reformat code</span>
        </div>
        <div class="co-item" @click="toggleOption('rearrange')">
          <div
            :class="[
              'custom-checkbox',
              'option-check',
              { checked: commitOptions.rearrange },
            ]"
          >
            <i class="fa-solid fa-check"></i>
          </div>
          <span>Rearrange code</span>
        </div>
      </div>
    </div>

    <!-- Commit Header -->
    <div class="commit-header">
      <div class="committing-as">
        <div class="author-avatar">LW</div>
        <div>Committing as <span>Lion Wilson</span></div>
      </div>
      <button
        class="w-10 text-[var(--p-text-muted)] hover:text-[var(--text-color)]"
        @click.stop="toggleCommitOptions"
      >
        <i class="fa-solid fa-ellipsis-vertical"></i>
      </button>
    </div>

    <!-- Inputs -->
    <input
      type="text"
      v-model="commitSummary"
      class="commit-input-field commit-summary"
      placeholder="Summary (required)"
    />
    <textarea
      v-model="commitDescription"
      class="commit-input-field commit-desc resize-y"
      placeholder="Description..."
    />

    <!-- Amend Option -->
    <div class="commit-options-row" @click="toggleAmend">
      <div :class="['custom-checkbox', { checked: amendChecked }]">
        <i class="fa-solid fa-check"></i>
      </div>
      <span>Amend last commit</span>
    </div>

    <!-- Buttons -->
    <div class="commit-buttons">
      <button class="btn-commit btn-commit-primary" @click="doCommit('commit')">
        Commit
      </button>
      <button class="btn-commit btn-commit-secondary" @click="doCommit('push')">
        Commit & Push
      </button>
    </div>
  </div>

  <!-- BOTTOM: SCROLLABLE FILE LIST -->
  <div class="flex-1 overflow-y-auto bg-[var(--bg-side)]">
    <!-- Staged Changes -->
    <div v-if="changeState.staged.length > 0">
      <div class="file-list-header">
        <div class="flex items-center gap-2">
          <i class="fa-solid fa-chevron-down text-[9px]" @click="toggleAllFiles('staged')"/>
          <span
            >Staged Changes
            <span class="ml-1 text-[var(--accent-color)]"
              >({{ changeState.staged.length }})</span
            ></span
          >
        </div>
      </div>
      <div
        v-for="file in changeState.staged"
        :key="file.id"
        class="change-file-item group"
        @click="toggleFileCheck('staged', file.id)"
      >
        <div
          :class="['custom-checkbox', { checked: file.checked }]"
          class="mr-3"
        >
          <i class="fa-solid fa-check"></i>
        </div>
        <span
          :class="getStatusColor(file.status)"
          class="w-5 font-mono font-bold text-[10px]"
        >
          {{ file.status }}
        </span>
        <component :is="getFileIcon(file.path)" />
        <div class="flex flex-col justify-center flex-1 min-w-0">
          <span
            class="text-[var(--text-color)] truncate text-[12px] leading-tight"
          >
            {{ getFileName(file.path) }}
          </span>
          <span
            v-if="getDirName(file.path)"
            class="text-[var(--p-text-dim)] truncate text-[10px] leading-tight"
          >
            {{ getDirName(file.path) }}
          </span>
        </div>
        <div
          class="opacity-0 group-hover:opacity-100 text-[var(--p-text-dim)] hover:text-[var(--text-color)] px-2 cursor-pointer"
          title="Unstage"
        >
          <i class="fa-solid fa-minus"></i>
        </div>
      </div>
    </div>
    <div
      v-else
      class="p-4 text-center text-[11px] text-[var(--p-text-dim)] italic border-b border-[var(--border-color)]"
    >
      No staged changes
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, h } from "vue";
import mitter from "@/plugins/mitter.js";

// Commit form state
const commitSummary = ref("");
const commitDescription = ref("");
const amendChecked = ref(false);
const showCommitOptions = ref(false);
const authorInput = ref("");

const commitOptions = ref({
  signOff: false,
  reformat: false,
  rearrange: false,
});

// Changes state
const changeState = ref({
  staged: [
    {
      id: "s1",
      path: "src/components/Toolbar.tsx",
      status: "M",
      checked: true,
    },
    { id: "u1", path: "src/App.css", status: "M", checked: false },
    { id: "u2", path: "public/old_logo.png", status: "D", checked: false },
    { id: "u3", path: "src/utils/helpers.ts", status: "A", checked: true },
  ]
});


const toggleCommitOptions = () => {
  showCommitOptions.value = !showCommitOptions.value;
};

const toggleOption = (option) => {
  commitOptions.value[option] = !commitOptions.value[option];
};

const toggleAmend = () => {
  amendChecked.value = !amendChecked.value;
  if (amendChecked.value) {
    commitSummary.value = "Last commit message...";
  } else {
    commitSummary.value = "";
  }
};

const toggleFileCheck = (type, id) => {
  const file = changeState.value[type].find((f) => f.id === id);
  if (file) {
    file.checked = !file.checked;
  }
};

const toggleAllFiles = (type) => {
  const list = changeState.value[type];
  const allChecked = list.every((f) => f.checked);
  list.forEach((f) => (f.checked = !allChecked));
};

const doCommit = (action) => {
  if (!commitSummary.value) {
    alert("Please enter a commit summary");
    return;
  }

  if (changeState.value.staged.length === 0 && !amendChecked.value) {
    alert("No staged files to commit");
    return;
  }

  const message =
    action === "push"
      ? "Committing & Pushing..."
      : amendChecked.value
      ? "Amending commit..."
      : "Committing...";

  alert(message);

  // Reset form
  setTimeout(() => {
    alert(
      action === "push"
        ? "Success: Committed and Pushed!"
        : "Success: Commit created!"
    );

    changeState.value.staged = [];
    amendChecked.value = false;
    commitSummary.value = "";
    commitDescription.value = "";

    // Emit event to refresh commit list
    mitter.emit("commit-created", { message: commitSummary.value });

  }, 300);
};

// Helper functions
const getStatusColor = (status) => {
  if (status === "M") return "text-[var(--p-yellow)]";
  if (status === "D") return "text-[var(--p-red)]";
  if (status === "A") return "text-[var(--p-green)]";
  return "";
};

const getFileIcon = (path) => {
  if (path.endsWith(".ts") || path.endsWith(".tsx")) {
    return h("i", { class: "fa-brands fa-js file-icon file-ts" });
  }
  if (path.endsWith(".css")) {
    return h("i", { class: "fa-brands fa-css3-alt file-icon file-css" });
  }
  if (path.endsWith(".html")) {
    return h("i", { class: "fa-brands fa-html5 file-icon file-html" });
  }
  if (path.endsWith(".json")) {
    return h("i", { class: "fa-solid fa-brackets-curly file-icon file-json" });
  }
  if (path.endsWith(".png") || path.endsWith(".jpg")) {
    return h("i", { class: "fa-solid fa-image file-icon file-img" });
  }
  return h("i", {
    class: "fa-solid fa-file file-icon text-[var(--p-text-dim)]",
  });
};

const getFileName = (path) => {
  const lastSlash = path.lastIndexOf("/");
  return lastSlash > -1 ? path.substring(lastSlash + 1) : path;
};

const getDirName = (path) => {
  const lastSlash = path.lastIndexOf("/");
  return lastSlash > -1 ? path.substring(0, lastSlash) : "";
};


// Lifecycle hooks
onMounted(() => {
  // Close commit options popup when clicking outside
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const handleClickOutside = () => {
  showCommitOptions.value = false;
};
</script>

<style scoped>

/* Commit Box Styles */
.commit-box {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-main);
  padding: 12px;
  position: relative;
}

.commit-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.committing-as {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--p-text-muted);
}

.committing-as span {
  color: var(--text-color);
  font-weight: 600;
}

.author-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: bold;
}

.commit-input-field {
  background-color: var(--bg-main);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 8px 10px;
  color: var(--text-color);
  font-size: 12px;
  outline: none;
  width: 100%;
  transition: border-color 0.2s;
}

.commit-input-field:focus {
  border-color: var(--accent-color);
}

.commit-summary {
  margin-bottom: 8px;
  font-weight: 500;
}

.commit-desc {
  height: 150px;
  margin-bottom: 8px;
  font-family: sans-serif;
}

.commit-options-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  cursor: pointer;
}

.commit-options-row span {
  font-size: 11px;
  color: var(--p-text-muted);
}

.commit-buttons {
  display: flex;
  gap: 8px;
}

.btn-commit {
  flex: 1;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
  color: #000;
}

.btn-commit:hover {
  opacity: 0.9;
}

.btn-commit-primary {
  background-color: var(--p-cyan-btn);
}

.btn-commit-secondary {
  background-color: var(--p-pink-btn);
}

/* Checkbox Styles */
.custom-checkbox {
  width: 14px;
  height: 14px;
  border: 1px solid var(--p-text-dim);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  background-color: transparent;
}

.custom-checkbox:hover {
  border-color: var(--text-color);
}

.custom-checkbox.checked {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: var(--bg-main);
}

.custom-checkbox i {
  font-size: 10px;
  display: none;
}

.custom-checkbox.checked i {
  display: block;
}

.custom-checkbox.option-check.checked {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: var(--bg-main);
}

/* Commit Options Popup */
.commit-options-popup {
  position: absolute;
  top: 28px;
  right: 12px;
  background-color: var(--bg-main);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  z-index: 2000;
  padding: 12px;
  font-size: 11px;
  color: var(--p-text-main);
  width: 250px;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.co-section {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.co-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.co-title {
  color: var(--p-text-dim);
  margin-bottom: 8px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.co-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  cursor: pointer;
  padding: 4px 0;
}

.co-item:hover span {
  color: var(--text-color);
}

.co-item:hover .custom-checkbox {
  border-color: var(--text-color);
}

.co-label {
  flex: 1;
  color: var(--p-text-muted);
}

/* File List Styles */
.file-list-header {
  padding: 8px 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--p-text-dim);
  background-color: var(--bg-side);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  border-bottom: 1px solid var(--border-color);
}

.file-list-header:hover {
  color: var(--text-color);
}

.change-file-item {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  transition: background-color 0.1s;
}

.change-file-item:hover {
  background-color: var(--p-hover);
}

.file-icon {
  margin-right: 8px;
  width: 14px;
  text-align: center;
}

.file-ts {
  color: #3178c6;
}
.file-json {
  color: #f1e05a;
}
.file-css {
  color: #563d7c;
}
.file-html {
  color: #e34c26;
}
.file-img {
  color: #a074c4;
}
</style>
