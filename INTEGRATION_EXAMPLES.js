// ============================================================================
// FINANCE TRACKER - ESEMPI DI INTEGRAZIONE PER PROGETTO finance-tracker-1316
// ============================================================================

// ----------------------------------------------------------------------------
// 1. CONFIGURAZIONE API BASE
// ----------------------------------------------------------------------------

// File: src/config/api.js (o src/utils/api.js)

import axios from 'axios';

// URL del backend condiviso
const API_BASE_URL = 'https://expo-finance-1.preview.emergentagent.com/api';

// Crea istanza axios configurata
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 secondi
});

// Interceptor: aggiungi automaticamente il token JWT a ogni richiesta
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor: gestisci errori globali (es. token scaduto)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token scaduto o non valido - effettua logout
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// ----------------------------------------------------------------------------
// 2. SERVIZIO AUTENTICAZIONE
// ----------------------------------------------------------------------------

// File: src/services/authService.js

import api from '../config/api';

export const authService = {
  // Registrazione nuovo utente
  register: async (email, password, name) => {
    try {
      const response = await api.post('/auth/register', {
        email,
        password,
        name,
      });
      
      // Salva token e dati utente
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('user', JSON.stringify({
        id: response.data.id,
        email: response.data.email,
        name: response.data.name,
      }));
      
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registrazione fallita');
    }
  },

  // Login utente esistente
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      
      // Salva token e dati utente
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('user', JSON.stringify({
        id: response.data.id,
        email: response.data.email,
        name: response.data.name,
      }));
      
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login fallito');
    }
  },

  // Logout
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = '/login';
  },

  // Ottieni utente corrente
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Verifica se utente è autenticato
  isAuthenticated: () => {
    return !!localStorage.getItem('authToken');
  },
};

// ----------------------------------------------------------------------------
// 3. SERVIZIO TRANSAZIONI
// ----------------------------------------------------------------------------

// File: src/services/transactionService.js

import api from '../config/api';

export const transactionService = {
  // Ottieni tutte le transazioni
  getAll: async () => {
    try {
      const response = await api.get('/transactions');
      return response.data;
    } catch (error) {
      throw new Error('Errore nel recupero delle transazioni');
    }
  },

  // Crea nuova transazione
  create: async (transactionData) => {
    try {
      const response = await api.post('/transactions', {
        type: transactionData.type, // 'income' o 'expense'
        amount: parseFloat(transactionData.amount),
        category: transactionData.category,
        description: transactionData.description || '',
        date: transactionData.date || new Date().toISOString(),
      });
      return response.data;
    } catch (error) {
      throw new Error('Errore nella creazione della transazione');
    }
  },

  // Elimina transazione
  delete: async (transactionId) => {
    try {
      const response = await api.delete(`/transactions/${transactionId}`);
      return response.data;
    } catch (error) {
      throw new Error('Errore nell\'eliminazione della transazione');
    }
  },
};

// ----------------------------------------------------------------------------
// 4. SERVIZIO BUDGET
// ----------------------------------------------------------------------------

// File: src/services/budgetService.js

import api from '../config/api';

export const budgetService = {
  // Ottieni tutti i budget
  getAll: async () => {
    try {
      const response = await api.get('/budgets');
      return response.data;
    } catch (error) {
      throw new Error('Errore nel recupero dei budget');
    }
  },

  // Crea nuovo budget
  create: async (budgetData) => {
    try {
      const response = await api.post('/budgets', {
        category: budgetData.category,
        limit: parseFloat(budgetData.limit),
        period: budgetData.period, // 'monthly' o 'weekly'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Errore nella creazione del budget');
    }
  },

  // Aggiorna budget esistente
  update: async (budgetId, budgetData) => {
    try {
      const response = await api.put(`/budgets/${budgetId}`, {
        category: budgetData.category,
        limit: parseFloat(budgetData.limit),
        period: budgetData.period,
      });
      return response.data;
    } catch (error) {
      throw new Error('Errore nell\'aggiornamento del budget');
    }
  },

  // Elimina budget
  delete: async (budgetId) => {
    try {
      const response = await api.delete(`/budgets/${budgetId}`);
      return response.data;
    } catch (error) {
      throw new Error('Errore nell\'eliminazione del budget');
    }
  },
};

// ----------------------------------------------------------------------------
// 5. SERVIZIO OBIETTIVI
// ----------------------------------------------------------------------------

// File: src/services/goalService.js

import api from '../config/api';

export const goalService = {
  // Ottieni tutti gli obiettivi
  getAll: async () => {
    try {
      const response = await api.get('/goals');
      return response.data;
    } catch (error) {
      throw new Error('Errore nel recupero degli obiettivi');
    }
  },

  // Crea nuovo obiettivo
  create: async (goalData) => {
    try {
      const response = await api.post('/goals', {
        name: goalData.name,
        target_amount: parseFloat(goalData.target_amount),
        deadline: goalData.deadline, // ISO 8601 string
      });
      return response.data;
    } catch (error) {
      throw new Error('Errore nella creazione dell\'obiettivo');
    }
  },

  // Aggiungi contributo a obiettivo
  contribute: async (goalId, amount) => {
    try {
      const response = await api.put(
        `/goals/${goalId}/contribute?amount=${parseFloat(amount)}`
      );
      return response.data;
    } catch (error) {
      throw new Error('Errore nell\'aggiunta del contributo');
    }
  },

  // Elimina obiettivo
  delete: async (goalId) => {
    try {
      const response = await api.delete(`/goals/${goalId}`);
      return response.data;
    } catch (error) {
      throw new Error('Errore nell\'eliminazione dell\'obiettivo');
    }
  },
};

// ----------------------------------------------------------------------------
// 6. SERVIZIO STATISTICHE
// ----------------------------------------------------------------------------

// File: src/services/statsService.js

import api from '../config/api';

export const statsService = {
  // Ottieni tutte le statistiche
  get: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
      /* Ritorna:
      {
        total_income: 4000.00,
        total_expenses: 1250.00,
        balance: 2750.00,
        category_expenses: {
          "Alimentari": 500.00,
          "Trasporti": 300.00,
          ...
        },
        recent_income: 2000.00,
        recent_expenses: 650.00,
        transaction_count: 25
      }
      */
    } catch (error) {
      throw new Error('Errore nel recupero delle statistiche');
    }
  },
};

