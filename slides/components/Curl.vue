<script setup lang="ts">
import { computed, ref } from 'vue'
import { pretty } from './pretty'

// A curl against the local agent. With jq + glow ticked on the setup slide it
// pipes the answer through them, and the example answer is shown as text.
const props = defineProps<{ prompt: string; answer?: string }>()

const cmd = computed(() =>
  `curl -s localhost:8080/invocations -d '{"prompt": ${JSON.stringify(props.prompt)}}'`
  + (pretty.value ? ' | jq -r .result | glow -' : ''))
const out = computed(() =>
  pretty.value ? props.answer : `{"result": ${JSON.stringify(props.answer)}}`)

const copied = ref(false)
async function copy() {
  await navigator.clipboard.writeText(cmd.value)
  copied.value = true
  setTimeout(() => (copied.value = false), 1200)
}
</script>

<template>
  <div class="curl">
    <pre class="box cmd"><code><span class="kw">curl</span>{{ cmd.slice(4) }}</code><button class="cp" :title="copied ? 'copied' : 'copy'" @click="copy">{{ copied ? '✓' : '⧉' }}</button></pre>
    <pre v-if="answer" class="box out"><code>{{ out }}</code></pre>
  </div>
</template>

<style scoped>
.curl { display: flex; flex-direction: column; gap: 0.35rem; }
.box {
  position: relative; margin: 0;
  background: var(--slidev-code-background, #f5f5f5);
  border-radius: var(--slidev-code-radius, 4px);
  padding: 0.6rem 2.4rem 0.6rem 0.8rem;
  font-family: 'Geist Mono', monospace; font-size: 0.78em; line-height: 1.5;
  white-space: pre-wrap; overflow-wrap: anywhere;
}
.cmd { color: #b56959; }
.kw { color: #59873a; }
.out { color: var(--ink-dim); }
.cp {
  position: absolute; top: 0.4rem; right: 0.5rem;
  border: none; background: none; cursor: pointer;
  color: var(--ink-dim); font-size: 1rem; opacity: 0.6;
}
.cp:hover { opacity: 1; }
</style>
