import { ref, watch } from 'vue';

// Thème cohérent pour tous les graphiques avec support dark mode réactif
export const useChartTheme = () => {
  const isDark = ref(document.documentElement.classList.contains('dark'));

  // Observe les changements de mode dark
  if (typeof window !== 'undefined') {
    const observer = new MutationObserver(() => {
      isDark.value = document.documentElement.classList.contains('dark');
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  }

  const chartColors = {
    // Couleurs vives pour les charts (non-zinc)
    primary: '#3b82f6',    // Bleu
    success: '#10b981',    // Vert
    warning: '#f59e0b',    // Orange
    danger: '#ef4444',     // Rouge
    info: '#06b6d4',       // Cyan
    purple: '#8b5cf6',     // Violet
    pink: '#ec4899',       // Rose
    indigo: '#6366f1',     // Indigo
    teal: '#14b8a6',       // Teal
    amber: '#f59e0b'       // Ambre
  };

  const zinc = {
    50: '#fafafa',
    100: '#f4f4f5',
    200: '#e4e4e7',
    300: '#d4d4d8',
    400: '#a1a1aa',
    500: '#71717a',
    600: '#52525b',
    700: '#3f3f46',
    800: '#27272a',
    900: '#18181b',
    950: '#09090b'
  };

  const textColor = ref(isDark.value ? zinc[300] : zinc[700]);
  const axisColor = ref(isDark.value ? zinc[600] : zinc[400]);
  const bgColor = ref(isDark.value ? zinc[900] : '#ffffff');
  const borderColor = ref(isDark.value ? zinc[800] : zinc[200]);

  // Update colors when dark mode changes
  watch(isDark, (dark) => {
    textColor.value = dark ? zinc[300] : zinc[700];
    axisColor.value = dark ? zinc[600] : zinc[400];
    bgColor.value = dark ? zinc[900] : '#ffffff';
    borderColor.value = dark ? zinc[800] : zinc[200];
  });

  return {
    isDark,
    chartColors,
    zinc,
    textColor,
    axisColor,
    bgColor,
    borderColor,
    getTooltip: () => ({
      backgroundColor: isDark.value ? zinc[800] : '#ffffff',
      borderColor: isDark.value ? zinc[700] : zinc[200],
      borderWidth: 1,
      textStyle: {
        color: isDark.value ? zinc[200] : zinc[700],
        fontSize: 12
      },
      padding: [8, 12],
      extraCssText: 'border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'
    }),
    getGrid: () => ({
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    }),
    getAxis: () => ({
      axisLine: {
        lineStyle: { color: isDark.value ? zinc[700] : zinc[300] }
      },
      axisTick: {
        lineStyle: { color: isDark.value ? zinc[700] : zinc[300] }
      },
      axisLabel: {
        color: isDark.value ? zinc[400] : zinc[600],
        fontSize: 11
      },
      splitLine: {
        lineStyle: {
          color: isDark.value ? zinc[800] : zinc[200],
          type: 'dashed'
        }
      }
    })
  };
};
