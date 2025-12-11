<template>
  <div class="min-h-screen bg-zinc-50 dark:bg-zinc-950">
    <!-- Header -->
    <div class="bg-gradient-to-br from-zinc-800 via-zinc-900 to-zinc-950 shadow-xl">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
        <button @click="$router.push('/')" class="mb-3 sm:mb-4 flex items-center text-zinc-300 hover:text-white transition-colors text-sm sm:text-base group">
          <Icon name="ArrowLeft" :size="16" class="mr-1.5 sm:mr-2 group-hover:-translate-x-1 transition-transform" />
          Retour
        </button>
        <div class="flex items-center justify-between gap-4">
          <div class="flex-1 min-w-0">
            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-white truncate">Réseau CPL</h1>
            <p class="text-zinc-400 mt-1 sm:mt-2 text-xs sm:text-sm">EDF Corse - Vue d'ensemble 3D</p>
          </div>
          <Icon name="globe" :size="32" class="text-zinc-600 sm:w-12 sm:h-12" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8 py-4 sm:py-6 lg:py-8">
      <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-zinc-600 mx-auto"></div>
          <p class="mt-4 text-zinc-500 text-sm">Chargement...</p>
        </div>
      </div>

      <div v-else class="space-y-4 sm:space-y-6">
        <!-- Stats Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
          <StatCard label="Total" :value="totalDevices" subtitle="équipements" icon="network"
            iconBgColor="bg-zinc-100 dark:bg-zinc-800" iconColor="text-zinc-600 dark:text-zinc-400" />
          <StatCard label="Installés" :value="stats.pose || 0" icon="map-pin"
            iconBgColor="bg-zinc-200 dark:bg-zinc-700" iconColor="text-zinc-700 dark:text-zinc-300" />
          <StatCard label="En Stock" :value="stats.en_stock || 0" icon="package"
            iconBgColor="bg-zinc-200 dark:bg-zinc-700" iconColor="text-zinc-700 dark:text-zinc-300" />
          <StatCard label="Transit" :value="stats.en_livraison || 0" icon="truck"
            iconBgColor="bg-zinc-200 dark:bg-zinc-700" iconColor="text-zinc-700 dark:text-zinc-300" />
          <StatCard label="Hors Service" :value="stats.HS || 0" icon="alert-triangle"
            iconBgColor="bg-rose-100 dark:bg-rose-950" iconColor="text-rose-700 dark:text-rose-400" />
        </div>

        <!-- Health Card -->
        <div class="bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800 p-4 sm:p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              <Icon name="activity" :size="20" class="text-zinc-600 dark:text-zinc-400" />
              Santé du Réseau
            </h3>
            <span class="text-2xl sm:text-3xl font-bold tabular-nums text-zinc-900 dark:text-zinc-100">{{ networkHealth }}%</span>
          </div>
          <div class="w-full bg-zinc-200 dark:bg-zinc-800 rounded-full h-3 sm:h-4 overflow-hidden">
            <div class="h-full rounded-full bg-gradient-to-r from-zinc-600 to-zinc-800 dark:from-zinc-400 dark:to-zinc-500 transition-all duration-1000"
              :style="{ width: networkHealth + '%' }"></div>
          </div>
          <div class="grid grid-cols-2 gap-3 sm:gap-4 mt-4">
            <div class="text-center p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-200 dark:border-zinc-700">
              <p class="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400">Opérationnels</p>
              <p class="text-lg sm:text-xl font-bold text-zinc-900 dark:text-zinc-100 mt-1 tabular-nums">{{ totalDevices - (stats.HS || 0) }}</p>
            </div>
            <div class="text-center p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-200 dark:border-zinc-700">
              <p class="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400">Défaillants</p>
              <p class="text-lg sm:text-xl font-bold text-rose-600 dark:text-rose-400 mt-1 tabular-nums">{{ stats.HS || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- Globe 3D - ÉLÉMENT PRINCIPAL EN PLEIN ÉCRAN -->
        <ChartCard
          title="Réseau CPL Corse - Vue Satellite"
          :option="globeOption"
          height="600px"
          titleClass="text-xl sm:text-2xl font-bold text-blue-500 truncate"
        />

        <!-- GL Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <!-- Bar3D -->
          <ChartCard title="Distribution 3D" :option="bar3DOption" height="400px" />

          <!-- Scatter3D -->
          <ChartCard title="Scatter 3D - Répartition Spatiale" :option="scatter3DOption" height="450px" />
        </div>

        <!-- Secondary Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
          <ChartCard title="Répartition" :option="pieOption" height="300px" />
          <ChartCard title="Tendance" :option="lineOption" height="300px" />
          <ChartCard title="Performance" :option="gaugeOption" height="300px" />
        </div>

        <!-- Heatmap -->
        <ChartCard
          title="Heatmap d'Activité"
          :option="heatmapOption"
          height="350px"
          titleClass="text-base sm:text-lg font-semibold text-lime-500 truncate"
        />

        <!-- Activity Table - Improved -->
        <div class="bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800 overflow-hidden">
          <div class="flex items-center justify-between p-4 sm:p-6 border-b border-zinc-200 dark:border-zinc-800">
            <div class="flex items-center gap-2">
              <div class="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
                <Icon name="list" :size="20" class="text-white" />
              </div>
              <div>
                <h3 class="text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100">
                  Activités Récentes
                </h3>
                <p class="text-xs text-zinc-500 dark:text-zinc-400">{{ recentActivity.length }} actions enregistrées</p>
              </div>
            </div>
            <button class="px-3 py-1.5 text-xs sm:text-sm font-medium text-zinc-700 dark:text-zinc-300 bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 rounded-lg transition-colors">
              Voir tout
            </button>
          </div>

          <!-- Empty state -->
          <div v-if="recentActivity.length === 0" class="p-8 text-center">
            <Icon name="inbox" :size="48" class="mx-auto text-zinc-300 dark:text-zinc-700 mb-3" />
            <p class="text-zinc-500 dark:text-zinc-400">Aucune activité récente</p>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-zinc-200 dark:divide-zinc-800">
              <thead class="bg-zinc-50 dark:bg-zinc-900/50">
                <tr>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase tracking-wider">
                    Action
                  </th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase tracking-wider hidden sm:table-cell">
                    Équipement
                  </th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase tracking-wider hidden md:table-cell">
                    Utilisateur
                  </th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-3 sm:px-6 py-3 text-right text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase tracking-wider hidden lg:table-cell">
                    Statut
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-zinc-900 divide-y divide-zinc-200 dark:divide-zinc-800">
                <tr v-for="(activity, index) in recentActivity.slice(0, 10)" :key="activity.id"
                    class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-all duration-200 group">
                  <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
                    <span :class="getActionBadge(activity.action_type)"
                          class="inline-flex items-center px-2.5 py-1 text-xs font-semibold rounded-lg transition-all group-hover:shadow-md">
                      {{ activity.action_type }}
                    </span>
                  </td>
                  <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap hidden sm:table-cell">
                    <div class="flex items-center gap-2">
                      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-zinc-100 to-zinc-200 dark:from-zinc-800 dark:to-zinc-700 flex items-center justify-center">
                        <Icon name="cpu" :size="14" class="text-zinc-600 dark:text-zinc-400" />
                      </div>
                      <span class="text-xs sm:text-sm font-medium text-zinc-900 dark:text-zinc-100">
                        #{{ activity.device_id }}
                      </span>
                    </div>
                  </td>
                  <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap hidden md:table-cell">
                    <div class="flex items-center gap-2">
                      <div class="w-6 h-6 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                        {{ (activity.user_id || 'N').charAt(0).toUpperCase() }}
                      </div>
                      <span class="text-xs sm:text-sm text-zinc-600 dark:text-zinc-400">
                        {{ activity.user_id || 'N/A' }}
                      </span>
                    </div>
                  </td>
                  <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <Icon name="clock" :size="14" class="text-zinc-400 dark:text-zinc-500" />
                      <span class="text-xs text-zinc-600 dark:text-zinc-400">
                        {{ formatDate(activity.timestamp, true) }}
                      </span>
                    </div>
                  </td>
                  <td class="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-right hidden lg:table-cell">
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-green-100 dark:bg-green-950 text-green-700 dark:text-green-300 text-xs font-medium rounded-full">
                      <span class="w-1.5 h-1.5 bg-green-600 dark:bg-green-400 rounded-full animate-pulse"></span>
                      Validé
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Footer -->
          <div v-if="recentActivity.length > 0" class="px-4 sm:px-6 py-3 bg-zinc-50 dark:bg-zinc-900/50 border-t border-zinc-200 dark:border-zinc-800">
            <div class="flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
              <span>Affichage de {{ Math.min(10, recentActivity.length) }} sur {{ recentActivity.length }} activités</span>
              <button class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors">
                Charger plus →
              </button>
            </div>
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
import { useChartTheme } from "../../../../composables/useChartTheme.js";
import 'echarts-gl';

const loading = ref(true);
const stocksData = ref({});
const recentActivity = ref([]);
const { isDark, chartColors, zinc, getTooltip, getGrid, getAxis } = useChartTheme();

const stats = computed(() => {
  const allStats = {};
  Object.values(stocksData.value).forEach(affectation => {
    Object.entries(affectation).forEach(([status, count]) => {
      allStats[status] = (allStats[status] || 0) + count;
    });
  });
  return allStats;
});

const totalDevices = computed(() => Object.values(stats.value).reduce((sum, count) => sum + count, 0));
const networkHealth = computed(() => {
  const total = totalDevices.value || 1;
  return Math.round(((total - (stats.value.HS || 0)) / total) * 100);
});

// GLOBE 3D - ÉLÉMENT PRINCIPAL avec TOUS les capteurs posés
const globeOption = computed(() => {
  // Générer TOUS les points de pose réels depuis les données
  // Utiliser les régions du stocksData pour créer des points géographiques
  const regions = Object.keys(stocksData.value).filter(k => k !== '[vide]');

  // Coordonnées réelles des villes/régions de Corse
  const regionCoords = {
    'Ajaccio': { lon: 8.7369, lat: 41.9270 },
    'Bastia': { lon: 9.4497, lat: 42.7028 },
    'Corte': { lon: 9.1508, lat: 42.3055 },
    'Porto-Vecchio': { lon: 9.2794, lat: 41.5914 },
    'Calvi': { lon: 8.7569, lat: 42.5679 },
    'Bonifacio': { lon: 9.1598, lat: 41.3875 },
    'Propriano': { lon: 8.9055, lat: 41.6744 },
    'Sartène': { lon: 8.9733, lat: 41.6222 },
    'Ghisonaccia': { lon: 9.4047, lat: 42.0114 },
    'Aléria': { lon: 9.5111, lat: 42.1028 },
    'Cervione': { lon: 9.5108, lat: 42.3381 },
    'Île-Rousse': { lon: 8.9378, lat: 42.6378 },
    'Saint-Florent': { lon: 9.3053, lat: 42.6797 },
    'Zonza': { lon: 9.1697, lat: 41.7433 },
    'Vico': { lon: 8.7947, lat: 42.1686 }
  };

  // Créer un point pour chaque région avec le nombre réel d'équipements posés
  const allSensors = [];
  regions.forEach(region => {
    const poseCount = stocksData.value[region]?.pose || 0;
    if (poseCount > 0) {
      // Trouver les coordonnées (ou utiliser une ville proche)
      let coords = regionCoords[region];

      // Si la région n'a pas de coordonnées exactes, utiliser une variation d'Ajaccio
      if (!coords) {
        const index = regions.indexOf(region);
        coords = {
          lon: 8.7 + (index * 0.15) % 1.5,
          lat: 41.8 + (index * 0.1) % 1.0
        };
      }

      allSensors.push({
        name: region,
        lon: coords.lon,
        lat: coords.lat,
        devices: poseCount
      });
    }
  });

  // Si pas de données, utiliser des exemples
  if (allSensors.length === 0) {
    allSensors.push(
      { name: 'Ajaccio', lon: 8.7369, lat: 41.9270, devices: 100 },
      { name: 'Bastia', lon: 9.4497, lat: 42.7028, devices: 85 },
      { name: 'Corte', lon: 9.1508, lat: 42.3055, devices: 65 },
      { name: 'Porto-Vecchio', lon: 9.2794, lat: 41.5914, devices: 75 },
      { name: 'Calvi', lon: 8.7569, lat: 42.5679, devices: 55 }
    );
  }

  // Préparer les données avec hauteur proportionnelle
  const seriesData = allSensors.map(s => ({
    name: s.name,
    value: [s.lon, s.lat, s.devices / 200], // Hauteur proportionnelle
    devices: s.devices
  }));

  return {
    // Fond étoilé
    backgroundColor: '#000',
    environment: 'https://vue-echarts.dev/assets/starfield-CL52QtHb.jpg',
    tooltip: {
      ...getTooltip(),
      formatter: (params) => {
        if (!params.data || !params.data.value) return '';
        const [lon, lat, devices] = params.data.value;
        return `<strong>${params.data.name}</strong><br/>Équipements CPL: ${params.data.devices}<br/>Coordonnées: ${lat.toFixed(2)}°N, ${lon.toFixed(2)}°E`;
      }
    },
    globe: {
      // Texture satellite Blue Marble (NASA - CDN rapide)
      baseTexture: 'https://unpkg.com/three-globe@2.24.3/example/img/earth-blue-marble.jpg',
      // Texture alternative de secours
      // baseTexture: 'https://vue-echarts.dev/assets/world-42pcE1u0.jpg',
      // Pas de heightTexture pour garder une sphère lisse
      heightTexture: null,
      displacementScale: 0,
      shading: 'realistic',
      realisticMaterial: {
        roughness: 0.2,
        metalness: 0.1
      },
      postEffect: {
        enable: true,
        bloom: {
          enable: true,
          intensity: 0.1
        },
        SSAO: {
          enable: true,
          radius: 2,
          intensity: 1.2
        }
      },
      temporalSuperSampling: {
        enable: true
      },
      light: {
        ambient: {
          intensity: 0.8
        },
        main: {
          intensity: 2,
          shadow: true,
          shadowQuality: 'high',
          alpha: 55,
          beta: 10
        },
        ambientCubemap: {
          texture: 'https://vue-echarts.dev/assets/starfield-CL52QtHb.jpg',
          diffuseIntensity: 0.3,
          specularIntensity: 0.8
        }
      },
      atmosphere: {
        show: true,
        offset: 10,
        color: '#4299e1',
        glowPower: 5,
        innerGlowPower: 3
      },
      viewControl: {
        autoRotate: false, // PAS DE ROTATION AUTOMATIQUE
        autoRotateSpeed: 0,
        damping: 0.8,
        rotateSensitivity: 1,
        zoomSensitivity: 1,
        panSensitivity: 1,
        // VUE FIXE sur la Corse - Vue de côté
        alpha: 70,  // Vue de côté (0=dessus, 90=côté)
        beta: -5,   // Rotation légère vers la Corse
        distance: 6, // ZOOM EXTRÊME (encore plus proche)
        center: [0, -8, 0], // Décalage vers le bas pour effet "vu de côté"
        targetCoord: [9.0, 42.15], // Centre exact de la Corse
        minDistance: 5,
        maxDistance: 200
      },
      itemStyle: {
        color: isDark.value ? '#475569' : '#64748b',
        opacity: 1,
        borderWidth: 0.5,
        borderColor: isDark.value ? '#1e293b' : '#334155'
      }
    },
    series: [{
      type: 'bar3D',
      coordinateSystem: 'globe',
      // Barres 3D : largeur normale, hauteur TRÈS courte
      shading: 'realistic',
      bevelSize: 0.1,
      bevelSmoothness: 2,
      minHeight: 0.01,
      barSize: [0.25, 0.25], // Largeur/profondeur NORMALE (visible)
      itemStyle: {
        color: (params) => {
          // Palette étendue pour tous les capteurs
          const colors = [
            chartColors.danger,   // Rouge
            chartColors.warning,  // Orange
            chartColors.info,     // Cyan
            chartColors.success,  // Vert
            chartColors.purple,   // Violet
            chartColors.primary,  // Bleu
            chartColors.pink,     // Rose
            chartColors.indigo,   // Indigo
            chartColors.teal,     // Teal
            chartColors.amber,    // Ambre
            '#f97316',            // Orange vif
            '#84cc16',            // Lime
            '#06b6d4',            // Cyan clair
            '#8b5cf6',            // Violet clair
            '#ec4899'             // Rose vif
          ];
          return colors[params.dataIndex % colors.length];
        },
        opacity: 0.95,
        borderWidth: 1,
        borderColor: '#ffffff',
        metalness: 0.2,
        roughness: 0.6
      },
      emphasis: {
        itemStyle: {
          color: chartColors.primary,
          opacity: 1,
          shadowBlur: 20,
          shadowColor: chartColors.primary
        },
        label: {
          show: true,
          formatter: (params) => `${params.data.name}\n${params.data.devices}`,
          color: '#ffffff',
          fontSize: 12,
          fontWeight: 'bold',
          backgroundColor: 'rgba(0,0,0,0.8)',
          padding: 6,
          borderRadius: 4
        }
      },
      label: {
        show: true,
        position: 'top',
        formatter: '{b}',
        color: isDark.value ? zinc[50] : zinc[900],
        fontSize: 11,
        fontWeight: 'bold',
        backgroundColor: isDark.value ? 'rgba(0,0,0,0.9)' : 'rgba(255,255,255,0.95)',
        padding: [5, 10],
        borderRadius: 6,
        borderWidth: 2,
        borderColor: (params) => {
          const colors = [chartColors.danger, chartColors.warning, chartColors.info, chartColors.success, chartColors.purple];
          return colors[params.dataIndex % colors.length];
        },
        distance: 5
      },
      data: seriesData
    }]
  };
});

// BAR3D - Real GL Chart with colored bars
const bar3DOption = computed(() => {
  const regions = Object.keys(stocksData.value).filter(k => k !== '[vide]');
  const statuses = ['en_stock', 'en_livraison', 'pose', 'HS'];
  const statusLabels = { en_stock: 'Stock', en_livraison: 'Transit', pose: 'Installé', HS: 'HS' };
  const statusColors = {
    en_stock: chartColors.info,
    en_livraison: chartColors.warning,
    pose: chartColors.success,
    HS: chartColors.danger
  };

  const data = [];
  regions.forEach((region, x) => {
    statuses.forEach((status, z) => {
      const value = stocksData.value[region]?.[status] || 0;
      if (value > 0) {
        data.push({
          value: [x, value, z],
          itemStyle: { color: statusColors[status] }
        });
      }
    });
  });

  return {
    backgroundColor: 'transparent',
    tooltip: {
      ...getTooltip(),
      formatter: (params) => {
        const [x, y, z] = params.value;
        const region = regions[x];
        const status = statuses[z];
        return `<strong>${region}</strong><br/>${statusLabels[status]}: ${y} équipements`;
      }
    },
    xAxis3D: {
      type: 'category',
      name: 'Régions',
      data: regions,
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    yAxis3D: {
      type: 'value',
      name: 'Quantité',
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    zAxis3D: {
      type: 'category',
      name: 'Statuts',
      data: statuses.map(s => statusLabels[s]),
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    grid3D: {
      boxWidth: 100,
      boxDepth: 80,
      boxHeight: 80,
      viewControl: {
        autoRotate: true,
        autoRotateSpeed: 4,
        distance: 180
      },
      light: {
        main: { intensity: 1.2, shadow: true },
        ambient: { intensity: 0.4 }
      }
    },
    series: [{
      type: 'bar3D',
      data: data,
      shading: 'realistic',
      label: { show: false },
      itemStyle: { opacity: 0.9 },
      emphasis: {
        label: {
          show: true,
          color: '#fff',
          fontSize: 12,
          fontWeight: 'bold'
        },
        itemStyle: {
          opacity: 1,
          borderWidth: 2,
          borderColor: '#ffffff'
        }
      }
    }]
  };
});

// SCATTER3D - Real GL Chart with colors
const scatter3DOption = computed(() => {
  const data = [
    [9.15, 42.22, 120, 'Bastia Nord'],
    [8.75, 41.93, 80, 'Ajaccio Centre'],
    [9.45, 42.70, 150, 'Bastia Sud'],
    [9.28, 41.59, 95, 'Porto-Vecchio'],
    [8.76, 42.57, 70, 'Calvi']
  ];

  return {
    backgroundColor: 'transparent',
    tooltip: {
      ...getTooltip(),
      formatter: (params) => `<strong>${params.data[3]}</strong><br/>Équipements: ${params.data[2]}<br/>Position: ${params.data[1].toFixed(2)}°N, ${params.data[0].toFixed(2)}°E`
    },
    visualMap: {
      show: true,
      min: 50,
      max: 150,
      dimension: 2,
      inRange: {
        color: [chartColors.info, chartColors.purple, chartColors.warning, chartColors.danger]
      },
      textStyle: {
        color: isDark.value ? zinc[300] : zinc[700],
        fontSize: 10
      },
      right: 10,
      top: 'center',
      itemWidth: 15,
      itemHeight: 80
    },
    xAxis3D: {
      name: 'Longitude',
      type: 'value',
      min: 8.5,
      max: 9.7,
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    yAxis3D: {
      name: 'Latitude',
      type: 'value',
      min: 41.5,
      max: 43,
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    zAxis3D: {
      name: 'Équipements',
      type: 'value',
      axisLabel: { color: isDark.value ? zinc[400] : zinc[600], fontSize: 10 },
      axisLine: { lineStyle: { color: isDark.value ? zinc[700] : zinc[300] } },
      nameTextStyle: { color: isDark.value ? zinc[300] : zinc[700], fontSize: 11 }
    },
    grid3D: {
      boxWidth: 100,
      boxDepth: 100,
      boxHeight: 80,
      viewControl: {
        autoRotate: true,
        autoRotateSpeed: 3,
        distance: 200
      },
      light: {
        main: { intensity: 1.2 },
        ambient: { intensity: 0.5 }
      }
    },
    series: [{
      type: 'scatter3D',
      data: data,
      symbolSize: (val) => Math.max(10, val[2] / 5),
      itemStyle: {
        opacity: 0.9,
        borderWidth: 2,
        borderColor: isDark.value ? zinc[900] : '#ffffff'
      },
      emphasis: {
        itemStyle: {
          color: chartColors.primary,
          opacity: 1,
          borderWidth: 3,
          borderColor: '#ffffff'
        }
      }
    }]
  };
});

// Regular Charts with vibrant colors
const pieOption = computed(() => ({
  tooltip: {
    ...getTooltip(),
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  legend: {
    bottom: 0,
    textStyle: {
      color: isDark.value ? zinc[300] : zinc[700],
      fontSize: 11
    }
  },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    center: ['50%', '45%'],
    data: [
      { value: stats.value.en_stock || 0, name: 'Stock', itemStyle: { color: chartColors.info } },
      { value: stats.value.en_livraison || 0, name: 'Transit', itemStyle: { color: chartColors.warning } },
      { value: stats.value.pose || 0, name: 'Installé', itemStyle: { color: chartColors.success } },
      { value: stats.value.HS || 0, name: 'HS', itemStyle: { color: chartColors.danger } }
    ].filter(item => item.value > 0),
    label: {
      color: isDark.value ? zinc[200] : zinc[700],
      fontSize: 11
    },
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
    }
  }]
}));

const lineOption = computed(() => ({
  tooltip: {
    ...getTooltip(),
    trigger: 'axis',
    formatter: '{b}: {c} activités'
  },
  grid: getGrid(),
  xAxis: {
    type: 'category',
    data: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
    ...getAxis()
  },
  yAxis: {
    type: 'value',
    name: 'Activités',
    ...getAxis()
  },
  series: [{
    type: 'line',
    smooth: true,
    data: [35, 42, 38, 45, 52, 28, 15],
    areaStyle: {
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: chartColors.primary + '66' }, // 40% opacity
          { offset: 1, color: chartColors.primary + '00' }  // 0% opacity
        ]
      }
    },
    itemStyle: { color: chartColors.primary },
    lineStyle: { width: 3 },
    emphasis: {
      itemStyle: {
        borderWidth: 3,
        borderColor: '#ffffff'
      }
    }
  }]
}));

const gaugeOption = computed(() => ({
  series: [{
    type: 'gauge',
    radius: '80%',
    startAngle: 200,
    endAngle: -20,
    min: 0,
    max: 100,
    axisLine: {
      lineStyle: {
        width: 10,
        color: [
          [0.3, chartColors.danger],
          [0.7, chartColors.warning],
          [1, chartColors.success]
        ]
      }
    },
    pointer: {
      itemStyle: { color: 'auto' },
      width: 5
    },
    axisTick: {
      distance: -10,
      length: 4,
      lineStyle: {
        color: isDark.value ? zinc[700] : '#ffffff',
        width: 1
      }
    },
    splitLine: {
      distance: -14,
      length: 14,
      lineStyle: {
        color: isDark.value ? zinc[700] : '#ffffff',
        width: 2
      }
    },
    axisLabel: {
      color: 'auto',
      distance: 20,
      fontSize: 10
    },
    detail: {
      valueAnimation: true,
      formatter: '{value}%',
      color: isDark.value ? zinc[100] : zinc[900],
      fontSize: 22,
      fontWeight: 'bold',
      offsetCenter: [0, '70%']
    },
    title: {
      show: false
    },
    data: [{ value: networkHealth.value }]
  }]
}));

const heatmapOption = computed(() => {
  const hours = ['00h', '04h', '08h', '12h', '16h', '20h'];
  const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
  const data = [];
  days.forEach((day, i) => {
    hours.forEach((hour, j) => {
      data.push([j, i, Math.floor(Math.random() * 50) + 10]);
    });
  });

  return {
    tooltip: {
      ...getTooltip(),
      position: 'top',
      formatter: (params) => `${days[params.data[1]]} ${hours[params.data[0]]}<br/>Activité: ${params.data[2]}`
    },
    grid: {
      height: '70%',
      top: '10%',
      left: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      splitArea: { show: true },
      axisLabel: {
        color: isDark.value ? zinc[400] : zinc[600],
        fontSize: 10
      },
      axisLine: {
        lineStyle: { color: isDark.value ? zinc[700] : zinc[300] }
      }
    },
    yAxis: {
      type: 'category',
      data: days,
      splitArea: { show: true },
      axisLabel: {
        color: isDark.value ? zinc[400] : zinc[600],
        fontSize: 10
      },
      axisLine: {
        lineStyle: { color: isDark.value ? zinc[700] : zinc[300] }
      }
    },
    visualMap: {
      min: 0,
      max: 60,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: [chartColors.info, chartColors.purple, chartColors.warning, chartColors.danger]
      },
      textStyle: {
        color: isDark.value ? zinc[300] : zinc[700],
        fontSize: 10
      }
    },
    series: [{
      type: 'heatmap',
      data: data,
      label: { show: false },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  };
});

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
    console.error('Erreur:', error);
  } finally {
    loading.value = false;
  }
};

const getActionBadge = (type) => {
  // Badges colorés selon le type d'action
  const badges = {
    'RECEPTION': 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300 dark:border-blue-800',
    'POSE': 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300 border border-green-300 dark:border-green-800',
    'DEPOSE': 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300 border border-orange-300 dark:border-orange-800',
    'TRANSFERT': 'bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-300 dark:border-purple-800',
    'TEST': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-950 dark:text-cyan-300 border border-cyan-300 dark:border-cyan-800',
    'AUTRE': 'bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-300 border border-zinc-300 dark:border-zinc-700'
  };
  return badges[type] || badges['AUTRE'];
};

const formatDate = (timestamp, mobile = false) => {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return mobile
    ? new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }).format(date)
    : new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }).format(date);
};

onMounted(() => fetchData());
</script>
