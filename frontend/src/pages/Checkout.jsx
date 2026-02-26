import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import api from '../api';

export default function Checkout() {
  const { cart, fetchCart } = useCart();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '',
    address: '', city: '', postal_code: '',
  });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const res = await api.post('/orders/checkout/', form);
      await fetchCart();
      navigate(`/orders/${res.data.id}`);
    } catch (err) {
      const data = err.response?.data;
      setError(data?.detail || JSON.stringify(data) || 'An error occurred.');
    } finally {
      setSubmitting(false);
    }
  };

  if (cart.items.length === 0) {
    return <p>Your cart is empty. <a href="/">Go shopping</a></p>;
  }

  return (
    <div className="checkout-page">
      <h1>Checkout</h1>
      <div className="checkout-layout">
        <form onSubmit={handleSubmit} className="checkout-form">
          <h2>Shipping Details</h2>
          {error && <p className="error-msg">{error}</p>}
          {[
            ['first_name', 'First Name'],
            ['last_name', 'Last Name'],
            ['email', 'Email'],
            ['address', 'Address'],
            ['city', 'City'],
            ['postal_code', 'Postal Code'],
          ].map(([name, label]) => (
            <div key={name} className="form-group">
              <label>{label}</label>
              <input
                type={name === 'email' ? 'email' : 'text'}
                name={name}
                value={form[name]}
                onChange={handleChange}
                required
              />
            </div>
          ))}
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'Placing Order...' : 'Place Order'}
          </button>
        </form>

        <div className="order-summary">
          <h2>Order Summary</h2>
          {cart.items.map(item => (
            <div key={item.product_id} className="summary-item">
              <span>{item.product_name} × {item.quantity}</span>
              <span>${item.total_price.toFixed(2)}</span>
            </div>
          ))}
          <hr />
          <strong>Total: ${cart.total_price.toFixed(2)}</strong>
        </div>
      </div>
    </div>
  );
}
