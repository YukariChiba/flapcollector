<template>
  <div class="d-flex flex-column gap-3">
    <!-- JSON Links -->
    <BCard no-body class="mb-0">
      <div class="card-header"><IBiFiletypeJson class="me-2" />API Usage</div>
      <div class="card-body p-3">
        <p class="small text-muted mb-2">
          Use the dynamic API to fetch ROA data with custom thresholds.
        </p>
        <div class="code-box p-2 mb-2" style="font-size: 0.75rem">
          <pre class="m-0 text-wrap" style="word-break: break-all">{{ apiUrl() }}</pre>
        </div>
        <div class="d-flex gap-2 justify-content-between small text-muted">
          <span>Default: <code>vote=1, rate=0</code></span>
        </div>
      </div>
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
          >
            {{ host }}
          </span>
          <span>
            <span v-if="props.meta[host]" class="badge rounded-pill bg-secondary me-2">{{
              props.meta[host]?.mode
            }}</span>
            <IBiCheck2 class="text-success" v-if="status[host]" />
            <IBiExclamationTriangle class="text-warning" v-else />
          </span>
        </BListGroupItem>
      </BListGroup>
    </BCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BCard, BListGroup, BListGroupItem, BBadge } from 'bootstrap-vue-next'
import type { ServerStatus, ServerMeta } from '../types'

const props = defineProps<{ status: ServerStatus; meta: ServerMeta }>()

const sortedHosts = computed(() => Object.keys(props.status).sort())

const apiUrl = () => `${window.location.origin}/roa.json?vote=<min_vote>&rate=<min_rate>`
</script>
