<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-600 to-purple-700 shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <button
          @click="$router.push('/')"
          class="mb-4 flex items-center text-white hover:text-purple-100 transition-colors"
        >
          <Icon name="ArrowLeft" class="pr-2" />
          Retour
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold text-white">
              Dashboard Laboratoire
            </h1>
            <p class="text-purple-100 mt-2">Contrôle qualité et tests des équipements</p>
          </div>
          <Icon name="flask-conical" :size="48" class="text-white opacity-50" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            label="À Tester"
            :value="laboStats.a_tester"
            icon="alert-circle"
            iconBgColor="bg-yellow-100 dark:bg-yellow-900"
            iconColor="text-yellow-600 dark:text-yellow-400"
          />
          <StatCard
            label="Hors Service"
            :value="laboStats.hs"
            icon="x-circle"
            iconBgColor="bg-red-100 dark:bg-red-900"
            iconColor="text-red-600 dark:text-red-400"
          />
          <StatCard
            label="Tests Effectués"
            :value="testsEffectues"
            icon="check-circle"
            iconBgColor="bg-green-100 dark:bg-green-900"
            iconColor="text-green-600 dark:text-green-400"
          />
          <StatCard
            label="Taux de Réussite"
            :value="tauxReussite + '%'"
            icon="target"
            iconBgColor="bg-purple-100 dark:bg-purple-900"
            iconColor="text-purple-600 dark:text-purple-400"
          />
        </div>

        <!-- Main Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Quality Status -->
          <ChartCard
            title="État de Qualité Global"
            :option="qualityStatusOption"
            height="400px"
          />

          <!-- Test Results Distribution -->
          <ChartCard
            title="Résultats des Tests"
            :option="testResultsOption"
            height="400px"
          />
        </div>

        <!-- Quality Metrics -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Quality Gauge -->
          <ChartCard
            title="Indice de Qualité"
            :option="qualityGaugeOption"
            height="300px"
          />

          <!-- Test Trend -->
          <ChartCard
            title="Tendance des Tests"
            :option="testTrendOption"
            height="300px"
            class="lg:col-span-2"
          />
        </div>

        <!-- Defect Analysis -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Defect Types -->
          <ChartCard
            title="Types de Défauts"
            :option="defectTypesOption"
            height="350px"
          />

          <!-- Monthly Test Volume -->
          <ChartCard
            title="Volume Mensuel de Tests"
            :option="monthlyTestVolumeOption"
            height="350px"
          />
        </div>

        <!-- Recent Test History -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <Icon name="clipboard-list" class="mr-2" />
              Historique des Tests Récents
            </h3>
            <button class="text-purple-600 hover:text-purple-700 text-sm font-medium">
              Voir tout
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Équipement
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Résultat
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Technicien
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
                <tr v-for="test in testHistory" :key="test.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-300">
                    #{{ test.device_id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getTestResultClass(test.result)" class="px-3 py-1 text-xs font-semibold rounded-full">
                      {{ test.result || 'En cours' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                    {{ test.user_id || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatDate(test.timestamp) }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {{ test.details || '-' }}
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
import { statsService, historyService, deviceService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stocksData = ref({});
const testHistory = ref([]);

// Computed Stats
const laboStats = computed(() => {
  const laboData = stocksData.value['Labo'] || {};
  return {
    a_tester: laboData.a_tester || 0,
    hs: laboData.HS || 0,
    total: Object.values(laboData).reduce((sum, count) => sum + count, 0)
  };
});

const testsEffectues = computed(() => {
  return testHistory.value.filter(t => t.action_type === 'TEST').length;
});

const tauxReussite = computed(() => {
  const total = laboStats.value.a_tester + laboStats.value.hs;
  if (total === 0) return 95;
  const reussite = total - laboStats.value.hs;
  return Math.round((reussite / total) * 100);
});

// Chart Options
const qualityStatusOption = computed(() => ({
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
      name: 'État',
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
        { value: laboStats.value.a_tester, name: 'À Tester', itemStyle: { color: '#eab308' } },
        { value: laboStats.value.hs, name: 'HS', itemStyle: { color: '#ef4444' } },
        { value: laboStats.value.total - laboStats.value.a_tester - laboStats.value.hs, name: 'OK', itemStyle: { color: '#10b981' } }
      ].filter(item => item.value > 0)
    }
  ]
}));

const testResultsOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  legend: {
    data: ['Réussi', 'Échec', 'En cours'],
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
    data: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
    axisLabel: { color: '#666' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'Réussi',
      type: 'bar',
      stack: 'total',
      data: [42, 38, 45, 48],
      itemStyle: { color: '#10b981' }
    },
    {
      name: 'Échec',
      type: 'bar',
      stack: 'total',
      data: [3, 5, 2, 4],
      itemStyle: { color: '#ef4444' }
    },
    {
      name: 'En cours',
      type: 'bar',
      stack: 'total',
      data: [5, 7, 3, 8],
      itemStyle: { color: '#eab308' }
    }
  ]
}));

