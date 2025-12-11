<template>
  <button
    class="flex w-full items-center justify-between px-3 py-2 text-sm rounded">
    <span class="flex items-center gap-2">
      <Icon v-if="icon" :name="icon" size="16" />
      <span class="truncate">{{ label }}</span>
    </span>

    <span
      v-if="badge !== null && badge !== undefined"
      class="ml-2 text-xs px-2 py-0.5 rounded bg-gray-700 text-white"
    >
      {{ badge }}
    </span>
  </button>
</template>

<script>
import Icon from "../lucide/Icon.vue";

export default {
  name: 'sidebar-item-default',
  components: { Icon },
  props: {
    label: String,
    icon: String,
    badge: [String, Number],
    active: Boolean,
  },
}
</script>
