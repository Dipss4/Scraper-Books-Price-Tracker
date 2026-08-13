"""
Run from project root: python setup_frontend.py
Creates all frontend files with correct content.
"""
import os

BASE = "frontend/src"

files = {}

# ─────────────────────────────────────────────
files["style.css"] = """\
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    background-color: #020617;
    color: #f1f5f9;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }

  ::-webkit-scrollbar {
    width: 6px;
  }
  ::-webkit-scrollbar-track {
    background: #0f172a;
  }
  ::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 9999px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #475569;
  }
}

@layer components {
  .card {
    @apply rounded-xl overflow-hidden transition-all duration-300;
    background-color: #172033;
    border: 1px solid #1e293b;
  }
  .card:hover {
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.06);
  }

  .btn-primary {
    @apply text-white font-medium px-4 py-2 rounded-lg
           transition-all duration-200 active:scale-[0.97]
           disabled:opacity-50 disabled:cursor-not-allowed
           focus:outline-none focus:ring-2 focus:ring-blue-500/40;
    background-color: #2563eb;
  }
  .btn-primary:hover:not(:disabled) {
    background-color: #1d4ed8;
  }

  .btn-secondary {
    @apply font-medium px-4 py-2 rounded-lg
           transition-all duration-200 active:scale-[0.97]
           focus:outline-none;
    background-color: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
  }
  .btn-secondary:hover {
    background-color: #334155;
    color: #e2e8f0;
  }

  .btn-danger {
    @apply text-white font-medium px-4 py-2 rounded-lg
           transition-all duration-200 active:scale-[0.97]
           focus:outline-none focus:ring-2 focus:ring-red-500/40;
    background-color: #dc2626;
  }
  .btn-danger:hover {
    background-color: #b91c1c;
  }

  .btn-ghost {
    @apply px-3 py-2 rounded-lg transition-all duration-200
           focus:outline-none;
    color: #94a3b8;
  }
  .btn-ghost:hover {
    background-color: #1e293b;
    color: #e2e8f0;
  }

  .input-field {
    @apply rounded-lg px-4 py-2.5 w-full
           transition-all duration-200
           focus:outline-none;
    background-color: #0f172a;
    border: 1px solid #1e293b;
    color: #f1f5f9;
  }
  .input-field::placeholder {
    color: #475569;
  }
  .input-field:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
  }

  .badge {
    @apply inline-flex items-center px-2.5 py-0.5
           rounded-full text-xs font-medium tracking-wide;
  }
  .badge-green {
    @apply badge;
    background-color: rgba(34, 197, 94, 0.12);
    color: #86efac;
  }
  .badge-red {
    @apply badge;
    background-color: rgba(239, 68, 68, 0.12);
    color: #fca5a5;
  }
  .badge-yellow {
    @apply badge;
    background-color: rgba(234, 179, 8, 0.12);
    color: #fde047;
  }
  .badge-blue {
    @apply badge;
    background-color: rgba(59, 130, 246, 0.12);
    color: #93c5fd;
  }
  .badge-neutral {
    @apply badge;
    background-color: rgba(100, 116, 139, 0.12);
    color: #94a3b8;
  }

  .section-title {
    @apply text-xl font-semibold text-white tracking-tight;
  }

  .label-sm {
    @apply text-xs text-gray-500 uppercase tracking-wider font-medium;
  }

  .divider {
    border-color: #1e293b;
  }
}
"""

# ─────────────────────────────────────────────
files["main.js"] = """\
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
"""

# ─────────────────────────────────────────────
files["App.vue"] = """\
<template>
  <div class="min-h-screen flex flex-col" style="background-color: #020617;">
    <Navbar />
    <main class="flex-1 container mx-auto px-4 sm:px-6 py-8 max-w-7xl">
      <router-view v-slot="{ Component }">
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-1"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150"
          leave-to-class="opacity-0"
          mode="out-in"
        >
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>
    <footer class="text-center py-6 text-xs text-gray-600 border-t divider">
      Books Price Tracker &middot; Portfolio Project
    </footer>
    <Toast />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Toast from './components/Toast.vue'
</script>
"""

