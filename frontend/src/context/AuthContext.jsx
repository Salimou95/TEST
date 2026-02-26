import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(undefined); // undefined = loading

  useEffect(() => {
    api.get('/auth/user/')
      .then(res => setUser(res.data))
      .catch(() => setUser(null));
  }, []);

  const login = async (username, password) => {
    const res = await api.post('/auth/login/', { username, password });
    setUser(res.data);
    return res.data;
  };

  const logout = async () => {
    await api.post('/auth/logout/');
    setUser(null);
  };

  const register = async (data) => {
    const res = await api.post('/auth/register/', data);
    setUser(res.data);
    return res.data;
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
