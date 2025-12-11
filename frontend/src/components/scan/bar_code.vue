<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserMultiFormatReader } from '@zxing/library';
import api from '@/services/api';

console.log('🚀 BARE_CODE.VUE IS LOADING');

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 200 }
});

const emits = defineEmits(['scan', 'error']);
const videoRef = ref(null);
let codeReader;

async function handleScan(result) {
  console.log('═══════════════════════════════════════');
  console.log('🔍 [BARE_CODE] QR SCANNED:', result);
  console.log('═══════════════════════════════════════');

  const serial_number = result.trim();
  if (!serial_number) {
    console.error('❌ QR Code is empty');
    return;
  }

  try {
    console.log('📡 Calling API with serial_number:', serial_number);
    console.log('🌐 API URL:', '/devices/');
    console.log('🔑 Params:', { serial_number });
    
    const response = await api.get('/devices/', {
      params: { serial_number }
    });
    
    console.log('═══ API RESPONSE ═══');
    console.log('Status:', response.status);
    console.log('Headers:', response.headers);
    console.log('Data:', response.data);
    console.log('Data type:', typeof response.data);
    console.log('Is array?', Array.isArray(response.data));
    console.log('═══════════════════');

    const device = Array.isArray(response.data) ? response.data[0] : response.data;
    
    if (!device) {
      console.warn('⚠️ No device in response');
      return;
    }

    console.log('✨ DEVICE OBJECT:', JSON.stringify(device, null, 2));

    console.log('═══ ALL DEVICE PROPERTIES ═══');
    Object.entries(device).forEach(([key, value]) => {
      console.log(`  📌 ${key}:`, value);
    });
    console.log('═══════════════════════════════');

    emits('scan', device);
    return device;

  } catch (err) {
    console.error('═══ ERROR ═══');
    console.error('💥 Error object:', err);
    console.error('Message:', err.message);
    console.error('Stack:', err.stack);
    
    if (err.response) {
      console.error('Response status:', err.response.status);
      console.error('Response data:', err.response.data);
      console.error('Response headers:', err.response.headers);
    } else if (err.request) {
      console.error('Request made but no response:', err.request);
    } else {
      console.error('Error config:', err.config);
    }
    console.error('═══════════════');
  }
}

onMounted(async () => {
  console.log('📷 [BARE_CODE] onMounted - Initializing scanner...');
  
  try {
    codeReader = new BrowserMultiFormatReader();
    console.log('✅ CodeReader created');
    
    await codeReader.decodeFromVideoDevice(null, videoRef.value, (result, err) => {
      if (result) {
        console.log('🎯 Decode callback triggered with result:', result.getText());
        handleScan(result.getText());
      }
      if (err && err.name !== 'NotFoundException') {
        console.error('❌ Decode error:', err);
      }
    });
    
    console.log('✅ [BARE_CODE] Scanner started successfully');
    
  } catch (err) {
    console.error('❌ Scanner init failed:', err);
  }
});

onBeforeUnmount(() => {
  console.log('🧹 [BARE_CODE] Cleaning up...');
  if (codeReader) codeReader.reset();
  if (videoRef.value?.srcObject) {
    videoRef.value.srcObject.getTracks().forEach(t => t.stop());
  }
});
</script>

<template>
  <div class="qr-scanner">
    <video ref="videoRef" :width="width" :height="height" playsinline></video>
  </div>
</template>

<style scoped>
.qr-scanner { 
  display: flex; 
  justify-content: center; 
  background: #f0f0f0;
  padding: 20px;
}
video { 
  border: 4px solid #ff0000; /* ROUGE pour être sûr que c'est le bon composant */
  border-radius: 8px; 
  background: #000; 
}
</style>