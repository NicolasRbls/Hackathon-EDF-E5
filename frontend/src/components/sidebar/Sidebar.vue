<template>
  <div class="fixed inset-y-0 left-0 w-64 bg-gray-900 text-white flex flex-col">
    <div class="h-full w-full flex flex-col gap-2 p-4">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'sidebar-default',
}
</script>
