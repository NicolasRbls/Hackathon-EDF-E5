<template>
  <div class="min-h-screen bg-zinc-50 dark:bg-zinc-950">
    <!-- Header -->
    <div class="bg-gradient-to-r from-slate-800 to-slate-900 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          @click="$router.push('/')"
          class="mb-4 flex items-center text-white hover:text-slate-300 transition-colors"
        >
          <Icon name="ArrowLeft" class="pr-2" />
          Retour
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold text-white">
              Dashboard Général
            </h1>
            <p class="text-slate-300 mt-2">Vue d'ensemble du réseau CPL - EDF Corse</p>
          </div>
          <Icon name="gauge" :size="48" class="text-white opacity-50" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-600"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Overview -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <StatCard
            label="Total Réseau"
            :value="totalDevices"
            subtitle="équipements"
            icon="network"
            iconBgColor="bg-slate-100 dark:bg-slate-800"
            iconColor="text-slate-600 dark:text-slate-400"
          />
          <StatCard
            label="Installés"
            :value="stats.pose || 0"
            icon="map-pin"
            iconBgColor="bg-green-100 dark:bg-green-900"
            iconColor="text-green-600 dark:text-green-400"
          />
          <StatCard
            label="En Stock"
            :value="stats.en_stock || 0"
            icon="package"
            iconBgColor="bg-edf-blue-100 dark:bg-edf-blue-900"
            iconColor="text-edf-orange dark:text-blue-400"
          />
          <StatCard
            label="En Transit"
            :value="stats.en_livraison || 0"
            icon="truck"
            iconBgColor="bg-orange-100 dark:bg-orange-900"
            iconColor="text-orange-600 dark:text-orange-400"
          />
          <StatCard
            label="Hors Service"
            :value="stats.HS || 0"
            icon="alert-triangle"
            iconBgColor="bg-red-100 dark:bg-red-900"
            iconColor="text-red-600 dark:text-red-400"
          />
        </div>

        <!-- Map & Quick Stats -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Interactive Map -->
          <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Icon name="map" class="mr-2" />
              Carte du Réseau Corse
            </h3>
            <div class="h-96">
              <map-default></map-default>
            </div>
          </div>

          <!-- Quick Stats Column -->
          <div class="space-y-6">
            <!-- Network Health -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Icon name="heart-pulse" class="mr-2" />
                Santé du Réseau
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Disponibilité</span>
                  <span class="text-lg font-bold text-green-600">{{ networkHealth }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div class="bg-green-600 h-2 rounded-full" :style="{ width: networkHealth + '%' }"></div>
                </div>
                <div class="flex justify-between items-center pt-2">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Opérationnels</span>
                  <span class="text-sm font-semibold text-gray-900 dark:text-white">{{ totalDevices - (stats.HS || 0) }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Défaillants</span>
                  <span class="text-sm font-semibold text-red-600">{{ stats.HS || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- Alerts -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Icon name="bell" class="mr-2" />
                Alertes
              </h3>
              <div class="space-y-3">
                <div v-if="stats.HS > 0" class="flex items-start space-x-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <Icon name="alert-circle" :size="20" class="text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-red-900 dark:text-red-200">{{ stats.HS }} équipement(s) HS</p>
                    <p class="text-xs text-red-700 dark:text-red-300">Intervention requise</p>
                  </div>
                </div>
                <div v-if="stats.a_tester > 0" class="flex items-start space-x-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                  <Icon name="alert-triangle" :size="20" class="text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-yellow-900 dark:text-yellow-200">{{ stats.a_tester }} à tester</p>
                    <p class="text-xs text-yellow-700 dark:text-yellow-300">Tests en attente</p>
                  </div>
                </div>
                <div v-if="!stats.HS && !stats.a_tester" class="flex items-start space-x-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <Icon name="check-circle" :size="20" class="text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-green-900 dark:text-green-200">Tout va bien</p>
                    <p class="text-xs text-green-700 dark:text-green-300">Aucune alerte active</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Regional Distribution -->
          <ChartCard
            title="Distribution Régionale"
            :option="regionalDistributionOption"
            height="350px"
          />

          <!-- Status Overview -->
          <ChartCard
            title="Vue d'Ensemble des Statuts"
            :option="statusOverviewOption"
            height="350px"
          />
        </div>

        <!-- Activity & Trends -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <ChartCard
            title="Activité Hebdomadaire"
            :option="weeklyActivityOption"
            height="300px"
          />
          <ChartCard
            title="Performance Globale"
            :option="performanceGaugeOption"
            height="300px"
          />
          <ChartCard
            title="Indicateurs Clés"
            :option="kpiRadarOption"
            height="300px"
          />
        </div>

        <!-- Recent Activity Table -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Icon name="activity" class="mr-2" />
              Activité Récente du Réseau
            </h3>
            <button class="text-slate-600 hover:text-slate-700 text-sm font-medium">
              Voir tout
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Action
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Équipement
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Utilisateur
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Détails
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="activity in recentActivity" :key="activity.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getActionBadgeClass(activity.action_type)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ activity.action_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-300">
                    #{{ activity.device_id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ activity.user_id || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(activity.timestamp) }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ activity.details || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import Icon from "../../../../components/lucide/Icon.vue";
import MapDefault from "../../../../components/map/map.vue";
import StatCard from "../../../../components/dashboard/StatCard.vue";
import ChartCard from "../../../../components/dashboard/ChartCard.vue";
import { statsService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stocksData = ref({});
const recentActivity = ref([]);

// Computed Stats
const stats = computed(() => {
  const allStats = {};
  Object.values(stocksData.value).forEach(affectation => {
    Object.entries(affectation).forEach(([status, count]) => {
      allStats[status] = (allStats[status] || 0) + count;
    });
  });
  return allStats;
});

const totalDevices = computed(() => {
  return Object.values(stats.value).reduce((sum, count) => sum + count, 0);
});

const networkHealth = computed(() => {
  const total = totalDevices.value || 1;
  const operational = total - (stats.value.HS || 0);
  return Math.round((operational / total) * 100);
});

// Chart Options
const regionalDistributionOption = computed(() => {
  const regions = Object.keys(stocksData.value).filter(key => key !== '[vide]');
  const data = regions.map(region => {
    const regionData = stocksData.value[region];
    return {
      name: region,
      value: Object.values(regionData).reduce((sum, count) => sum + count, 0)
    };
  });

  return {
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
        name: 'Région',
        type: 'pie',
        radius: ['40%', '70%'],
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
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: data
      }
    ]
  };
});

const statusOverviewOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['En Stock', 'En Livraison', 'Posé', 'À Tester', 'HS'],
    axisLabel: {
      rotate: 30,
      color: '#666'
    }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'Équipements',
      type: 'bar',
      data: [
        { value: stats.value.en_stock || 0, itemStyle: { color: '#3b82f6' } },
        { value: stats.value.en_livraison || 0, itemStyle: { color: '#8b5cf6' } },
        { value: stats.value.pose || 0, itemStyle: { color: '#10b981' } },
        { value: stats.value.a_tester || 0, itemStyle: { color: '#eab308' } },
        { value: stats.value.HS || 0, itemStyle: { color: '#ef4444' } }
      ],
      itemStyle: {
        borderRadius: [8, 8, 0, 0]
      }
    }
  ]
}));

const weeklyActivityOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
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
      name: 'Actions',
      type: 'line',
      smooth: true,
      data: [35, 42, 38, 45, 52, 28, 15],
      itemStyle: { color: '#64748b' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(100, 116, 139, 0.3)' },
            { offset: 1, color: 'rgba(100, 116, 139, 0)' }
          ]
        }
      }
    }
  ]
}));

const performanceGaugeOption = computed(() => ({
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 8,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.3, '#ef4444'],
            [0.7, '#eab308'],
            [1, '#10b981']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: { color: 'auto' }
      },
      axisTick: {
        length: 12,
        lineStyle: { color: 'auto', width: 2 }
      },
      splitLine: {
        length: 20,
        lineStyle: { color: 'auto', width: 5 }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 10,
        distance: -60
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 12,
        color: '#666'
      },
      detail: {
        fontSize: 24,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: '{value}%',
        color: 'auto'
      },
      data: [{ value: networkHealth.value, name: 'Performance' }]
    }
  ]
}));

const kpiRadarOption = computed(() => ({
  tooltip: {},
  radar: {
    indicator: [
      { name: 'Disponibilité', max: 100 },
      { name: 'Déploiement', max: 100 },
      { name: 'Qualité', max: 100 },
      { name: 'Maintenance', max: 100 },
      { name: 'Stock', max: 100 }
    ]
  },
  series: [
    {
      name: 'KPI',
      type: 'radar',
      data: [
        {
          value: [networkHealth.value, 75, 88, 92, 70],
          name: 'Réseau EDF',
          itemStyle: { color: '#64748b' },
          areaStyle: { opacity: 0.3 }
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
      statsService.getDashboardHistory(20)
    ]);

    stocksData.value = stocksResponse.data;
    recentActivity.value = historyResponse.data;
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
