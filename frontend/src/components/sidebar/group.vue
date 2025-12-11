<template>
  <div class="mt-3">
    <button
      class="flex w-full items-center justify-between text-xs font-semibold uppercase text-gray-400"
      @click="open = !open"
    >
      <span>{{ title }}</span>
      <span>{{ open ? '▾' : '▸' }}</span>
    </button>

    <div v-show="open" class="mt-1 space-y-1">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'sidebar-group-default',
  props: {
    title: String,
    defaultOpen: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      open: this.defaultOpen,
    }
  },
}
</script>
