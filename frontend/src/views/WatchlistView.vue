<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="section-title">Watchlist</h1>
        <p class="text-sm text-gray-500 mt-1">Books you are monitoring for price drops</p>
      </div>
      <span class="badge-blue">{{ store.items.length }} items</span>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center py-24">
      <svg class="animate-spin h-8 w-8 text-blue-500" viewBox="0 0 24 24" fill="none">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
    </div>

    <!-- Empty -->
    <div v-else-if="!store.items.length" class="text-center py-24">
      <div
        class="w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center"
        style="background:rgba(139,92,246,0.1);"
      >
        <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
      </div>
      <p class="text-lg text-gray-300 font-medium">No books tracked</p>
      <p class="text-sm text-gray-500 mt-1 mb-4">
        Add books from the catalog to start monitoring prices.
      </p>
      <router-link to="/books" class="btn-primary inline-block">
        Browse Catalog
      </router-link>
    </div>

    <!-- Items -->
    <div v-else class="space-y-3">
      <WatchlistItem
        v-for="(item, i) in store.items"
        :key="item.title"
        :item="item"
        @update="(d) => store.update(i, d)"
        @remove="store.remove(i)"
        @history="openHistory(item.title)"
      />
    </div>

    <!-- History modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div
          v-if="historyTitle"
          class="fixed inset-0 z-[100] flex items-center justify-center p-4"
        >
          <div
            class="absolute inset-0"
            style="background:rgba(0,0,0,0.85); backdrop-filter:blur(8px);"
            @click="historyTitle = null"
          />
          <div class="relative w-full max-w-2xl max-h-[80vh] overflow-y-auto rounded-xl">
            <button
              @click="historyTitle = null"
              class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full
                     flex items-center justify-center text-gray-400 hover:text-white"
              style="background:rgba(0,0,0,0.5);"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
            <PriceChart :title="historyTitle" :entries="historyEntries" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import WatchlistItem from '../components/WatchlistItem.vue'
import PriceChart    from '../components/PriceChart.vue'
import { useWatchlistStore } from '../stores/watchlist.js'
import { getHistory }        from '../api/index.js'

const store          = useWatchlistStore()
const historyTitle   = ref(null)
const historyEntries = ref([])

async function openHistory(title) {
  historyTitle.value = title
  try { historyEntries.value = (await getHistory(title)).data.entries }
  catch { historyEntries.value = [] }
}

onMounted(() => store.fetch())
</script>
