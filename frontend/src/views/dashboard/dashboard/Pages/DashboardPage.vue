<template>
  <div class="h-full w-full grid grid-cols-4 grid-rows-3">
    <map-default class="col-span-2 row-span-2"></map-default>


  </div>
</template>

<script>
import Icon from "../../../../components/lucide/Icon.vue";
import MapDefault from "../../../../components/map/map.vue";

export default {
  name: 'dashboard',
  components: {MapDefault, Icon}
}
</script>
