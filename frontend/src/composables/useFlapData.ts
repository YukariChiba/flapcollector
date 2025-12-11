import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { RawData, ProcessedRow, ServerStatus, ServerMeta, FilterState } from '../types'

export function useFlapData() {
  const rawData = ref<ProcessedRow[]>([])
  const serverStatus = ref<ServerStatus>({})
  const serverMeta = ref<ServerMeta>({})
  const loading = ref(false)
  const generatedTime = ref(0)

  const filters = ref<FilterState>({
    votes: 3,
    family: 'all',
  })

  // Format helper
  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds}s`
    const m = Math.floor(seconds / 60)
    if (m < 60) return `${m}m`
    const h = Math.floor(m / 60)
    return `${h}h ${m % 60}m`
  }

  const loadStatus = async () => {
    try {
      const res = await fetch(`/status.json?t=${Date.now()}`)
      const json = await res.json()
      serverStatus.value = json.servers || {}
    } catch (e) {
      console.error(e)
    }
  }

  const loadMeta = async () => {
    try {
      const res = await fetch(`/servers.json?t=${Date.now()}`)
      if (res.ok) serverMeta.value = await res.json()
    } catch (e) {
      console.error(e)
    }
  }

  const loadData = async () => {
    loading.value = true
    try {
      const res = await fetch(`/all.json?t=${Date.now()}`)
      if (!res.ok) throw new Error('Failed to load')
      const json: RawData = await res.json()

      generatedTime.value = json.metadata?.generated || Math.floor(Date.now() / 1000)

      rawData.value = (json.roas || [])
        .map((r) => {
          const votersList = Object.entries(r.metadata || {}).map(([host, stats]) => {
            const firstSeen = stats.FirstSeen || generatedTime.value
            const duration = Math.max(1, generatedTime.value - firstSeen)
            return {
              host,
              totalCount: stats.TotalCount || 0,
              duration,
              rate: (stats.TotalCount || 0) / duration,
            }
          })

          votersList.sort((a, b) => a.host.localeCompare(b.host))

          return {
            prefix: r.prefix,
            count: votersList.length,
            voters: votersList,
          }
        })
        .sort((a, b) => b.count - a.count || a.prefix.localeCompare(b.prefix))
    } catch (e) {
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  const filteredData = computed(() => {
    return rawData.value.filter((item) => {
      if (item.count < filters.value.votes) return false
      const isV6 = item.prefix.includes(':')
      if (filters.value.family === 'v4' && isV6) return false
      if (filters.value.family === 'v6' && !isV6) return false
      return true
    })
  })

  let intervalId: ReturnType<typeof setInterval>
  const init = () => {
    Promise.all([loadStatus(), loadMeta(), loadData()])
    intervalId = setInterval(() => {
      loadStatus()
      loadData()
    }, 30000)
  }

  onMounted(init)
  onUnmounted(() => clearInterval(intervalId))

  return {
    loading,
    filters,
    filteredData,
    serverStatus,
    serverMeta,
    formatDuration,
    refresh: loadData,
  }
}
