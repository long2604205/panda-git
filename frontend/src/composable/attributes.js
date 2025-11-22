export function getStatusIcon (status) {
  switch (status) {
    case 'clean':
      return 'fa-check-circle'
    case 'dirty':
      return 'fa-exclamation-circle'
    case 'untracked':
      return 'fa-question-circle'
    default:
      return 'fa-circle'
  }
}

export function getStatusColor (status) {
  switch (status) {
    case 'clean':
      return 'text-success'
    case 'dirty':
      return 'text-warning'
    case 'untracked':
      return 'text-secondary'
    default:
      return 'text-muted'
  }
}
