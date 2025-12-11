<template>
  <div id="app" class="min-h-screen bg-zinc-50 dark:bg-zinc-950 dark:text-zinc-200">
    <navbar-default>
      <navbar-item-default icon="home" title="Accueil" />
      <navbar-spacer />
      <navbar-search-default placeholder="Cherchez" />
    </navbar-default>
    <main class="min-h-screen w-full">
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
