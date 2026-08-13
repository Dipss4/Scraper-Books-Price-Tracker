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
