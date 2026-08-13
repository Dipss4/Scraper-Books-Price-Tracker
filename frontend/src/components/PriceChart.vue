<template>
  <div class="card p-6 space-y-4">
    <h3 class="font-semibold text-white text-sm leading-snug line-clamp-2">
      {{ title }}
    </h3>

    <div v-if="!entries.length" class="text-center py-10 text-gray-500 text-sm">
      No price data recorded yet.
    </div>

    <div v-else class="space-y-5">
      <!-- Bar chart -->
      <div class="flex items-end gap-[3px] h-32 px-1">
        <div
          v-for="(e, i) in normalized"
          :key="i"
          class="flex-1 rounded-t-sm transition-all duration-200 relative group cursor-default"
          style="min-height:3px;"
          :style="{
            height: e.h + '%',
            background: i === normalized.length - 1
              ? 'rgba(34,197,94,0.5)'
              : 'rgba(59,130,246,0.3)',
          }"
        >
          <div
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2
                   opacity-0 group-hover:opacity-100 transition-opacity
                   pointer-events-none z-10 whitespace-nowrap"
          >
            <div
              class="rounded-lg px-3 py-2 text-xs shadow-xl"
              style="background:#020617; border:1px solid #1e293b;"
            >
              <p class="text-green-400 font-semibold tabular-nums">
                \u00a3{{ e.price.toFixed(2) }}
              </p>
              <p class="text-gray-500 mt-0.5">{{ e.date.slice(0, 10) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Data table -->
      <div class="max-h-44 overflow-y-auto">
        <table class="w-full text-xs">
          <thead>
            <tr class="text-gray-500 uppercase border-b divider">
              <th class="py-2 text-left font-medium">Date</th>
              <th class="py-2 text-right font-medium">Price</th>
              <th class="py-2 text-right font-medium">Change</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(e, i) in reversed"
              :key="i"
              class="border-b"
              style="border-color:rgba(30,41,59,0.4);"
            >
              <td class="py-1.5 text-gray-400 tabular-nums">{{ e.date.slice(0, 10) }}</td>
              <td class="py-1.5 text-right text-green-400 font-mono tabular-nums">
                \u00a3{{ e.price.toFixed(2) }}
              </td>
              <td class="py-1.5 text-right font-mono tabular-nums">
                <span
                  v-if="i < reversed.length - 1"
                  :class="delta(i) > 0 ? 'text-red-400' : delta(i) < 0 ? 'text-green-400' : 'text-gray-600'"
                >
                  {{ delta(i) > 0 ? '+' : '' }}{{ delta(i).toFixed(2) }}
                </span>
                <span v-else class="text-gray-700">&mdash;</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title:   String,
  entries: { type: Array, default: () => [] },
})

const normalized = computed(() => {
  if (!props.entries.length) return []
  const prices = props.entries.map((e) => e.price)
  const min = Math.min(...prices)
  const max = Math.max(...prices)
  const range = max - min || 1
  return props.entries.map((e) => ({
    ...e,
    h: ((e.price - min) / range) * 75 + 15,
  }))
})

const reversed = computed(() => [...props.entries].reverse())

function delta(i) {
  const r = reversed.value
  if (i >= r.length - 1) return 0
  return r[i].price - r[i + 1].price
}
</script>
