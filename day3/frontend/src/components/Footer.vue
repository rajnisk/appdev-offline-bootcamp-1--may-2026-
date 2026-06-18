<template>
  <footer class="bg-light border-top mt-auto py-3">
    <div class="container text-center text-muted small">
      Task Manager &copy; {{ year }}
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      year: new Date().getFullYear(),
    }
  },
}
</script>