# ─────────────────────────────────────────────
files["api/index.js"] = """\
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export const getBooks              = (params = {}) => api.get('/books', { params })
export const getBook               = (id)          => api.get(`/books/${id}`)

export const getWatchlist          = ()            => api.get('/watchlist')
export const addToWatchlist        = (data)        => api.post('/watchlist', data)
export const updateWatchlistItem   = (i, data)     => api.put(`/watchlist/${i}`, data)
export const removeFromWatchlist   = (i)           => api.delete(`/watchlist/${i}`)

export const getHistory            = (title)       => api.get(`/history/${encodeURIComponent(title)}`)
export const getAllHistory          = ()            => api.get('/history')

export const triggerScrape         = ()            => api.post('/scrape')
export const getScrapeStatus       = ()            => api.get('/scrape/status')
export const runPipeline           = ()            => api.post('/pipeline')

export const getStats              = ()            => api.get('/stats')

export default api
"""

# ─────────────────────────────────────────────
files["router/index.js"] = """\
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
  },
  {
    path: '/books',
    name: 'books',
    component: () => import('../views/BooksView.vue'),
  },
  {
    path: '/watchlist',
    name: 'watchlist',
    component: () => import('../views/WatchlistView.vue'),
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('../views/HistoryView.vue'),
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
"""

# ─────────────────────────────────────────────
files["stores/toast.js"] = """\
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let nextId = 0

  function show(message, type = 'info', duration = 4000) {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter((t) => t.id !== id)
    }, duration)
  }

  return {
    toasts,
    success: (m) => show(m, 'success'),
    error:   (m) => show(m, 'error'),
    info:    (m) => show(m, 'info'),
    warning: (m) => show(m, 'warning'),
  }
})
"""

# ─────────────────────────────────────────────
files["stores/books.js"] = """\
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getBooks } from '../api/index.js'

export const useBooksStore = defineStore('books', () => {
  const books        = ref([])
  const total        = ref(0)
  const page         = ref(1)
  const pages        = ref(1)
  const loading      = ref(false)
  const search       = ref('')
  const sort         = ref('')
  const ratingFilter = ref(null)

  async function fetchBooks(params = {}) {
    loading.value = true
    try {
      const res = await getBooks({
        search: search.value || undefined,
        sort:   sort.value   || undefined,
        rating: ratingFilter.value || undefined,
        page:   page.value,
        limit:  20,
        ...params,
      })
      books.value = res.data.books
      total.value = res.data.total
      pages.value = res.data.pages
    } catch (e) {
      console.error('Failed to fetch books:', e)
    } finally {
      loading.value = false
    }
  }

  return { books, total, page, pages, loading, search, sort, ratingFilter, fetchBooks }
})
"""

# ─────────────────────────────────────────────
files["stores/watchlist.js"] = """\
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getWatchlist, addToWatchlist,
  updateWatchlistItem, removeFromWatchlist,
} from '../api/index.js'
import { useToastStore } from './toast.js'

export const useWatchlistStore = defineStore('watchlist', () => {
  const items   = ref([])
  const loading = ref(false)

  async function fetch() {
    loading.value = true
    try {
      const res = await getWatchlist()
      items.value = res.data.items ?? []
    } catch (e) {
      console.error('Watchlist fetch error:', e)
    } finally {
      loading.value = false
    }
  }

  async function add(title, targetPrice, email) {
    const toast = useToastStore()
    try {
      await addToWatchlist({ title, target_price: targetPrice, email })
      toast.success('Book added to watchlist.')
      await fetch()
    } catch (e) {
      if (e.response?.status === 409) toast.warning('This book is already in your watchlist.')
      else toast.error('Failed to add book to watchlist.')
    }
  }

  async function update(index, data) {
    const toast = useToastStore()
    try {
      await updateWatchlistItem(index, data)
      toast.success('Watchlist entry updated.')
      await fetch()
    } catch {
      useToastStore().error('Failed to update entry.')
    }
  }

  async function remove(index) {
    const toast = useToastStore()
    try {
      await removeFromWatchlist(index)
      toast.success('Book removed from watchlist.')
      await fetch()
    } catch {
      toast.error('Failed to remove book.')
    }
  }

  function isTracked(title) {
    return items.value.some((i) => i.title === title)
  }

  return { items, loading, fetch, add, update, remove, isTracked }
})
"""

# ─────────────────────────────────────────────
files["components/StatusBadge.vue"] = """\
<template>
  <span :class="stock === 'Available' ? 'badge-green' : 'badge-red'">
    {{ stock === 'Available' ? 'In Stock' : 'Out of Stock' }}
  </span>
</template>

<script setup>
defineProps({ stock: String })
</script>
"""

