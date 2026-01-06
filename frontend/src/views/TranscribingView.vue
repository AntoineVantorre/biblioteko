<template>
  <div class="transcribing-page">
    <div class="card">
      
      <div v-if="loading && !markdown">
        <h1>Transcription en cours</h1>
        <p class="subtitle">Le fichier est en cours de transcription en Markdown. Patientez...</p>

        <div class="loading">
          <p>{{ statusMessage }} <small v-if="startTime" class="elapsed">· écoulé {{ elapsedLabel }}</small></p>
          <div class="progress">
            <div class="progress-bar" :style="{ width: ((stepIndex + 1) / steps.length * 100) + '%' }"></div>
          </div>
        </div>
      </div>

      <div v-if="error" class="error">
        <h1>Une erreur est survenue</h1>
        <p>{{ error }}</p>
        <button @click="$router.push('/')">Réessayer</button>
      </div>

      <div v-if="markdown" class="result-container">
        <h1>Transcription terminée</h1>
        <p class="subtitle">Votre livre a été numérisé avec succès.</p>
        
        <div class="markdown-result-wrapper">
          <div class="markdown-result" v-html="sanitizedHtml"></div>
        </div>
        
        <div class="actions">
          <button @click="$router.push('/')" class="btn-secondary">Numériser un autre fichier</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import uploadStore from '@/services/uploadStore';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: 'TranscribingView',
  data() {
    return {
      loading: true,
      statusMessage: 'Démarrage...',
      error: '',
      markdown: '',
      sanitizedHtml: '',
      // Progress cycler
      steps: [
        'Envoi du fichier au serveur...',
        'Formatage des pages (format_small_book)...',
        'Préparation des images pour OCR...',
        'Transcription OCR (mistral)...',
        'Finalisation et assemblage du Markdown...'
      ],
      stepIndex: 0,
      progressInterval: null,
      timerInterval: null,
      startTime: null,
      elapsedLabel: '0s'
    };
  },
  async mounted() {
    const { file, meta } = uploadStore.getUpload();
    if (!file) {
      this.error = 'Aucun fichier trouvé pour la transcription.';
      this.loading = false;
      return;
    }

    try {
      this.statusMessage = 'Envoi du fichier au serveur...';
      this._startProgressCycler();
      const formData = new FormData();
      formData.append('file', file);
      if (meta && meta.prefix) formData.append('prefix', meta.prefix);

      this.statusMessage = 'Traitement (formatage + transcription)... ceci peut prendre plusieurs minutes. Ne quittez pas.';

      const resp = await fetch('http://localhost:8000/api/transcribe', {
        method: 'POST',
        body: formData
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || 'Erreur lors de la transcription');
      }

      const data = await resp.json();
      this.markdown = data.markdown || '';
      // Convert markdown to HTML and sanitize
      const rawHtml = marked.parse(this.markdown || '');
      // initial sanitize
      let html = DOMPurify.sanitize(rawHtml);
      // post-process: render math if katex available, otherwise keep HTML as-is
      html = await this._postProcessMath(html);
      this.sanitizedHtml = DOMPurify.sanitize(html);
      this.statusMessage = 'Transcription terminée.';
    } catch (e) {
      this.error = e.message || String(e);
    } finally {
      this._stopProgressCycler();
      this.loading = false;
      uploadStore.clearUpload();
    }
  },
  methods: {
    _startProgressCycler() {
      this.startTime = Date.now();
      this.elapsedLabel = '0s';
      // immediately set message to first step
      this.stepIndex = 0;
      this.statusMessage = this.steps[this.stepIndex];

      // rotate messages every few seconds to give user feedback
      this.progressInterval = setInterval(() => {
        this.stepIndex = (this.stepIndex + 1) % this.steps.length;
        this.statusMessage = this.steps[this.stepIndex];
      }, 3500);

      // update elapsed timer
      this.timerInterval = setInterval(() => {
        const s = Math.floor((Date.now() - this.startTime) / 1000);
        this.elapsedLabel = this._formatElapsed(s);
      }, 1000);
    },
    _stopProgressCycler() {
      if (this.progressInterval) {
        clearInterval(this.progressInterval);
        this.progressInterval = null;
      }
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },
    _formatElapsed(s) {
      const m = Math.floor(s / 60);
      const sec = s % 60;
      return m > 0 ? `${m}m ${sec}s` : `${sec}s`;
    }
    ,
    async _postProcessMath(html) {
      // try to render LaTeX math blocks using KaTeX if available
      // handle $$...$$ (display) then $...$ (inline)
      try {
          let katex = null;
          try {
            const moduleName = 'katex';
            katex = await import(moduleName);
          } catch (e) {
            katex = null;
          }
          if (katex) {
            // replace display math
            html = html.replace(/\$\$([\s\S]+?)\$\$/g, (m, tex) => {
              try { return katex.renderToString(tex, { throwOnError: false, displayMode: true }); }
              catch (e) { return m; }
            });
            // replace inline math
            html = html.replace(/\$([^\$\n]+?)\$/g, (m, tex) => {
              try { return katex.renderToString(tex, { throwOnError: false, displayMode: false }); }
              catch (e) { return m; }
            });
          }
      } catch (e) {
        // KaTeX not available — return original HTML
      }
      return html;
    }
  }
};
</script>

<style scoped>
.transcribing-page { min-height: 100vh; display:flex; align-items:center; justify-content:center; padding:2rem; background:#f5f7fa }
.card { width:100%; max-width:900px; background:white; padding:2rem; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.08) }
.subtitle { color:#666 }
.loading { padding:1rem 0 }
.error { color:#d93025; font-weight:600 }
  
.progress { height:10px; background:#eee; border-radius:6px; overflow:hidden; margin-top:8px }
.progress-bar { height:100%; background:linear-gradient(90deg,#4f46e5,#06b6d4); width:0%; transition:width 0.6s ease }
.elapsed { color:#666; font-size:0.9rem; margin-left:8px }

/* Markdown content improvements */
.markdown-result img { display:block; max-width:100%; height:auto; margin:0.75rem auto; object-fit:contain; image-orientation: from-image; -webkit-image-orientation: from-image }
.markdown-result pre { background:#0f172a; color:#e6eef8; padding:0.75rem 1rem; border-radius:8px; overflow:auto; max-width:100%; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace; font-size:0.9rem }
.markdown-result code { background:rgba(15,23,42,0.04); padding:0.15rem 0.35rem; border-radius:4px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace; word-break:break-word; white-space:pre-wrap }
.katex-display { margin:0.5rem 0 }
</style>
