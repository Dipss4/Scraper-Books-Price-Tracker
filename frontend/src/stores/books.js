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
