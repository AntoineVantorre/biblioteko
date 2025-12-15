<template>
  <div class="submit-page">
    <div class="card">
      <h1>Modération d'une oeuvre</h1>
      <p class="subtitle">Vérifiez les détails et acceptez ou rejetez l'oeuvre soumise.</p>

      <div class="moderation-layout">
        <aside class="left-column">
          <div class="meta">
            <div class="meta-row"><strong>Titre :</strong> <span>{{ title }}</span></div>
            <div class="meta-row"><strong>Édition :</strong> <span>{{ edition }}</span></div>
            <div class="meta-row"><strong>Auteur·rice(s) :</strong> <span>{{ authorsDisplay }}</span></div>
            <div class="meta-row"><strong>Statut copyright :</strong> <span>{{ copyrightStatus }}</span></div>
          </div>

          <div class="field">
            <label>Description / Résumé</label>
            <p class="description" v-if="description">{{ description }}</p>
            <p v-else class="description muted">Aucune description fournie.</p>
          </div>

          <div class="moderation">
            <div class="field">
              <label for="comment">Commentaire du modérateur</label>
              <textarea id="comment" v-model="comment" placeholder="Expliquez la décision..." rows="4"></textarea>
            </div>

            <p v-if="error" class="error">{{ error }}</p>
            <p v-if="success" class="success">{{ success }}</p>

            <div class="actions">
              <button class="reject" :disabled="loading" @click="handleDecision('reject')">{{ loading && lastAction==='reject' ? 'En cours...' : 'Rejeter' }}</button>
              <button class="accept" :disabled="loading" @click="handleDecision('accept')">{{ loading && lastAction==='accept' ? 'En cours...' : 'Accepter' }}</button>
            </div>
          </div>
        </aside>

        <main class="right-column">
          <label>Contenu (Markdown)</label>
          <div class="content-container">
            <div class="markdown-wrapper">
              <div class="markdown-preview" v-html="renderedMarkdown"></div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: 'ModerationView',
  data() {
    return {
      // Example placeholders; in real app these will be loaded from API
      title: 'Titre de l\'oeuvre à modérer',
      edition: '1re édition',
      authors: ['Auteur Un', 'Auteur Deux'],
      copyrightStatus: 'Domaine public',
      description: 'Court résumé ou description fournie par le soumetteur.',
      contentMarkdown: '# Chapitre 1\n\nCeci est un exemple de contenu en **Markdown**.\n\n- Élément 1\n- Élément 2\n\n```\nCode exemple\n```',

      comment: '',
      loading: false,
      lastAction: null,
      error: '',
      success: ''
    };
  },
  computed: {
    authorsDisplay() {
      return this.authors.join(', ');
    },
    renderedMarkdown() {
      const md = this.contentMarkdown || '';
      try {
        return DOMPurify.sanitize(marked.parse(md));
      } catch (e) {
        return '<p class="muted">(Erreur de rendu du markdown)</p>';
      }
    }
  },
  methods: {
    async handleDecision(decision) {
      this.error = '';
      this.success = '';
      if (decision === 'reject' && !this.comment.trim()) {
        this.error = 'Un commentaire est requis pour justifier le rejet.';
        return;
      }
      this.loading = true;
      this.lastAction = decision;
      try {
        // Simulated API call - replace with real API request
        await new Promise(resolve => setTimeout(resolve, 800));

        console.log('Decision:', decision, { comment: this.comment });
        this.success = decision === 'accept' ? 'Oeuvre acceptée.' : 'Oeuvre rejetée.';
        // Reset comment after action
        this.comment = '';
      } catch (e) {
        this.error = 'Erreur lors de l\'envoi de la décision. Réessayez.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.submit-page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 0;
  background: #f5f7fa;
}

.card {
  width: 100vw;
  max-width: calc(100vw - 48px);
  margin: 0 24px;
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

h1 { margin: 0 0 0.5rem; color: #2d2d2d; }
.subtitle { margin: 0 0 1.5rem; color: #6c7280; }

.meta { display: grid; gap: 0.6rem; margin-bottom: 1rem; }
.meta-row { display:flex; gap:0.6rem; align-items:center; }
.field { display:flex; flex-direction:column; gap:0.35rem; margin-bottom:1rem; }
label { font-weight:600; color:#333; }
.description { padding:0.9rem 1rem; border-radius:10px; background:#fbfbfd; border:1px solid #eef0f6; }
.muted { color:#6c7280 }
.moderation-layout { display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem; align-items:start; }
.left-column { display:flex; flex-direction:column; gap:1rem; }
.right-column { display:flex; flex-direction:column; }
.content-container { height: calc(100vh - 180px); overflow:auto; }
.markdown-wrapper { border:1px solid #d8dde6; border-radius:10px; padding:1rem; background:#fff; min-height:200px; }
.markdown-preview h1, .markdown-preview h2, .markdown-preview h3 { margin:0.5rem 0; }
.markdown-preview pre { background:#f6f7fb; padding:0.8rem; border-radius:8px; overflow:auto; }
.markdown-preview ul { padding-left:1.25rem; margin:0.5rem 0; }

textarea { padding:0.9rem 1rem; border:1px solid #d8dde6; border-radius:10px; font-size:1rem; min-height:80px; resize:vertical; }

.moderation .actions { display:flex; gap:0.75rem; justify-content:flex-end; margin-top:0.5rem; }
button { padding:0.75rem 1.1rem; border:none; border-radius:10px; font-weight:700; cursor:pointer; }
.accept { background:#198754; color:#fff; }
.reject { background:#d93025; color:#fff; }
.error { color:#d93025; font-weight:600; }
.success { color:#198754; font-weight:600; }

@media (max-width: 640px) { .card { padding:1.6rem; } }
@media (max-width: 900px) {
  .moderation-layout { grid-template-columns: 1fr; }
  .content-container { height: auto; max-height: 60vh; }
}
</style>