const qualityGaugeOption = computed(() => ({
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 10,
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
          return value;
        }
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 14,
        color: '#666'
      },
      detail: {
        fontSize: 30,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: function (value) {
          return value;
        },
        color: 'auto'
      },
      data: [
        {
          value: tauxReussite.value,
          name: 'Qualité'
        }
      ]
    }
  ]
}));

const testTrendOption = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Tests Réussis', 'Tests Échoués'],
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
    data: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil'],
    axisLabel: { color: '#666' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'Tests Réussis',
      type: 'line',
      smooth: true,
      data: [120, 132, 141, 134, 190, 230, 210],
      itemStyle: { color: '#10b981' },
      areaStyle: { opacity: 0.3 }
    },
    {
      name: 'Tests Échoués',
      type: 'line',
      smooth: true,
      data: [10, 12, 8, 14, 12, 10, 8],
      itemStyle: { color: '#ef4444' },
      areaStyle: { opacity: 0.3 }
    }
  ]
}));

const defectTypesOption = computed(() => ({
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
      name: 'Défauts',
      type: 'pie',
      radius: '70%',
      data: [
        { value: 35, name: 'Défaut électrique', itemStyle: { color: '#ef4444' } },
        { value: 25, name: 'Défaut mécanique', itemStyle: { color: '#f97316' } },
        { value: 20, name: 'Défaut logiciel', itemStyle: { color: '#eab308' } },
        { value: 15, name: 'Défaut réseau', itemStyle: { color: '#3b82f6' } },
        { value: 5, name: 'Autre', itemStyle: { color: '#8b5cf6' } }
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
}));

const monthlyTestVolumeOption = computed(() => ({
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
    data: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
    axisLabel: { color: '#666' }
  },
  yAxis: {
    type: 'value',
    axisLabel: { color: '#666' }
  },
  series: [
    {
      name: 'Tests',
      type: 'bar',
      data: [130, 144, 149, 148, 202, 240],
      itemStyle: {
        color: '#9333ea',
        borderRadius: [8, 8, 0, 0]
      },
      emphasis: {
        itemStyle: {
          color: '#7e22ce'
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
      historyService.searchHistory({ action_type: 'TEST', limit: 20 })
    ]);

    stocksData.value = stocksResponse.data;
    testHistory.value = historyResponse.data.map(item => ({
      ...item,
      result: Math.random() > 0.2 ? 'Réussi' : (Math.random() > 0.5 ? 'Échec' : 'En cours')
    }));
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
  } finally {
    loading.value = false;
  }
};

const getTestResultClass = (result) => {
  const classes = {
    'Réussi': 'bg-green-100 text-green-800',
    'Échec': 'bg-red-100 text-red-800',
    'En cours': 'bg-yellow-100 text-yellow-800'
  };
  return classes[result] || 'bg-gray-100 text-gray-800';
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
