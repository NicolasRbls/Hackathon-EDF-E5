<template>
  <div class="w-full flex flex-col gap-10">
    <!-- Titre -->
    <h1 class="text-4xl font-bold text-center sm:text-left">
      Interface <span class="text-orange-500">Admin</span>
    </h1>

    <!-- GRID -->
    <div class="w-full max-w-5xl mx-auto px-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-1">
          <Icon name="UserCog" size="48" class="mb-4" />
          <p class="text-xl font-semibold">blabla</p>
        </div>

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-2">
          <Icon name="Database" size="48" class="mb-4" />
          <p class="text-xl font-semibold">Données des K</p>
        </div>

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-3">
          <Icon name="Settings" size="48" class="mb-4" />
          <p class="text-xl font-semibold">bloblo</p>
        </div>

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-3">
          <Icon name="Activity" size="48" class="mb-4" />
          <p class="text-xl font-semibold">blibli</p>
        </div>

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-3">
          <Icon name="Code" size="48" class="mb-4" />
          <p class="text-xl font-semibold">Mode test</p>
        </div>

        <div class="bg-slate-500 rounded-xl p-6 flex flex-col justify-center items-center min-h-[250px] md:col-span-3">
          <Icon name="BarChart3" size="48" class="mb-4" />
          <p class="text-xl font-semibold">KPI Admin</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import Icon from "../../../../components/lucide/Icon.vue";

export default {
  name: 'Admin',
  components: { Icon }
}
</script>
