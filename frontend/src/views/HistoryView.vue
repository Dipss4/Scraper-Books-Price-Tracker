<template>
  <div class="space-y-6">
    <div>
      <h1 class="section-title">Price History</h1>
      <p class="text-sm text-gray-500 mt-1">Historical price data for tracked books</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-24">
      <svg class="animate-spin h-8 w-8 text-blue-500" viewBox="0 0 24 24" fill="none">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
    </div>

    <!-- Empty -->
    <div v-else-if="!Object.keys(history).length" class="text-center py-24">
      <div
        class="w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center"
        style="background:rgba(34,197,94,0.1);"
      >
        <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
      </div>
      <p class="text-lg text-gray-300 font-medium">No price history</p>
      <p class="text-sm text-gray-500 mt-1">
        Add books to your watchlist and run the pipeline to begin tracking.
      </p>
    </div>

    <!-- Charts -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <PriceChart
        v-for="(entries, title) in history"
        :key="title"
        :title="title"
        :entries="entries"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PriceChart from '../components/PriceChart.vue'
import { getAllHistory } from '../api/index.js'

const history = ref({})
const loading = ref(true)

onMounted(async () => {
  try { history.value = (await getAllHistory()).data }
  catch { console.error('Failed to load history') }
  finally { loading.value = false }
})
</script>
