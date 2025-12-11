<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Gestion des Utilisateurs</h1>
    <div class="bg-white p-6 rounded shadow max-w-lg">
      <h2 class="text-xl font-bold mb-4">Créer un utilisateur</h2>
      <form @submit.prevent="createUser">
        <div class="mb-4">
          <label class="block text-gray-700 font-bold mb-2">Nom d'utilisateur</label>
          <input v-model="form.username" type="text" class="w-full border rounded p-2" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 font-bold mb-2">Mot de passe</label>
          <input v-model="form.password" type="password" class="w-full border rounded p-2" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 font-bold mb-2">Rôle</label>
          <select v-model="form.role" class="w-full border rounded p-2">
            <option value="viewer">Viewer</option>
            <option value="magasin">Magasin</option>
            <option value="bo_nord">BO Nord</option>
            <option value="bo_centre">BO Centre</option>
            <option value="bo_sud">BO Sud</option>
            <option value="labo">Labo</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full">
          Créer
        </button>
      </form>
      <div v-if="message" :class="messageClass" class="mt-4 p-2 rounded text-center">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const form = ref({ username: '', password: '', role: 'viewer' });
const message = ref('');
const isError = ref(false);
const API_URL = 'http://127.0.0.1:8000';

const messageClass = ref('');

const createUser = async () => {
  try {
    const res = await axios.post(`${API_URL}/auth/users`, form.value);
    message.value = `Utilisateur ${res.data.username} créé !`;
    isError.value = false;
    messageClass.value = 'bg-green-100 text-green-800';
    form.value.username = '';
    form.value.password = '';
  } catch (e) {
    console.error(e);
    message.value = 'Erreur lors de la création';
    isError.value = true;
    messageClass.value = 'bg-red-100 text-red-800';
  }
};
</script>
