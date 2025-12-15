<template>
  <div class="submit-page">
    <div class="card">
      <h1>Espace bibliothécaire</h1>
      <p class="subtitle">Tâches de modération et aperçu des dernières oeuvres.</p>

      <section class="grid">
        <div class="panel to-moderate">
          <h2>Oeuvres à modérer</h2>
          <ul>
            <li v-for="item in toModerate" :key="item.id">
              <div class="row">
                <div>
                  <strong>{{ item.title }}</strong>
                  <div class="meta-small">{{ (item.authors || []).join(', ') }} — {{ item.edition }}</div>
                </div>
                <router-link :to="{ name: 'Moderation', params: { id: item.id } }" class="btn">Modérer</router-link>
              </div>
            </li>
          </ul>
          <p v-if="toModerate.length===0" class="muted">Aucune oeuvre à modérer pour l'instant.</p>
        </div>

        <div class="panel recent">
          <h2>Dernières oeuvres ajoutées</h2>
          <ul>
            <li v-for="item in recentAdded" :key="item.id">
              <strong>{{ item.title }}</strong>
              <div class="meta-small">{{ (item.authors || []).join(', ') }} — {{ item.addedAt }}</div>
            </li>
          </ul>
        </div>

        <div class="panel accepted">
          <h2>Dernières oeuvres acceptées</h2>
          <ul>
            <li v-for="item in recentAccepted" :key="item.id">
              <strong>{{ item.title }}</strong>
              <div class="meta-small">{{ (item.authors || []).join(', ') }} — {{ item.acceptedAt }}</div>
            </li>
          </ul>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LibrarianHomeView',
  data() {
    return {
      // placeholders — replace with API data in integration
      toModerate: [
        { id: 1, title: 'Oeuvre en attente 1', authors: ['Auteur A'], edition: 'Éd. 2020' },
        { id: 2, title: 'Oeuvre en attente 2', authors: ['Auteur B'], edition: 'Éd. 1950' }
      ],
      recentAdded: [
        { id: 11, title: 'Nouveau Livre 1', authors: ['Auteur C'], addedAt: '2025-12-10' },
        { id: 12, title: 'Nouveau Livre 2', authors: ['Auteur D'], addedAt: '2025-12-09' }
      ],
      recentAccepted: [
        { id: 21, title: 'Accepté 1', authors: ['Auteur E'], acceptedAt: '2025-12-08' },
        { id: 22, title: 'Accepté 2', authors: ['Auteur F'], acceptedAt: '2025-12-05' }
      ]
    };
  }
};
</script>

<style scoped>
.submit-page { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem; background:#f5f7fa; }
.card { width:100%; max-width:1100px; background:white; padding:2.5rem; border-radius:16px; box-shadow:0 10px 30px rgba(0,0,0,0.08); }
h1 { margin:0 0 0.5rem; color:#2d2d2d }
.subtitle { margin:0 0 1.5rem; color:#6c7280 }
.grid { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:1rem }
.panel { background:#fff; border:1px solid #eef0f6; border-radius:12px; padding:1rem }
.panel h2 { margin:0 0 0.5rem; font-size:1.05rem }
ul { list-style:none; padding:0; margin:0 }
li { padding:0.6rem 0; border-bottom:1px solid #f2f4f8 }
.row { display:flex; justify-content:space-between; align-items:center }
.btn { background:#667eea; color:#fff; padding:0.45rem 0.8rem; border-radius:8px; text-decoration:none }
.meta-small { color:#6c7280; font-size:0.9rem }
.muted { color:#6c7280 }
@media (max-width:900px) { .grid { grid-template-columns: 1fr; } }
</style>
