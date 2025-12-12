<template>
  <div class="action-form bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6">
    <!-- Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-zinc-900 dark:text-white mb-2">
        {{ formTitle }}
      </h2>
      <p class="text-sm text-zinc-600 dark:text-zinc-400">
        {{ formDescription }}
      </p>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    </div>

    <!-- Success Display -->
    <div v-if="success" class="mb-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
      <p class="text-sm text-green-600 dark:text-green-400">{{ success }}</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="space-y-5">

      <!-- Device Serial Number (if not pre-filled) -->
      <div v-if="!deviceSerial">
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Numéro de série *
        </label>
        <input
          v-model="formData.device_serial"
          type="text"
          required
          placeholder="Entrez le numéro de série"
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        />
      </div>

      <!-- Pre-filled Serial Number Display -->
      <div v-else class="p-4 bg-edf-blue-50 dark:bg-edf-blue-900/20 border border-edf-blue-200 dark:border-edf-blue-800 rounded-lg">
        <p class="text-sm text-zinc-600 dark:text-zinc-400">Numéro de série</p>
        <p class="text-lg font-semibold text-zinc-900 dark:text-white">{{ deviceSerial }}</p>
      </div>

      <!-- Action Type (if multiple allowed) -->
      <div v-if="!actionType && allowedActions.length > 1">
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Type d'action *
        </label>
        <select
          v-model="formData.action_type"
          required
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        >
          <option value="">Sélectionnez une action</option>
          <option v-for="action in allowedActions" :key="action.value" :value="action.value">
            {{ action.label }}
          </option>
        </select>
      </div>

      <!-- New Affectation (for TRANSFERT, RECEPTION) -->
      <div v-if="showAffectationField">
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Nouvelle affectation *
        </label>
        <select
          v-model="formData.new_affectation"
          required
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        >
          <option value="">Sélectionnez une affectation</option>
          <option v-for="aff in affectations" :key="aff" :value="aff">
            {{ aff }}
          </option>
        </select>
      </div>

      <!-- New Status (for most actions) -->
      <div v-if="showStatusField">
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Nouveau statut *
        </label>
        <select
          v-model="formData.new_status"
          required
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        >
          <option value="">Sélectionnez un statut</option>
          <option v-for="status in statuses" :key="status" :value="status">
            {{ getStatusLabel(status) }}
          </option>
        </select>
      </div>

      <!-- Poste Pose (for POSE action) -->
      <div v-if="currentActionType === 'POSE'">
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Poste de pose *
        </label>
        <input
          v-model="formData.poste_pose"
          type="text"
          required
          placeholder="Ex: Poste Bastia Centre"
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        />
      </div>

      <!-- Geolocation (for POSE action) -->
      <div v-if="currentActionType === 'POSE'" class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
            Latitude
          </label>
          <input
            v-model.number="formData.latitude"
            type="number"
            step="0.000001"
            placeholder="42.xxxxx"
            class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
            Longitude
          </label>
          <input
            v-model.number="formData.longitude"
            type="number"
            step="0.000001"
            placeholder="9.xxxxx"
            class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
          />
        </div>
        <div class="col-span-2">
          <button
            type="button"
            @click="getCurrentLocation"
            :disabled="loadingLocation"
            class="w-full px-4 py-2 bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-colors disabled:opacity-50"
          >
            {{ loadingLocation ? 'Récupération...' : 'Utiliser ma position actuelle' }}
          </button>
        </div>
      </div>

      <!-- Details/Comments -->
      <div>
        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
          Détails / Commentaires
        </label>
        <textarea
          v-model="formData.details"
          rows="3"
          placeholder="Informations complémentaires..."
          class="w-full px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white focus:ring-2 focus:ring-edf-orange/50 focus:border-edf-orange transition-colors"
        ></textarea>
      </div>

      <!-- Submit Button -->
      <div class="flex gap-3">
        <button
          type="submit"
          :disabled="loading"
          class="flex-1 px-6 py-3 bg-edf-orange hover:bg-edf-orange-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Enregistrement...' : submitButtonText }}
        </button>
        <button
          v-if="showCancelButton"
          type="button"
          @click="$emit('cancel')"
          class="px-6 py-3 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-300 font-medium rounded-lg transition-colors"
        >
          Annuler
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { actionService } from '@/services/api'

/**
 * ActionForm Component
 *
 * Composant réutilisable pour créer des formulaires de saisie d'actions sur les concentrateurs CPL.
 * Supporte tous les types d'actions : RECEPTION, POSE, DEPOSE, TRANSFERT, TEST, AUTRE
 *
 * @props {String} deviceSerial - Numéro de série pré-rempli (optionnel)
 * @props {String} actionType - Type d'action fixe (optionnel, sinon sélectionnable)
 * @props {Array} allowedActions - Liste des types d'actions autorisées
 * @props {String} formTitle - Titre du formulaire
 * @props {String} formDescription - Description du formulaire
 * @props {String} submitButtonText - Texte du bouton de soumission
 * @props {Boolean} showCancelButton - Afficher le bouton annuler
 * @props {Object} prefilledData - Données pré-remplies additionnelles
 *
 * @emits {Object} success - Émis lors du succès avec les données de l'action créée
 * @emits cancel - Émis lors de l'annulation
 */

