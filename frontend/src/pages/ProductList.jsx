import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import api from '../api';

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const selectedCategory = searchParams.get('category') || '';

  useEffect(() => {
    api.get('/categories/').then(res => setCategories(res.data));
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = selectedCategory ? { category: selectedCategory } : {};
    api.get('/products/', { params })
      .then(res => setProducts(res.data.results || res.data))
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  return (
    <div className="product-list-page">
      <aside className="sidebar">
        <h3>Categories</h3>
        <ul>
          <li>
            <button
              className={!selectedCategory ? 'active' : ''}
              onClick={() => setSearchParams({})}
            >
              All
            </button>
          </li>
          {categories.map(cat => (
            <li key={cat.id}>
              <button
                className={selectedCategory === cat.slug ? 'active' : ''}
                onClick={() => setSearchParams({ category: cat.slug })}
              >
                {cat.name}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      <main className="products-grid">
        {loading ? (
          <p>Loading...</p>
        ) : products.length === 0 ? (
          <p>No products found.</p>
        ) : (
          products.map(product => (
            <div key={product.id} className="product-card">
              {product.image ? (
                <img src={product.image} alt={product.name} />
              ) : (
                <div className="no-image">No Image</div>
              )}
              <h3>
                <Link to={`/product/${product.id}/${product.slug}`}>{product.name}</Link>
              </h3>
              <p className="price">${product.price}</p>
              <Link to={`/product/${product.id}/${product.slug}`} className="btn">View</Link>
            </div>
          ))
        )}
      </main>
    </div>
  );
}
