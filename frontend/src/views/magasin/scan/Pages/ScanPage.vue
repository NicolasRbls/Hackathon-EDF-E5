<template>
  <div class="h-[100dvh] w-screen flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-sm p-4 flex items-center justify-between z-10 flex-none">
      <h1 class="text-xl font-bold text-gray-800 dark:text-white flex items-center">
        <Icon name="scan-line" class="mr-3 text-edf-orange" />
        Scanner
      </h1>
      <router-link :to="{ name: 'dashboard-index' }" class="text-gray-500 hover:text-gray-700">
        Fermer
      </router-link>
    </div>

    <!-- Scanner Area -->
    <div class="flex-1 relative bg-black overflow-hidden">
      <BarcodeScanner 
        v-if="!scannedDevice" 
        @scan="handleScan" 
        @error="handleError"
        class="absolute inset-0 w-full h-full"
        :rounded="false"
      />
      
      <!-- Result Overlay -->
      <transition 
        enter-active-class="transform transition duration-500 ease-out" 
        enter-from-class="translate-y-full opacity-0" 
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transform transition duration-300 ease-in"
        leave-from-class="translate-y-0 opacity-100" 
        leave-to-class="translate-y-full opacity-0"
      >
        <div v-if="scannedDevice" class="absolute inset-0 bg-gray-900 bg-opacity-95 backdrop-blur-sm p-6 flex flex-col justify-center items-center z-20">
          <div class="w-full max-w-md">
             <div class="mb-6 flex justify-between items-center text-white">
                <h2 class="text-xl font-bold">Résultat du Scan</h2>
                <button @click="resetScan" class="text-gray-400 hover:text-white">
                  <Icon name="x" size="24" />
                </button>
             </div>
             
             <DeviceCard :device="scannedDevice">
                <template #actions>
                   <button @click="resetScan" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100 transition">
                     Scanner à nouveau
                   </button>
                   <router-link 
                      :to="{ name: 'bo-device-details', params: { serial: scannedDevice.serial_number } }"
                      class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 transition flex items-center"
                   >
                     Gérer <Icon name="arrow-right" class="ml-2" size="16"/>
                   </router-link>
                </template>
             </DeviceCard>
          </div>
        </div>
      </transition>
    </div>

    <!-- Error Toast -->
     <transition enter-active-class="transition duration-300 ease-out" enter-from-class="translate-y-full opacity-0" enter-to-class="translate-y-0 opacity-100">
        <div v-if="error" class="fixed bottom-6 left-6 right-6 z-50">
            <div class="bg-red-600 text-white p-4 rounded-lg shadow-xl flex items-center justify-between max-w-md mx-auto">
                <span class="flex items-center"><Icon name="alert-circle" class="mr-2"/> {{ error }}</span>
                <button @click="error = ''"><Icon name="x" size="16" /></button>
            </div>
        </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import BarcodeScanner from "../../../../components/scanner/BarcodeScanner.vue";
import DeviceCard from "../../../../components/device/DeviceCard.vue";
import Icon from "../../../../components/lucide/Icon.vue";

const scannedDevice = ref(null);
const error = ref('');
const API_URL = 'http://127.0.0.1:8000';

const handleScan = async (code) => {
  try {
    const res = await axios.get(`${API_URL}/devices/${code}`);
    scannedDevice.value = res.data;
    error.value = '';
  } catch (err) {
    if (err.response && err.response.status === 404) {
      error.value = `Appareil ${code} introuvable.`;
    } else {
      error.value = 'Erreur de connexion.';
    }
    setTimeout(() => error.value = '', 3000);
  }
};

const handleError = (err) => {
   console.warn(err);
};

const resetScan = () => {
  scannedDevice.value = null;
  error.value = '';
};
</script>
