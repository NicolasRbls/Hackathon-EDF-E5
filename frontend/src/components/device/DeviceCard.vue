<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden transform transition hover:scale-[1.01] hover:border-edf-orange/30">
    <!-- Header: Status & ID -->
    <div class="p-6 border-b border-gray-100 dark:border-gray-700 flex justify-between items-start">
      <div>
        <p class="text-xs font-bold text-gray-400 tracking-wider uppercase mb-1">Numéro de Série</p>
        <h3 class="text-2xl font-black text-gray-800 dark:text-white font-mono">{{ device.serial_number }}</h3>
      </div>
      <div :class="statusBadgeClass" class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide flex items-center shadow-sm">
        <span class="w-2 h-2 rounded-full mr-2 bg-current animate-pulse"></span>
        {{ device.current_status }}
      </div>
    </div>

    <!-- Body: Details -->
    <div class="p-6 grid grid-cols-2 gap-6">
       <div>
         <div class="flex items-center text-gray-500 mb-1">
            <Icon name="package" size="14" class="mr-2" />
            <span class="text-xs font-medium uppercase">Carton</span>
         </div>
         <p class="font-semibold text-gray-800 dark:text-gray-200">{{ device.num_carton || "" }}</p>
       </div>
       
       <div>
         <div class="flex items-center text-gray-500 mb-1">
            <Icon name="map-pin" size="14" class="mr-2" />
            <span class="text-xs font-medium uppercase">Affectation</span>
         </div>
         <p class="font-semibold text-gray-800 dark:text-gray-200">{{ device.affectation || "Non défini" }}</p>
       </div>

        <div>
         <div class="flex items-center text-gray-500 mb-1">
            <Icon name="user" size="14" class="mr-2" />
            <span class="text-xs font-medium uppercase">Opérateur</span>
         </div>
         <p class="font-semibold text-gray-800 dark:text-gray-200">{{ device.operateur || "" }}</p>
       </div>

       <div>
         <div class="flex items-center text-gray-500 mb-1">
            <Icon name="calendar" size="14" class="mr-2" />
            <span class="text-xs font-medium uppercase">MàJ</span>
         </div>
         <p class="font-semibold text-gray-800 dark:text-gray-200 text-sm">{{ formatDate(device.last_updated) }}</p>
       </div>
    </div>

    <!-- Footer: Actions -->
    <div class="p-4 bg-gray-50 dark:bg-gray-900 flex justify-end space-x-3">
       <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import Icon from "../lucide/Icon.vue";

const props = defineProps({
  device: { type: Object, required: true }
});

const statusBadgeClass = computed(() => {
  const map = {
    'en_stock': 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    'en_livraison': 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    'pose': 'bg-edf-blue-100 text-edf-blue-700 dark:bg-edf-blue-900/30 dark:text-edf-blue-400',
    'HS': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
    'a_tester': 'bg-edf-orange-100 text-edf-orange-700 dark:bg-edf-orange-900/30 dark:text-edf-orange-400'
  };
  return map[props.device.current_status] || 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400';
});

const formatDate = (d) => {
    if(!d) return '-';
    return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
}
</script>
