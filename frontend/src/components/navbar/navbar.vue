<template>
  <header class="w-full px-5 bg-white dark:bg-zinc-900 border-b border-edf-orange/20 dark:border-edf-orange/30 gap-2 h-13 sticky top-0 z-50">
    <div class="m-auto max-w-4xl h-full flex items-center gap-2 -mb-px">
      <slot />
      <div class="px-1 cursor-pointer hover:drop-shadow-sm" @click="logout">Se déconnectez</div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'navbar-default',
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
}
</script>
