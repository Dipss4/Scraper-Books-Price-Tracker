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
