<script setup>
import { computed } from 'vue';
import * as icons from "lucide-vue-next";

const props = defineProps({
  name: { type: String, required: true },
  size: [Number, String],
  color: String,
  strokeWidth: Number,
  defaultClass: String
});

const toPascalCase = str => str.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join('');
const icon = computed(() => icons[toPascalCase(props.name)]);
</script>

<template>
  <component
    :is="icon"
    :size="size"
    :color="color"
    :stroke-width="strokeWidth"
    :class="defaultClass"
  />
</template>
