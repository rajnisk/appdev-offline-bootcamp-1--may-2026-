<template>
  <div class="d-flex flex-column min-vh-100">
    <NavBar />
    <main class="container py-4 flex-grow-1">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: { NavBar, Footer },
}
</script>
