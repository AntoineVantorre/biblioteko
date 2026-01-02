// Configuration de base
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Fonction helper pour les requêtes
async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

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
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

// ==========================================
// AUTH
// ==========================================

export const authAPI = {
  // Connexion
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);  // OAuth2 utilise 'username'
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Email ou mot de passe incorrect');
    }

    const data = await response.json();
    // Stocker le token
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
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

  // Vérifier si connecté
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },
};

// ==========================================
// BOOKS (LIVRES)
// ==========================================

export const booksAPI = {
  // Liste tous les livres disponibles
  async getAll() {
    return fetchAPI('/books/');
  },

  // Obtenir un livre par ID
  async getById(id) {
    return fetchAPI(`/books/${id}`);
  },

  // Rechercher des livres
  async search(titre) {
    const params = titre ? `?titre=${encodeURIComponent(titre)}` : '';
    return fetchAPI(`/books/search/${params}`);
  },

  // ---- ROUTES PROTÉGÉES ----

  // Proposer une œuvre (membre)
  async proposeBook(bookData) {
    return fetchAPI('/books/propose', {
      method: 'POST',
      body: JSON.stringify(bookData),
    });
  },

  // Mes propositions
  async getMyPropositions() {
    return fetchAPI('/books/mes-propositions/');
  },

  // ---- ADMIN/BIBLIOTHÉCAIRE ----

  // Liste des livres à vérifier
  async getBooksToVerify() {
    return fetchAPI('/books/admin/a-verifier');
  },

  // Valider une œuvre
  async validateBook(id) {
    return fetchAPI(`/books/${id}/valider`, {
      method: 'PATCH',
    });
  },

  // Rejeter une œuvre
  async rejectBook(id) {
    return fetchAPI(`/books/${id}/rejeter`, {
      method: 'PATCH',
    });
  },

  // Modifier un livre
  async updateBook(id, updateData) {
    return fetchAPI(`/books/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  },

  // Supprimer un livre (admin)
  async deleteBook(id) {
    return fetchAPI(`/books/${id}`, {
      method: 'DELETE',
    });
  },
};

// ==========================================
// USERS
// ==========================================

export const usersAPI = {
  // Créer un utilisateur
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