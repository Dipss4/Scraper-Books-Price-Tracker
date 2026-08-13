<template>
  <div
    class="card group cursor-pointer select-none"
    @click="$emit('select', book)"
  >
    <div class="relative overflow-hidden" style="aspect-ratio:2/3; background:#0f172a;">
      <img
        :src="book.image"
        :alt="book.title"
        class="w-full h-full object-cover transition-transform duration-500
               group-hover:scale-105"
        loading="lazy"
        @error="(e) => e.target.src = 'https://placehold.co/200x300/0f172a/334155?text=No+Cover'"
      />

      <div class="absolute top-2 left-2">
        <span class="badge-yellow text-[10px] font-semibold">
          {{ stars }} / 5
        </span>
      </div>

      <div v-if="tracked" class="absolute top-2 right-2">
        <span class="badge-blue text-[10px]">Tracked</span>
      </div>

      <div
        class="absolute inset-x-0 bottom-0 h-20 pointer-events-none"
        style="background:linear-gradient(to top, #172033, transparent);"
      />
    </div>

    <div class="p-3 space-y-1.5">
      <h3
        class="text-xs font-medium leading-snug line-clamp-2 text-gray-300
               group-hover:text-blue-400 transition-colors duration-200"
      >
        {{ book.title }}
      </h3>
      <div class="flex items-center justify-between gap-2">
        <span class="text-sm font-bold text-green-400 tabular-nums">
          {{ formattedPrice }}
        </span>
        <StatusBadge :stock="book.inStock" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'
import { useWatchlistStore } from '../stores/watchlist.js'

const props = defineProps({ book: Object })
defineEmits(['select'])

const watchlist = useWatchlistStore()
const tracked   = computed(() => watchlist.isTracked(props.book.title))
const stars     = computed(() => parseInt(props.book.rating) || 0)

const formattedPrice = computed(() => {
  const raw = (props.book.price || '0').replace(/[\xc2\xa3\u00a3Â£]/g, '').trim()
  const num = parseFloat(raw)
  return isNaN(num) ? props.book.price : `\u00a3${num.toFixed(2)}`
})
</script>
