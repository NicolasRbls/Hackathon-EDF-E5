<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Gérer le matériel</h1>
      <router-link :to="{ name: 'bo-device-search' }" class="text-gray-600 hover:text-gray-900">Retour</router-link>
    </div>

    <div v-if="loading" class="text-center">Chargement...</div>
    <div v-else class="bg-white rounded shadow p-6 max-w-2xl mx-auto">
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Numéro de Série</label>
        <p class="p-2 bg-gray-100 rounded">{{ device.serial_number }}</p>
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Numéro de Carton</label>
        <input v-model="form.num_carton" type="text" class="w-full border rounded p-2">
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Opérateur</label>
        <input v-model="form.operateur" type="text" class="w-full border rounded p-2" placeholder="Nom de l'opérateur">
      </div>

      <h2 class="text-xl font-bold mt-8 mb-4">Nouvelle Action</h2>
      <div class="border-t pt-4">
        <div class="mb-4">
          <label class="block text-gray-700 font-bold mb-2">Type d'action</label>
          <select v-model="actionForm.action_type" class="w-full border rounded p-2">
            <option value="TRANSFERT">Transfert</option>
            <option value="TEST">Test</option>
            <option value="POSE">Pose</option>
            <option value="DEPOSE">Dépose</option>
            <option value="AUTRE">Autre</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-gray-700 font-bold mb-2">Détails</label>
          <textarea v-model="actionForm.details" class="w-full border rounded p-2"></textarea>
        </div>

        <button @click="submitAction" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full">
          Enregistrer l'action
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const serial = route.params.serial;
const device = ref({});
const loading = ref(true);
const API_URL = 'http://127.0.0.1:8000';

const form = ref({ num_carton: '', operateur: '' });
const actionForm = ref({ action_type: 'TRANSFERT', details: '' });

onMounted(async () => {
  if (serial) {
    try {
      const res = await axios.get(`${API_URL}/devices/${serial}`);
      device.value = res.data;
      form.value.num_carton = res.data.num_carton;
      form.value.operateur = res.data.operateur;
    } catch (e) {
      console.error('Failed to load device', e);
    } finally {
      loading.value = false;
    }
  }
});

const submitAction = async () => {
  try {
    const payload = {
      device_serial: serial,
      action_type: actionForm.value.action_type,
      user_id: 'admin',
      details: actionForm.value.details
    };
    await axios.post(`${API_URL}/actions/`, payload);
    alert('Action enregistrée');
    const res = await axios.get(`${API_URL}/devices/${serial}`);
    device.value = res.data;
  } catch (e) {
    console.error('Failed to save action', e);
    alert('Erreur');
  }
};
</script>
