<template>
  <div class="submit-page">
    <div class="card">
      <h1>Soumettre une oeuvre</h1>
      <p class="subtitle">Ajoutez un nouveau PDF à la bibliothèque.</p>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="field">
          <label for="title">Titre</label>
          <input id="title" v-model="title" type="text" required />
        </div>

        <div class="field">
          <label for="author">Auteur</label>
          <input id="author" v-model="author" type="text" required />
        </div>

        <div class="field">
          <label for="edition">Édition</label>
          <input id="edition" v-model="edition" type="text" required />
        </div>

        <div class="field">
          <label for="publicationDate">Date de parution</label>
          <input id="publicationDate" v-model="publicationDate" type="date" required />
        </div>

        <div class="field">
          <label for="file">Fichier (PDF uniquement)</label>
          <input
            id="file"
            type="file"
            accept="application/pdf"
            @change="onFileChange"
            required
          />
          <p v-if="fileName" class="file-name">Fichier sélectionné : {{ fileName }}</p>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Envoi...' : 'Soumettre' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import uploadStore from '@/services/uploadStore';

export default {
  name: 'SubmitFileView',
  data() {
    return {
      title: '',
      author: '',
      edition: '',
      publicationDate: '',
      file: null,
      fileName: '',
      loading: false,
      error: '',
      success: ''
    };
  },
  methods: {
    onFileChange(event) {
      this.error = '';
      const file = event.target.files?.[0];
      if (!file) return;
      if (file.type !== 'application/pdf') {
        this.error = 'Seuls les fichiers PDF sont acceptés.';
        this.file = null;
        this.fileName = '';
        return;
      }
      this.file = file;
      this.fileName = file.name;
    },
    async handleSubmit() {
      this.error = '';
      this.success = '';
      if (!this.title || !this.author || !this.edition || !this.publicationDate || !this.file) {
        this.error = 'Tous les champs sont requis.';
        return;
      }

      // Store file in temporary in-memory store and navigate to transcribing page
      uploadStore.setUpload(this.file, { prefix: this.title || this.file.name.split('.')[0] });
      this.$router.push({ name: 'Transcribing' });
    }
  }
};
</script>

<style scoped>
.submit-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f5f7fa;
}

.card {
  width: 100%;
  max-width: 720px;
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

h1 {
  margin: 0 0 0.5rem;
  color: #2d2d2d;
}

.subtitle {
  margin: 0 0 1.5rem;
  color: #6c7280;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

label {
  font-weight: 600;
  color: #333;
}

input[type="text"],
input[type="file"],
input[type="date"] {
  padding: 0.9rem 1rem;
  border: 1px solid #d8dde6;
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s, box-shadow 0.2s;
}

input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.file-name {
  color: #555;
  font-size: 0.95rem;
}

button {
  padding: 0.95rem 1.2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

button:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(102, 126, 234, 0.25);
}

.error {
  color: #d93025;
  font-weight: 600;
}

.success {
  color: #198754;
  font-weight: 600;
}

@media (max-width: 640px) {
  .card {
    padding: 1.6rem;
  }
}
</style>