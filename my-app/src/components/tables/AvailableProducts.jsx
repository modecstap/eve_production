import React, { useState, useEffect } from "react";
import { serverIP } from "../../constants/serverIP";
import "./table.css";

const AvailableProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(`${serverIP}/api/product/get_available_products`);
        if (response.ok) {
          const data = await response.json();
          setProducts(data);
          setLoading(false);
        } else {
          throw new Error("Failed to fetch available products.");
        }
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div className="loading">загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="products-container">
      <h1 className="products-title">Доступные продукты</h1>
      <table className="products-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Тип продукта</th>
            <th>дата производства</th>
            <th>себестоимость</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{product.name}</td>
              <td>{new Date(product.production_date).toLocaleString()}</td>
              <td>{product.product_cost} ISK</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AvailableProducts;