const props = defineProps({
  deviceSerial: {
    type: String,
    default: null
  },
  actionType: {
    type: String,
    default: null
  },
  allowedActions: {
    type: Array,
    default: () => [
      { value: 'RECEPTION', label: 'Réception' },
      { value: 'POSE', label: 'Pose' },
      { value: 'DEPOSE', label: 'Dépose' },
      { value: 'TRANSFERT', label: 'Transfert' },
      { value: 'TEST', label: 'Test' },
      { value: 'AUTRE', label: 'Autre' }
    ]
  },
  formTitle: {
    type: String,
    default: 'Enregistrer une action'
  },
  formDescription: {
    type: String,
    default: 'Saisissez les informations de l\'action à enregistrer'
  },
  submitButtonText: {
    type: String,
    default: 'Enregistrer l\'action'
  },
  showCancelButton: {
    type: Boolean,
    default: false
  },
  prefilledData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['success', 'cancel'])

// State
const loading = ref(false)
const loadingLocation = ref(false)
const error = ref(null)
const success = ref(null)

// Dictionaries (loaded from API)
const affectations = ref([])
const statuses = ref([])

// Form data
const formData = ref({
  device_serial: props.deviceSerial || '',
  action_type: props.actionType || '',
  user_id: localStorage.getItem('username') || '',
  details: '',
  new_affectation: null,
  new_status: null,
  poste_pose: null,
  latitude: null,
  longitude: null
})

// Computed
const currentActionType = computed(() => {
  return formData.value.action_type || props.actionType
})

const showAffectationField = computed(() => {
  const type = currentActionType.value
  return type === 'TRANSFERT' || type === 'RECEPTION'
})

const showStatusField = computed(() => {
  const type = currentActionType.value
  return type !== '' // Tous sauf vide
})

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

// Methods
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    error.value = 'La géolocalisation n\'est pas supportée par votre navigateur'
    return
  }

  loadingLocation.value = true
  navigator.geolocation.getCurrentPosition(
    (position) => {
      formData.value.latitude = position.coords.latitude
      formData.value.longitude = position.coords.longitude
      loadingLocation.value = false
    },
    (err) => {
      error.value = 'Impossible de récupérer votre position : ' + err.message
      loadingLocation.value = false
    }
  )
}

const handleSubmit = async () => {
  error.value = null
  success.value = null
  loading.value = true

  try {
    // Prepare payload
    const payload = {
      device_serial: formData.value.device_serial,
      action_type: currentActionType.value,
      user_id: formData.value.user_id,
      details: formData.value.details || null,
      new_affectation: formData.value.new_affectation || null,
      new_status: formData.value.new_status || null,
      poste_pose: formData.value.poste_pose || null,
      latitude: formData.value.latitude || null,
      longitude: formData.value.longitude || null
    }

    // Remove null values
    Object.keys(payload).forEach(key => {
      if (payload[key] === null || payload[key] === '') {
        delete payload[key]
      }
    })

    const response = await actionService.createAction(payload)

    success.value = 'Action enregistrée avec succès !'

    // Emit success event
    emit('success', response.data)

    // Reset form if not pre-filled
    if (!props.deviceSerial) {
      formData.value = {
        device_serial: '',
        action_type: props.actionType || '',
        user_id: localStorage.getItem('username') || '',
        details: '',
        new_affectation: null,
        new_status: null,
        poste_pose: null,
        latitude: null,
        longitude: null
      }
    } else {
      // Reset only some fields
      formData.value.details = ''
      formData.value.new_affectation = null
      formData.value.new_status = null
      formData.value.poste_pose = null
      formData.value.latitude = null
      formData.value.longitude = null
    }

    // Clear success message after 3 seconds
    setTimeout(() => {
      success.value = null
    }, 3000)

  } catch (err) {
    console.error('Error creating action:', err)
    error.value = err.response?.data?.detail || 'Erreur lors de l\'enregistrement de l\'action'
  } finally {
    loading.value = false
  }
}

// Load dictionaries
const loadDictionaries = async () => {
  try {
    const response = await actionService.getDictionaries()
    const data = response.data

    if (data.affectations) {
      affectations.value = data.affectations
    }
    if (data.statuses) {
      statuses.value = data.statuses
    }
  } catch (err) {
    console.error('Error loading dictionaries:', err)
  }
}

// Lifecycle
onMounted(() => {
  loadDictionaries()

  // Apply prefilled data
  if (props.prefilledData) {
    Object.assign(formData.value, props.prefilledData)
  }
})

// Watch for deviceSerial changes
watch(() => props.deviceSerial, (newVal) => {
  if (newVal) {
    formData.value.device_serial = newVal
  }
})
</script>

<style scoped>
.action-form {
  max-width: 600px;
}
</style>
