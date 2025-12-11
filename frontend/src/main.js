import { createApp } from 'vue'
import Alpine from 'alpinejs'
import App from './App.vue'
import router from './router'
import './assets/main.css'

window.Alpine = Alpine
Alpine.start()

const app = createApp(App)

app.use(router)
app.mount('#app')

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(
      registration => {
        console.log('ServiceWorker registered:', registration)
      },
      err => {
        console.log('ServiceWorker registration failed:', err)
      }
    )
  })
}
