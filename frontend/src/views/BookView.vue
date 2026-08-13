<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <h1 class="text-2xl font-bold text-white">📖 Books</h1>
      <div class="flex flex-wrap gap-3 w-full sm:w-auto">
        <input
          v-model="store.search"
          @input="debouncedSearch"
          placeholder="Search books..."
          class="input-field sm:w-64"
        />
        <select v-model="store.sort" @change="reload" class="input-field w-40">
          <option value="">Sort by</option>
          <option value="price_asc">Price ↑</option>
          <option value="price_desc">Price ↓</option>
          <option value="rating">Rating ↓</option>
          <option value="title">Title A-Z</option>
        </select>
        <select v-model="ratingVal" @change="filterRating" class="input-field w-36">
          <option :value="null">All ratings</option>
          <option v-for="r in 5" :key="r" :value="r">
            {{ '★'.repeat(r) }}{{ '☆'.repeat(5 - r) }}+
          </option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center py-20">
      <svg class="animate-spin h-10 w-10 text-blue-500" viewBox="0 0 24 24" fill="none">
        <circle class="opacity-25" cx="12" cy="12" r="10"
          stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="!store.loading && store.books.length === 0"
      class="text-center py-20 text-gray-500"
    >
      <p class="text-6xl mb-4">📭</p>
      <p class="text-xl mb-2">No books found.</p>
      <p class="text-sm">Try scraping first using the button in the navbar.</p>
    </div>

    <!-- Books grid -->
    <div v-else>
      <p class="text-sm text-gray-500 mb-4">
        Showing <span class="text-white font-medium">{{ store.books.length }}</span>
        of <span class="text-white font-medium">{{ store.total }}</span> books
      </p>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <BookCard
          v-for="book in store.books"
          :key="book.id"
          :book="book"
          @select="selectedBook = book"
        />
      </div>

      <!-- Pagination -->
      <div v-if="store.pages > 1" class="flex items-center justify-center gap-2 mt-10">
        <button
          @click="goPage(store.page - 1)"
          :disabled="store.page <= 1"
          class="btn-ghost disabled:opacity-30"
        >
          ← Prev
        </button>

        <template v-for="p in visiblePages" :key="p">
          <span v-if="p === '...'" class="text-gray-600 px-1">…</span>
          <button
            v-else
            @click="goPage(p)"
            class="px-3 py-1.5 rounded-lg text-sm transition-all"
            :style="p === store.page
              ? 'background-color:#2563eb; color:#fff;'
              : 'color:#94a3b8;'"
            :class="p !== store.page ? 'hover:bg-gray-700' : ''"
          >
            {{ p }}
          </button>
        </template>

        <button
          @click="goPage(store.page + 1)"
          :disabled="store.page >= store.pages"
          class="btn-ghost disabled:opacity-30"
        >
          Next →
        </button>
      </div>
    </div>

    <!-- Book detail modal -->
    <BookModal :book="selectedBook" @close="selectedBook = null" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BookCard from '../components/BookCard.vue'
import BookModal from '../components/BookModal.vue'
import { useBooksStore } from '../stores/books.js'
import { useWatchlistStore } from '../stores/watchlist.js'

const store = useBooksStore()
const watchlist = useWatchlistStore()
const selectedBook = ref(null)
const ratingVal = ref(null)

let searchTimeout = null
function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    store.page = 1
    store.fetchBooks()
  }, 400)
}

function filterRating() {
  store.ratingFilter = ratingVal.value
  store.page = 1
  store.fetchBooks()
}

function reload() {
  store.page = 1
  store.fetchBooks()
}

function goPage(p) {
  if (p < 1 || p > store.pages) return
  store.page = p
  store.fetchBooks()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const visiblePages = computed(() => {
  const total = store.pages
  const cur = store.page
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)

  const pages = [1]
  if (cur > 3) pages.push('...')
  for (let i = Math.max(2, cur - 1); i <= Math.min(total - 1, cur + 1); i++) {
    pages.push(i)
  }
  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

onMounted(() => {
  store.fetchBooks()
  watchlist.fetch()
})
</script>
