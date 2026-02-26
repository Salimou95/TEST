import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

export default function Cart() {
  const { cart, removeFromCart } = useCart();
  const navigate = useNavigate();

  if (cart.items.length === 0) {
    return (
      <div className="cart-page">
        <h1>Your Cart</h1>
        <p>Your cart is empty. <Link to="/">Continue shopping</Link></p>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>Your Cart</h1>
      <table className="cart-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {cart.items.map(item => (
            <tr key={item.product_id}>
              <td>
                <Link to={`/product/${item.product_id}/${item.product_slug}`}>
                  {item.product_name}
                </Link>
              </td>
              <td>${item.price.toFixed(2)}</td>
              <td>{item.quantity}</td>
              <td>${item.total_price.toFixed(2)}</td>
              <td>
                <button
                  onClick={() => removeFromCart(item.product_id)}
                  className="btn btn-danger"
                >
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="cart-summary">
        <strong>Total: ${cart.total_price.toFixed(2)}</strong>
        <button onClick={() => navigate('/checkout')} className="btn btn-primary">
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}
