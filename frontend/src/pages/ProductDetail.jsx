import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import { useCart } from '../context/CartContext';

export default function ProductDetail() {
  const { id, slug } = useParams();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const { addToCart } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    api.get(`/products/${id}/`)
      .then(res => setProduct(res.data))
      .catch(() => navigate('/'))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  const handleAddToCart = async () => {
    await addToCart(product.id, quantity);
    setMessage('Added to cart!');
    setTimeout(() => setMessage(''), 2000);
  };

  if (loading) return <p>Loading...</p>;
  if (!product) return null;

  return (
    <div className="product-detail">
      <div className="product-detail-image">
        {product.image ? (
          <img src={product.image} alt={product.name} />
        ) : (
          <div className="no-image">No Image</div>
        )}
      </div>
      <div className="product-detail-info">
        <h1>{product.name}</h1>
        <p className="category">Category: {product.category?.name}</p>
        <p className="price">${product.price}</p>
        <p className="description">{product.description}</p>
        <p className="stock">
          {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
        </p>
        {product.stock > 0 && (
          <div className="add-to-cart">
            <label>
              Quantity:
              <input
                type="number"
                min="1"
                max={product.stock}
                value={quantity}
                onChange={e => setQuantity(parseInt(e.target.value, 10))}
              />
            </label>
            <button onClick={handleAddToCart} className="btn btn-primary">
              Add to Cart
            </button>
          </div>
        )}
        {message && <p className="success-msg">{message}</p>}
      </div>
    </div>
  );
}
