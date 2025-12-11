<template>
  <div class="h-12 border-b-2 flex items-center gap-2 px-1 cursor-pointer">
    <Icon :name="icon" size="16" />
    <p>{{ title }}</p>
  </div>
</template>

<script>
import Icon from "../lucide/Icon.vue";

export default {
  name: 'navbar-item-default',
  components: {Icon},
  props: {
    title: String,
    icon: String
  }
}
</script>
