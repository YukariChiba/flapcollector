<template>
  <BCard class="h-100 mb-0 border-primary" style="background: linear-gradient(145deg, #1e2227 0%, #16191d 100%);" body-class="p-3 d-flex align-items-center justify-content-between">
    <div>
      <div class="text-muted small text-uppercase mb-1">Network Status</div>
      <div :class="['status-hero', statusClass]" :title="statusTooltip" :style="statusStyle">
        {{ statusText }}
      </div>
    </div>
    <div class="text-end ps-4 border-start border-secondary">
      <div class="text-muted small">Total Active</div>
      <div class="fs-2 fw-bold text-light">{{ count }}</div>
    </div>
  </BCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BCard } from 'bootstrap-vue-next'

const props = defineProps<{ count: number; minVotes: number }>()

const statusText = computed(() => {
  if (props.minVotes < 3) return 'Unreliable'
  if (props.count < 10) return 'Calm'
  if (props.count < 50) return 'Breezy'
  if (props.count < 200) return 'Windy'
  return 'Stormy'
})

const statusClass = computed(() => {
  if (props.minVotes < 3) return 'text-muted'
  if (props.count < 10) return 'text-success'
  if (props.count < 50) return 'text-info'
  if (props.count < 200) return 'text-warning'
  return 'text-danger'
})

const statusTooltip = computed(() => props.minVotes < 3 ? 'Results may include false positives.' : undefined)
const statusStyle = computed(() => props.minVotes < 3 ? { cursor: 'help', textDecoration: 'underline dotted' } : { fontSize: '1.5rem', fontWeight: '700' })
</script>

<style scoped>
.status-hero { font-size: 1.5rem; font-weight: 700; }
</style>
