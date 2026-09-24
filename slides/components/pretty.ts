import { useStorage } from '@vueuse/core'

// Ticked on the setup slide: the participant has jq + glow installed.
// Per viewer, remembered across reloads.
export const pretty = useStorage('ai-sre-lab:pretty', false)