# ─────────────────────────────────────────────
files["components/Toast.vue"] = """\
<template>
  <div class="fixed bottom-4 right-4 z-[200] flex flex-col gap-2 pointer-events-none">
    <TransitionGroup
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-x-full opacity-0"
      enter-to-class="translate-x-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="translate-x-full opacity-0"
    >
      <div
        v-for="t in toasts"
        :key="t.id"
        class="px-4 py-3 rounded-lg shadow-xl border flex items-center gap-3
               min-w-72 pointer-events-auto"
        :style="styleMap[t.type]"
      >
        <span class="flex-shrink-0 w-2 h-2 rounded-full" :style="dotStyle[t.type]" />
        <span class="text-sm font-medium">{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useToastStore } from '../stores/toast.js'

const { toasts } = storeToRefs(useToastStore())

const styleMap = {
  success: 'background:#0d2818; border-color:#166534; color:#bbf7d0;',
  error:   'background:#2a0a0a; border-color:#7f1d1d; color:#fecaca;',
  warning: 'background:#2a1a03; border-color:#78350f; color:#fde68a;',
  info:    'background:#0c1a3a; border-color:#1e3a8a; color:#bfdbfe;',
}

const dotStyle = {
  success: 'background-color:#22c55e;',
  error:   'background-color:#ef4444;',
  warning: 'background-color:#eab308;',
  info:    'background-color:#3b82f6;',
}
</script>
"""

# ─────────────────────────────────────────────
files["components/Navbar.vue"] = """\
<template>
  <nav
    class="sticky top-0 z-50"
    style="background:rgba(15,23,42,0.95); border-bottom:1px solid #1e293b;
           backdrop-filter:blur(12px);"
  >
    <div class="container mx-auto max-w-7xl px-4 sm:px-6">
      <div class="flex items-center justify-between h-16">

        <router-link to="/" class="flex items-center gap-2.5 no-underline">
          <div
            class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold"
            style="background:linear-gradient(135deg,#2563eb,#7c3aed); color:#fff;"
          >PT</div>
          <span class="text-white font-semibold text-base tracking-tight hidden sm:block">
            Price Tracker
          </span>
        </router-link>

        <div class="flex items-center gap-0.5">
          <router-link
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-all
                   duration-200 no-underline"
            :style="isActive(link.to)
              ? 'background:rgba(37,99,235,0.15); color:#93c5fd;'
              : 'color:#64748b;'"
          >
            {{ link.label }}
          </router-link>
        </div>

        <button
          @click="scrape"
          :disabled="scraping"
          class="btn-primary flex items-center gap-2 text-sm"
        >
          <svg
            v-if="scraping"
            class="animate-spin h-3.5 w-3.5"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10"
              stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ scraping ? 'Scraping...' : 'Run Scraper' }}
        </button>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { triggerScrape, getScrapeStatus } from '../api/index.js'
import { useToastStore } from '../stores/toast.js'

const route    = useRoute()
const toast    = useToastStore()
const scraping = ref(false)

const links = [
  { to: '/',          label: 'Dashboard' },
  { to: '/books',     label: 'Catalog'   },
  { to: '/watchlist', label: 'Watchlist' },
  { to: '/history',   label: 'History'   },
]

function isActive(to) {
  if (to === '/') return route.path === '/'
  return route.path.startsWith(to)
}

async function scrape() {
  try {
    scraping.value = true
    await triggerScrape()
    toast.info('Scraper started. This may take a moment.')

    const poll = setInterval(async () => {
      try {
        const res = await getScrapeStatus()
        if (!res.data.running) {
          clearInterval(poll)
          scraping.value = false
          toast.success('Scrape completed successfully.')
        }
      } catch {
        clearInterval(poll)
        scraping.value = false
      }
    }, 2000)
  } catch (e) {
    scraping.value = false
    if (e.response?.status === 409) toast.warning('Scraper is already running.')
    else toast.error('Failed to start scraper.')
  }
}
</script>
"""

# ─────────────────────────────────────────────
files["components/BookCard.vue"] = """\
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
  const raw = (props.book.price || '0').replace(/[\\xc2\\xa3\\u00a3Â£]/g, '').trim()
  const num = parseFloat(raw)
  return isNaN(num) ? props.book.price : `\\u00a3${num.toFixed(2)}`
})
</script>
"""

