<template>
  <router-link :to="destination" class="book-card-link">
    <div class="book-card-root">
      <div class="book-cover">
        <img v-if="book.cover" :src="book.cover" :alt="book.title" />
      </div>
      <div class="book-info">
        <h3 class="book-title">{{ book.title }}</h3>
        <p class="book-author">{{ book.author }}</p>
        <div class="book-meta">
          <span class="book-category">{{ book.genre || book.category }}</span>
          <span class="book-date">{{ formattedDate }}</span>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'BookCard',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    },
    destination() {
      if (this.isAuthenticated) {
        return { name: 'Work', params: { id: this.book.id } }
      }
      // redirect to login with return path
      return { name: 'Login', query: { redirect: `/works/${this.book.id}` } }
    },
    formattedDate() {
      const d = this.book.date
      if (!d) return ''
      try { return new Date(d).toLocaleDateString('fr-FR') } catch(e){ return d }
    }
  }
}
</script>

<style scoped>
.book-card-link { text-decoration: none; color: inherit; display: block; cursor: pointer; }
.book-card-root {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: transform 220ms ease, box-shadow 220ms ease;
  will-change: transform;
}
.book-card-link:hover .book-card-root,
.book-card-link:focus .book-card-root {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
.book-card-link:focus { outline: none; }
.book-cover {
  height: 160px;
  background: linear-gradient(135deg,#667eea,#764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  border-radius: 6px;
  margin-bottom: 0.8rem;
  overflow: hidden;
  transition: transform 280ms ease;
}
.book-card-link:hover .book-cover { transform: translateY(-4px) scale(1.03); }
.book-cover img { width:100%; height:100%; object-fit:cover; }
.book-title { font-weight:600; margin:0 0 0.4rem 0; }
.book-author { color:#666; margin:0 0 0.6rem 0; }
.book-meta { display:flex; justify-content:space-between; font-size:0.85rem; color:#888; margin-top:auto; }
</style>
