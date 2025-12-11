<template>
  <div class="w-full h-full relative">
    <div ref="mapContainer" class="absolute inset-0"></div>

    <div
      v-if="modal.visible"
      class="fixed inset-0 flex justify-center items-center"
      @click.self="closeModal"
    >
      <div class="text-zinc-200 p-6 rounded-lg bg-zinc-800 shadow-xl min-w-[300px]">
        <h2 class="text-xl font-bold mb-2">{{ modal.data.name }}</h2>
        <p>Valeur : {{ modal.data.value }}</p>
        <p>Coordonnées : {{ modal.data.coords }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

export default {
  name: "map-points-modal",

  data() {
    return {
      map: null,
      points: [
        { coords: [9.1497, 42.2205], name: "Station A", value: 12, size: 20 },
        { coords: [8.75, 41.93],     name: "Station B", value: 40, size: 35 },
        { coords: [9.45, 42.7],      name: "Station C", value: 80, size: 50 }
      ],
      modal: {
        visible: false,
        data: null
      }
    };
  },

  mounted() {
    this.map = new maplibregl.Map({
      container: this.$refs.mapContainer,
      style: "https://demotiles.maplibre.org/style.json",
      center: [9.1497, 42.2205],
      zoom: 7
    });

    this.map.on("load", () => {
      this.points.forEach(p => this.addPoint(p));
    });
  },

  methods: {
    addPoint(point) {
      const el = document.createElement("div");
      el.style.width = point.size + "px";
      el.style.height = point.size + "px";
      el.style.borderRadius = "50%";
      el.style.background = "rgba(220,38,38,0.9)";
      el.style.border = "2px solid white";
      el.style.cursor = "pointer";
      el.style.boxShadow = "0 0 6px rgba(0,0,0,0.5)";

      el.addEventListener("click", () => {
        this.openModal(point);
      });

      new maplibregl.Marker({ element: el })
        .setLngLat(point.coords)
        .addTo(this.map);
    },

    openModal(point) {
      this.modal.visible = true;
      this.modal.data = {
        name: point.name,
        value: point.value,
        coords: point.coords.join(", ")
      };
    },

    closeModal() {
      this.modal.visible = false;
    }
  },

  beforeUnmount() {
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }
};
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
