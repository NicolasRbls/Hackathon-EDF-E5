<template>
    <div class="mx-auto mb-8">
      <button @click="$router.push('/')"
        class="mb-4 flex items-center hover:text-orange-500">
        <Icon name="ArrowLeft" class="pr-2"/>
        Retour
      </button>
      <h1 class="text-4xl font-bold">
        Interface <span class="text-orange-500">Magasin</span>
      </h1>
    </div>
    <!--todo rajouter une liste des trucs qu'on peu faire en tant que technicien-->
</template>

<script>
import Icon from "../../../../components/lucide/Icon.vue";

export default {
  name: 'Staff',
  components: {Icon}
}
</script>
