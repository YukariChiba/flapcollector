<template>
  <BCard no-body class="overflow-hidden">
    <div class="card-header d-flex justify-content-between align-items-center bg-transparent py-3">
      <span>Route Flapping Data</span>
      <div class="d-flex align-items-center gap-2">
        <BButtonGroup size="sm">
          <BButton
            size="sm"
            variant="outline-light"
            :active="filterFamily === 'all'"
            @click="$emit('update:filterFamily', 'all')"
          >
            All
          </BButton>
          <BButton
            size="sm"
            variant="outline-light"
            :active="filterFamily === 'v4'"
            @click="$emit('update:filterFamily', 'v4')"
          >
            IPv4
          </BButton>
          <BButton
            size="sm"
            variant="outline-light"
            :active="filterFamily === 'v6'"
            @click="$emit('update:filterFamily', 'v6')"
          >
            IPv6
          </BButton>
        </BButtonGroup>

        <div class="vr h-auto mx-1 opacity-25"></div>

        <BButton size="sm" variant="outline-secondary" @click="$emit('refresh')">
          <IBiArrowClockwise />
        </BButton>
      </div>
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
                <span class="opacity-50 border-start ps-1 ms-1">
                  <span :class="getChipClass(v.current_rate)">{{
                    formatRate(v.current_rate)
                  }}</span>
                  /
                  <span :class="getChipClass(v.average_rate)">{{
                    formatRate(v.average_rate)
                  }}</span>
                </span>
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
              <BBadge>Current Rate:</BBadge>
              {{ formatRate(v.current_rate) }}/s
              <BBadge>Average Rate:</BBadge>
              {{ formatRate(v.average_rate) }}/s
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
import { BCard, BTable, BButton, BTooltip, BBadge, BButtonGroup } from 'bootstrap-vue-next'
import type { ProcessedRow, ServerMeta, FilterState } from '../types'

const props = defineProps<{
  data: ProcessedRow[]
  serverMeta: ServerMeta
  formatDuration: (s: number) => string
  filterFamily: FilterState['family']
}>()

defineEmits<{
  refresh: []
  'update:filterFamily': [value: FilterState['family']]
}>()

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
  return rate < 0.01 ? '<0.01' : `${rate.toFixed(2)}`
}

function openServer(host: string, prefix: string) {
  const meta = props.serverMeta[host]
  if (meta?.url) {
    window.open(`${meta.url}/analyze/?prefix=${prefix}`, '_blank')
  }
}
</script>
