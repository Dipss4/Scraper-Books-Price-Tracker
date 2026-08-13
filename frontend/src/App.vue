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
