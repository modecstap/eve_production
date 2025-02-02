import React, { useState, useEffect } from "react";
import { serverIP } from "../constants/serverIP";
import "./AvailableMaterials.css";

const AvailableMaterials = () => {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const response = await fetch(`${serverIP}/api/transaction/get_available_materials`);
        if (response.ok) {
          const data = await response.json();
          setMaterials(data);
          setLoading(false);
        } else {
          throw new Error("Failed to fetch materials.");
        }
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchMaterials();
  }, []);

  if (loading) return <div className="loading">загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="materials-container">
      <h1 className="materials-title">Доступные материалы</h1>
      <table className="materials-table">
        <thead>
          <tr>
            <th>#</th>
            <th>тип</th>
            <th>количества</th>
            <th>средняя стоимость</th>
          </tr>
        </thead>
        <tbody>
          {materials.map((material, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{material.name}</td>
              <td>{material.count}</td>
              <td>{material.mean_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AvailableMaterials;
