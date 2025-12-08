<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo et lien vers accueil -->
      <router-link to="/" class="nav-logo">
        <span class="logo-icon">📚</span>
        <span class="logo-text">Biblioteko</span>
      </router-link>

      <!-- Barre de recherche -->
      <div class="nav-search">
        <span class="search-icon">🔍</span>
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="Rechercher..."
          class="search-input"
          @keyup.enter="performSearch"
        />
      </div>

      <!-- Navigation droite -->
      <div class="nav-actions">
        <!-- Si l'utilisateur n'est pas connecté -->
        <template v-if="!isAuthenticated">
          <router-link to="/login" class="nav-link">
            <span class="nav-icon">🔐</span>
            Se connecter
          </router-link>
          <button class="btn-register" @click="goToRegister">
            S'inscrire
          </button>
        </template>

        <!-- Si l'utilisateur est connecté -->
        <template v-else>
          <router-link to="/catalog" class="nav-link">
            <span class="nav-icon">📖</span>
            Catalogue
          </router-link>

          <router-link to="/submit" class="btn-new">
            + New
          </router-link>

          <router-link to="/profile" class="nav-link profile-link">
            <span class="nav-icon">👤</span>
            <span class="username">{{ userName }}</span>
          </router-link>
          <button class="btn-logout" @click="logout" title="Se déconnecter">
            <span class="nav-icon">🚪</span>
          </button>
        </template>

        <!-- Bouton menu mobile -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu">
          <span>☰</span>
        </button>
      </div>
    </div>

    <!-- Menu mobile -->
    <div class="mobile-menu" :class="{ 'is-open': mobileMenuOpen }">
      <div class="mobile-search">
        <input 
          type="text" 
          v-model="searchQuery"
          placeholder="Rechercher..."
          @keyup.enter="performSearch"
        />
        <button @click="performSearch">🔍</button>
      </div>
      
      <template v-if="!isAuthenticated">
        <router-link to="/login" class="mobile-link" @click="closeMobileMenu">
          🔐 Se connecter
        </router-link>
        <button class="mobile-btn" @click="goToRegisterMobile">
          S'inscrire
        </button>
      </template>

      <template v-else>
        <router-link to="/catalog" class="mobile-link" @click="closeMobileMenu">
          📖 Catalogue
        </router-link>
        <router-link to="/submit" class="mobile-link" @click="closeMobileMenu">
          + New
        </router-link>
        <router-link to="/profile" class="mobile-link" @click="closeMobileMenu">
          👤 Mon profil
        </router-link>
        <button class="mobile-link logout" @click="logout">
          🚪 Se déconnecter
        </button>
      </template>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      searchQuery: '',
      mobileMenuOpen: false
    }
  },
  computed: {
    isAuthenticated() {
      // Vérifier si l'utilisateur est connecté (token dans localStorage)
      return !!localStorage.getItem('token')
    },
    userName() {
      // Récupérer le nom d'utilisateur depuis localStorage
      const user = localStorage.getItem('user')
      if (user) {
        try {
          return JSON.parse(user).username || 'Profil'
        } catch (e) {
          return 'Profil'
        }
      }
      return 'Profil'
    }
  },
  methods: {
    performSearch() {
      if (this.searchQuery.trim()) {
        console.log('Recherche:', this.searchQuery)
        this.closeMobileMenu()
        // Rediriger vers la page de recherche avec query
        this.$router.push({ 
          name: 'Search', 
          query: { q: this.searchQuery } 
        }).catch(() => {
          // Route n'existe pas encore
          alert(`Recherche: ${this.searchQuery}`)
        })
      }
    },
    goToRegister() {
      this.$router.push('/register').catch(() => {
        console.log('Route register non configurée')
      })
    },
    goToRegisterMobile() {
      this.closeMobileMenu()
      this.goToRegister()
    },
    logout() {
      try {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.dispatchEvent(new Event('auth-changed'));
      } finally {
        this.closeMobileMenu();
        this.$router.push('/').catch(() => {});
      }
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    }
  },
  mounted() {
    // Écouter les changements d'authentification
    window.addEventListener('auth-changed', () => {
      this.$forceUpdate()
    })
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #667eea;
  font-size: 1.5rem;
  font-weight: 700;
  white-space: nowrap;
  transition: transform 0.3s;
}

.nav-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 1.8rem;
}

.logo-text {
  font-size: 1.5rem;
}

/* Barre de recherche */
.nav-search {
  flex: 1;
  max-width: 500px;
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 25px;
  padding: 0.5rem 1rem;
  transition: all 0.3s;
}

.nav-search:focus-within {
  background: white;
  box-shadow: 0 0 0 2px #667eea;
}

.search-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
  color: #666;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 1rem;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}

/* Actions navigation */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #555;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s;
  white-space: nowrap;
}

.nav-link:hover {
  background: #f5f7fa;
  color: #667eea;
}

.nav-icon {
  font-size: 1.2rem;
}

.username {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-link {
  background: #e8ecff;
  color: #667eea;
  font-weight: 600;
}

.profile-link:hover {
  background: #d5dcf7;
}

.btn-register,
.btn-logout {
  padding: 0.6rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-register:hover,
.btn-logout:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-logout {
  padding: 0.6rem 1rem;
  background: transparent;
  color: #666;
  border: 1px solid #ddd;
}

.btn-logout:hover {
  background: #fee;
  color: #e74c3c;
  border-color: #e74c3c;
  box-shadow: none;
}

.btn-new {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 0.6rem 1.3rem;
  border-radius: 10px;
  font-weight: 700;
  border: none;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-new:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.35);
}

/* Menu mobile */
.mobile-menu-btn {
  display: none;
  background: transparent;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #667eea;
  padding: 0.5rem;
}

.mobile-menu {
  display: none;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: #f9f9f9;
  border-top: 1px solid #eee;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.mobile-menu.is-open {
  max-height: 500px;
}

.mobile-search {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.mobile-search input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.mobile-search button {
  padding: 0.8rem 1.2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.mobile-link {
  display: block;
  padding: 1rem;
  text-decoration: none;
  color: #333;
  background: white;
  border-radius: 8px;
  transition: all 0.3s;
}

.mobile-link:hover {
  background: #667eea;
  color: white;
}

.mobile-link.logout {
  border: none;
  text-align: left;
  width: 100%;
  font-size: 1rem;
  background: white;
  color: #e74c3c;
}

.mobile-link.logout:hover {
  background: #fee;
}

.mobile-btn {
  padding: 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

/* Responsive */
@media (max-width: 968px) {
  .nav-search {
    max-width: 300px;
  }

  .username {
    display: none;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
    gap: 1rem;
  }

  .nav-search {
    display: none;
  }

  .nav-actions > *:not(.mobile-menu-btn) {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .mobile-menu {
    display: flex;
  }

  .logo-text {
    display: none;
  }
}
</style>