<template>
  <div 
    class="relative w-full h-full bg-black overflow-hidden group"
    :class="{ 'rounded-lg': rounded }"
  >
    <!-- Video Element -->
    <video ref="videoRef" class="w-full h-full object-cover"></video>

    <!-- Overlay UI -->
    <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
      <!-- Scanner Frame (Wide for Barcode) -->
      <div class="relative w-80 h-40 border border-white border-opacity-20 rounded-lg">
        <!-- Corners -->
        <div class="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-blue-500 rounded-tl-lg"></div>
        <div class="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-blue-500 rounded-tr-lg"></div>
        <div class="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-blue-500 rounded-bl-lg"></div>
        <div class="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-blue-500 rounded-br-lg"></div>
        
        <!-- Scanning Line Animation (Horizontal) -->
        <div v-if="scanning" class="absolute top-1/2 left-0 w-full h-1 bg-red-500 bg-opacity-80 shadow-[0_0_10px_rgba(239,68,68,0.8)] animate-pulse-line"></div>
      </div>
      
      <p class="mt-8 text-white text-opacity-80 font-medium bg-black bg-opacity-50 px-4 py-2 rounded-full backdrop-blur-sm">
        Scannez le code-barres
      </p>
    </div>

    <!-- Controls -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-6 bg-black bg-opacity-40 p-3 rounded-full backdrop-blur-md z-10 pointer-events-auto">
       <button @click.stop="toggleCamera" class="p-2 text-white hover:text-edf-orange transition transform hover:scale-110" title="Changer de caméra">
          <Icon name="switch-camera" size="24" />
       </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="absolute top-4 left-4 right-4 bg-red-600 text-white p-3 rounded shadow-lg text-sm flex items-center z-20">
      <Icon name="alert-circle" size="20" class="mr-2" />
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader, NotFoundException } from '@zxing/library';
import Icon from "../lucide/Icon.vue";

const props = defineProps({
  autoStart: { type: Boolean, default: true },
  rounded: { type: Boolean, default: true }
});

const emits = defineEmits(['scan', 'error', 'init']);

const videoRef = ref(null);
const codeReader = new BrowserMultiFormatReader();
const scanning = ref(false);
const error = ref('');
const selectedDeviceId = ref(null);

const startScanner = async () => {
  if (scanning.value) return; 
  scanning.value = true;
  error.value = '';
  
  try {
    const videoInputDevices = await codeReader.listVideoInputDevices();
    if (videoInputDevices.length === 0) {
      throw new Error('Aucune caméra détectée.');
    }

    if (!selectedDeviceId.value) {
        selectedDeviceId.value = videoInputDevices.find(device => device.label.toLowerCase().includes('back'))?.deviceId || videoInputDevices[0].deviceId;
    }

    await codeReader.decodeFromVideoDevice(selectedDeviceId.value, videoRef.value, (result, err) => {
      if (result) {
        emits('scan', result.getText());
      }
    });
    
    emits('init', true);

  } catch (err) {
    if (err.name === 'NotAllowedError') {
        error.value = 'Accès caméra refusé.';
    } else if (err.message && err.message.includes('already playing')) {
         console.warn('Video already playing, ignoring.');
    } else {
        error.value = 'Erreur caméra: ' + (err.message || 'Inconnue');
    }
    
    if (error.value) emits('error', err);
  }
};

const stopScanner = () => {
  try {
    codeReader.reset();
  } catch(e) { console.warn(e); }
  scanning.value = false;
};

const toggleCamera = async () => {
    try {
        const devices = await codeReader.listVideoInputDevices();
        if (devices.length < 2) return;
        
        const currentIndex = devices.findIndex(d => d.deviceId === selectedDeviceId.value);
        const nextIndex = (currentIndex + 1) % devices.length;
        selectedDeviceId.value = devices[nextIndex].deviceId;
        
        stopScanner();
        setTimeout(startScanner, 200);
    } catch (e) { console.error(e); }
};

onMounted(() => {
  if (props.autoStart) {
    setTimeout(startScanner, 100);
  }
});

onBeforeUnmount(() => {
  stopScanner();
});

defineExpose({ startScanner, stopScanner });
</script>

<style scoped>
@keyframes pulse-line {
  0% { opacity: 0.4; height: 2px; }
  50% { opacity: 1; height: 3px; }
  100% { opacity: 0.4; height: 2px; }
}
.animate-pulse-line {
  animation: pulse-line 1.5s ease-in-out infinite;
}
</style>
