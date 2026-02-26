import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

// Fetch CSRF token from Django on first mutating request if not present
let csrfReady = false;

async function ensureCsrf() {
  if (csrfReady) return;
  // Trigger Django to set the csrftoken cookie
  await axios.get('/api/csrf/', { withCredentials: true });
  csrfReady = true;
}

// Attach CSRF token to every mutating request
api.interceptors.request.use(async (config) => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    await ensureCsrf();
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) {
      config.headers['X-CSRFToken'] = match[1];
    }
  }
  return config;
});

export default api;