// ----------------------------------------------------------------------------
// 7. SERVIZIO CONSIGLI AI
// ----------------------------------------------------------------------------

// File: src/services/adviceService.js

import api from '../config/api';

export const adviceService = {
  // Ottieni consigli finanziari personalizzati
  get: async (context = '') => {
    try {
      const response = await api.post('/advice', {
        context: context, // Domanda opzionale
      });
      return response.data.advice;
    } catch (error) {
      throw new Error('Errore nel recupero dei consigli');
    }
  },
};

// ----------------------------------------------------------------------------
// 8. ESEMPIO COMPONENTE REACT - LOGIN
// ----------------------------------------------------------------------------

// File: src/components/Login.jsx

import React, { useState } from 'react';
import { authService } from '../services/authService';

function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await authService.login(email, password);
      } else {
        await authService.register(email, password, name);
      }
      // Redirect alla dashboard
      window.location.href = '/dashboard';
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>{isLogin ? 'Accedi' : 'Registrati'}</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <input
            type="text"
            placeholder="Nome"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required={!isLogin}
          />
        )}
        
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        
        <button type="submit" disabled={loading}>
          {loading ? 'Caricamento...' : isLogin ? 'Accedi' : 'Registrati'}
        </button>
      </form>
      
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Non hai un account? Registrati' : 'Hai già un account? Accedi'}
      </button>
    </div>
  );
}

export default Login;

// ----------------------------------------------------------------------------
// 9. ESEMPIO COMPONENTE REACT - DASHBOARD
// ----------------------------------------------------------------------------

