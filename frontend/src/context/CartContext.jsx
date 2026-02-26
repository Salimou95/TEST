import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api';

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [], total_price: 0, total_items: 0 });

  const fetchCart = async () => {
    try {
      const res = await api.get('/cart/');
      setCart(res.data);
    } catch {
      // ignore
    }
  };

  useEffect(() => { fetchCart(); }, []);

  const addToCart = async (productId, quantity = 1) => {
    await api.post(`/cart/add/${productId}/`, { quantity });
    await fetchCart();
  };

  const removeFromCart = async (productId) => {
    await api.post(`/cart/remove/${productId}/`);
    await fetchCart();
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, fetchCart }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}
