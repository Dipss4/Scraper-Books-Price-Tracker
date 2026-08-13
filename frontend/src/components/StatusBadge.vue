<template>
  <span :class="stock === 'Available' ? 'badge-green' : 'badge-red'">
    {{ stock === 'Available' ? 'In Stock' : 'Out of Stock' }}
  </span>
</template>

<script setup>
defineProps({ stock: String })
</script>
