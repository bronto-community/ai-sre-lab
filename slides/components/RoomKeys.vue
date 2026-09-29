<script setup lang="ts">
import QrCode from './QrCode.vue'

// The room's key link, shown only when slides/local.json exists (gitignored):
//   { "secretUrl": "https://…/#s=<passphrase>" }
// The deployed deck has no such file and shows a pointer to the room instead.
const files = import.meta.glob<{ secretUrl?: string }>('../local.json', { eager: true, import: 'default' })
const url = Object.values(files)[0]?.secretUrl
</script>

<template>
  <div class="rk">
    <template v-if="url">
      <QrCode :url="url" :size="300" />
      <a class="rk-url" :href="url" target="_blank" rel="noopener">{{ url.replace(/^https:\/\//, '') }}</a>
    </template>
    <div v-else class="rk-none">Ask for the link in the room.</div>
  </div>
</template>

<style scoped>
.rk { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.rk-url { font-family: 'Geist Mono', monospace; font-size: 1rem; color: var(--ink); border: none; }
.rk-none { font-size: 1.3rem; color: var(--ink-dim); }
</style>
