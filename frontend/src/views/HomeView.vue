<template>
  <div class="home-container">
    <header class="hero">
      <h1 class="app-name">Biblioteko</h1>
      <p class="tagline">Votre bibliothèque numérique</p>
      <div class="cta-buttons">
        <button class="btn-primary" @click="goToLogin">Se connecter</button>
        <button class="btn-secondary" @click="goToRegister">S'inscrire</button>
      </div>
    </header>

    <section class="features">
      <div class="feature-card">
        <div class="icon">📚</div>
        <h3>Gérez vos livres</h3>
        <p>Organisez votre collection de livres facilement</p>
      </div>
      <div class="feature-card">
        <div class="icon">🔍</div>
        <h3>Recherche rapide</h3>
        <p>Trouvez vos livres en un instant</p>
      </div>
      <div class="feature-card">
        <div class="icon">📖</div>
        <h3>Suivi de lecture</h3>
        <p>Gardez une trace de vos lectures</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    goToLogin() {
      this.$router.push('/login')
    },
    goToRegister() {
      console.log('Redirection vers inscription')
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: white;
  text-align: center;
  padding: 2rem;
}

.app-name {
  font-size: 4rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: fadeInDown 1s ease-out;
}

.tagline {
  font-size: 1.5rem;
  margin: 1rem 0 2rem;
  opacity: 0.9;
  animation: fadeInUp 1s ease-out 0.2s backwards;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  animation: fadeInUp 1s ease-out 0.4s backwards;
}

.btn-primary,
.btn-secondary {
  padding: 1rem 2rem;
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
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
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

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  margin: 1rem 0;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

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

@media (max-width: 768px) {
  .app-name {
    font-size: 2.5rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
  }
}
</style>