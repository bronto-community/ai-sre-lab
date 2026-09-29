<script setup lang="ts">
import QrCode from './QrCode.vue'

// The room's key link, shown only when slides/local.json exists (gitignored):
//   { "secretUrl": "https://…/#s=<passphrase>" }
// The deployed deck has no such file, so this renders nothing there.
const files = import.meta.glob<{ secretUrl?: string }>('../local.json', { eager: true, import: 'default' })
const url = Object.values(files)[0]?.secretUrl
</script>

<template>
  <div v-if="url" class="rk">
    <QrCode :url="url" :size="104" caption="lab keys" />
    <a class="rk-url" :href="url" target="_blank" rel="noopener">{{ url.replace(/^https:\/\//, '') }}</a>
  </div>
</template>

<style scoped>
.rk {
  position: absolute; right: 3.5rem; bottom: 1rem;
  display: flex; flex-direction: column; align-items: center; gap: 0.4rem;
}
.rk-url { font-family: 'Geist Mono', monospace; font-size: 0.62rem; color: var(--ink-dim); border: none; }
</style>
