<template>
  <div class="bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800 p-4 sm:p-6 overflow-hidden">
    <div class="flex items-center justify-between mb-3 sm:mb-4">
      <h3 :class="titleClass || 'text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100 truncate'">{{ title }}</h3>
      <slot name="actions"></slot>
    </div>
    <div :style="{ height: height }" class="min-h-[200px]">
      <v-chart
        :option="option"
        :autoresize="true"
        class="w-full h-full"
      />
    </div>
  </div>
</template>

<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import {
  PieChart,
  BarChart,
  LineChart,
  GaugeChart,
  RadarChart,
  HeatmapChart,
  ScatterChart
} from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  VisualMapComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

// Import echarts-gl for 3D charts (it auto-registers itself)
import 'echarts-gl';

use([
  CanvasRenderer,
  PieChart,
  BarChart,
  LineChart,
  GaugeChart,
  RadarChart,
  HeatmapChart,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  VisualMapComponent
]);

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  option: {
    type: Object,
    required: true
  },
  height: {
    type: String,
    default: '400px'
  },
  titleClass: {
    type: String,
    default: null
  }
});
</script>
