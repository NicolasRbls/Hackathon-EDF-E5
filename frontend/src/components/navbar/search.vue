<template>
  <div class="h-12 flex items-center gap-2 px-1">
    <Icon name="search" size="20" />
    <input :placeholder="placeholder" class="px-2 py-1 border rounded-lg block leading-[1.375rem] bg-white dark:bg-white/10 text-zinc-700 placeholder-zinc-400 dark:text-zinc-300 dark:placeholder-zinc-400 border-zinc-200 border-b-zinc-300/80 dark:border-white/10"/>
  </div>
</template>

<script>
import Icon from "../lucide/Icon.vue";

export default {
  name: 'navbar-search-default',
  components: {Icon},
  props: {
    placeholder: String,
  }
}
</script>
