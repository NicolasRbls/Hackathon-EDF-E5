<template>
  <main-layout>
    <div class="min-h-screen bg-zinc-50 dark:bg-zinc-900 py-8 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">

        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-zinc-900 dark:text-white mb-2">
            Recherche de concentrateur
          </h1>
          <p class="text-zinc-600 dark:text-zinc-400">
            Recherchez un concentrateur par numéro de série et consultez son état actuel et son historique complet
          </p>
        </div>

        <!-- Search Form -->
        <div class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6 mb-8">
          <form @submit.prevent="handleSearch" class="space-y-4">
            <div class="flex gap-4">
              <div class="flex-1">
                <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Numéro de série
                </label>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Entrez le numéro de série du concentrateur"
                  class="w-full px-4 py-3 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
              <div class="flex items-end">
                <button
                  type="submit"
                  :disabled="loading"
                  class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <Icon name="search" :size="20" />
                  {{ loading ? 'Recherche...' : 'Rechercher' }}
                </button>
              </div>
            </div>

            <!-- Advanced Filters (collapsed) -->
            <div v-if="showAdvancedFilters" class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-zinc-200 dark:border-zinc-700">
              <div>
                <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Statut
                </label>
                <select
                  v-model="filters.status"
                  class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white"
                >
                  <option value="">Tous</option>
                  <option value="en_livraison">En livraison</option>
                  <option value="en_stock">En stock</option>
                  <option value="pose">Posé</option>
                  <option value="a_tester">À tester</option>
                  <option value="HS">Hors service</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Affectation
                </label>
                <select
                  v-model="filters.affectation"
                  class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white"
                >
                  <option value="">Toutes</option>
                  <option value="Magasin">Magasin</option>
                  <option value="BO Nord">BO Nord</option>
                  <option value="BO Centre">BO Centre</option>
                  <option value="BO Sud">BO Sud</option>
                  <option value="Labo">Labo</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  N° de carton
                </label>
                <input
                  v-model="filters.num_carton"
                  type="text"
                  placeholder="N° de carton"
                  class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white"
                />
              </div>
            </div>

            <button
              type="button"
              @click="showAdvancedFilters = !showAdvancedFilters"
              class="text-sm text-blue-600 dark:text-blue-400 hover:underline"
            >
              {{ showAdvancedFilters ? 'Masquer les filtres avancés' : 'Afficher les filtres avancés' }}
            </button>
          </form>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-8 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p class="text-red-600 dark:text-red-400">{{ error }}</p>
        </div>

        <!-- Device Info (if found) -->
        <div v-if="device" class="space-y-6">

          <!-- Current Status Card -->
          <div class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold text-zinc-900 dark:text-white mb-6 flex items-center gap-2">
              <Icon name="info" :size="24" />
              État actuel
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Numéro de série</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ device.serial_number }}</p>
              </div>
              <div>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Statut</p>
                <span :class="getStatusBadgeClass(device.current_status)" class="inline-block px-3 py-1 rounded-full text-sm font-medium">
                  {{ getStatusLabel(device.current_status) }}
                </span>
              </div>
              <div>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Affectation</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ device.affectation }}</p>
              </div>
              <div>
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Dernière mise à jour</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ formatDate(device.last_updated) }}</p>
              </div>
            </div>

            <div v-if="device.num_carton || device.poste_pose || device.operateur" class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 pt-6 border-t border-zinc-200 dark:border-zinc-700">
              <div v-if="device.num_carton">
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">N° de carton</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ device.num_carton }}</p>
              </div>
              <div v-if="device.poste_pose">
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Poste de pose</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ device.poste_pose }}</p>
              </div>
              <div v-if="device.operateur">
                <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-1">Opérateur</p>
                <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ device.operateur }}</p>
              </div>
            </div>

            <!-- Geolocation if available -->
            <div v-if="device.latitude && device.longitude" class="mt-6 pt-6 border-t border-zinc-200 dark:border-zinc-700">
              <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-2">Localisation</p>
              <p class="text-sm text-zinc-700 dark:text-zinc-300">
                Lat: {{ device.latitude }}, Lon: {{ device.longitude }}
              </p>
            </div>
          </div>

          <!-- History Timeline -->
          <div class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-bold text-zinc-900 dark:text-white mb-6 flex items-center gap-2">
              <Icon name="clock" :size="24" />
              Historique complet
            </h2>

            <div v-if="loadingHistory" class="text-center py-8">
              <p class="text-zinc-600 dark:text-zinc-400">Chargement de l'historique...</p>
            </div>

            <div v-else-if="history.length === 0" class="text-center py-8">
              <p class="text-zinc-600 dark:text-zinc-400">Aucun historique disponible</p>
            </div>

            <div v-else class="relative">
              <!-- Timeline Line -->
              <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-zinc-200 dark:bg-zinc-700"></div>

              <!-- Timeline Items -->
              <div class="space-y-6">
                <div
                  v-for="item in history"
                  :key="item.id"
                  class="relative pl-12"
                >
                  <!-- Timeline Dot -->
                  <div :class="getActionDotClass(item.action_type)" class="absolute left-0 w-8 h-8 rounded-full flex items-center justify-center">
                    <Icon :name="getActionIcon(item.action_type)" :size="16" class="text-white" />
                  </div>

                  <!-- Timeline Content -->
                  <div class="bg-zinc-50 dark:bg-zinc-900 rounded-lg p-4 border border-zinc-200 dark:border-zinc-700">
                    <div class="flex justify-between items-start mb-2">
                      <div>
                        <span :class="getActionBadgeClass(item.action_type)" class="inline-block px-2 py-1 rounded text-xs font-medium mb-2">
                          {{ item.action_type }}
                        </span>
                        <p class="text-sm text-zinc-600 dark:text-zinc-400">
                          {{ formatDate(item.timestamp) }}
                        </p>
                      </div>
                      <p v-if="item.user_id" class="text-sm text-zinc-600 dark:text-zinc-400">
                        Par: {{ item.user_id }}
                      </p>
                    </div>
                    <p v-if="item.details" class="text-sm text-zinc-700 dark:text-zinc-300 mt-2">
                      {{ item.details }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Search Results List (when using filters) -->
        <div v-if="!device && searchResults.length > 0" class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-bold text-zinc-900 dark:text-white mb-6">
            Résultats de recherche ({{ searchResults.length }})
          </h2>

          <div class="space-y-4">
            <div
              v-for="result in searchResults"
              :key="result.serial_number"
              @click="selectDevice(result.serial_number)"
              class="p-4 border border-zinc-200 dark:border-zinc-700 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-900 cursor-pointer transition-colors"
            >
              <div class="flex justify-between items-center">
                <div>
                  <p class="font-semibold text-zinc-900 dark:text-white">{{ result.serial_number }}</p>
                  <p class="text-sm text-zinc-600 dark:text-zinc-400">{{ result.affectation }}</p>
                </div>
                <span :class="getStatusBadgeClass(result.current_status)" class="px-3 py-1 rounded-full text-sm font-medium">
                  {{ getStatusLabel(result.current_status) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="searched && !device && searchResults.length === 0 && !error" class="bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-12 text-center">
          <Icon name="search-x" :size="48" class="mx-auto text-zinc-400 mb-4" />
          <h3 class="text-lg font-semibold text-zinc-900 dark:text-white mb-2">Aucun résultat</h3>
          <p class="text-zinc-600 dark:text-zinc-400">Aucun concentrateur ne correspond à votre recherche</p>
        </div>

      </div>
    </div>
  </main-layout>
</template>

<script setup>
import { ref } from 'vue'
import { deviceService, historyService } from '@/services/api'
import { useDashboard } from '@/composables/useDashboard'
import MainLayout from '@/components/layouts/main.vue'
import Icon from '@/components/lucide/Icon.vue'

/**
 * SearchPage Component
 *
 * Page de recherche de concentrateurs CPL permettant de :
 * - Rechercher un concentrateur par numéro de série
 * - Afficher son état actuel (statut, affectation, localisation, etc.)
 * - Consulter l'historique complet de toutes les actions effectuées
 * - Filtrer par statut, affectation, numéro de carton
 */

const { formatDate, getActionBadgeClass } = useDashboard()

// State
const searchQuery = ref('')
const showAdvancedFilters = ref(false)
const filters = ref({
  status: '',
  affectation: '',
  num_carton: ''
})

const loading = ref(false)
const loadingHistory = ref(false)
const error = ref(null)
const searched = ref(false)

const device = ref(null)
const history = ref([])
const searchResults = ref([])

// Status labels mapping
const statusLabels = {
  'en_livraison': 'En livraison',
  'en_stock': 'En stock',
  'pose': 'Posé',
  'a_tester': 'À tester',
  'HS': 'Hors service'
}

const getStatusLabel = (status) => {
  return statusLabels[status] || status
}

const getStatusBadgeClass = (status) => {
  const classes = {
    'en_livraison': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    'en_stock': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    'pose': 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
    'a_tester': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    'HS': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
  }
  return classes[status] || 'bg-zinc-100 text-zinc-800 dark:bg-zinc-900/30 dark:text-zinc-400'
}

const getActionDotClass = (actionType) => {
  const classes = {
    'RECEPTION': 'bg-blue-500',
    'POSE': 'bg-green-500',
    'DEPOSE': 'bg-red-500',
    'TRANSFERT': 'bg-purple-500',
    'TEST': 'bg-yellow-500',
    'AUTRE': 'bg-zinc-500'
  }
  return classes[actionType] || 'bg-zinc-500'
}

const getActionIcon = (actionType) => {
  const icons = {
    'RECEPTION': 'package',
    'POSE': 'plug',
    'DEPOSE': 'unplug',
    'TRANSFERT': 'truck',
    'TEST': 'flask-conical',
    'AUTRE': 'more-horizontal'
  }
  return icons[actionType] || 'circle'
}

// Methods
const handleSearch = async () => {
  error.value = null
  searched.value = true
  device.value = null
  history.value = []
  searchResults.value = []

  // If we have a specific serial number, get that device
  if (searchQuery.value.trim()) {
    await searchBySerial(searchQuery.value.trim())
  } else {
    // Otherwise use filters
    await searchWithFilters()
  }
}

const searchBySerial = async (serialNumber) => {
  loading.value = true
  try {
    const response = await deviceService.getDevice(serialNumber)
    device.value = response.data

    // Load history for this device
    await loadHistory(serialNumber)
  } catch (err) {
    console.error('Error fetching device:', err)
    if (err.response?.status === 404) {
      error.value = 'Concentrateur non trouvé'
    } else {
      error.value = err.response?.data?.detail || 'Erreur lors de la recherche'
    }
  } finally {
    loading.value = false
  }
}

const searchWithFilters = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.affectation) params.affectation = filters.value.affectation
    if (filters.value.num_carton) params.num_carton = filters.value.num_carton

    const response = await deviceService.searchDevices(params)
    searchResults.value = response.data

    if (searchResults.value.length === 1) {
      // Auto-select if only one result
      selectDevice(searchResults.value[0].serial_number)
    }
  } catch (err) {
    console.error('Error searching devices:', err)
    error.value = err.response?.data?.detail || 'Erreur lors de la recherche'
  } finally {
    loading.value = false
  }
}

const selectDevice = (serialNumber) => {
  searchQuery.value = serialNumber
  searchResults.value = []
  searchBySerial(serialNumber)
}

const loadHistory = async (serialNumber) => {
  loadingHistory.value = true
  try {
    const response = await historyService.searchHistory({
      device_serial: serialNumber,
      limit: 100
    })
    history.value = response.data.sort((a, b) =>
      new Date(b.timestamp) - new Date(a.timestamp)
    )
  } catch (err) {
    console.error('Error loading history:', err)
    // Don't show error for history, just log it
  } finally {
    loadingHistory.value = false
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
