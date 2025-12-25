from enum import Enum

class PullState(str, Enum):
    IDLE = "IDLE"
    PRECHECK = "PRECHECK"
    FETCHING = "FETCHING"
    ANALYZING = "ANALYZING"
    MERGING = "MERGING"
    REBASING = "REBASING"
    CONFLICT = "CONFLICT"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

class RepoStatus(str, Enum):
    CLEAN = "CLEAN"
    DIRTY = "DIRTY"
    BLOCKED = "BLOCKED" # Đang rebase/merge dở dang

class MergeStrategy(str, Enum):
    DEFAULT = "merge" # Fast-forward if possible, else merge commit
    REBASE = "rebase"