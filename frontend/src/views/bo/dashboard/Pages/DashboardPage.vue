<template>
  <div class="min-h-screen p-6">
    <div class="mx-auto mb-8">
      <button @click="$router.push('/')"
        class="mb-4 flex items-center hover:text-orange-500">
        <Icon name="ArrowLeft" class="pr-2"/>
        Retour
      </button>
      <h1 class="text-4xl font-bold">
        Interface <span class="text-orange-500">BO</span>
      </h1>
    </div>
    <!--todo rajouter un dashboard avec graphs etc... un truc qui fait plaisir aux managers-->
  </div>
</template>

<script>
import Icon from "../../../../components/lucide/Icon.vue";

export default {
  name: 'Manager',
  components: {Icon}
}
</script>
