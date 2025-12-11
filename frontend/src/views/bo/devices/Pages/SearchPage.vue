<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Recherche Matériel</h1>
    <div class="bg-white p-4 rounded shadow mb-6 filter-section">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Numéro de Série</label>
          <input v-model="filters.q" type="text" class="w-full border rounded p-2" placeholder="Ex: 12345">
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Numéro de Carton</label>
          <input v-model="filters.num_carton" type="text" class="w-full border rounded p-2">
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Statut</label>
          <select v-model="filters.status" class="w-full border rounded p-2">
            <option value="">Tous</option>
            <option v-for="status in dictionaries.status" :key="status" :value="status">{{ status }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Affectation</label>
          <select v-model="filters.affectation" class="w-full border rounded p-2">
            <option value="">Toutes</option>
            <option v-for="aff in dictionaries.affectation" :key="aff" :value="aff">{{ aff }}</option>
          </select>
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button @click="search" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Rechercher
        </button>
      </div>
    </div>
    <div v-if="loading" class="text-center py-4">Chargement...</div>
    <div v-else-if="results.length === 0 && searched" class="text-center py-4 text-gray-500">Aucun résultat trouvé.</div>
    <div v-else-if="results.length > 0" class="bg-white rounded shadow overflow-x-auto">
      <table class="min-w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Série</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Carton</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Affectation</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="device in results" :key="device.id">
            <td class="px-6 py-4 whitespace-nowrap">{{ device.serial_number }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ device.num_carton || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="statusClass(device.current_status)" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ device.current_status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{{ device.affectation }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <router-link :to="{ name: 'bo-device-details', params: { serial: device.serial_number } }" class="text-indigo-600 hover:text-indigo-900">Gérer</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const filters = ref({
  q: '',
  num_carton: '',
  status: '',
  affectation: ''
});

const results = ref([]);
const loading = ref(false);
const searched = ref(false);
const dictionaries = ref({ status: [], affectation: [] });

const API_URL = 'http://127.0.0.1:8000';

onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/devices/dictionaries`);
    dictionaries.value = res.data;
    if (!dictionaries.value.status) {
        dictionaries.value = {
            status: ['en_livraison', 'en_stock', 'pose', 'a_tester', 'HS'],
            affectation: ['Magasin', 'BO Nord', 'BO Centre', 'BO Sud', 'Labo']
        };
    }
  } catch (e) {
    console.error('Failed to load dictionaries', e);
  }
});

const search = async () => {
  loading.value = true;
  searched.value = true;
  try {
    const params = {};
    if (filters.value.q) params.q = filters.value.q;
    if (filters.value.num_carton) params.num_carton = filters.value.num_carton;
    if (filters.value.status) params.status = filters.value.status;
    if (filters.value.affectation) params.affectation = filters.value.affectation;

    const res = await axios.get(`${API_URL}/devices/search`, { params });
    results.value = res.data;
  } catch (e) {
    console.error('Search failed', e);
    results.value = [];
  } finally {
    loading.value = false;
  }
};

const statusClass = (status) => {
  switch (status) {
    case 'en_stock': return 'bg-green-100 text-green-800';
    case 'HS': return 'bg-red-100 text-red-800';
    case 'en_livraison': return 'bg-yellow-100 text-yellow-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};
</script>
