import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '', password2: '' });
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    if (form.password !== form.password2) {
      setError('Passwords do not match.');
      return;
    }
    try {
      await register(form);
      navigate('/');
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const msgs = Object.values(data).flat().join(' ');
        setError(msgs);
      } else {
        setError('Registration failed.');
      }
    }
  };

  return (
    <div className="auth-page">
      <h1>Register</h1>
      <form onSubmit={handleSubmit} className="auth-form">
        {error && <p className="error-msg">{error}</p>}
        {[
          ['username', 'Username', 'text'],
          ['email', 'Email', 'email'],
          ['password', 'Password', 'password'],
          ['password2', 'Confirm Password', 'password'],
        ].map(([name, label, type]) => (
          <div key={name} className="form-group">
            <label>{label}</label>
            <input
              type={type}
              value={form[name]}
              onChange={e => setForm({ ...form, [name]: e.target.value })}
              required
            />
          </div>
        ))}
        <button type="submit" className="btn btn-primary">Register</button>
        <p>Already have an account? <Link to="/login">Login</Link></p>
      </form>
    </div>
  );
}
