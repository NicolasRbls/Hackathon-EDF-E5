<script setup>
import { ref, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader, NotFoundException } from '@zxing/library';

// Props pour la taille de la vidéo
const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 200 }
});

// Événements pour transmettre les résultats
const emits = defineEmits(['scan', 'error']);

// Référence vers la balise video
const videoRef = ref(null);
let codeReader = null;
let stream = null;

// Flag pour savoir si le scan est actif
const scanning = ref(false);

// Fonction appelée quand un QR code est scanné
function handleScan(result) {
  console.log('QR Code scanned:', result);
}

// Fonction appelée en cas d'erreur
function handleError(err) {
  console.error('QR Code scan error:', err);
}

// Démarrer le scan
async function startScan() {
  if (scanning.value) return; // Evite plusieurs scans en parallèle
  scanning.value = true;

  codeReader = new BrowserMultiFormatReader();

  try {
    // Accès à la caméra arrière
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    videoRef.value.srcObject = stream;
    videoRef.value.setAttribute('playsinline', true); // iOS
    await videoRef.value.play();

    // Scanner le flux vidéo en continu
    codeReader.decodeFromVideoDevice(null, videoRef.value, (result, err) => {
      if (result) {
        const text = result.getText();
        emits('scan', text);
        handleScan(text);

        // Arrêter le scan automatiquement dès qu’un QR code est détecté
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

// Nettoyage à la destruction du composant
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