# ─────────────────────────────────────────────
files["components/BookModal.vue"] = """\
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
  const raw = (props.book?.price || '0').replace(/[\\xc2\\xa3\\u00a3Â£]/g, '').trim()
  const num = parseFloat(raw)
  return isNaN(num) ? props.book?.price : `\\u00a3${num.toFixed(2)}`
})

watch(() => props.book, (b) => {
  if (!b) return
  const raw = (b.price || '0').replace(/[\\xc2\\xa3\\u00a3Â£]/g, '').trim()
  const p = parseFloat(raw)
  targetPrice.value = isNaN(p) ? 0 : Math.max(0, p - 5).toFixed(2)
  email.value = ''
})

async function addTrack() {
  if (!targetPrice.value || !email.value) return
  await watchlist.add(props.book.title, parseFloat(targetPrice.value), email.value)
}
</script>
"""

# ─────────────────────────────────────────────
files["components/WatchlistItem.vue"] = """\
<template>
  <div class="card p-5 space-y-3">
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <h3 class="font-medium text-white text-sm truncate">{{ item.title }}</h3>

        <div class="flex flex-wrap gap-x-6 gap-y-2 mt-3">
          <div>
            <p class="label-sm">Target</p>
            <p class="text-blue-400 font-semibold text-sm tabular-nums mt-0.5">
              \\u00a3{{ item.target_price?.toFixed(2) }}
            </p>
          </div>
          <div>
            <p class="label-sm">Last Price</p>
            <p class="text-green-400 font-semibold text-sm tabular-nums mt-0.5">
              {{ item.last_price ? '\\u00a3' + item.last_price.toFixed(2) : 'N/A' }}
            </p>
          </div>
          <div>
            <p class="label-sm">Alert Email</p>
            <p class="text-gray-400 text-xs mt-0.5 truncate max-w-48">{{ item.email }}</p>
          </div>
        </div>

        <div class="mt-2.5">
          <span v-if="belowTarget" class="badge-green">Target reached</span>
          <span v-else class="badge-neutral">Monitoring</span>
        </div>
      </div>

      <div class="flex items-center gap-1 flex-shrink-0">
        <button @click="showEdit = !showEdit" class="btn-ghost text-sm" title="Edit">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
        <button @click="$emit('history')" class="btn-ghost text-sm" title="View history">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </button>
        <button
          @click="$emit('remove')"
          class="btn-ghost text-sm hover:!text-red-400"
          title="Remove"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </button>
      </div>
    </div>

    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150"
      leave-to-class="opacity-0"
    >
      <div v-if="showEdit" class="pt-4 border-t divider">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="label-sm mb-1.5 block">New Target</label>
            <input
              v-model.number="editTarget"
              type="number"
              step="0.01"
              class="input-field"
            />
          </div>
          <div>
            <label class="label-sm mb-1.5 block">New Email</label>
            <input
              v-model="editEmail"
              type="email"
              class="input-field"
            />
          </div>
          <div class="flex items-end gap-2">
            <button @click="save" class="btn-primary flex-1">Save</button>
            <button @click="showEdit = false" class="btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ item: Object })
const emit  = defineEmits(['update', 'remove', 'history'])

const showEdit   = ref(false)
const editTarget = ref(props.item.target_price)
const editEmail  = ref(props.item.email)

const belowTarget = computed(() =>
  props.item.last_price > 0 && props.item.last_price <= props.item.target_price
)

function save() {
  emit('update', { target_price: editTarget.value, email: editEmail.value })
  showEdit.value = false
}
</script>
"""

# ─────────────────────────────────────────────
files["components/PriceChart.vue"] = """\
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
                \\u00a3{{ e.price.toFixed(2) }}
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
                \\u00a3{{ e.price.toFixed(2) }}
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
"""

# ─────────────────────────────────────────────
files["views/DashboardView.vue"] = """\
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
import { ref, computed, onMounted } from 'vue'
import { getStats, runPipeline, getScrapeStatus } from '../api/index.js'
import { useToastStore } from '../stores/toast.js'

const toast   = useToastStore()
const stats   = ref({})
const running = ref(false)

const statCards = computed(() => [
  { label: 'Total Books',      value: stats.value.total_books ?? 0,           color: 'text-white'      },
  { label: 'Average Price',    value: `\\u00a3${stats.value.avg_price ?? '0.00'}`, color: 'text-green-400'  },
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
"""

