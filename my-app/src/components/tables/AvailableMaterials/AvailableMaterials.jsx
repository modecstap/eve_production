import React, { useState, useEffect } from "react";
import { serverIP } from "../../../constants/serverIP";
import "./AvailableMaterials.css";
import ItemList from "../../stuff/ItemList/ItemList"

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
          throw new Error("Ошибка получения материалов.");
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
      <ItemList data={materials} disableAction={false} />
    </div>
  );
};

export default AvailableMaterials;
