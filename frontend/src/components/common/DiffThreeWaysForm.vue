<template>
  <base-form
    ref="openForm"
    v-model="visible"
    title="Merge Conflict"
  >
    <template #content>
<!--      <draft-merge-conflict :merge-segments="segments"/>-->
      <diff-three-ways :merge-segments="segments"/>
    </template>
    <template #footer>
      <button
        class="btn btn-secondary"
        @click="close"
      >
        <span>Close</span>
      </button>
      <button
        class="btn btn-primary"
        @click="save"
      >
        <span>Save</span>
      </button>
    </template>
  </base-form>
</template>

<script setup>
import {ref} from 'vue'
import BaseForm from '@/components/common/BaseForm.vue'
// import DraftMergeConflict from '@/components/common/DraftMergeConflict.vue'
import DiffThreeWays from '@/components/common/DiffThreeWays.vue'

defineProps({
  params: {
    type: Object,
    default: () => ({})
  }
})

const visible = ref(false)
const openForm = ref(null)

const close = () => {
  openForm.value.close()
}

const save = async () => {
  close()
}

const segments = [
  // ================= HEADER =================
  {
    type: 'common',
    text: [
      "package com.example.service;",
      "",
      "import java.util.*;",
      "import java.util.stream.Collectors;",
      "import org.slf4j.Logger;",
      "import org.slf4j.LoggerFactory;",
      "import org.springframework.transaction.annotation.Transactional;",
      ""
    ]
  },

  // ================= EDIT LEFT =================
  {
    type: 'edit-left',
    local: [
      "// [LOCAL] Logger initialized",
      "private static final Logger log = LoggerFactory.getLogger(UserService.class);"
    ],
    remote: [
      "// [REMOTE] Logger not used",
      "private static final Logger log = null;"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "public class UserService {",
      "",
      "    private final UserRepository repo;",
      "    private final NotificationService notifier;",
      ""
    ]
  },

  // ================= CONFLICT 1 =================
  {
    type: 'conflict',
    local: [
      "    // Local: Constructor Injection",
      "    public UserService(UserRepository repo, NotificationService notifier) {",
      "        this.repo = repo;",
      "        this.notifier = notifier;",
      "    }"
    ],
    remote: [
      "    // Remote: Manual instantiation",
      "    public UserService(UserRepository repo) {",
      "        this.repo = repo;",
      "        this.notifier = new EmailService();",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "    // ================= QUERY =================",
      ""
    ]
  },

  // ================= AUTO MERGE =================
  {
    type: 'auto-merge-right',
    text: [
      "    public Optional<User> findById(String id) {",
      "        return repo.findById(id);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [""]
  },

  // ================= EDIT RIGHT =================
  {
    type: 'edit-right',
    local: [
      "    public List<User> findAll() {",
      "        return repo.findAll();",
      "    }"
    ],
    remote: [
      "    public List<User> findAll() {",
      "        return repo.findAllActive();",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [""]
  },

  // ================= CONFLICT 2 =================
  {
    type: 'conflict',
    local: [
      "    public User create(User user) {",
      "        validate(user);",
      "        return repo.save(user);",
      "    }"
    ],
    remote: [
      "    public User create(User user) {",
      "        if (repo.existsByEmail(user.getEmail())) {",
      "            throw new DuplicateUserException();",
      "        }",
      "        return repo.save(user);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "    // ================= UPDATE =================",
      ""
    ]
  },

  // ================= CONFLICT 3 =================
  {
    type: 'conflict',
    local: [
      "    @Transactional",
      "    public User update(String id, User payload) {",
      "        User u = repo.findById(id).orElseThrow();",
      "        u.setName(payload.getName());",
      "        return repo.save(u);",
      "    }"
    ],
    remote: [
      "    public User update(String id, User payload) {",
      "        return repo.updatePartial(id, payload);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [""]
  },

  // ================= EDIT LEFT =================
  {
    type: 'edit-left',
    local: [
      "    public void notifyUser(User user) {",
      "        log.info(\"Notify user {}\", user.getEmail());",
      "        notifier.send(user);",
      "    }"
    ],
    remote: [
      "    public void notifyUser(User user) {",
      "        notifier.send(user);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "    // ================= DELETE =================",
      ""
    ]
  },

  // ================= EDIT RIGHT =================
  {
    type: 'edit-right',
    local: [
      "    public void delete(String id) {",
      "        repo.deleteById(id);",
      "    }"
    ],
    remote: [
      "    public void delete(String id) {",
      "        repo.softDelete(id, true);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [""]
  },

  // ================= CONFLICT 4 =================
  {
    type: 'conflict',
    local: [
      "    public void deleteUser(String id) {",
      "        repo.deleteById(id);",
      "    }"
    ],
    remote: [
      "    public void deleteUser(String id) {",
      "        repo.softDelete(id);",
      "        notifier.sendDeletionNotice(id);",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "    // ================= UTIL =================",
      ""
    ]
  },

  // ================= AUTO MERGE =================
  {
    type: 'auto-merge-right',
    text: [
      "    private void validate(User user) {",
      "        if (user.getEmail() == null) {",
      "            throw new IllegalArgumentException(\"email required\");",
      "        }",
      "    }"
    ]
  },

  {
    type: 'common',
    text: [
      "",
      "}"
    ]
  }
];

</script>

<style scoped>
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

.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 10px var(--p-selection);
}
</style>
