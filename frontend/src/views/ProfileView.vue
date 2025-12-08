<template>
  <div class="profile-page">
    <section class="profile-hero">
      <div class="user-card">
        <div class="avatar">{{ initial }}</div>
        <div>
          <h1>{{ user.username }}</h1>
          <p class="email">{{ user.email || 'Email non renseigné' }}</p>
          <div class="badges">
            <span class="badge status">{{ user.status }}</span>
            <span class="badge role">{{ user.role }}</span>
            <span class="badge join">Inscrit le {{ formatDate(user.joinedAt) }}</span>
          </div>
        </div>
      </div>
      <div class="meta-grid">
        <div class="meta">
          <div class="meta-label">Oeuvres proposées</div>
          <div class="meta-value">{{ contributions.length }}</div>
        </div>
        <div class="meta">
          <div class="meta-label">Consultées récemment</div>
          <div class="meta-value">{{ recent.length }}</div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-header">
        <h2>Mes oeuvres proposées</h2>
        <small>{{ contributions.length }} oeuvre(s)</small>
      </div>
      <div v-if="contributions.length" class="cards">
        <article v-for="item in contributions" :key="item.id" class="card">
          <div class="card-title">{{ item.title }}</div>
          <div class="card-meta">
            <span>{{ item.author }}</span>
            <span>•</span>
            <span>{{ item.edition }}</span>
          </div>
          <div class="card-footer">
            <span class="chip">{{ item.status }}</span>
            <span class="date">{{ formatDate(item.submittedAt) }}</span>
          </div>
        </article>
      </div>
      <p v-else class="empty">Aucune oeuvre proposée pour l’instant.</p>
    </section>

    <section class="panel">
      <div class="panel-header">
        <h2>Consultées récemment</h2>
        <small>{{ recent.length }} oeuvre(s)</small>
      </div>
      <div v-if="recent.length" class="cards">
        <article v-for="item in recent" :key="item.id" class="card">
          <div class="card-title">{{ item.title }}</div>
          <div class="card-meta">
            <span>{{ item.author }}</span>
            <span>•</span>
            <span>{{ item.edition }}</span>
          </div>
          <div class="card-footer">
            <span class="chip neutral">Consulté</span>
            <span class="date">Le {{ formatDate(item.lastAccessed) }}</span>
          </div>
        </article>
      </div>
      <p v-else class="empty">Aucune consultation récente.</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ProfileView',
  data() {
    let parsed = {};
    try {
      const stored = localStorage.getItem('user');
      parsed = stored ? JSON.parse(stored) : {};
    } catch (e) {
      console.warn('Profil: JSON user invalide, on réinitialise.', e);
      localStorage.removeItem('user');
    }
    return {
      user: {
        username: parsed.username || 'Utilisateur',
        email: parsed.email || '',
        status: parsed.status || 'Actif',
        role: parsed.role || 'Membre',
        joinedAt: parsed.joinedAt || '2024-01-01'
      },
      contributions: [
        { id: 1, title: 'Les Étapes de la Biologie', author: 'Maurice Caullery', edition: 'PUF, 1954', status: 'En cours de modération', submittedAt: '2024-12-05' },
        { id: 2, title: 'Introduction à la Philosophie', author: 'J.-P. Sartre', edition: 'Folio', status: 'Publié', submittedAt: '2024-11-20' }
      ],
      recent: [
        { id: 3, title: 'Histoire de France', author: 'J. Bainville', edition: 'Perrin', lastAccessed: '2024-12-07' },
        { id: 4, title: 'Le Petit Prince', author: 'A. de Saint-Exupéry', edition: 'Gallimard', lastAccessed: '2024-12-06' }
      ]
    };
  },
  computed: {
    initial() {
      return this.user.username ? this.user.username.charAt(0).toUpperCase() : '?';
    }
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('fr-FR', { year: 'numeric', month: 'short', day: 'numeric' });
    }
  }
};
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.25rem 3rem;
}

.profile-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-card {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  display: grid;
  place-items: center;
  font-size: 1.8rem;
  font-weight: 700;
}

.email {
  margin: 0.25rem 0;
  opacity: 0.9;
}

.badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.badge.status { background: rgba(46, 204, 113, 0.25); border-color: rgba(46, 204, 113, 0.5); }
.badge.role { background: rgba(255, 255, 255, 0.2); }
.badge.join { background: rgba(255, 255, 255, 0.12); }

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}

.meta {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 0.9rem 1rem;
}

.meta-label { opacity: 0.9; }
.meta-value { font-size: 1.4rem; font-weight: 700; }

.panel {
  margin-top: 1.5rem;
  background: white;
  border-radius: 14px;
  padding: 1.25rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
}

.card {
  border: 1px solid #e8ecf4;
  border-radius: 12px;
  padding: 1rem;
  background: #fafbff;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.card-title {
  font-weight: 700;
  color: #222;
}

.card-meta {
  color: #666;
  display: flex;
  gap: 0.35rem;
  font-size: 0.95rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.35rem;
  font-size: 0.9rem;
}

.chip {
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  background: #e8f5e9;
  color: #2e7d32;
  font-weight: 600;
  font-size: 0.85rem;
}

.chip.neutral {
  background: #eef2ff;
  color: #3949ab;
}

.date {
  color: #888;
}

.empty {
  color: #777;
  font-style: italic;
  margin: 0;
  padding: 0.5rem 0;
}

@media (max-width: 720px) {
  .profile-hero { padding: 1.2rem; }
  .user-card { flex-direction: column; align-items: flex-start; }
}
</style>