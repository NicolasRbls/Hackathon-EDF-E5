<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl border-t-4 border-edf-orange">
      <div>
        <!-- EDF Logo Placeholder or Title -->
        <h1 class="text-center text-4xl font-extrabold text-edf-blue tracking-tight">
          CPL <span class="text-edf-orange">Hackathon</span>
        </h1>
        <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
          Connexion
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Accédez à la plateforme de gestion des CPL
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <input type="hidden" name="remember" value="true" />
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">Identifiant</label>
            <input 
              id="username" 
              name="username" 
              type="text" 
              required 
              v-model="username"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-edf-orange focus:border-edf-orange focus:z-10 sm:text-sm" 
              placeholder="Identifiant"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Mot de passe</label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              required 
              v-model="password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-edf-orange focus:border-edf-orange focus:z-10 sm:text-sm" 
              placeholder="Mot de passe" 
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <!-- Heroicon: exclamation -->
              <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ error }}
              </p>
            </div>
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-edf-orange hover:bg-edf-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-edf-orange disabled:opacity-50 transition-colors duration-200"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- Heroicon: lock-closed -->
              <svg class="h-5 w-5 text-white/70 group-hover:text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
            </span>
            <span v-if="!isLoading">Se connecter</span>
            <span v-else>Connexion en cours...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '../../services/api';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    await authService.login(username.value, password.value);
    
    // Redirect based on Role (Basic routing logic)
    const role = authService.getUserRole();
    
    if (role === 'admin') {
      router.push('/admin');
    } else if (role === 'magasin') {
      router.push('/magasin');
    } else if (role === 'labo') {
      router.push('/labo');
    } else if (role === 'bo_nord' || role === 'bo_sud') {
      router.push('/bo');
    } else if (role === 'viewer') {
      router.push('/dashboard');
    } else {
      router.push('/'); // Fallback
    }
    
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = "Identifiant ou mot de passe incorrect.";
    } else {
      error.value = "Une erreur est revenue. Veuillez vérifier votre connexion.";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>
