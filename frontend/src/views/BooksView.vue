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
