<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-250 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200"
      leave-to-class="opacity-0"
    >
      <div
        v-if="book"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4"
      >
        <div
          class="absolute inset-0"
          style="background:rgba(0,0,0,0.85); backdrop-filter:blur(8px);"
          @click="$emit('close')"
        />

        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
        >
          <div
            v-if="book"
            class="relative rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh]
                   overflow-y-auto flex flex-col md:flex-row"
            style="background:#0f172a; border:1px solid #1e293b;"
          >
            <button
              @click="$emit('close')"
              class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full
                     flex items-center justify-center text-gray-500
                     hover:text-white transition-colors"
              style="background:rgba(15,23,42,0.8);"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>

            <div class="md:w-2/5 flex-shrink-0">
              <img
                :src="book.image"
                :alt="book.title"
                class="w-full h-60 md:h-full object-cover
                       rounded-t-2xl md:rounded-l-2xl md:rounded-tr-none"
                @error="(e) => e.target.src = 'https://placehold.co/300x450/0f172a/334155?text=No+Cover'"
              />
            </div>

            <div class="flex-1 p-6 space-y-5">
              <div>
                <p class="label-sm mb-1">Book Title</p>
                <h2 class="text-lg font-semibold text-white leading-snug">
                  {{ book.title }}
                </h2>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="label-sm mb-1">Current Price</p>
                  <p class="text-2xl font-bold text-green-400 tabular-nums">
                    {{ formattedPrice }}
                  </p>
                </div>
                <div>
                  <p class="label-sm mb-1">Rating</p>
                  <div class="flex items-center gap-1.5">
                    <div class="flex gap-0.5">
                      <div
                        v-for="i in 5"
                        :key="i"
                        class="w-3.5 h-3.5 rounded-sm"
                        :style="i <= stars
                          ? 'background:#eab308;'
                          : 'background:#1e293b;'"
                      />
                    </div>
                    <span class="text-sm text-gray-400">{{ stars }}/5</span>
                  </div>
                </div>
                <div>
                  <p class="label-sm mb-1">Availability</p>
                  <StatusBadge :stock="book.inStock" />
                </div>
                <div>
                  <p class="label-sm mb-1">Tracking Status</p>
                  <span v-if="tracked" class="badge-blue">Tracked</span>
                  <span v-else class="badge-neutral">Not Tracked</span>
                </div>
              </div>

              <a
                :href="book.url"
                target="_blank"
                rel="noopener"
                class="inline-flex items-center gap-1.5 text-sm text-blue-400
                       hover:text-blue-300 transition-colors"
              >
                View source page
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>

              <hr class="divider" />

              <div v-if="!tracked" class="space-y-4">
                <p class="text-sm font-medium text-gray-300">Add to Watchlist</p>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="label-sm mb-1.5 block">Target Price</label>
                    <input
                      v-model.number="targetPrice"
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      class="input-field"
                    />
                  </div>
                  <div>
                    <label class="label-sm mb-1.5 block">Alert Email</label>
                    <input
                      v-model="email"
                      type="email"
                      placeholder="name@example.com"
                      class="input-field"
                    />
                  </div>
                </div>
                <button
                  @click="addTrack"
                  :disabled="!targetPrice || !email"
                  class="btn-primary w-full"
                >
                  Add to Watchlist
                </button>
              </div>

              <div
                v-else
                class="rounded-lg p-4 text-sm"
                style="background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.2);"
              >
                <p class="text-blue-300">
                  This book is already being tracked.
                  <router-link
                    to="/watchlist"
                    class="underline underline-offset-2 ml-1 hover:text-blue-200"
                    @click="$emit('close')"
                  >Manage watchlist</router-link>
                </p>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import StatusBadge from './StatusBadge.vue'
import { useWatchlistStore } from '../stores/watchlist.js'

const props = defineProps({ book: Object })
defineEmits(['close'])

const watchlist    = useWatchlistStore()
const tracked      = computed(() => props.book && watchlist.isTracked(props.book.title))
const targetPrice  = ref(null)
const email        = ref('')
const stars        = computed(() => parseInt(props.book?.rating) || 0)

const formattedPrice = computed(() => {
  const raw = (props.book?.price || '0').replace(/[\xc2\xa3\u00a3Â£]/g, '').trim()
  const num = parseFloat(raw)
  return isNaN(num) ? props.book?.price : `£${num.toFixed(2)}`
})

watch(() => props.book, (b) => {
  if (!b) return
  const raw = (b.price || '0').replace(/[\xc2\xa3\u00a3Â£]/g, '').trim()
  const p = parseFloat(raw)
  targetPrice.value = isNaN(p) ? 0 : Math.max(0, p - 5).toFixed(2)
  email.value = ''
})

async function addTrack() {
  if (!targetPrice.value || !email.value) return
  await watchlist.add(props.book.title, parseFloat(targetPrice.value), email.value)
}
</script>
