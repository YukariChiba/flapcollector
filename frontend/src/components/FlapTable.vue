<template>
  <BCard no-body class="overflow-hidden">
    <div class="card-header d-flex justify-content-between align-items-center bg-transparent py-3">
      <span>Route Flapping Data</span>
      <BButton size="sm" variant="outline-secondary" @click="$emit('refresh')">
        <IBiArrowClockwise />
      </BButton>
    </div>
    <BTable
      sticky-header="100vh"
      :items="data"
      :fields="fields"
      dark
      hover
      class="mb-0 align-middle"
    >
      <!-- Votes Column -->
      <template #cell(count)="{ item }">
        <div class="text-center">
          <span :class="['count-badge fw-bold', getBadgeClass(item.count)]">{{ item.count }}</span>
        </div>
      </template>

      <!-- Prefix Column -->
      <template #cell(prefix)="{ value }">
        <span class="ps-2 font-monospace text-light fw-bold">{{ value }}</span>
      </template>

      <!-- Voters Column -->
      <template #cell(voters)="{ item }">
        <div class="text-wrap py-2">
          <BTooltip v-for="v in item.voters" :key="v.host">
            <template #target>
              <span
                class="badge voter-badge me-1 mb-1 text-body-secondary"
                @click="openServer(v.host, item.prefix)"
              >
                {{ v.host }}
                <span class="opacity-50 border-start ps-1 ms-1" :class="getChipClass(v.rate)">{{
                  formatRate(v.rate)
                }}</span>
              </span>
            </template>
            <div style="text-align: left">
              <BBadge>Host:</BBadge>
              {{ v.host }}
              <br />
              <BBadge>Total:</BBadge>
              {{ v.totalCount }}
              <br />
              <BBadge>Duration:</BBadge>
              {{ props.formatDuration(v.duration) }}
              <br />
              <BBadge>Rate:</BBadge>
              {{ formatRate(v.rate) }}
            </div>
          </BTooltip>
        </div>
      </template>

      <template #empty>
        <div class="text-center py-5 text-muted">No flapping routes found matching criteria.</div>
      </template>
    </BTable>
  </BCard>
</template>

<script setup lang="ts">
import { BCard, BTable, BButton, BTooltip, BBadge } from 'bootstrap-vue-next'
import type { ProcessedRow, ServerMeta } from '../types'

const props = defineProps<{
  data: ProcessedRow[]
  serverMeta: ServerMeta
  formatDuration: (s: number) => string
}>()

defineEmits(['refresh'])

const fields = [
  { key: 'prefix', label: 'Prefix', thStyle: { width: '30%' } },
  {
    key: 'count',
    label: 'Votes',
    thClass: 'text-center',
    thStyle: { width: '10%' },
    sortable: true,
  },
  { key: 'voters', label: 'Source Servers', thStyle: { width: '60%' } },
]

function getChipClass(rate: number) {
  if (rate >= 7) return 'text-danger-emphasis'
  if (rate >= 5) return 'text-warning-emphasis'
  if (rate >= 3) return 'text-body-emphasis'
  if (rate >= 1) return 'text-body-secondary'
  return 'text-body-tertiary'
}

function getBadgeClass(count: number) {
  if (count >= 7) return 'bg-danger'
  if (count >= 5) return 'bg-warning text-dark'
  if (count >= 3) return 'bg-info text-dark'
  return 'bg-secondary'
}

function formatRate(rate: number) {
  return rate < 0.01 ? '<0.01/s' : `${rate.toFixed(2)}/s`
}

function openServer(host: string, prefix: string) {
  const meta = props.serverMeta[host]
  if (meta?.url) {
    window.open(`${meta.url}/analyze/?prefix=${prefix}`, '_blank')
  }
}
</script>
