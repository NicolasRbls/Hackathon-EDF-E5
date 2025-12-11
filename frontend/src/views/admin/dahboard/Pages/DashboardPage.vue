<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-gradient-to-r from-orange-500 to-orange-600 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          @click="$router.push('/')"
          class="mb-4 flex items-center text-white hover:text-orange-100 transition-colors"
        >
          <Icon name="ArrowLeft" class="pr-2" />
          Retour
        </button>
        <h1 class="text-4xl font-bold text-white">
          Dashboard Admin
        </h1>
        <p class="text-orange-100 mt-2">Vue d'ensemble de la gestion des équipements EDF Corse</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            label="Total Équipements"
            :value="totalDevices"
            icon="package"
            iconBgColor="bg-blue-100 dark:bg-blue-900"
            iconColor="text-blue-600 dark:text-blue-400"
          />
          <StatCard
            label="En Stock"
            :value="stats.en_stock || 0"
            icon="box"
            iconBgColor="bg-green-100 dark:bg-green-900"
            iconColor="text-green-600 dark:text-green-400"
          />
          <StatCard
            label="Posés"
            :value="stats.pose || 0"
            icon="check-circle"
            iconBgColor="bg-orange-100 dark:bg-orange-900"
            iconColor="text-orange-600 dark:text-orange-400"
          />
          <StatCard
            label="En Livraison"
            :value="stats.en_livraison || 0"
            icon="truck"
            iconBgColor="bg-purple-100 dark:bg-purple-900"
            iconColor="text-purple-600 dark:text-purple-400"
          />
        </div>

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
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Icon name="activity" class="mr-2" />
              Historique des Actions Récentes
            </h3>
            <button class="text-orange-600 hover:text-orange-700 text-sm font-medium">
              Voir tout
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Type
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Utilisateur
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Équipement
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="item in recentHistory" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getActionBadgeClass(item.action_type)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ item.action_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ item.user_id || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    #{{ item.device_id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(item.timestamp) }}
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
import StatCard from "../../../../components/dashboard/StatCard.vue";
import ChartCard from "../../../../components/dashboard/ChartCard.vue";
import { statsService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stocksData = ref({});
const recentHistory = ref([]);

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
        show: true,
        formatter: '{b}: {c}'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: stats.value.en_stock || 0, name: 'En Stock', itemStyle: { color: '#10b981' } },
        { value: stats.value.en_livraison || 0, name: 'En Livraison', itemStyle: { color: '#8b5cf6' } },
        { value: stats.value.pose || 0, name: 'Posé', itemStyle: { color: '#f97316' } },
        { value: stats.value.a_tester || 0, name: 'À Tester', itemStyle: { color: '#eab308' } },
        { value: stats.value.HS || 0, name: 'HS', itemStyle: { color: '#ef4444' } }
      ].filter(item => item.value > 0)
    }
  ]
}));

const affectationChartOption = computed(() => {
  const affectations = Object.keys(stocksData.value);
  const data = affectations.map(aff => {
    return Object.values(stocksData.value[aff]).reduce((sum, count) => sum + count, 0);
  });

  return {
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
      data: affectations,
      axisTick: { alignWithLabel: true },
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
        barWidth: '60%',
        data: data,
        itemStyle: {
          color: '#f97316',
          borderRadius: [8, 8, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: '#ea580c'
          }
        }
      }
    ]
  };
});

const boDistributionOption = computed(() => {
  const boData = ['BO Nord', 'BO Centre', 'BO Sud'].map(bo => {
    const data = stocksData.value[bo];
    return data ? Object.values(data).reduce((sum, count) => sum + count, 0) : 0;
  });

  return {
    tooltip: {
      trigger: 'item'
    },
    series: [
      {
        name: 'BO',
        type: 'pie',
        radius: '70%',
        data: [
          { value: boData[0], name: 'Nord', itemStyle: { color: '#3b82f6' } },
          { value: boData[1], name: 'Centre', itemStyle: { color: '#f97316' } },
          { value: boData[2], name: 'Sud', itemStyle: { color: '#10b981' } }
        ],
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
});

const availabilityGaugeOption = computed(() => {
  const available = (stats.value.en_stock || 0) + (stats.value.en_livraison || 0);
  const total = totalDevices.value || 1;
  const percentage = ((available / total) * 100).toFixed(1);

  return {
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
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          length: 12,
          lineStyle: {
            color: 'auto',
            width: 2
          }
        },
        splitLine: {
          length: 20,
          lineStyle: {
            color: 'auto',
            width: 5
          }
        },
        axisLabel: {
          color: '#464646',
          fontSize: 12,
          distance: -60,
          formatter: function (value) {
            return value + '%';
          }
        },
        title: {
          offsetCenter: [0, '-20%'],
          fontSize: 14,
          color: '#666'
        },
        detail: {
          fontSize: 24,
          offsetCenter: [0, '0%'],
          valueAnimation: true,
          formatter: function (value) {
            return value + '%';
          },
          color: 'auto'
        },
        data: [
          {
            value: percentage,
            name: 'Disponible'
          }
        ]
      }
    ]
  };
});

const qualityChartOption = computed(() => {
  const ok = totalDevices.value - (stats.value.HS || 0) - (stats.value.a_tester || 0);

  return {
    tooltip: {
      trigger: 'item'
    },
    series: [
      {
        name: 'État',
        type: 'pie',
        radius: '70%',
        data: [
          { value: ok, name: 'Opérationnel', itemStyle: { color: '#10b981' } },
          { value: stats.value.a_tester || 0, name: 'À Tester', itemStyle: { color: '#eab308' } },
          { value: stats.value.HS || 0, name: 'HS', itemStyle: { color: '#ef4444' } }
        ],
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
});

// Methods
const fetchData = async () => {
  try {
    loading.value = true;

    const [stocksResponse, historyResponse] = await Promise.all([
      statsService.getStocks(),
      statsService.getDashboardHistory(15)
    ]);

    stocksData.value = stocksResponse.data;
    recentHistory.value = historyResponse.data;
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
  } finally {
    loading.value = false;
  }
};

const getActionBadgeClass = (actionType) => {
  const classes = {
    'RECEPTION': 'bg-blue-100 text-blue-800',
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

<style scoped>
/* Animation pour le chargement */
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
