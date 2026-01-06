// Configuration de base
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Helper unifié pour les requêtes API
 * Gère automatiquement le Token, le JSON et les erreurs.
 */
async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const config = {
    ...options,
    headers: {
      ...options.headers,
    },
  };

  // Par défaut, on utilise JSON sauf si on envoie du FormData/URLSearchParams
  if (!(options.body instanceof URLSearchParams)) {
    config.headers['Content-Type'] = 'application/json';
  }

  // Ajouter le token si disponible
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  
  // Gérer les erreurs
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Erreur réseau' }));
    throw new Error(error.detail || `Erreur ${response.status}`);
  }

  // Retourner null pour les 204 (No Content)
  if (response.status === 204) return null;

  return response.json();
}

// ==========================================
// AUTHENTIFICATION
// ==========================================

export const authAPI = {
  // Inscription
  async register(prenom, nom, email, mot_de_passe) {
    return fetchAPI('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ prenom, nom, email, mot_de_passe }),
    });
  },

  // Connexion (Utilise x-www-form-urlencoded pour OAuth2PasswordRequestForm)
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email); // Requis par FastAPI
    formData.append('password', password);

    const data = await fetchAPI('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    // Stockage local
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  // Vérifier l'email avec le code
  async verifyEmail(email, code) {
    const data = await fetchAPI('/auth/verify-email', {
      method: 'POST',
      body: JSON.stringify({ email, code }),
    });

    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  // Renvoyer le code
  async resendCode(email) {
    return fetchAPI('/auth/resend-code', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  },

  // Déconnexion
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  // Récupérer l'utilisateur connecté
  async getCurrentUser() {
    return fetchAPI('/auth/me');
  },

  // Vérifier l'état de connexion
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },
};

// ==========================================
// BOOKS (LIVRES)
// ==========================================

export const booksAPI = {
  async getAll() {
    return fetchAPI('/books/');
  },

  async getById(id) {
    return fetchAPI(`/books/${id}`);
  },

  async search(titre) {
    const params = titre ? `?titre=${encodeURIComponent(titre)}` : '';
    return fetchAPI(`/books/search${params}`);
  },

  // ---- ROUTES PROTÉGÉES ----

  async proposeBook(bookData) {
    return fetchAPI('/books/propose', {
      method: 'POST',
      body: JSON.stringify(bookData),
    });
  },

  async getMyPropositions() {
    return fetchAPI('/books/mes-propositions/');
  },

  // ---- ADMIN / MODÉRATION ----

  async getBooksToVerify() {
    return fetchAPI('/books/admin/a-verifier');
  },

  async validateBook(id) {
    return fetchAPI(`/books/${id}/valider`, { method: 'PATCH' });
  },

  async rejectBook(id) {
    return fetchAPI(`/books/${id}/rejeter`, { method: 'PATCH' });
  },

  async updateBook(id, updateData) {
    return fetchAPI(`/books/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  },

  async deleteBook(id) {
    return fetchAPI(`/books/${id}`, { method: 'DELETE' });
  },
};

// ==========================================
// USERS (ADMIN)
// ==========================================

export const usersAPI = {
  async create(userData) {
    return fetchAPI('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
};

export default {
  auth: authAPI,
  books: booksAPI,
  users: usersAPI,
};