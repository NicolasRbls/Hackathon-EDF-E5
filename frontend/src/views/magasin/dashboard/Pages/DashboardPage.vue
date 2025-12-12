<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">Tableau de Bord Magasin</h1>

    <!-- Quick Actions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Réception -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow cursor-pointer hover:shadow-md transition" @click="openModal('reception')">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-green-100 text-green-600 rounded-full">
            <Icon name="package-plus" size="24" />
          </div>
          <div>
            <h3 class="font-bold text-gray-800 dark:text-white">Réception</h3>
            <p class="text-sm text-gray-500">Ajout Capteur/Carton</p>
          </div>
        </div>
      </div>

      <!-- Transfert -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow cursor-pointer hover:shadow-md transition" @click="openModal('transfert')">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-blue-100 text-edf-orange rounded-full">
            <Icon name="arrow-right-left" size="24" />
          </div>
          <div>
            <h3 class="font-bold text-gray-800 dark:text-white">Transfert</h3>
            <p class="text-sm text-gray-500">Déplacer un Carton</p>
          </div>
        </div>
      </div>

      <!-- Scanner -->
      <router-link :to="{ name: 'scan-index' }" class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow cursor-pointer hover:shadow-md transition block">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-purple-100 text-purple-600 rounded-full">
            <Icon name="scan" size="24" />
          </div>
          <div>
            <h3 class="font-bold text-gray-800 dark:text-white">Scanner</h3>
            <p class="text-sm text-gray-500">Info Capteur</p>
          </div>
        </div>
      </router-link>

      <!-- Export CSV -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow cursor-pointer hover:shadow-md transition" @click="openModal('export')">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-orange-100 text-orange-600 rounded-full">
            <Icon name="file-spreadsheet" size="24" />
          </div>
          <div>
            <h3 class="font-bold text-gray-800 dark:text-white">Export CSV</h3>
            <p class="text-sm text-gray-500">Historique</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Réception Modal -->
    <div v-if="modals.reception" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Réception Matériel</h3>
        <p class="mb-4 text-sm text-gray-600">Entrez le code (k... pour capteur, c... pour carton)</p>
        <input v-model="forms.reception.code" @keyup.enter="handleReception" type="text" placeholder="Ex: k123456 ou c987" class="w-full border p-2 rounded mb-4" autofocus>
        
        <div class="flex justify-end space-x-2">
          <button @click="closeModals" class="px-4 py-2 border rounded hover:bg-gray-100">Annuler</button>
          <button @click="handleReception" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Valider</button>
        </div>
      </div>
    </div>

    <!-- Transfert Modal -->
    <div v-if="modals.transfert" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Transfert Carton</h3>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Numéro Carton</label>
          <input v-model="forms.transfert.num_carton" type="text" class="w-full border p-2 rounded">
        </div>
        <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Nouvelle Affectation</label>
            <select v-model="forms.transfert.affectation" class="w-full border rounded p-2">
                <option value="Magasin">Magasin</option>
                <option value="BO Nord">BO Nord</option>
                <option value="BO Centre">BO Centre</option>
                <option value="BO Sud">BO Sud</option>
                <option value="Labo">Labo</option>
            </select>
        </div>
        <div class="flex justify-end space-x-2">
          <button @click="closeModals" class="px-4 py-2 border rounded hover:bg-gray-100">Annuler</button>
          <button @click="handleTransfert" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Transférer</button>
        </div>
      </div>
    </div>

    <!-- Export Modal -->
    <div v-if="modals.export" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Export CSV</h3>
        <p class="mb-4 text-sm text-gray-600">Exporter l\'historique des actions.</p>
        <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Nombre de lignes limite</label>
            <input v-model.number="forms.export.limit" type="number" class="w-full border p-2 rounded">
        </div>
        <div class="flex justify-end space-x-2">
          <button @click="closeModals" class="px-4 py-2 border rounded hover:bg-gray-100">Annuler</button>
          <button @click="handleExport" class="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700">Exporter</button>
        </div>
      </div>
    </div>

    <!-- KPI Cards (Existing) -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Total Stocks"
        :value="totalStocks"
        icon="package"
        color="bg-edf-orange"
      />
      <StatCard
        title="Cartons"
        :value="stats.cartons_count || 0"
        icon="box"
        color="bg-green-500"
      />
      <StatCard
        title="En Attente"
        :value="stats.pending_transfer || 0"
        icon="clock"
        color="bg-yellow-500"
      />
       <StatCard
        title="Alertes"
        :value="stats.alerts || 0"
        icon="alert-triangle"
        color="bg-red-500"
      />
    </div>

    <!-- Charts will go here (keeping existing structure implies passing existing chart options if any) -->
     <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8" v-if="!loading">   
          <!-- Stock Movement -->
          <ChartCard
            title="Mouvements de Stock"
            :option="stockMovementOption"
            height="350px"
          />

          <!-- Delivery Progress -->
          <ChartCard
            title="Progression des Livraisons"
            :option="deliveryProgressOption"
            height="350px"
          />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import StatCard from "../../../../components/dashboard/StatCard.vue";
