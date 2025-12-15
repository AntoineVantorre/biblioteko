<template>
  <div class="search-view">
    <header class="search-header">
      <h1>Résultats de recherche</h1>
      <p v-if="query">Recherche pour : « {{ query }} »</p>
      <p v-else>Entrez un terme dans la barre de recherche.</p>
    </header>

    <section class="results">
      <div v-if="filtered.length === 0" class="no-results">
        <p>Aucun résultat pour votre recherche.</p>
      </div>

      <div v-else class="books-grid">
        <BookCard v-for="book in filtered" :key="book.id" :book="book" />
      </div>
    </section>
  </div>
</template>

<script>
import BookCard from '@/components/BookCard.vue'
export default {
  name: 'SearchView',
  components: { BookCard },
  data() {
    return {
      works: [
        { id: 1, title: 'Les Étapes de la Biologie', author: 'Maurice Caullery', genre: 'Sciences', date: '1954-01-01', cover: null },
        { id: 2, title: 'Introduction à la Philosophie', author: 'Jean-Paul Sartre', genre: 'Philosophie', date: '1946-05-10', cover: null },
        { id: 3, title: 'Histoire de France', author: 'Jacques Bainville', genre: 'Histoire', date: '1930-03-12', cover: null },
        { id: 4, title: 'Le Petit Prince', author: 'Antoine de Saint-Exupéry', genre: 'Littérature', date: '1943-04-06', cover: null },
        { id: 5, title: 'Physique pour tous', author: 'Marie Curie', genre: 'Sciences', date: '1920-07-01', cover: null }
      ]
    }
  },
  computed: {
    query() {
      return (this.$route && this.$route.query && this.$route.query.q) || ''
    },
    filtered() {
      const q = (this.query || '').trim().toLowerCase()
      if (!q) return []
      return this.works.filter(w => {
        return (
          (w.title && w.title.toLowerCase().includes(q)) ||
          (w.author && w.author.toLowerCase().includes(q)) ||
          (w.genre && w.genre.toLowerCase().includes(q))
        )
      })
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      try { return new Date(dateStr).toLocaleDateString('fr-FR') } catch(e) { return dateStr }
    }
  }
}
</script>

<style scoped>
.search-view { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
.search-header h1 { margin: 0 0 0.5rem 0; }
.no-results { padding: 2rem; color: #666; }
.books-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(220px,1fr)); gap:1rem; }
.book-card { background:white; border-radius:8px; padding:1rem; box-shadow:0 4px 12px rgba(0,0,0,0.06); }
.book-cover { height:120px; background:linear-gradient(135deg,#667eea,#764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:2rem; border-radius:4px; margin-bottom:0.8rem; }
.book-cover img { width:100%; height:100%; object-fit:cover; border-radius:4px; }
.book-title { font-weight:600; margin:0 0 0.4rem 0; }
.book-author { color:#666; margin:0 0 0.6rem 0; }
.book-meta { display:flex; justify-content:space-between; font-size:0.85rem; color:#888; }
</style>
