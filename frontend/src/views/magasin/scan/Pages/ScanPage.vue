<script setup>
import { ref, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader, NotFoundException } from '@zxing/library';
import api from '../../../../services/api'; // Chemin relatif temporaire

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 200 }
});

const emits = defineEmits(['scan', 'error']);
const videoRef = ref(null);
let codeReader = null;
let stream = null;
const scanning = ref(false);

// Fonction appelée quand un QR code est scanné
async function handleScan(result) {
  console.log('QR Code scanned:', result);

  const serial_number = result.trim();
  if (!serial_number) {
    console.error('QR Code is empty');
    return;
  }

  try {
    console.log('Fetching device data for:', serial_number);
    
    // Essayer avec le serial_number directement dans l'URL
    const response = await api.get(`/devices/${serial_number}`);
    
    console.log('Response status:', response.status);
    console.log('Raw API Response:', response.data);
    console.log('Response type:', typeof response.data);
    console.log('Is array?', Array.isArray(response.data));

    const device = Array.isArray(response.data) ? response.data[0] : response.data;
    
    if (!device) {
      console.warn('No device found in response');
      return;
    }

    console.log('Device object:', device);

    Object.entries(device).forEach(([key, value]) => {
      console.log(`  ${key}:`, value);
    });

    // Émettre l'événement avec toutes les données
    emits('scan', device);
    
    return device;

  } catch (err) {
    console.error('💥 Fetch error:', err);
    console.error('📄 Error message:', err.message);
    
    if (err.response) {
      console.error('🚨 Response status:', err.response.status);
      console.error('📝 Response data:', err.response.data);
    } else if (err.request) {
      console.error('📡 No response received');
    }
    
    emits('error', err);
  }
}

// Fonction appelée en cas d'erreur
function handleError(err) {
  console.error('QR Code scan error:', err);
}

// Démarrer le scan
async function startScan() {
  if (scanning.value) return;
  scanning.value = true;

  codeReader = new BrowserMultiFormatReader();

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    videoRef.value.srcObject = stream;
    videoRef.value.setAttribute('playsinline', true);
    await videoRef.value.play();

    codeReader.decodeFromVideoDevice(null, videoRef.value, (result, err) => {
      if (result) {
        const text = result.getText();
        handleScan(text); // ← Appelle handleScan qui fait l'appel API

        // Arrêter le scan automatiquement
        codeReader.reset();
        scanning.value = false;
      }

      if (err && !(err instanceof NotFoundException)) {
        emits('error', err);
        handleError(err);
      }
    });

  } catch (err) {
    emits('error', err);
    handleError(err);
    scanning.value = false;
  }
}

// Nettoyage
onBeforeUnmount(() => {
  if (codeReader) {
    codeReader.reset();
  }
  if (videoRef.value && videoRef.value.srcObject) {
    const tracks = videoRef.value.srcObject.getTracks();
    tracks.forEach(track => track.stop());
  }
});
</script>

<template>
  <div class="flex flex-col items-center gap-4">
    <video
      ref="videoRef"
      :width="width"
      :height="height"
      class="border border-gray-300 rounded bg-black"
    ></video>

    <button
      @click="startScan"
      :disabled="scanning"
      class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
    >
      {{ scanning ? 'Scan en cours...' : 'Démarrer le scan' }}
    </button>
  </div>
</template>

<style scoped>
video {
  object-fit: cover;
}
</style>