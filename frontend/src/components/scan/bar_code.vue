<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader } from '@zxing/library';
import { useFetch } from '@vueuse/core'; // si tu utilises VueUse

// Props pour la taille de la vidéo
const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 200 }
});

// Événements pour transmettre les résultats
const emits = defineEmits(['scan', 'error']);

// Référence vers la balise video
const videoRef = ref(null);
let codeReader;
async function handleScan(result) {
  console.log('QR Code scanned:', result);

  const serial_number = result.trim();
  if (!serial_number) return console.error('QR Code is empty');

  try {
    console.log('Fetching device data for:', serial_number);
    
    // Utiliser fetch natif au lieu de useFetch
    const response = await fetch(`/devices/?serial_number=${encodeURIComponent(serial_number)}`);
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      console.error('HTTP Error:', response.status, response.statusText);
      return;
    }

    const data = await response.json();
    console.log('Raw API Response:', data);
    console.log('Response type:', typeof data);
    console.log('Is array?', Array.isArray(data));

    // Gérer tableau ou objet
    const device = Array.isArray(data) ? data[0] : data;
    
    if (!device) {
      console.warn('No device found in response');
      return;
    }

    console.log('Device object:', device);

    // Afficher les champs spécifiques
    console.log('=== Device Details ===');
    ['num_carton', 'operateur', 'poste_pose', 'current_status', 'affectation', 'latitude', 'longitude', 'last_updated']
      .forEach(key => {
        console.log(`${key}:`, device[key]);
      });

    // Afficher TOUTES les propriétés
    console.log('=== All Properties ===');
    Object.entries(device).forEach(([key, value]) => {
      console.log(`${key}:`, value);
    });

  } catch (err) {
    console.error('Fetch error:', err);
    console.error('Error details:', err.message);
  }
}

// Nettoyage à la destruction du composant
onBeforeUnmount(() => {
  if (codeReader) codeReader.reset();
  if (videoRef.value && videoRef.value.srcObject) {
    const tracks = videoRef.value.srcObject.getTracks();
    tracks.forEach(track => track.stop());
  }
});
</script>

<template>
  <div>
    <video
      ref="videoRef"
      :width="width"
      :height="height"
    ></video>
  </div>
</template>
