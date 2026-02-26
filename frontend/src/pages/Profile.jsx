import { useState, useEffect } from 'react';
import api from '../api';

export default function Profile() {
  const [profile, setProfile] = useState({ address: '', city: '', postal_code: '', phone: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/auth/profile/').then(res => setProfile(res.data));
  }, []);

  const handleSubmit = async e => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      await api.put('/auth/profile/', profile);
      setMessage('Profile updated successfully.');
    } catch (err) {
      setError(err.response?.data?.detail || 'Update failed.');
    }
  };

  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      <form onSubmit={handleSubmit} className="auth-form">
        {message && <p className="success-msg">{message}</p>}
        {error && <p className="error-msg">{error}</p>}
        {[
          ['address', 'Address', 'text'],
          ['city', 'City', 'text'],
          ['postal_code', 'Postal Code', 'text'],
          ['phone', 'Phone', 'tel'],
        ].map(([name, label, type]) => (
          <div key={name} className="form-group">
            <label>{label}</label>
            <input
              type={type}
              value={profile[name] || ''}
              onChange={e => setProfile({ ...profile, [name]: e.target.value })}
            />
          </div>
        ))}
        <button type="submit" className="btn btn-primary">Save</button>
      </form>
    </div>
  );
}
