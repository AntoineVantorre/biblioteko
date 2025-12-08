<template>
  <div class="home-container">
    <!-- Hero section avec barre de recherche -->
    <header class="hero">
      <h1 class="app-name">Biblioteko</h1>
      <p class="tagline">Votre bibliothèque numérique collaborative</p>
      
      <!-- Barre de recherche principale (version desktop étendue) -->
      <div class="search-container">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Rechercher un livre, un auteur, une catégorie..."
            class="search-input"
            @keyup.enter="performSearch"
          />
          <button class="search-button" @click="performSearch">Rechercher</button>
        </div>
      </div>
    </header>

    <!-- Description du site -->
    <section class="description">
      <div class="description-content">
        <h2>Bienvenue sur Biblioteko</h2>
        <p class="description-text">
          Biblioteko est une plateforme collaborative de partage d'oeuvres numériques. 
          Découvrez, partagez et gérez votre collection d'oeuvres numériques en toute simplicité. 
          Notre bibliothèque communautaire vous permet d'accéder à un vaste catalogue de contenus, 
          d'emprunter des ouvrages et de contribuer à enrichir le fond commun.
        </p>
      </div>
    </section>

    <!-- Derniers contenus ajoutés -->
    <section class="latest-content">
      <div class="section-header">
        <h2>📖 Derniers livres ajoutés</h2>
        <button class="btn-see-all" @click="goToCatalog">Voir tout le catalogue →</button>
      </div>
      
      <div class="books-grid" v-if="!loading">
        <div class="book-card" v-for="book in latestBooks" :key="book.id">
          <div class="book-cover">
            <img v-if="book.cover" :src="book.cover" :alt="book.title" />
          </div>
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            <div class="book-meta">
              <span class="book-category">{{ book.category }}</span>
              <span class="book-date">{{ formatDate(book.date) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="loading" v-else>
        <p>Chargement des dernières oeuvres...</p>
      </div>
    </section>

    <!-- Fonctionnalités -->
    <section class="features">
      <h2 class="features-title">Pourquoi choisir Biblioteko ?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="icon">📚</div>
          <h3>Gérez vos oeuvres</h3>
          <p>Organisez votre collection personnelle et partagez vos médias préférés avec la communauté</p>
        </div>
        <div class="feature-card">
          <div class="icon">🔍</div>
          <h3>Recherche avancée</h3>
          <p>Trouvez rapidement les oeuvres que vous cherchez grâce à notre moteur de recherche</p>
        </div>
        <div class="feature-card">
          <div class="icon">📖</div>
          <h3>Emprunt facile</h3>
          <p>Empruntez des oeuvres numériques et gérez vos emprunts en quelques clics</p>
        </div>
        <div class="feature-card">
          <div class="icon">✨</div>
          <h3>Modération</h3>
          <p>Tous les contenus sont vérifiés pour garantir la qualité de la bibliothèque</p>
        </div>
      </div>
    </section>

    <!-- Call to action final -->
    <section class="cta-section">
      <h2>Prêt à commencer ?</h2>
      <p>Rejoignez Biblioteko dès maintenant</p>
      <div class="cta-buttons">
        <button class="btn-primary" @click="goToRegister">Créer un compte gratuitement</button>
        <button class="btn-secondary" @click="goToLogin">J'ai déjà un compte</button>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      searchQuery: '',
      loading: false,
      latestBooks: [
        {
          id: 1,
          title: 'Les Étapes de la Biologie',
          author: 'Maurice Caullery',
          category: 'Sciences',
          date: '2024-12-07',
          cover: null
        },
        {
          id: 2,
          title: 'Introduction à la Philosophie',
          author: 'Jean-Paul Sartre',
          category: 'Philosophie',
          date: '2024-12-06',
          cover: null
        },
        {
          id: 3,
          title: 'Histoire de France',
          author: 'Jacques Bainville',
          category: 'Histoire',
          date: '2024-12-05',
          cover: null
        },
        {
          id: 4,
          title: 'Le Petit Prince',
          author: 'Antoine de Saint-Exupéry',
          category: 'Littérature',
          date: '2024-12-04',
          cover: null
        }
      ]
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    },
    goToRegister() {
      this.$router.push('/register').catch(() => {
        console.log('Route register non configurée')
      })
    },
    goToCatalog() {
      this.$router.push('/catalog').catch(() => {
        console.log('Route catalog non configurée')
      })
    },
    performSearch() {
      if (this.searchQuery.trim()) {
        console.log('Recherche:', this.searchQuery)
        this.$router.push({ 
          name: 'Search', 
          query: { q: this.searchQuery } 
        }).catch(() => {
          alert(`Recherche: ${this.searchQuery}`)
        })
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays === 0) return "Aujourd'hui"
      if (diffDays === 1) return "Hier"
      if (diffDays < 7) return `Il y a ${diffDays} jours`
      return date.toLocaleDateString('fr-FR')
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.home-container {
  min-height: 100vh;
  background: #f5f7fa;
}

/* Hero section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 4rem 2rem;
}

.app-name {
  font-size: 3.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: fadeInDown 1s ease-out;
}

.tagline {
  font-size: 1.3rem;
  margin: 0 0 3rem 0;
  opacity: 0.95;
  animation: fadeInUp 1s ease-out 0.2s backwards;
}

/* Barre de recherche */
.search-container {
  max-width: 800px;
  margin: 0 auto;
  animation: fadeInUp 1s ease-out 0.3s backwards;
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 50px;
  padding: 0.5rem 0.5rem 0.5rem 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s;
}

.search-box:focus-within {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.search-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.1rem;
  padding: 0.8rem;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}

.search-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.search-button:hover {
  background: #5568d3;
  transform: scale(1.05);
}

/* Description section */
.description {
  background: white;
  padding: 4rem 2rem;
}

.description-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.description-content h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.description-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #666;
  max-width: 900px;
  margin: 0 auto 3rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.stat-item {
  padding: 1.5rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #666;
}

/* Latest content section */
.latest-content {
  padding: 4rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.btn-see-all {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-see-all:hover {
  background: #667eea;
  color: white;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.book-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.book-cover {
  width: 100%;
  height: 300px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  color: white;
}

.book-cover::before {
  content: '📖';
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-info {
  padding: 1.5rem;
}

.book-title {
  font-size: 1.2rem;
  color: #333;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.book-author {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.book-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.book-category {
  background: #e8ecff;
  color: #667eea;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.book-date {
  color: #999;
  font-size: 0.85rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

/* Features section */
.features {
  background: white;
  padding: 4rem 2rem;
}

.features-title {
  text-align: center;
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  margin: 1rem 0;
  font-size: 1.3rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* CTA section */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 5rem 2rem;
}

.cta-section h2 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
}

.cta-section p {
  font-size: 1.2rem;
  margin: 0 0 2rem 0;
  opacity: 0.95;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .app-name {
    font-size: 2.5rem;
  }

  .search-box {
    flex-direction: column;
    border-radius: 12px;
    padding: 1rem;
  }

  .search-input {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .search-button {
    width: 100%;
    border-radius: 8px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .books-grid {
    grid-template-columns: 1fr;
  }

  .description-content h2 {
    font-size: 2rem;
  }

  .features-title {
    font-size: 2rem;
  }

  .cta-buttons {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
  }
}
</style>