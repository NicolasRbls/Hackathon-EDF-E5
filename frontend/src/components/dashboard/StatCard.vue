<template>
  <div class="bg-white dark:bg-zinc-900 rounded-xl shadow-sm hover:shadow-md transition-all duration-300 border border-zinc-200 dark:border-zinc-800 p-4 sm:p-6">
    <div class="flex items-start justify-between gap-3">
      <div class="flex-1 min-w-0">
        <p class="text-xs sm:text-sm font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wide truncate">{{ label }}</p>
        <p class="mt-1.5 sm:mt-2 text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-zinc-100 tabular-nums">{{ value }}</p>
        <p v-if="subtitle" class="mt-0.5 sm:mt-1 text-xs sm:text-sm text-zinc-500 dark:text-zinc-400">{{ subtitle }}</p>
      </div>
      <div v-if="icon" :class="['p-2 sm:p-3 rounded-xl flex-shrink-0', iconBgColor]">
        <Icon :name="icon" :size="20" :class="iconColor" class="sm:w-6 sm:h-6" />
      </div>
    </div>
    <div v-if="trend !== null && trend !== undefined" class="mt-3 sm:mt-4 flex items-center text-xs sm:text-sm">
      <Icon
        :name="trend > 0 ? 'trending-up' : 'trending-down'"
        :size="14"
        :class="trend > 0 ? 'text-emerald-500' : 'text-rose-500'"
        class="sm:w-4 sm:h-4"
      />
      <span :class="trend > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'" class="ml-1 font-medium tabular-nums">
        {{ Math.abs(trend) }}%
      </span>
      <span class="ml-1 text-zinc-500 dark:text-zinc-400 hidden sm:inline">vs. période précédente</span>
    </div>
  </div>
</template>

<script setup>
import Icon from '../lucide/Icon.vue';

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  iconBgColor: {
    type: String,
    default: 'bg-blue-100 dark:bg-blue-900'
  },
  iconColor: {
    type: String,
    default: 'text-blue-600 dark:text-blue-400'
  },
  trend: {
    type: Number,
    default: null
  }
});
</script>
