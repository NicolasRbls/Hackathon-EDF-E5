// Palette Zinc pour tous les dashboards
export const zincColors = {
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

// Couleurs pour les graphiques (priorité zinc)
export const chartColors = {
  primary: zincColors[500],
  secondary: zincColors[600],
  tertiary: zincColors[700],
  quaternary: zincColors[800],
  light: zincColors[300],
  lighter: zincColors[200],
  lightest: zincColors[100],
  // Couleurs d'accent (utilisées avec parcimonie)
  accent: {
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#06b6d4'
  }
};

// Classes Tailwind pour StatCard (zinc prioritaire)
export const statCardClasses = {
  default: {
    iconBgColor: 'bg-zinc-100 dark:bg-zinc-800',
    iconColor: 'text-zinc-600 dark:text-zinc-400'
  },
  primary: {
    iconBgColor: 'bg-zinc-200 dark:bg-zinc-700',
    iconColor: 'text-zinc-700 dark:text-zinc-300'
  },
  secondary: {
    iconBgColor: 'bg-zinc-300 dark:bg-zinc-600',
    iconColor: 'text-zinc-800 dark:text-zinc-200'
  },
  // Seulement pour les alertes critiques
  danger: {
    iconBgColor: 'bg-rose-100 dark:bg-rose-950',
    iconColor: 'text-rose-700 dark:text-rose-400'
  }
};

// Thème pour ECharts (zinc)
export const getEchartsTheme = (isDark = false) => ({
  color: [
    zincColors[500],
    zincColors[600],
    zincColors[700],
    zincColors[400],
    zincColors[300]
  ],
  backgroundColor: 'transparent',
  textStyle: {
    color: isDark ? zincColors[300] : zincColors[700]
  },
  title: {
    textStyle: {
      color: isDark ? zincColors[100] : zincColors[900]
    }
  },
  line: {
    itemStyle: {
      borderWidth: 1
    },
    lineStyle: {
      width: 2
    },
    symbolSize: 4,
    smooth: true
  },
  radar: {
    itemStyle: {
      borderWidth: 1
    },
    lineStyle: {
      width: 2
    },
    symbolSize: 4
  },
  bar: {
    itemStyle: {
      barBorderWidth: 0,
      barBorderColor: '#ccc'
    }
  },
  pie: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  scatter: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  boxplot: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  parallel: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  sankey: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  funnel: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  },
  gauge: {
    itemStyle: {
      borderWidth: 0,
      borderColor: '#ccc'
    }
  }
});

// Gradient headers (zinc avec petites touches de couleur)
export const headerGradients = {
  default: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-zinc-950',
  admin: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-amber-950',
  bo: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-blue-950',
  labo: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-purple-950',
  magasin: 'bg-gradient-to-br from-zinc-800 via-zinc-900 to-emerald-950'
};
