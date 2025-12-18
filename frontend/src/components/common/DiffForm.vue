<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="Merge Conflict"
  >
    <template #content>
      <div class="git-toolbar">
        <!-- MAIN LEFT GROUP (Repo Info + Actions) -->
        <div class="toolbar-left">
          <!-- --- 2. ACTIONS --- -->
          <div class="actions-group">
            <div class="control-group-transparent">
              <button
                class="control-btn group"
                :disabled="
                  (nextBlock === 'conflict' && diffThreeWayRef?.totalConflicts === 0) ||
                    (nextBlock === 'changes' && diffThreeWayRef?.totalChanges === 0)"
                @click="triggerPrev"
              >
                <panda-icon
                  name="arrow-up"
                  size="12px"
                  color="#22d3ee"
                />
                <span class="tooltip-arrow-box">
                  Previous changes
                </span>
              </button>
              <button
                class="control-btn group"
                :disabled="
                  (nextBlock === 'conflict' && diffThreeWayRef?.totalConflicts === 0) ||
                    (nextBlock === 'changes' && diffThreeWayRef?.totalChanges === 0)
                "
                @click="triggerNext"
              >
                <panda-icon
                  name="arrow-down"
                  size="12px"
                  color="#22d3ee"
                />
                <span class="tooltip-arrow-box">
                  Next changes
                </span>
              </button>
              <div class="toolbar-divider" />
              <button
                class="control-btn group"
                :disabled="diffThreeWayRef?.totalConflicts === 0"
                @click="triggerAcceptLocal"
              >
                <panda-icon
                  name="angles-right"
                  size="12px"
                  color="rgb(52, 211, 153)"
                />
                <span class="tooltip-arrow-box">
                  Accept left
                </span>
              </button>
              <button
                class="control-btn group"
                :disabled="diffThreeWayRef?.totalConflicts === 0"
                @click="triggerAcceptAllBoth"
              >
                <angles-merge-icon style="color: rgb(52, 211, 153)" />
                <span class="tooltip-arrow-box">
                  Accept both
                </span>
              </button>
              <button
                class="control-btn group"
                :disabled="diffThreeWayRef?.totalConflicts === 0"
                @click="triggerAcceptRemote"
              >
                <panda-icon
                  name="angles-left"
                  size="12px"
                  color="rgb(52, 211, 153)"
                />
                <span class="tooltip-arrow-box">
                  Accept right
                </span>
              </button>
              <div class="toolbar-divider" />
              <panda-select-option
                v-model="nextBlock"
                style="width: 100px"
                :options="[
                  { id: 'changes', label: 'Changes' },
                  { id: 'conflict', label: 'Conflict' },
                ]"
                value="id"
                text="label"
                value-default="changes"
              />
              <panda-select-option
                v-model="modeView"
                style="width: 160px"
                :options="[
                  { id: 'all', label: 'Side-by-side viewer' },
                  { id: 'hcm', label: 'Unified viewer' },
                ]"
                value="id"
                text="label"
                value-default="all"
              />
            </div>
          </div>
        </div>

        <!-- RIGHT: Tools & Layout -->
        <div class="toolbar-right">
          <!-- Tools Group -->
          <div class="tools-group mr-4">
            <span style="font-size: 11px; color: var(--p-text-muted);">
              {{ diffThreeWayRef?.totalConflicts }} conflicts, {{ diffThreeWayRef?.totalChanges }} Total Changes
            </span>
          </div>
        </div>
      </div>
      <diff-three-ways
        ref="diffThreeWayRef"
        :merge-segments="segments"
        :nav-mode="nextBlock"
      />
    </template>
    <template #footer>
      <button
        :disabled="diffThreeWayRef?.totalConflicts > 0"
        class="btn btn-primary"
        @click="save"
      >
        <span>Apply</span>
      </button>
      <button
        class="btn btn-secondary"
        @click="close"
      >
        <span>Close</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import {ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
import DiffThreeWays from '@/components/common/DiffThreeWays.vue'
import PandaSelectOption from '@/components/common/PandaSelectOption.vue'
import AnglesMergeIcon from '@/components/icons/AnglesMergeIcon.vue'
import PandaIcon from '@/components/icons/PandaIcon.vue'

defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})
const diffThreeWayRef = ref(null)

