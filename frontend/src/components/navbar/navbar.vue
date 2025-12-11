<template>
  <header class="w-full bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-700 gap-2 h-13 sticky top-0 z-50">
    <div class="m-auto max-w-4xl h-full flex items-center gap-2 -mb-px">
      <slot />
    </div>
  </header>
</template>

<script>
export default {
  name: 'navbar-default',
}
</script>
