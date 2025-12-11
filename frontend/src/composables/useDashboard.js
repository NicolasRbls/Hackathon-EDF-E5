import { ref, computed } from 'vue';

export const useDashboard = () => {
  const loading = ref(true);
  const error = ref(null);

  const formatDate = (timestamp, mobile = false) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    if (mobile) {
      return new Intl.DateTimeFormat('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
    return new Intl.DateTimeFormat('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getActionBadgeClass = (actionType) => {
    const classes = {
      'RECEPTION': 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800',
      'POSE': 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800',
      'DEPOSE': 'bg-rose-50 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400 border border-rose-200 dark:border-rose-800',
      'TRANSFERT': 'bg-purple-50 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400 border border-purple-200 dark:border-purple-800',
      'TEST': 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 border border-amber-200 dark:border-amber-800',
      'AUTRE': 'bg-zinc-50 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700'
    };
    return classes[actionType] || classes['AUTRE'];
  };

  const handleError = (err, message = 'Erreur lors du chargement des données') => {
    console.error(message, err);
    error.value = message;
  };

  return {
    loading,
    error,
    formatDate,
    getActionBadgeClass,
    handleError
  };
};

export const useStats = (stocksData) => {
  const stats = computed(() => {
    const allStats = {};
    Object.values(stocksData.value).forEach(affectation => {
      Object.entries(affectation).forEach(([status, count]) => {
        allStats[status] = (allStats[status] || 0) + count;
      });
    });
    return allStats;
  });

  const totalDevices = computed(() =>
    Object.values(stats.value).reduce((sum, count) => sum + count, 0)
  );

  const networkHealth = computed(() => {
    const total = totalDevices.value || 1;
    const operational = total - (stats.value.HS || 0);
    return Math.round((operational / total) * 100);
  });

  return {
    stats,
    totalDevices,
    networkHealth
  };
};
