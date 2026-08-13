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
