<template>
  <div class="min-h-screen flex flex-col items-center justify-center gap-3">

    <h1 class="text-5xl font-bold dark:text-white mb-2">
      EDF CPL
    </h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl w-full">
      <div class="card aspect-video grid items-center" @click="navigateTo('/staff')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Vous êtes Technicien</h2>
      </div>


      <div class="card aspect-video grid items-center" @click="navigateTo('/manager')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Vous êtes Manager</h2>
      </div>
    </div>
  </div>
</template>

<script>
import Icon from "../components/lucide/Icon.vue";

export default {
  name: 'Home',
  components: {Icon},
  methods: {
    navigateTo(path) {
      this.$router.push(path)
    }
  }
}
</script>
