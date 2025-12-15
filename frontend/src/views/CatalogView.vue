<template>
  <div class="catalog-container">
    <header class="catalog-hero">
      <h1>Catalogue</h1>
      <div class="catalog-search">
        <input v-model="searchQuery" @keyup.enter="applySearch" placeholder="Rechercher un titre, auteur, catégorie..." />
        <select v-model="groupBy">
          <option value="genre">Grouper par genre</option>
          <option value="date">Grouper par date</option>
        </select>
      </div>
    </header>

    <section class="catalog-list">
      <div v-if="Object.keys(grouped).length === 0">Aucun résultat</div>
      <div v-for="(items, key) in grouped" :key="key" class="group">
        <h2 class="group-title">{{ key }}</h2>
        <div class="books-grid">
          <BookCard v-for="book in items" :key="book.id" :book="book" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import BookCard from '@/components/BookCard.vue'
export default {
  name: 'CatalogView',
  components: { BookCard },
  data() {
    return {
      searchQuery: '',
      groupBy: 'genre',
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
    filtered() {
      const q = this.searchQuery.trim().toLowerCase()
      if (!q) return this.works
      return this.works.filter(w => {
        return (
          (w.title && w.title.toLowerCase().includes(q)) ||
          (w.author && w.author.toLowerCase().includes(q)) ||
          (w.genre && w.genre.toLowerCase().includes(q))
        )
      })
    },
    grouped() {
      const groups = {}
      if (this.groupBy === 'genre') {
        this.filtered.forEach(w => {
          const key = w.genre || 'Autre'
          if (!groups[key]) groups[key] = []
          groups[key].push(w)
        })
      } else if (this.groupBy === 'date') {
        this.filtered.forEach(w => {
          const year = w.date ? new Date(w.date).getFullYear() : 'Date inconnue'
          if (!groups[year]) groups[year] = []
          groups[year].push(w)
        })
      }
      // sort group keys
      const ordered = {}
      Object.keys(groups).sort().forEach(k => { ordered[k] = groups[k] })
      return ordered
    }
  },
  methods: {
    applySearch() {
      // nothing else for now; computed will react
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      try {
        const d = new Date(dateStr)
        return d.toLocaleDateString('fr-FR')
      } catch (e) {
        return dateStr
      }
    }
  }
}
</script>

<style scoped>
.catalog-container { padding: 2rem; max-width: 1200px; margin: 0 auto; }
.catalog-hero { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:1.5rem; }
.catalog-search { display:flex; gap:0.5rem; align-items:center; }
.catalog-search input { padding:0.5rem 0.8rem; border-radius:8px; border:1px solid #ddd; }
.catalog-search select { padding:0.5rem; border-radius:8px; }
.group { margin-bottom:2rem; }
.group-title { font-size:1.4rem; margin-bottom:1rem; color:#333; }
.books-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1rem; }
.book-card { background:white; border-radius:8px; padding:1rem; box-shadow:0 4px 12px rgba(0,0,0,0.06); }
.book-cover { height:140px; background:linear-gradient(135deg,#667eea,#764ba2); display:flex; align-items:center; justify-content:center; color:white; font-size:2rem; border-radius:4px; margin-bottom:0.8rem; }
.book-cover img { width:100%; height:100%; object-fit:cover; border-radius:4px; }
.book-title { font-weight:600; margin:0 0 0.4rem 0; }
.book-author { color:#666; margin:0 0 0.6rem 0; }
.book-meta { display:flex; justify-content:space-between; font-size:0.85rem; color:#888; }
</style>