const visible = ref(false)
const openForm = ref(null)

const close = () => {
  openForm.value.close()
}

const save = async () => {
  close()
}

const nextBlock = ref('changes')
const modeView = ref('all')
// 2. Các hành động của Cha (chỉ đơn giản là gọi hàm của con)
const triggerNext = () => {
  // "Ê con, chạy hàm goNext đi!"
  diffThreeWayRef.value?.goNext()
}

const triggerPrev = () => {
  diffThreeWayRef.value?.goPrev()
}

const triggerAcceptLocal = () => {
  diffThreeWayRef.value?.acceptLocal()
}

const triggerAcceptRemote = () => {
  diffThreeWayRef.value?.acceptRemote()
}
const triggerAcceptAllBoth = () => {
  diffThreeWayRef.value?.acceptAllBoth()
}

const segments = [
  // ================= HEADER =================
  {
    type: 'common',
    text: [
      'package com.example.service;',
      '',
      'import java.util.*;',
      'import java.util.stream.Collectors;',
      'import org.slf4j.Logger;',
      'import org.slf4j.LoggerFactory;',
      'import org.springframework.transaction.annotation.Transactional;',
      ''
    ]
  },

  // ================= EDIT LEFT =================
  {
    type: 'edit-left',
    local: [
      '// [LOCAL] Logger initialized',
      'private static final Logger log = LoggerFactory.getLogger(UserService.class);'
    ],
    remote: [
      '// [REMOTE] Logger not used',
      'private static final Logger log = null;'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      'public class UserService {',
      '',
      '    private final UserRepository repo;',
      '    private final NotificationService notifier;',
      ''
    ]
  },

  // ================= CONFLICT 1 =================
  {
    type: 'conflict',
    local: [
      '    // Local: Constructor Injection',
      '    public UserService(UserRepository repo, NotificationService notifier) {',
      '        this.repo = repo;',
      '        this.notifier = notifier;',
      '    }'
    ],
    remote: [
      '    // Remote: Manual instantiation',
      '    public UserService(UserRepository repo) {',
      '        this.repo = repo;',
      '        this.notifier = new EmailService();',
      '    }'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      '    // ================= QUERY =================',
      ''
    ]
  },

  // ================= AUTO MERGE =================
  {
    type: 'auto-merge-right',
    text: [
      '    public Optional<User> findById(String id) {',
      '        return repo.findById(id);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: ['']
  },

  // ================= EDIT RIGHT =================
  {
    type: 'edit-right',
    local: [
      '    public List<User> findAll() {',
      '        return repo.findAll();',
      '    }'
    ],
    remote: [
      '    public List<User> findAll() {',
      '        return repo.findAllActive();',
      '    }'
    ]
  },

  {
    type: 'common',
    text: ['']
  },

  // ================= CONFLICT 2 =================
  {
    type: 'conflict',
    local: [
      '    public User create(User user) {',
      '        validate(user);',
      '        return repo.save(user);',
      '    }'
    ],
    remote: [
      '    public User create(User user) {',
      '        if (repo.existsByEmail(user.getEmail())) {',
      '            throw new DuplicateUserException();',
      '        }',
      '        return repo.save(user);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      '    // ================= UPDATE =================',
      ''
    ]
  },

  // ================= CONFLICT 3 =================
  {
    type: 'conflict',
    local: [
      '    @Transactional',
      '    public User update(String id, User payload) {',
      '        User u = repo.findById(id).orElseThrow();',
      '        u.setName(payload.getName());',
      '        return repo.save(u);',
      '    }'
    ],
    remote: [
      '    public User update(String id, User payload) {',
      '        return repo.updatePartial(id, payload);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: ['']
  },

  // ================= EDIT LEFT =================
  {
    type: 'edit-left',
    local: [
      '    public void notifyUser(User user) {',
      '        log.info("Notify user {}", user.getEmail());',
      '        notifier.send(user);',
      '    }'
    ],
    remote: [
      '    public void notifyUser(User user) {',
      '        notifier.send(user);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      '    // ================= DELETE =================',
      ''
    ]
  },

  // ================= EDIT RIGHT =================
  {
    type: 'edit-right',
    local: [
      '    public void delete(String id) {',
      '        repo.deleteById(id);',
      '    }'
    ],
    remote: [
      '    public void delete(String id) {',
      '        repo.softDelete(id, true);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: ['']
  },

  // ================= CONFLICT 4 =================
  {
    type: 'conflict',
    local: [
      '    public void deleteUser(String id) {',
      '        repo.deleteById(id);',
      '    }'
    ],
    remote: [
      '    public void deleteUser(String id) {',
      '        repo.softDelete(id);',
      '        notifier.sendDeletionNotice(id);',
      '    }'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      '    // ================= UTIL =================',
      ''
    ]
  },

  // ================= AUTO MERGE =================
  {
    type: 'auto-merge-right',
    text: [
      '    private void validate(User user) {',
      '        if (user.getEmail() == null) {',
      '            throw new IllegalArgumentException("email required");',
      '        }',
      '    }'
    ]
  },

  {
    type: 'common',
    text: [
      '',
      '}'
    ]
  }
]

</script>

<style scoped lang="scss">
:deep(.modal-body) {
  padding: 0 !important;
}

.btn {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-secondary {
  background-color: transparent;
  border-color: var(--p-text-muted);
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: var(--bg-side);
}

.btn-primary {
  background-color: var(--accent-color);
  color: #000;
  font-weight: 600;
}

.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 10px var(--p-selection);
}
</style>
<style scoped>
/* --- MAIN TOOLBAR CONTAINER --- */
.git-toolbar {
  height: 40px;
  background-color: var(--bg-header);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  user-select: none;
  position: relative;
}

/* --- LEFT SECTION --- */
.toolbar-left {
  display: flex;
  align-items: center;
  margin-right: auto;
}

/* --- ACTIONS GROUP --- */
.actions-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.control-group-transparent {
  margin-left: 5px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.control-btn {
  width: 24px;
  height: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
  color: var(--p-text-muted);
  transition: all 0.2s;
  position: relative;
  background: none;
  border: none;
}

.control-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.control-btn:hover {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.control-btn:active {
  transform: scale(0.98);
  background-color: var(--p-selection);
}

.control-btn:active .tooltip-arrow-box {
  opacity: 0 !important;
  transition: none !important;
  visibility: hidden;
}

.control-btn i {
  font-size: 14px;
}

.control-btn span {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background-color: var(--border-color);
  margin: 0 4px;
  opacity: 0.5;
}

.badge-dot {
  position: absolute;
  top: 6px;
  right: 18px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--accent-color);
  box-shadow: 0 0 5px var(--accent-color);
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0% {
    opacity: 0.6;
    box-shadow: 0 0 2px var(--accent-color);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 8px var(--accent-color);
  }
  100% {
    opacity: 0.6;
    box-shadow: 0 0 2px var(--accent-color);
  }
}

.action-spacer {
  width: 16px;
}

/* --- RIGHT SECTION --- */
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.tools-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tooltip-arrow-box {
  @apply absolute top-full mt-1 left-0 z-50
         whitespace-nowrap rounded-md px-3 py-1.5 text-[11px] font-semibold
         opacity-0 group-hover:opacity-100 transition-all duration-200 ease-out
         -translate-y-1 group-hover:translate-y-0 pointer-events-none group-hover:delay-700;

  background-color: var(--bg-header);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.tooltip-arrow-box::before {
  content: "";
  position: absolute;
  top: -5px;
  left: 12px;
  transform: translateX(-50%) rotate(45deg);
  width: 9px;
  height: 9px;
  background-color: var(--bg-header);
  border-top: 1px solid var(--border-color);
  border-left: 1px solid var(--border-color);
  z-index: 10;
}
</style>
