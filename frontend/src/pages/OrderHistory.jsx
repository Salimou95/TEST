import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

export default function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/orders/')
      .then(res => setOrders(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="orders-page">
      <h1>My Orders</h1>
      {orders.length === 0 ? (
        <p>No orders yet. <Link to="/">Start shopping</Link></p>
      ) : (
        orders.map(order => (
          <div key={order.id} className="order-card">
            <div className="order-header">
              <span><strong>Order #{order.id}</strong></span>
              <span>{new Date(order.created).toLocaleDateString()}</span>
              <span className={order.paid ? 'paid' : 'unpaid'}>
                {order.paid ? 'Paid' : 'Pending'}
              </span>
              <Link to={`/orders/${order.id}`}>View Details</Link>
            </div>
            <p>Total: ${order.total_cost.toFixed(2)}</p>
          </div>
        ))
      )}
    </div>
  );
}
