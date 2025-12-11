<template>
  <BApp>
    <div class="container py-4" style="max-width: 1200px">
      <!-- Header -->
      <header class="d-flex justify-content-between align-items-center mb-4">
        <div class="d-flex align-items-center gap-3">
          <h1 class="h4 mb-0 fw-bold tracking-tight">DN42 Flap Alert</h1>
          <BSpinner v-if="loading" small variant="primary" />
        </div>
        <div class="text-end">
          <BBadge variant="dark" class="border text-muted fw-normal">
            <IBiClockHistory class="me-1" /> Auto-refresh: 30s
          </BBadge>
        </div>
      </header>

      <!-- Controls & Status -->
      <div class="row g-3 mb-4">
        <div class="col-lg-7">
          <FilterControls v-model="filters" />
        </div>
        <div class="col-lg-5">
          <StatusCard :count="filteredData.length" :min-votes="filters.votes" />
        </div>
      </div>

      <!-- Main Table -->
      <FlapTable
        :data="filteredData"
        :server-meta="serverMeta"
        :format-duration="formatDuration"
        @refresh="refresh"
      />

      <!-- Bottom Section -->
      <div class="row g-4 mt-2">
        <div class="col-lg-8">
          <ConfigGuide />
          <div class="card mt-3">
            <div class="card-header"><IBiLink class="me-2" />Useful Links</div>
            <div class="card-body">
              <BButton
                href="https://github.com/Kioubit/FlapAlerted"
                target="_blank"
                variant="outline-primary"
                size="sm"
              >
                FlapAlerted
              </BButton>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <ServerList :status="serverStatus" />
        </div>
      </div>

      <footer class="text-center text-muted small mt-5 mb-3">
        Strategic Explorations Network &copy; {{ year }}
      </footer>
    </div>
  </BApp>
</template>

<script setup lang="ts">
import { useFlapData } from './composables/useFlapData'
import { useColorMode } from 'bootstrap-vue-next'
import { BApp, BSpinner, BBadge, BButton } from 'bootstrap-vue-next'
import FilterControls from './components/FilterControls.vue'
import StatusCard from './components/StatusCard.vue'
import FlapTable from './components/FlapTable.vue'
import ConfigGuide from './components/ConfigGuide.vue'
import ServerList from './components/ServerList.vue'

const { loading, filters, filteredData, serverStatus, serverMeta, refresh, formatDuration } =
  useFlapData()
const year = new Date().getFullYear()

useColorMode().value = 'dark'
</script>
