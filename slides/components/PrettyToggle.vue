<script setup lang="ts">
import { pretty } from './pretty'
</script>

<template>
  <label class="pt">
    <input v-model="pretty" type="checkbox" />
    <span><slot>I installed jq and glow</slot></span>
  </label>
</template>

<style scoped>
.pt { display: inline-flex; align-items: center; gap: 0.6rem; cursor: pointer; font-weight: 600; }
.pt input { width: 1.1rem; height: 1.1rem; accent-color: var(--sapphire); cursor: pointer; }
</style>