# ─────────────────────────────────────────────
files["views/BooksView.vue"] = """\
<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div>
        <h1 class="section-title">Book Catalog</h1>
        <p class="text-sm text-gray-500 mt-1">Browse and track book prices</p>
      </div>
      <div class="flex flex-wrap gap-3 w-full sm:w-auto">
        <input
          v-model="store.search"
          @input="debouncedSearch"
          placeholder="Search by title..."
          class="input-field w-full sm:w-52"
        />
        <select v-model="store.sort" @change="reload" class="input-field w-36">
          <option value="">Sort by</option>
          <option value="price_asc">Price: Low to High</option>
          <option value="price_desc">Price: High to Low</option>
          <option value="rating">Highest Rated</option>
          <option value="title">Alphabetical</option>
        </select>
        <select v-model="ratingVal" @change="filterRating" class="input-field w-32">
          <option :value="null">All Ratings</option>
          <option v-for="r in 5" :key="r" :value="r">{{ r }}+ Stars</option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center py-24">
      <svg class="animate-spin h-8 w-8 text-blue-500" viewBox="0 0 24 24" fill="none">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
    </div>

    <!-- Empty -->
    <div v-else-if="store.books.length === 0" class="text-center py-24">
      <div
        class="w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center"
        style="background:rgba(59,130,246,0.1);"
      >
        <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
        </svg>
      </div>
      <p class="text-lg text-gray-300 font-medium">No books found</p>
      <p class="text-sm text-gray-500 mt-1">
        Run the scraper to populate the catalog.
      </p>
    </div>

    <!-- Grid -->
    <div v-else>
      <p class="text-xs text-gray-500 mb-4 tabular-nums">
        Showing {{ store.books.length }} of {{ store.total }} results
      </p>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <BookCard
          v-for="book in store.books"
          :key="book.id"
          :book="book"
          @select="selected = book"
        />
      </div>

      <!-- Pagination -->
      <div v-if="store.pages > 1" class="flex items-center justify-center gap-1.5 mt-10">
        <button
          @click="goPage(store.page - 1)"
          :disabled="store.page <= 1"
          class="btn-ghost text-sm disabled:opacity-30"
        >Previous</button>

        <template v-for="p in visiblePages" :key="'p' + p">
          <span v-if="p === '...'" class="text-gray-600 px-2 text-sm">...</span>
          <button
            v-else
            @click="goPage(p)"
            class="w-9 h-9 rounded-lg text-sm font-medium transition-all"
            :style="p === store.page
              ? 'background:#2563eb; color:#fff;'
              : 'color:#64748b;'"
          >{{ p }}</button>
        </template>

        <button
          @click="goPage(store.page + 1)"
          :disabled="store.page >= store.pages"
          class="btn-ghost text-sm disabled:opacity-30"
        >Next</button>
      </div>
    </div>

    <BookModal :book="selected" @close="selected = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BookCard  from '../components/BookCard.vue'
import BookModal from '../components/BookModal.vue'
import { useBooksStore }     from '../stores/books.js'
import { useWatchlistStore } from '../stores/watchlist.js'

const store     = useBooksStore()
const watchlist = useWatchlistStore()
const selected  = ref(null)
const ratingVal = ref(null)

let t = null
function debouncedSearch() {
  clearTimeout(t)
  t = setTimeout(() => { store.page = 1; store.fetchBooks() }, 400)
}
function filterRating() { store.ratingFilter = ratingVal.value; store.page = 1; store.fetchBooks() }
function reload()        { store.page = 1; store.fetchBooks() }
function goPage(p) {
  if (p < 1 || p > store.pages) return
  store.page = p
  store.fetchBooks()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const visiblePages = computed(() => {
  const { page: cur, pages: total } = store
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const ps = [1]
  if (cur > 3) ps.push('...')
  for (let i = Math.max(2, cur - 1); i <= Math.min(total - 1, cur + 1); i++) ps.push(i)
  if (cur < total - 2) ps.push('...')
  ps.push(total)
  return ps
})

onMounted(() => { store.fetchBooks(); watchlist.fetch() })
</script>
"""

# ─────────────────────────────────────────────
files["views/WatchlistView.vue"] = """\
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
"""

# ─────────────────────────────────────────────
files["views/HistoryView.vue"] = """\
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
"""

# ─────────────────────────────────────────────
# Write all files
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {full_path}")

print(f"\nAll {len(files)} files created successfully.")
print("Run: cd frontend && npm run dev")