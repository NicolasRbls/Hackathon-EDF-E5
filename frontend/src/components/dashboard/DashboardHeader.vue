<template>
  <div :class="['shadow-xl', gradientClass]">
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
      <button
        @click="$router.push('/')"
        class="mb-3 sm:mb-4 flex items-center text-white/90 hover:text-white transition-colors text-sm sm:text-base group"
      >
        <Icon name="ArrowLeft" :size="16" class="mr-1.5 sm:mr-2 group-hover:-translate-x-1 transition-transform" />
        Retour
      </button>
      <div class="flex items-center justify-between gap-4">
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white truncate">
            {{ title }}
          </h1>
          <p class="text-white/80 mt-1 sm:mt-2 text-xs sm:text-sm">{{ subtitle }}</p>
        </div>
        <div v-if="icon" class="flex-shrink-0">
          <Icon :name="icon" :size="32" class="text-white/30 sm:w-12 sm:h-12" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from '../lucide/Icon.vue';

defineProps({
  title: {
    type: String,
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
  gradientClass: {
    type: String,
    default: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-black'
  }
});
</script>
