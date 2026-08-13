<template>
  <div class="space-y-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="section-title">Dashboard</h1>
        <p class="text-sm text-gray-500 mt-1">Overview of your price tracking system</p>
      </div>
      <button
        @click="runFullPipeline"
        :disabled="running"
        class="btn-primary flex items-center gap-2"
      >
        <svg v-if="running" class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
          <circle class="opacity-25" cx="12" cy="12" r="10"
            stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ running ? 'Running Pipeline...' : 'Run Full Pipeline' }}
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="s in statCards" :key="s.label" class="card p-5 space-y-1">
        <p class="label-sm">{{ s.label }}</p>
        <p class="text-2xl font-bold tabular-nums" :class="s.color">{{ s.value }}</p>
      </div>
    </div>

    <!-- Info row -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="card p-6 space-y-2">
        <p class="label-sm">Last Scrape</p>
        <p class="text-white text-sm">
          {{ stats.last_scrape
              ? new Date(stats.last_scrape).toLocaleString()
              : 'No scrapes recorded. Use the Run Scraper button.' }}
        </p>
      </div>
      <div class="card p-6 space-y-2">
        <p class="label-sm">Alerts Triggered</p>
        <p>
          <span class="text-green-400 text-2xl font-bold tabular-nums">
            {{ stats.below_target ?? 0 }}
          </span>
          <span class="text-gray-500 text-sm ml-2">books below target price</span>
        </p>
      </div>
    </div>

    <!-- Navigation cards -->
    <div>
      <p class="label-sm mb-3">Quick Access</p>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <router-link
          v-for="link in quickLinks"
          :key="link.to"
          :to="link.to"
          class="card p-5 flex items-center gap-4 group no-underline"
        >
          <div
            class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
            :style="link.bg"
          >
            <svg class="w-5 h-5" :style="link.fg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="link.icon"/>
            </svg>
          </div>
          <div>
            <p class="font-medium text-sm text-white group-hover:text-blue-400 transition-colors">
              {{ link.label }}
            </p>
            <p class="text-xs text-gray-500 mt-0.5">{{ link.sub }}</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getScrapeStatus, getStats, runPipeline } from '../api/index.js'
import { useToastStore } from '../stores/toast.js'

const toast   = useToastStore()
const stats   = ref({})
const running = ref(false)

const statCards = computed(() => [
  { label: 'Total Books',      value: stats.value.total_books ?? 0,           color: 'text-white'      },
  { label: 'Average Price',    value: `£${stats.value.avg_price ?? '0.00'}`, color: 'text-green-400'  },
  { label: 'Watchlist Items',  value: stats.value.watchlist_count ?? 0,       color: 'text-blue-400'   },
  { label: 'Price Records',    value: stats.value.tracked_books_history ?? 0, color: 'text-yellow-400' },
])

const quickLinks = computed(() => [
  {
    to: '/books', label: 'Book Catalog',
    sub: `${stats.value.total_books ?? 0} books available`,
    bg: 'background:rgba(59,130,246,0.12);',
    fg: 'color:#60a5fa;',
    icon: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
  },
  {
    to: '/watchlist', label: 'Watchlist',
    sub: `${stats.value.watchlist_count ?? 0} books tracked`,
    bg: 'background:rgba(139,92,246,0.12);',
    fg: 'color:#a78bfa;',
    icon: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
  },
  {
    to: '/history', label: 'Price History',
    sub: `${stats.value.tracked_books_history ?? 0} records`,
    bg: 'background:rgba(34,197,94,0.12);',
    fg: 'color:#86efac;',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
  },
])

async function fetchStats() {
  try { stats.value = (await getStats()).data } catch {}
}

async function runFullPipeline() {
  running.value = true
  try {
    await runPipeline()
    toast.info('Full pipeline started. Scraping, checking prices, and sending alerts.')
    const poll = setInterval(async () => {
      try {
        const res = await getScrapeStatus()
        if (!res.data.running) {
          clearInterval(poll)
          running.value = false
          toast.success('Pipeline completed successfully.')
          fetchStats()
        }
      } catch {
        clearInterval(poll)
        running.value = false
      }
    }, 2000)
  } catch {
    running.value = false
    toast.error('Failed to start pipeline.')
  }
}

onMounted(fetchStats)
</script>
