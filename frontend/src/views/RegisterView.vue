<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Logo et titre -->
      <div class="header">
        <div class="logo">📚</div>
        <h1>Créer un compte</h1>
        <p class="subtitle">Rejoignez Biblioteko pour accéder à notre catalogue d'œuvres numériques</p>
      </div>

      <!-- Étape 1 : Formulaire d'inscription -->
      <form v-if="step === 1" @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="prenom">Prénom *</label>
            <input
              id="prenom"
              v-model="form.prenom"
              type="text"
              placeholder="Jean"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="nom">Nom *</label>
            <input
              id="nom"
              v-model="form.nom"
              type="text"
              placeholder="Dupont"
              required
              :disabled="loading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="email">Adresse email *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="jean.dupont@example.com"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">Mot de passe *</label>
          <input
            id="password"
            v-model="form.mot_de_passe"
            type="password"
            placeholder="Minimum 6 caractères"
            minlength="6"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmer le mot de passe *</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            placeholder="Retapez votre mot de passe"
            required
            :disabled="loading"
          />
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <!-- Bouton d'inscription -->
        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="!loading">S'inscrire</span>
          <span v-else>Création en cours...</span>
        </button>

        <!-- Lien vers connexion -->
        <p class="login-link">
          Vous avez déjà un compte ? 
          <router-link to="/login">Se connecter</router-link>
        </p>
      </form>

      <!-- Étape 2 : Vérification email -->
      <div v-if="step === 2" class="verification-step">
        <div class="icon-success">✉️</div>
        <h2>Vérifiez votre email</h2>
        <p class="verification-text">
          Nous avons envoyé un code de vérification à<br />
          <strong>{{ form.email }}</strong>
        </p>

        <form @submit.prevent="handleVerifyEmail" class="verification-form">
          <div class="form-group">
            <label for="code">Code de vérification</label>
            <input
              id="code"
              v-model="verificationCode"
              type="text"
              placeholder="123456"
              maxlength="6"
              pattern="[0-9]{6}"
              required
              :disabled="loading"
              class="code-input"
            />
            <small>Entrez le code à 6 chiffres reçu par email</small>
          </div>

          <!-- Message d'erreur -->
          <div v-if="error" class="alert alert-error">
            {{ error }}
          </div>

          <!-- Message de succès -->
          <div v-if="success" class="alert alert-success">
            {{ success }}
          </div>

          <!-- Bouton de vérification -->
          <button type="submit" class="btn-primary" :disabled="loading">
            <span v-if="!loading">Vérifier mon email</span>
            <span v-else>Vérification...</span>
          </button>

          <!-- Renvoyer le code -->
          <button 
            type="button" 
            @click="handleResendCode" 
            class="btn-secondary"
            :disabled="loading || resendCooldown > 0"
          >
            {{ resendCooldown > 0 ? `Renvoyer (${resendCooldown}s)` : 'Renvoyer le code' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// État
const step = ref(1); // 1 = Inscription, 2 = Vérification
const form = ref({
  prenom: '',
  nom: '',
  email: '',
  mot_de_passe: ''
});
const confirmPassword = ref('');
const verificationCode = ref('');
const loading = ref(false);
const error = ref('');
const success = ref('');
const resendCooldown = ref(0);

// URL de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// ========================================
// ÉTAPE 1 : INSCRIPTION
// ========================================
async function handleRegister() {
  error.value = '';
  
  // Validation
  if (form.value.mot_de_passe !== confirmPassword.value) {
    error.value = 'Les mots de passe ne correspondent pas';
    return;
  }

  if (form.value.mot_de_passe.length < 6) {
    error.value = 'Le mot de passe doit contenir au moins 6 caractères';
    return;
  }

  loading.value = true;

  // 🔍 DEBUG : Afficher l'URL complète
  const url = `${API_BASE_URL}/auth/register`;
  console.log('🌐 URL appelée:', url);
  console.log('📦 Données envoyées:', form.value);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value),
    });

    console.log('📡 Statut de la réponse:', response.status);

    const data = await response.json();
    console.log('📨 Réponse reçue:', data);

    if (!response.ok) {
      throw new Error(data.detail || 'Erreur lors de l\'inscription');
    }

    // Succès - Passer à l'étape de vérification
    step.value = 2;
    
    // Si en mode dev, afficher le code
    if (data.code_debug) {
      console.log('🔐 CODE DE VÉRIFICATION (dev):', data.code_debug);
      alert(`CODE DE VÉRIFICATION (dev): ${data.code_debug}`);
    }

  } catch (err) {
    console.error('❌ Erreur complète:', err);
    
    // Afficher une erreur plus détaillée
    if (err.message === 'Failed to fetch') {
      error.value = `Impossible de contacter le serveur à ${url}. Vérifiez que le backend est démarré.`;
    } else {
      error.value = err.message;
    }
  } finally {
    loading.value = false;
  }
}

// ========================================
// ÉTAPE 2 : VÉRIFICATION EMAIL
// ========================================
async function handleVerifyEmail() {
  error.value = '';
  success.value = '';

  if (verificationCode.value.length !== 6) {
    error.value = 'Le code doit contenir 6 chiffres';
    return;
  }

  loading.value = true;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/verify-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: form.value.email,
        code: verificationCode.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Code de vérification incorrect');
    }

    // Stocker le token et les infos utilisateur
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    success.value = 'Email vérifié avec succès ! Redirection...';

    // Rediriger vers l'accueil après 1 seconde
    setTimeout(() => {
      router.push('/');
    }, 1000);

  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

// ========================================
// RENVOYER LE CODE
// ========================================
async function handleResendCode() {
  error.value = '';
  success.value = '';
  loading.value = true;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/resend-code`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: form.value.email,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Erreur lors du renvoi du code');
    }

    success.value = 'Un nouveau code a été envoyé à votre email';

    // Cooldown de 60 secondes
    resendCooldown.value = 60;
    const interval = setInterval(() => {
      resendCooldown.value--;
      if (resendCooldown.value <= 0) {
        clearInterval(interval);
      }
    }, 1000);

  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
}

.register-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 100%;
  padding: 3rem 2.5rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 3rem;
  margin-bottom: 1rem;
}

h1 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.95rem;
  line-height: 1.5;
}

.register-form {
  margin-top: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

small {
  display: block;
  margin-top: 0.25rem;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.alert-error {
  background-color: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.alert-success {
  background-color: #efe;
  color: #3c3;
  border: 1px solid #cfc;
}

.btn-primary,
.btn-secondary {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover:not(:disabled) {
  background: #f0f2ff;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 1.5rem;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Étape vérification */
.verification-step {
  text-align: center;
}

.icon-success {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.verification-step h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.verification-text {
  color: #7f8c8d;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.verification-form {
  margin-top: 2rem;
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 0.5rem;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 600px) {
  .register-card {
    padding: 2rem 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 1.5rem;
  }
}
</style>