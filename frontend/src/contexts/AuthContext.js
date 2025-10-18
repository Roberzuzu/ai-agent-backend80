import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Set axios default headers
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/auth/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
      // Token invalid, clear it
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    // Create form data for OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append('username', email); // OAuth2 uses 'username' but we pass email
    formData.append('password', password);

    const response = await axios.post(
      `${BACKEND_URL}/api/auth/login`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    const { access_token, user: userData } = response.data;
    
    // Save token
    localStorage.setItem('token', access_token);
    setToken(access_token);
    setUser(userData);
    
    // Set default header
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    
    return userData;
  };

  const register = async (userData) => {
    const response = await axios.post(`${BACKEND_URL}/api/auth/register`, userData);
    
    const { access_token, user: newUser } = response.data;
    
    // Save token
    localStorage.setItem('token', access_token);
    setToken(access_token);
    setUser(newUser);
    
    // Set default header
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    
    return newUser;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    isAffiliate: user?.role === 'affiliate',
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export default AuthContext;
