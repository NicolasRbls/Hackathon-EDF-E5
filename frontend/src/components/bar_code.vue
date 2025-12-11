<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader } from '@zxing/library';


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

// Fonctions de callback pour le scan
function handleScan(result) {
  console.log('QR Code scanned:', result);
}

function handleError(err) {
  console.error('QR Code scan error:', err);
}

// Initialisation du lecteur QR à l'arrivée sur le composant
onMounted(async () => {
  codeReader = new BrowserMultiFormatReader();

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    videoRef.value.srcObject = stream;
    videoRef.value.setAttribute('playsinline', true); // iOS

    videoRef.value.play();

    // Décode le flux vidéo en temps réel
    codeReader.decodeFromVideoDevice(null, videoRef.value, (result, err) => {
      if (result) {
        emits('scan', result.getText());
        handleScan(result.getText());
      }
      if (err && !(err.message.includes('No barcode found'))) {
        emits('error', err);
        handleError(err);
      }
    });
  } catch (err) {
    emits('error', err);
    handleError(err);
  }
});

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
  <div>
    <video
      ref="videoRef"
      :width="width"
      :height="height"
    ></video>
  </div>
</template>
