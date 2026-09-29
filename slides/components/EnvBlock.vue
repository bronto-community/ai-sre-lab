<script setup lang="ts">
import { computed, ref } from 'vue'
import { secrets } from './secrets'

// .env lines, filled in from the room's sealed link when present, else "...".
// `fixed` values are shown as-is (e.g. a region or model to pick yourself).
const props = defineProps<{ names?: string[]; fixed?: Record<string, string> }>()

const lines = computed(() => [
  ...Object.entries(props.fixed ?? {}).map(([k, v]) => `${k}=${v}`),
  ...(props.names ?? []).map((k) => `${k}=${secrets.value[k] ?? '...'}`),
])
const filled = computed(() => (props.names ?? []).some((k) => secrets.value[k]))

const copied = ref(false)
async function copy() {
  await navigator.clipboard.writeText(lines.value.join('\n') + '\n')
  copied.value = true
  setTimeout(() => (copied.value = false), 1200)
}
</script>

<template>
  <pre class="env" :class="{ filled }"><code><template v-for="(l, i) in lines" :key="i"><span class="k">{{ l.slice(0, l.indexOf('=')) }}</span>={{ l.slice(l.indexOf('=') + 1) }}
</template></code><button class="cp" :title="copied ? 'copied' : 'copy'" @click="copy">{{ copied ? '✓' : '⧉' }}</button></pre>
</template>

<style scoped>
.env {
  position: relative; margin: 0;
  background: var(--slidev-code-background, #f5f5f5);
  border-radius: var(--slidev-code-radius, 4px);
  padding: 0.6rem 2.4rem 0.6rem 0.8rem;
  font-family: 'Geist Mono', monospace; font-size: 0.78em; line-height: 1.5;
  white-space: pre-wrap; overflow-wrap: anywhere; color: var(--ink);
}
.env.filled { box-shadow: inset 3px 0 0 var(--mint); }
.k { color: #1e754f; }
.cp {
  position: absolute; top: 0.4rem; right: 0.5rem;
  border: none; background: none; cursor: pointer;
  color: var(--ink-dim); font-size: 1rem; opacity: 0.6;
}
.cp:hover { opacity: 1; }
</style>
