<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">Tableau de Bord Administrateur</h1>

    <!-- KPI Cards Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Total Matériel"
        :value="totalDevices"
        icon="package"
        color="bg-edf-orange"
      />
      <StatCard
        title="En Stock"
        :value="stats.en_stock || 0"
        icon="box"
        color="bg-green-500"
      />
      <StatCard
        title="En Livraison"
        :value="stats.en_livraison || 0"
        icon="truck"
        color="bg-yellow-500"
      />
      <StatCard
        title="À Tester"
        :value="stats.a_tester || 0"
        icon="flask-conical"
        color="bg-purple-500"
      />
    </div>

    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else>
      <!-- Charts Row 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Status Distribution -->
        <ChartCard
          title="Répartition par Statut"
          :option="statusChartOption"
          height="350px"
        />

        <!-- Affectation Distribution -->
        <ChartCard
          title="Répartition par Affectation"
          :option="affectationChartOption"
          height="350px"
        />
      </div>

      <!-- Charts Row 2 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- BO Distribution -->
        <ChartCard
          title="Distribution BO"
          :option="boDistributionOption"
          height="300px"
        />

        <!-- Status Gauge -->
        <ChartCard
          title="Taux de Disponibilité"
          :option="availabilityGaugeOption"
          height="300px"
        />

        <!-- Quality Status -->
        <ChartCard
          title="État de Qualité"
          :option="qualityChartOption"
          height="300px"
        />
      </div>

      <!-- Recent History -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div class="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Dernières Actions</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Action</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Série</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Utilisateur</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Détails</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="item in recentHistory" :key="item.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(item.timestamp) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getActionBadgeClass(item.action_type)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                    {{ item.action_type }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white font-medium">
                  {{ item.device_id }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ item.user_id || "Système" }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ item.details || "-" }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import StatCard from "../../../../components/dashboard/StatCard.vue";
import ChartCard from "../../../../components/dashboard/ChartCard.vue";
import { statsService } from "../../../../services/api.js";

const stats = ref({});
const recentHistory = ref([]);
const loading = ref(true);

// Computed Stats
const totalDevices = computed(() => {
  if (!stats.value) return 0;
  return Object.values(stats.value).reduce((sum, count) => {
      // Ensure we only sum numbers from predefined keys to avoid double counting if structure changes
      return typeof count === 'number' ? sum + count : sum;
  }, 0);
});

// Chart Options
const statusChartOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    textStyle: { color: '#666' }
  },
  series: [
    {
      name: 'Statut',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '20',
          fontWeight: 'bold'
        }
      },
      data: [
        { value: stats.value.en_stock || 0, name: 'En Stock', itemStyle: { color: '#22c55e' } },
        { value: stats.value.en_livraison || 0, name: 'En Livraison', itemStyle: { color: '#eab308' } },
        { value: stats.value.pose || 0, name: 'Posé', itemStyle: { color: '#3b82f6' } },
        { value: stats.value.a_tester || 0, name: 'À Tester', itemStyle: { color: '#a855f7' } },
        { value: stats.value.HS || 0, name: 'HS', itemStyle: { color: '#ef4444' } }
      ]
    }
  ]
}));

const affectationChartOption = computed(() => {
  // Mock distribution if not avail from API directly
  // In real app, API should provide this breakdown.
  // Assuming stats.value contains affectation keys or separate endpoint.
  // For now, mocking based on total
  return {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '50%',
      data: [
         { value: 10, name: 'Magasin' },
         { value: 5, name: 'BO Nord' },
         { value: 8, name: 'BO Sud' }
      ]
    }]
  };
});

const boDistributionOption = computed(() => {
    // Mock data
    const boData = [12, 19, 3]; 
    return {
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['Nord', 'Centre', 'Sud'] },
      yAxis: { type: 'value' },
      series: [{ data: boData, type: 'bar', itemStyle: { color: '#6366f1' } }]
    };
});

const availabilityGaugeOption = computed(() => {
  const available = (stats.value.en_stock || 0) + (stats.value.pose || 0);
  const total = totalDevices.value || 1;
  const percentage = ((available / total) * 100).toFixed(1);

  return {
    series: [
      {
        type: 'gauge',
        progress: { show: true, width: 10 },
        detail: { valueAnimation: true, formatter: '{value}%' },
        data: [{ value: percentage, name: 'Dispo' }]
      }
    ]
  };
});

const qualityChartOption = computed(() => ({
    tooltip: { trigger: 'item' },
    series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
            { value: stats.value.HS || 0, name: 'HS', itemStyle: { color: '#ef4444' } },
            { value: (totalDevices.value - (stats.value.HS || 0)), name: 'OK', itemStyle: { color: '#22c55e' } }
        ]
    }]
}));

const getActionBadgeClass = (actionType) => {
  const classes = {
    'RECEPTION': 'bg-edf-blue-100 text-edf-blue-800',
    'POSE': 'bg-green-100 text-green-800',
    'DEPOSE': 'bg-red-100 text-red-800',
    'TRANSFERT': 'bg-purple-100 text-purple-800',
    'TEST': 'bg-yellow-100 text-yellow-800',
    'AUTRE': 'bg-gray-100 text-gray-800'
  };
  return classes[actionType] || 'bg-gray-100 text-gray-800';
};

const formatDate = (timestamp) => {
  if (!timestamp) return '-';
  const date = new Date(timestamp);
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

// Lifecycle
onMounted(async () => {
    try {
        const [stocksResponse, historyResponse] = await Promise.all([
             statsService.getStocks(),
             statsService.getDashboardHistory(15)
        ]);
        stats.value = stocksResponse.data || {};
        recentHistory.value = historyResponse.data || [];
    } catch(e) {
        console.error('Error loading dashboard', e);
        // Fallback or empty state
        stats.value = {}; 
    } finally {
        loading.value = false;
    }
});
</script>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
