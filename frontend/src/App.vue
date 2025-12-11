<template>
  <div id="app" class="min-h-screen bg-white dark:bg-zinc-900 dark:text-gray-200">
    <layout-default>
        <router-view />
    </layout-default>
  </div>
</template>

<script> import LayoutDefault from "./components/layouts/main.vue";

export default { name: 'App',
  components: {LayoutDefault}
} </script>
