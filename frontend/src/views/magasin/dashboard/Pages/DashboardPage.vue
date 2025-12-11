<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          @click="$router.push('/')"
          class="mb-4 flex items-center text-white hover:text-emerald-100 transition-colors"
        >
          <Icon name="ArrowLeft" class="pr-2" />
          Retour
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold text-white">
              Dashboard Magasin
            </h1>
            <p class="text-emerald-100 mt-2">Gestion d'inventaire et actions terrain</p>
          </div>
          <Icon name="warehouse" :size="48" class="text-white opacity-50" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            label="En Stock"
            :value="magasinStats.en_stock"
            icon="package"
            iconBgColor="bg-emerald-100 dark:bg-emerald-900"
            iconColor="text-emerald-600 dark:text-emerald-400"
          />
          <StatCard
            label="En Livraison"
            :value="magasinStats.en_livraison"
            icon="truck"
            iconBgColor="bg-blue-100 dark:bg-blue-900"
            iconColor="text-blue-600 dark:text-blue-400"
          />
          <StatCard
            label="Réceptions ce mois"
            :value="receptionsMois"
            icon="inbox"
            iconBgColor="bg-purple-100 dark:bg-purple-900"
            iconColor="text-purple-600 dark:text-purple-400"
          />
          <StatCard
            label="Transferts ce mois"
            :value="transfertsMois"
            icon="repeat"
            iconBgColor="bg-orange-100 dark:bg-orange-900"
            iconColor="text-orange-600 dark:text-orange-400"
          />
        </div>

        <!-- Quick Actions Panel -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700 mb-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Icon name="zap" class="mr-2" />
            Actions Rapides
          </h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button class="flex flex-col items-center justify-center p-6 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors border-2 border-emerald-200 dark:border-emerald-800">
              <Icon name="inbox" :size="32" class="text-emerald-600 dark:text-emerald-400 mb-2" />
              <span class="text-sm font-medium text-gray-900 dark:text-white">Réception</span>
            </button>
            <button class="flex flex-col items-center justify-center p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors border-2 border-blue-200 dark:border-blue-800">
              <Icon name="repeat" :size="32" class="text-blue-600 dark:text-blue-400 mb-2" />
              <span class="text-sm font-medium text-gray-900 dark:text-white">Transfert</span>
            </button>
            <button class="flex flex-col items-center justify-center p-6 bg-purple-50 dark:bg-purple-900/20 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors border-2 border-purple-200 dark:border-purple-800">
              <Icon name="scan" :size="32" class="text-purple-600 dark:text-purple-400 mb-2" />
              <span class="text-sm font-medium text-gray-900 dark:text-white">Scanner</span>
            </button>
            <button class="flex flex-col items-center justify-center p-6 bg-orange-50 dark:bg-orange-900/20 rounded-lg hover:bg-orange-100 dark:hover:bg-orange-900/30 transition-colors border-2 border-orange-200 dark:border-orange-800">
              <Icon name="file-down" :size="32" class="text-orange-600 dark:text-orange-400 mb-2" />
              <span class="text-sm font-medium text-gray-900 dark:text-white">Export CSV</span>
            </button>
          </div>
        </div>

        <!-- Main Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Stock Status -->
          <ChartCard
            title="État du Stock"
            :option="stockStatusOption"
            height="400px"
          />

          <!-- Stock Movement Trend -->
          <ChartCard
            title="Mouvements de Stock"
            :option="stockMovementOption"
            height="400px"
          />
        </div>

        <!-- Inventory Details -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Inventory by Status -->
          <ChartCard
            title="Inventaire par Statut"
            :option="inventoryByStatusOption"
            height="300px"
          />

          <!-- Delivery Progress -->
          <ChartCard
            title="Progression des Livraisons"
            :option="deliveryProgressOption"
            height="300px"
          />

          <!-- Monthly Activity -->
          <ChartCard
            title="Activité Mensuelle"
            :option="monthlyActivityOption"
            height="300px"
          />
        </div>

        <!-- Recent Movements -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Icon name="list" class="mr-2" />
              Mouvements Récents
            </h3>
            <button class="text-emerald-600 hover:text-emerald-700 text-sm font-medium">
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
                    Équipement
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Destination
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Technicien
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="movement in recentMovements" :key="movement.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getActionBadgeClass(movement.action_type)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ movement.action_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-300">
                    #{{ movement.device_id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ movement.destination || '-' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ movement.user_id || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(movement.timestamp) }}
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
import { statsService, historyService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stocksData = ref({});
const recentMovements = ref([]);

// Computed Stats
const magasinStats = computed(() => {
  const magasinData = stocksData.value['Magasin'] || {};
  return {
    en_stock: magasinData.en_stock || 0,
    en_livraison: magasinData.en_livraison || 0,
    total: Object.values(magasinData).reduce((sum, count) => sum + count, 0)
  };
});

const receptionsMois = computed(() => {
  return recentMovements.value.filter(m => m.action_type === 'RECEPTION').length;
});

const transfertsMois = computed(() => {
  return recentMovements.value.filter(m => m.action_type === 'TRANSFERT').length;
});

// Chart Options
const stockStatusOption = computed(() => ({
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
      name: 'Stock',
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
        { value: magasinStats.value.en_stock, name: 'En Stock', itemStyle: { color: '#10b981' } },
        { value: magasinStats.value.en_livraison, name: 'En Livraison', itemStyle: { color: '#3b82f6' } }
      ].filter(item => item.value > 0)
    }
  ]
}));

const stockMovementOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Réceptions', 'Transferts', 'Poses'],
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
      name: 'Réceptions',
      type: 'line',
      smooth: true,
      data: [15, 12, 18, 22, 16, 8, 5],
      itemStyle: { color: '#10b981' },
      areaStyle: { opacity: 0.3 }
    },
    {
      name: 'Transferts',
      type: 'line',
      smooth: true,
      data: [8, 10, 12, 15, 18, 14, 9],
      itemStyle: { color: '#3b82f6' },
      areaStyle: { opacity: 0.3 }
    },
    {
      name: 'Poses',
      type: 'line',
      smooth: true,
      data: [5, 8, 10, 12, 14, 16, 12],
      itemStyle: { color: '#f97316' },
      areaStyle: { opacity: 0.3 }
    }
  ]
}));

const inventoryByStatusOption = computed(() => {
  const magasinData = stocksData.value['Magasin'] || {};

  return {
    tooltip: {
      trigger: 'item'
    },
    series: [
      {
        name: 'Statut',
        type: 'pie',
        radius: '70%',
        data: [
          { value: magasinData.en_stock || 0, name: 'En Stock', itemStyle: { color: '#10b981' } },
          { value: magasinData.en_livraison || 0, name: 'En Livraison', itemStyle: { color: '#3b82f6' } },
          { value: magasinData.pose || 0, name: 'Posé', itemStyle: { color: '#f97316' } },
          { value: magasinData.a_tester || 0, name: 'À Tester', itemStyle: { color: '#eab308' } }
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
});

const deliveryProgressOption = computed(() => ({
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
      data: [
        {
          value: 78,
          name: 'Livraisons'
        }
      ]
    }
  ]
}));

const monthlyActivityOption = computed(() => ({
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
    data: ['S1', 'S2', 'S3', 'S4'],
    axisLabel: { color: '#666' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'Actions',
      type: 'bar',
      data: [82, 95, 108, 112],
      itemStyle: {
        color: '#10b981',
        borderRadius: [8, 8, 0, 0]
      },
      emphasis: {
        itemStyle: {
          color: '#059669'
        }
      }
    }
  ]
}));

// Methods
const fetchData = async () => {
  try {
    loading.value = true;

    const [stocksResponse, historyResponse] = await Promise.all([
      statsService.getStocks(),
      historyService.searchHistory({ role: 'magasin', limit: 20 })
    ]);

    stocksData.value = stocksResponse.data;
    recentMovements.value = historyResponse.data.map(item => ({
      ...item,
      destination: ['BO Nord', 'BO Centre', 'BO Sud', 'Labo'][Math.floor(Math.random() * 4)]
    }));
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
  } finally {
    loading.value = false;
  }
};

const getActionBadgeClass = (actionType) => {
  const classes = {
    'RECEPTION': 'bg-emerald-100 text-emerald-800',
    'POSE': 'bg-orange-100 text-orange-800',
    'DEPOSE': 'bg-red-100 text-red-800',
    'TRANSFERT': 'bg-blue-100 text-blue-800',
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