import ChartCard from "../../../../components/dashboard/ChartCard.vue";
import Icon from "../../../../components/lucide/Icon.vue";
import { statsService, deviceService, actionService, historyService } from "../../../../services/api.js";

// State
const loading = ref(true);
const stats = ref({});
const modals = reactive({ reception: false, transfert: false, export: false });
const forms = reactive({
    reception: { code: '' },
    transfert: { num_carton: '', affectation: 'BO Nord' },
    export: { limit: 100 }
});

// Mock/Real Chart Options
const stockMovementOption = computed(() => ({
    title: { text: 'Mouvements (Simulé)' },
    xAxis: { type: 'category', data: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven'] },
    yAxis: { type: 'value' },
    series: [{ data: [120, 200, 150, 80, 70], type: 'bar', itemStyle: { color: '#3b82f6' } }]
}));

const deliveryProgressOption = computed(() => ({
    series: [{
        type: 'gauge',
        progress: { show: true },
        detail: { formatter: '{value}%' },
        data: [{ value: 75, name: 'Complété' }]
    }]
}));

const totalStocks = computed(() => {
    return (stats.value.en_stock || 0) + (stats.value.en_livraison || 0);
});

// Actions
const openModal = (name) => {
    Object.keys(modals).forEach(k => modals[k] = false);
    modals[name] = true;
};

const closeModals = () => {
    Object.keys(modals).forEach(k => modals[k] = false);
    forms.reception.code = '';
    forms.transfert.num_carton = '';
};

const handleReception = async () => {
    const code = forms.reception.code.trim();
    if (!code) return;
    
    try {
        if (code.toLowerCase().startsWith('k')) {
            // Sensor logic
            const payload = {
                serial_number: code,
                current_status: 'en_stock',
                affectation: 'Magasin',
                last_updated: new Date().toISOString()
            };
            await deviceService.createDevice(payload);
            alert(`Capteur ${code} ajouté au stock.`);
        } else if (code.toLowerCase().startsWith('c')) {
             const payload = {
                serial_number: `PREFIX-${code}`, 
                num_carton: code,
                current_status: 'en_stock',
                affectation: 'Magasin',
                last_updated: new Date().toISOString()
            };
            await deviceService.createDevice(payload);
            alert(`Carton ${code} enregistré (Simulation).`);
        } else {
            alert('Format invalide. Utilisez k... pour capteur ou c... pour carton.');
            return;
        }
        closeModals();
        fetchData();
    } catch (e) {
        console.error(e);
        alert('Erreur lors de la réception');
    }
};

const handleTransfert = async () => {
    if (!forms.transfert.num_carton) return;
    try {
        const res = await deviceService.search({ num_carton: forms.transfert.num_carton });
        const devices = res.data;
        
        if (devices.length === 0) {
            alert('Aucun appareil trouvé dans ce carton.');
            return;
        }

        const promises = devices.map(d => actionService.createAction({
            device_serial: d.serial_number,
            action_type: 'TRANSFERT',
            user_id: 'current_user', 
            new_affectation: forms.transfert.affectation,
            details: `Transfert Carton ${forms.transfert.num_carton}`
        }));

        await Promise.all(promises);
        alert(`${devices.length} appareils transférés vers ${forms.transfert.affectation}`);
        closeModals();
        fetchData();
    } catch (e) {
         console.error(e);
         alert('Erreur transfert');
    }
};

const handleExport = async () => {
    try {
        const res = await historyService.searchHistory({ limit: forms.export.limit });
        const data = res.data;
        
        if (!data || data.length === 0) {
             alert('Aucune donnée à exporter.');
             return;
        }

        // Convert to CSV
        const headers = ['Date', 'Action', 'Utilisateur', 'Appareil', 'Details'];
        const rows = data.map(row => [
            row.timestamp,
            row.action_type,
            row.user_id,
            row.device_id,
            `"${(row.details || '').replace(/"/g, '""')}"`
        ]);

        const csvContent = [
            headers.join(','),
            ...rows.map(r => r.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', `export_magasin_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        closeModals();
    } catch (e) {
         console.error(e);
         alert('Erreur export');
    }
};

const fetchData = async () => {
    try {
        const res = await statsService.getStocks();
        stats.value = res.data || {};
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchData();
});
</script>

<style scoped>
/* Quick Actions Hover Effects */
</style>
