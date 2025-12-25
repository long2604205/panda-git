from dataclasses import dataclass
from typing import Optional
from constants.constants import RepoStatus

@dataclass
class PrePullResult:
    status: RepoStatus
    current_branch: Optional[str]
    upstream: Optional[str]
    message: Optional[str]