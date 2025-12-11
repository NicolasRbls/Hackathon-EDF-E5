<template>
  <div id="app" class="min-h-screen min-w-screen bg-white dark:bg-zinc-900 dark:text-gray-200">
    <navbar-default>
      <navbar-item-default icon="home" title="Accueil" />
      <navbar-spacer />
      <navbar-search-default placeholder="Cherchez" />
    </navbar-default>
    <!-- TODO ici implémentez la sidebar -->
    <main class="h-full w-full max-w-4xl m-auto dark:bg-zinc-900 pt-6">
      <slot/>
    </main>
  </div>
</template>

<script>
import NavbarDefault from "../navbar/navbar.vue";
import NavbarItemDefault from "../navbar/item.vue";
import NavbarSearchDefault from "../navbar/search.vue";
import NavbarSpacer from "../navbar/spacer.vue";

export default {
  name: 'layout-default',
  components: {NavbarSpacer, NavbarSearchDefault, NavbarItemDefault, NavbarDefault},
}
</script>
