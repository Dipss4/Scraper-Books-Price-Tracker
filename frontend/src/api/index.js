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
