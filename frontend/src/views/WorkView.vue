<template>
  <div class="work-view">
    <header class="work-header">
      <h1>{{ work.title || ('Ouvrage #' + id) }}</h1>
      <p class="work-author" v-if="work.author">par {{ work.author }}</p>
    </header>

    <section class="work-content">
      <div v-if="work.content">
        <p>{{ work.content }}</p>
      </div>
      <div v-else>
        <p>Contenu non disponible pour l'instant. (ID = {{ id }})</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'WorkView',
  data() {
    return {
      id: this.$route.params.id,
      work: {}
    }
  },
  mounted() {
    // Placeholder: try to find work in sample lists present in other views
    // Fallback: show id-only placeholder
    // In future replace with API request to backend
    const possibleLists = [
      // try reading global window sample lists if set
      window.__SAMPLE_WORKS__
    ].filter(Boolean)

    for (const list of possibleLists) {
      const found = list.find(w => String(w.id) === String(this.id))
      if (found) { this.work = found; break }
    }
  }
}
</script>

<style scoped>
.work-view { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
.work-header h1 { margin:0 0 0.5rem 0; }
.work-author { color:#666; margin:0 0 1rem 0; }
.work-content { background:white; padding:1.5rem; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.06); }
</style>
