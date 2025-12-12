<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 to-blue-700 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          @click="$router.push('/')"
          class="mb-4 flex items-center text-white hover:text-white transition-colors"
        >
          <Icon name="ArrowLeft" class="pr-2" />
          Retour
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold text-white">
              Dashboard Bureaux d'Opération
            </h1>
            <p class="text-white/90 mt-2">Suivi des équipements par bureau régional</p>
          </div>
          <Icon name="building-2" :size="48" class="text-white opacity-50" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Cards per BO -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            label="BO Nord"
            :value="boStats.nord"
            subtitle="équipements"
            icon="map-pin"
            iconBgColor="bg-edf-blue-100 dark:bg-edf-blue-900"
            iconColor="text-edf-orange dark:text-blue-400"
          />
          <StatCard
            label="BO Centre"
            :value="boStats.centre"
            subtitle="équipements"
            icon="map-pin"
            iconBgColor="bg-orange-100 dark:bg-orange-900"
            iconColor="text-orange-600 dark:text-orange-400"
          />
          <StatCard
            label="BO Sud"
            :value="boStats.sud"
            subtitle="équipements"
            icon="map-pin"
            iconBgColor="bg-green-100 dark:bg-green-900"
            iconColor="text-green-600 dark:text-green-400"
          />
        </div>

        <!-- Main Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- BO Distribution Pie -->
          <ChartCard
            title="Répartition par Bureau"
            :option="boDistributionOption"
            height="400px"
          />

          <!-- Status per BO Stacked Bar -->
          <ChartCard
            title="Statut par Bureau"
            :option="statusPerBoOption"
            height="400px"
          />
        </div>

        <!-- Detailed Status Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- BO Nord Status -->
          <ChartCard
            title="BO Nord - Détails"
            :option="getBoDetailOption('BO Nord', '#3b82f6')"
            height="300px"
          />

          <!-- BO Centre Status -->
          <ChartCard
            title="BO Centre - Détails"
            :option="getBoDetailOption('BO Centre', '#f97316')"
            height="300px"
          />

          <!-- BO Sud Status -->
          <ChartCard
            title="BO Sud - Détails"
            :option="getBoDetailOption('BO Sud', '#10b981')"
            height="300px"
          />
        </div>

        <!-- Recent Activity -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700 mb-8">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Icon name="activity" class="mr-2" />
              Activités Récentes des BO
            </h3>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Bureau
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Action
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Utilisateur
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="item in boHistory" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full bg-edf-blue-100 text-edf-blue-800">
                      {{ item.bureau || 'N/A' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getActionBadgeClass(item.action_type)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ item.action_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ item.user_id || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(item.timestamp) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Activity Trend -->
          <ChartCard
            title="Tendance d'Activité par BO"
            :option="activityTrendOption"
            height="300px"
          />

          <!-- Efficiency Radar -->
          <ChartCard
            title="Vue d'Ensemble des BO"
            :option="boRadarOption"
            height="300px"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import Icon from "../../../../components/lucide/Icon.vue";
import StatCard from "../../../../components/dashboard/StatCard.vue";
import ChartCard from "../../../../components/dashboard/ChartCard.vue";
import { statsService, historyService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stocksData = ref({});
const boHistory = ref([]);

// Computed Stats
const boStats = computed(() => ({
  nord: stocksData.value['BO Nord']
    ? Object.values(stocksData.value['BO Nord']).reduce((sum, count) => sum + count, 0)
    : 0,
  centre: stocksData.value['BO Centre']
    ? Object.values(stocksData.value['BO Centre']).reduce((sum, count) => sum + count, 0)
    : 0,
  sud: stocksData.value['BO Sud']
    ? Object.values(stocksData.value['BO Sud']).reduce((sum, count) => sum + count, 0)
    : 0
}));

// Chart Options
const boDistributionOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} équipements ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    textStyle: { color: '#666' }
  },
  series: [
    {
      name: 'Bureau',
      type: 'pie',
      radius: ['50%', '80%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{c}'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: boStats.value.nord, name: 'BO Nord', itemStyle: { color: '#3b82f6' } },
        { value: boStats.value.centre, name: 'BO Centre', itemStyle: { color: '#f97316' } },
        { value: boStats.value.sud, name: 'BO Sud', itemStyle: { color: '#10b981' } }
      ]
    }
  ]
}));

