<template>
  <div class="d-flex flex-column gap-3">
    <!-- JSON Links -->
    <BCard no-body class="mb-0">
      <div class="card-header"><IBiFiletypeJson class="me-2" />Raw JSON Files</div>
      <BListGroup flush>
        <BListGroupItem
          v-for="f in files"
          :key="f"
          class="bg-transparent border-secondary border-opacity-25 d-flex justify-content-between align-items-center py-2"
        >
          <span class="font-monospace text-muted small">/{{ f }}</span>
          <BButton variant="link" size="sm" class="text-decoration-none p-0" @click="copyUrl(f)">
            <IBiCopy />
          </BButton>
        </BListGroupItem>
      </BListGroup>
    </BCard>

    <!-- Server Status -->
    <BCard no-body class="mb-0">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span><IBiHddRack class="me-2" />Data Sources</span>
        <BBadge variant="secondary">{{ Object.keys(status).length }}</BBadge>
      </div>
      <BListGroup flush class="small" style="max-height: 800px; overflow-y: auto">
        <BListGroupItem
          v-if="Object.keys(status).length === 0"
          class="bg-transparent text-muted text-center py-3"
        >
          Waiting for data...
        </BListGroupItem>
        <BListGroupItem
          v-for="host in sortedHosts"
          :key="host"
          class="bg-transparent border-secondary border-opacity-25 d-flex justify-content-between align-items-center"
        >
          <span
            :class="['text-truncate', status[host] ? 'text-light' : 'text-muted']"
            style="max-width: 85%"
            >{{ host }}</span
          >
          <IBiCheck2 class="text-success" v-if="status[host]" />
          <IBiExclamationTriangle class="text-warning" v-else />
        </BListGroupItem>
      </BListGroup>
    </BCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BCard, BListGroup, BListGroupItem, BButton, BBadge } from 'bootstrap-vue-next'
import type { ServerStatus } from '../types'

const props = defineProps<{ status: ServerStatus }>()

const files = ['all.json', 'min_2.json', 'min_3.json', 'min_5.json', 'min_7.json', 'min_11.json']
const sortedHosts = computed(() => Object.keys(props.status).sort())

const copyUrl = (f: string) => navigator.clipboard.writeText(`${window.location.origin}/${f}`)
</script>
