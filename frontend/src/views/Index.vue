<template>
  <div class="min-h-screen bg-zinc-900 text-white">
    <!-- SIDEBAR -->
    <Sidebar>
      
      <SidebarItem icon="Home" label="Home" :active="true" />
      <SidebarItem icon="Inbox" label="Inbox" />
      <SidebarItem icon="FileText" label="Documents" />
      <SidebarItem icon="Calendar" label="Calendar" />

      <SidebarGroup title="Favorites">
        <SidebarItem label="Marketing site" />
        <SidebarItem label="Android app" />
        <SidebarItem label="Brand guidelines" />
      </SidebarGroup>

    </Sidebar>
    <!-- Contenu à droite -->
  <div class="flex-1 flex flex-col items-center justify-center gap-3 p-6 ml-10">

    <h1 class="text-5xl font-bold dark:text-white mb-2">
      EDF CPL
    </h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl w-full">

      <div class="card aspect-video grid items-center" @click="navigateTo('/bo')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">BO</h2>
      </div>


      <div class="card aspect-video grid items-center" @click="navigateTo('/magasin')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Magasin</h2>
      </div>


      <div class="card aspect-video grid items-center" @click="navigateTo('/labo')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Labo</h2>
      </div>

      <div class="card aspect-video grid items-center" @click="navigateTo('/admin')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Admin</h2>
      </div>

      <div class="card aspect-video grid items-center justify-center md:col-span-2" @click="navigateTo('/dashboard')">
          <Icon name="Briefcase" size="64" class="m-auto"/>
          <h2 class="text-center text-2xl">Dashboard</h2>
      </div>
    </div>



    </div>
  </div>
</template>

<script>
import Icon from "../components/lucide/Icon.vue";
import Sidebar from "../components/sidebar/Sidebar.vue";
import SidebarItem from "../components/sidebar/item.vue";
import SidebarGroup from "../components/sidebar/group.vue";
import SidebarSpacer from "../components/sidebar/spacer.vue";

export default {
  name: 'Home',
  components: {Icon, Sidebar, SidebarItem, SidebarGroup, SidebarSpacer},
  methods: {
    navigateTo(path) {
      this.$router.push(path)
    }
  }
}
</script>