const statusPerBoOption = computed(() => {
  const bos = ['BO Nord', 'BO Centre', 'BO Sud'];
  const statuses = ['en_stock', 'en_livraison', 'pose', 'a_tester', 'HS'];

  const series = statuses.map(status => ({
    name: status.replace('_', ' ').toUpperCase(),
    type: 'bar',
    stack: 'total',
    emphasis: {
      focus: 'series'
    },
    data: bos.map(bo => stocksData.value[bo]?.[status] || 0)
  }));

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: statuses.map(s => s.replace('_', ' ').toUpperCase()),
      textStyle: { color: '#666' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: bos,
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#666' }
    },
    series: series
  };
});

const getBoDetailOption = (boName, color) => {
  const boData = stocksData.value[boName] || {};

  return {
    tooltip: {
      trigger: 'item'
    },
    series: [
      {
        name: boName,
        type: 'pie',
        radius: '70%',
        data: [
          { value: boData.en_stock || 0, name: 'En Stock', itemStyle: { color: '#10b981' } },
          { value: boData.en_livraison || 0, name: 'En Livraison', itemStyle: { color: '#8b5cf6' } },
          { value: boData.pose || 0, name: 'Posé', itemStyle: { color: '#f97316' } },
          { value: boData.a_tester || 0, name: 'À Tester', itemStyle: { color: '#eab308' } },
          { value: boData.HS || 0, name: 'HS', itemStyle: { color: '#ef4444' } }
        ].filter(item => item.value > 0),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
};

const activityTrendOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['BO Nord', 'BO Centre', 'BO Sud'],
    textStyle: { color: '#666' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
    axisLabel: { color: '#666' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'BO Nord',
      type: 'line',
      smooth: true,
      data: [12, 15, 18, 22, 19, 14, 10],
      itemStyle: { color: '#3b82f6' },
      areaStyle: { opacity: 0.3 }
    },
    {
      name: 'BO Centre',
      type: 'line',
      smooth: true,
      data: [8, 12, 14, 16, 18, 12, 9],
      itemStyle: { color: '#f97316' },
      areaStyle: { opacity: 0.3 }
    },
    {
      name: 'BO Sud',
      type: 'line',
      smooth: true,
      data: [10, 13, 16, 18, 20, 16, 12],
      itemStyle: { color: '#10b981' },
      areaStyle: { opacity: 0.3 }
    }
  ]
}));

const boRadarOption = computed(() => ({
  tooltip: {},
  radar: {
    indicator: [
      { name: 'Stock Total', max: Math.max(boStats.value.nord, boStats.value.centre, boStats.value.sud) || 100 },
      { name: 'Disponibilité', max: 100 },
      { name: 'Posés', max: 100 },
      { name: 'En Livraison', max: 50 },
      { name: 'Qualité', max: 100 }
    ]
  },
  series: [
    {
      name: 'Bureaux',
      type: 'radar',
      data: [
        {
          value: [boStats.value.nord, 85, 65, 30, 90],
          name: 'BO Nord',
          itemStyle: { color: '#3b82f6' }
        },
        {
          value: [boStats.value.centre, 78, 55, 25, 85],
          name: 'BO Centre',
          itemStyle: { color: '#f97316' }
        },
        {
          value: [boStats.value.sud, 92, 70, 35, 95],
          name: 'BO Sud',
          itemStyle: { color: '#10b981' }
        }
      ]
    }
  ]
}));

// Methods
const fetchData = async () => {
  try {
    loading.value = true;

    const [stocksResponse, historyResponse] = await Promise.all([
      statsService.getStocks(),
      historyService.searchHistory({ role: 'bo_nord', limit: 20 })
    ]);

    stocksData.value = stocksResponse.data;
    boHistory.value = historyResponse.data;
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
  } finally {
    loading.value = false;
  }
};

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
onMounted(() => {
  fetchData();
});
</script>
