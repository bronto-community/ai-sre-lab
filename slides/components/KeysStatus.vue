<script setup lang="ts">
import { computed } from 'vue'
import { secrets } from './secrets'
const n = computed(() => Object.keys(secrets.value).length)
</script>

<template>
  <span v-if="n" class="ks">🔓 Lab keys loaded: the .env blocks on the next slides are filled in.</span>
</template>

<style scoped>
.ks { display: inline-block; font-size: 0.9rem; color: #1e754f; background: var(--mint-soft); border-radius: 999px; padding: 0.25rem 0.8rem; }
</style>
