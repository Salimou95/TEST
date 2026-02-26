import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

export default function OrderDetail() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/orders/${id}/`)
      .then(res => setOrder(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (!order) return <p>Order not found.</p>;

  return (
    <div className="order-detail-page">
      <h1>Order #{order.id} — Confirmed!</h1>
      <p>Thank you, {order.first_name}! Your order has been placed.</p>
      <div className="order-info">
        <p><strong>Shipping to:</strong> {order.address}, {order.city}, {order.postal_code}</p>
        <p><strong>Email:</strong> {order.email}</p>
        <p><strong>Status:</strong> {order.paid ? 'Paid' : 'Pending'}</p>
      </div>
      <h2>Items</h2>
      <table className="cart-table">
        <thead>
          <tr><th>Product</th><th>Price</th><th>Qty</th><th>Total</th></tr>
        </thead>
        <tbody>
          {order.items.map(item => (
            <tr key={item.id}>
              <td>{item.product.name}</td>
              <td>${item.price}</td>
              <td>{item.quantity}</td>
              <td>${item.total.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p><strong>Order Total: ${order.total_cost.toFixed(2)}</strong></p>
      <Link to="/orders">Back to Orders</Link>
    </div>
  );
}
