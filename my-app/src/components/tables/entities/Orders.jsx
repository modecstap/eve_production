import React, { useState, useEffect } from "react";
import { serverIP } from "../../../constants/serverIP";
import "../table.css";
import ItemList from "../../stuff/ItemList/ItemList";

const Stations = () => {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const endPoint = "api/orders"

  const fetchMaterials = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${serverIP}/${endPoint}`);
      if (response.ok) {
        const data = await response.json();
        setMaterials(data);
      } else {
        throw new Error("Ошибка получения станций.");
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMaterials();
  }, []);

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="materials-container">
      <div className="materials-header">
        <h1 className="materials-title">Станции</h1>
        <button className="refresh-button" onClick={fetchMaterials}>&#10226;</button>
      </div>
      <ItemList data={materials} disableAction={false} apiUrl={`${serverIP}/${endPoint}`} />
    </div>
  );
};

export default Stations;
