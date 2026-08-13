<template>
  <div class="card p-5 space-y-3">
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <h3 class="font-medium text-white text-sm truncate">{{ item.title }}</h3>

        <div class="flex flex-wrap gap-x-6 gap-y-2 mt-3">
          <div>
            <p class="label-sm">Target</p>
            <p class="text-blue-400 font-semibold text-sm tabular-nums mt-0.5">
              £{{ item.target_price?.toFixed(2) }}
            </p>
          </div>
          <div>
            <p class="label-sm">Last Price</p>
            <p class="text-green-400 font-semibold text-sm tabular-nums mt-0.5">
              {{ item.last_price ? '£' + item.last_price.toFixed(2) : 'N/A' }}
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
import { computed, ref } from 'vue'

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