// File: src/components/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { statsService } from '../services/statsService';
import { authService } from '../services/authService';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await statsService.get();
      setStats(data);
    } catch (err) {
      setError('Errore nel caricamento delle statistiche');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
  };

  if (loading) return <div>Caricamento...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!stats) return null;

  return (
    <div className="dashboard">
      <header>
        <h1>Dashboard</h1>
        <button onClick={handleLogout}>Logout</button>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Saldo Totale</h3>
          <p className={stats.balance >= 0 ? 'positive' : 'negative'}>
            €{stats.balance.toFixed(2)}
          </p>
        </div>

        <div className="stat-card">
          <h3>Entrate Totali</h3>
          <p className="positive">€{stats.total_income.toFixed(2)}</p>
        </div>

        <div className="stat-card">
          <h3>Spese Totali</h3>
          <p className="negative">€{stats.total_expenses.toFixed(2)}</p>
        </div>

        <div className="stat-card">
          <h3>Transazioni</h3>
          <p>{stats.transaction_count}</p>
        </div>
      </div>

      <div className="recent-activity">
        <h2>Ultimi 30 giorni</h2>
        <div className="activity-grid">
          <div>
            <p>Entrate: €{stats.recent_income.toFixed(2)}</p>
          </div>
          <div>
            <p>Uscite: €{stats.recent_expenses.toFixed(2)}</p>
          </div>
        </div>
      </div>

      {Object.keys(stats.category_expenses).length > 0 && (
        <div className="categories">
          <h2>Spese per Categoria</h2>
          <ul>
            {Object.entries(stats.category_expenses).map(([category, amount]) => (
              <li key={category}>
                <span>{category}</span>
                <span>€{amount.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

// ----------------------------------------------------------------------------
// 10. ESEMPIO COMPONENTE REACT - TRANSAZIONI
// ----------------------------------------------------------------------------

// File: src/components/Transactions.jsx

import React, { useState, useEffect } from 'react';
import { transactionService } from '../services/transactionService';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState({
    type: 'expense',
    amount: '',
    category: 'Alimentari',
    description: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      const data = await transactionService.getAll();
      setTransactions(data);
    } catch (err) {
      alert('Errore nel caricamento delle transazioni');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await transactionService.create({
        ...formData,
        date: new Date(formData.date).toISOString(),
      });
      setShowForm(false);
      setFormData({
        type: 'expense',
        amount: '',
        category: 'Alimentari',
        description: '',
        date: new Date().toISOString().split('T')[0],
      });
      loadTransactions();
    } catch (err) {
      alert('Errore nella creazione della transazione');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Vuoi eliminare questa transazione?')) {
      try {
        await transactionService.delete(id);
        loadTransactions();
      } catch (err) {
        alert('Errore nell\'eliminazione');
      }
    }
  };

  if (loading) return <div>Caricamento...</div>;

  return (
    <div className="transactions">
      <header>
        <h1>Transazioni</h1>
        <button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annulla' : 'Nuova Transazione'}
        </button>
      </header>

      {showForm && (
        <form onSubmit={handleSubmit} className="transaction-form">
          <select
            value={formData.type}
            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
          >
            <option value="expense">Uscita</option>
            <option value="income">Entrata</option>
          </select>

          <input
            type="number"
            step="0.01"
            placeholder="Importo"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
            required
          />

          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          >
            <option>Alimentari</option>
            <option>Trasporti</option>
            <option>Intrattenimento</option>
            <option>Bollette</option>
            <option>Salute</option>
            <option>Shopping</option>
            <option>Stipendio</option>
            <option>Altro</option>
          </select>

          <input
            type="text"
            placeholder="Descrizione (opzionale)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />

          <input
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />

          <button type="submit">Crea Transazione</button>
        </form>
      )}

      <div className="transaction-list">
        {transactions.length === 0 ? (
          <p>Nessuna transazione</p>
        ) : (
          transactions.map((transaction) => (
            <div key={transaction.id} className="transaction-item">
              <div className="transaction-info">
                <h3>{transaction.category}</h3>
                <p>{transaction.description}</p>
                <small>{new Date(transaction.date).toLocaleDateString('it-IT')}</small>
              </div>
              <div className="transaction-amount">
                <span className={transaction.type === 'income' ? 'positive' : 'negative'}>
                  {transaction.type === 'income' ? '+' : '-'}€{transaction.amount.toFixed(2)}
                </span>
                <button onClick={() => handleDelete(transaction.id)}>🗑️</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Transactions;

// ----------------------------------------------------------------------------
// 11. ESEMPIO COMPONENTE REACT - CONSIGLI AI
// ----------------------------------------------------------------------------

// File: src/components/AIAdvice.jsx

import React, { useState } from 'react';
import { adviceService } from '../services/adviceService';

function AIAdvice() {
  const [context, setContext] = useState('');
  const [advice, setAdvice] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGetAdvice = async () => {
    setLoading(true);
    try {
      const result = await adviceService.get(context);
      setAdvice(result);
    } catch (err) {
      alert('Errore nel recupero dei consigli');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-advice">
      <h1>Consigli AI</h1>
      
      <div className="advice-input">
        <textarea
          placeholder="Fai una domanda specifica (opzionale)..."
          value={context}
          onChange={(e) => setContext(e.target.value)}
          rows={3}
        />
        <button onClick={handleGetAdvice} disabled={loading}>
          {loading ? 'Caricamento...' : 'Ottieni Consigli'}
        </button>
      </div>

      {advice && (
        <div className="advice-result">
          <h2>I tuoi consigli personalizzati:</h2>
          <p style={{ whiteSpace: 'pre-wrap' }}>{advice}</p>
        </div>
      )}
    </div>
  );
}

export default AIAdvice;

// ----------------------------------------------------------------------------
// 12. ROUTE PROTETTE (Protected Routes)
// ----------------------------------------------------------------------------

// File: src/components/ProtectedRoute.jsx

import React from 'react';
import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';

function ProtectedRoute({ children }) {
  const isAuthenticated = authService.isAuthenticated();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default ProtectedRoute;

// Utilizzo in App.jsx:
/*
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
*/

// ----------------------------------------------------------------------------
// 13. NOTE IMPORTANTI
// ----------------------------------------------------------------------------

/*
COSA FARE NEL PROGETTO finance-tracker-1316:

1. COPIA il file api.js (sezione 1) e sostituisci la configurazione API esistente

2. COPIA i servizi (sezioni 2-7) in cartelle apposite:
   - src/services/authService.js
   - src/services/transactionService.js
   - src/services/budgetService.js
   - src/services/goalService.js
   - src/services/statsService.js
   - src/services/adviceService.js

3. AGGIORNA i componenti esistenti per usare i nuovi servizi

4. VERIFICA che localStorage sia usato per token e user

5. TESTA il flusso completo:
   - Registrazione
   - Login
   - Creazione transazioni
   - Sincronizzazione con app mobile

RISULTATO FINALE:
✅ Web app e mobile app condivideranno:
   - Stesso database utenti
   - Stesse transazioni
   - Stessi budget
   - Stessi obiettivi
   - Stesse statistiche
   - Stessi consigli AI

✅ Un utente potrà:
   - Registrarsi su web e accedere da mobile (e viceversa)
   - Aggiungere dati su un'app e vederli sull'altra
   - Usare entrambe le app in modo intercambiabile
*/
