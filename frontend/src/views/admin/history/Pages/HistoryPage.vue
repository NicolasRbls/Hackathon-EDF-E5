<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Historique Global</h1>

    <div class="bg-white p-4 rounded shadow mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Utilisateur (match)</label>
          <input v-model="filters.username" type="text" class="w-full border rounded p-2">
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Rôle</label>
           <select v-model="filters.role" class="w-full border rounded p-2">
            <option value="">Tous</option>
            <option value="viewer">Viewer</option>
            <option value="magasin">Magasin</option>
            <option value="bo_nord">BO Nord</option>
            <option value="bo_centre">BO Centre</option>
            <option value="bo_sud">BO Sud</option>
            <option value="labo">Labo</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Action</label>
          <select v-model="filters.action_type" class="w-full border rounded p-2">
            <option value="">Toutes</option>
             <option value="TRANSFERT">Transfert</option>
            <option value="TEST">Test</option>
            <option value="POSE">Pose</option>
            <option value="DEPOSE">Dépose</option>
            <option value="AUTRE">Autre</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Série Appareil</label>
          <input v-model="filters.device_serial" type="text" class="w-full border rounded p-2">
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button @click="search" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Rechercher</button>
      </div>
    </div>

    <div v-if="loading" class="text-center">Chargement...</div>
    <div v-else class="bg-white rounded shadow overflow-x-auto">
      <table class="min-w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left">Date</th>
            <th class="px-6 py-3 text-left">Action</th>
            <th class="px-6 py-3 text-left">Appareil</th>
            <th class="px-6 py-3 text-left">Utilisateur</th>
            <th class="px-6 py-3 text-left">Détails</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in history" :key="h.id" class="border-t">
            <td class="px-6 py-4">{{ new Date(h.timestamp).toLocaleString() }}</td>
            <td class="px-6 py-4">{{ h.action_type }}</td>
            <td class="px-6 py-4">{{ h.device_id }}</td>
            <td class="px-6 py-4">{{ h.user_id }}</td>
            <td class="px-6 py-4">{{ h.details }}</td>
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
  username: '',
  role: '',
  action_type: '',
  device_serial: ''
});
const history = ref([]);
const loading = ref(false);
const API_URL = 'http://127.0.0.1:8000';

const search = async () => {
  loading.value = true;
  try {
    const params = {};
    if (filters.value.username) params.username = filters.value.username;
    if (filters.value.role) params.role = filters.value.role;
    if (filters.value.action_type) params.action_type = filters.value.action_type;
    if (filters.value.device_serial) params.device_serial = filters.value.device_serial;

    const res = await axios.get(`${API_URL}/history/`, { params });
    history.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  search();
});
</script>
