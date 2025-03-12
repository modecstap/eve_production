import React, { useState, useEffect } from "react";
import "./ProductionForm.css"; // Подключаем стили
import { serverIP } from "../constants/serverIP";

const ProductionForm = () => {
  const [types, setTypes] = useState([]);
  const [selectedType, setSelectedType] = useState("");
  const [productionDate, setProductionDate] = useState("");
  const [stations, setStations] = useState([]); // Changed from station to stations for proper handling
  const [selectedStation, setSelectedStation] = useState(""); // Default as empty string for single station selection
  const [blueprintEfficiency, setBlueprintEfficiency] = useState(1);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    // Fetch available types from the API
    const fetchTypes = async () => {
      try {
        const response = await fetch(`${serverIP}/api/type_info/get_types`);
        if (response.ok) {
          const data = await response.json();
          setTypes(data); // Assume `data` is an array of types like [{id: 1, name: "Type A"}, ...]
        } else {
          console.error("Failed to fetch types");
        }
      } catch (error) {
        console.error("Error fetching types:", error);
      }
    };

    fetchTypes();
  }, []);

  useEffect(() => {
    // Fetch available stations from the API
    const fetchStations = async () => {
      try {
        const response = await fetch(`${serverIP}/api/station/get_stations`);
        if (response.ok) {
          const data = await response.json();
          setStations(data); // Set stations data
        } else {
          console.error("Failed to fetch stations");
        }
      } catch (error) {
        console.error("Error fetching stations:", error);
      }
    };

    fetchStations();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedType || !productionDate || quantity < 1 || !selectedStation) {
      alert("Заполни всё корректно");
      return;
    }

    const formattedData = Array.from({ length: quantity }).map(() => ({
      type_id: parseInt(selectedType, 10),
      production_date: productionDate,
      blueprint_efficiency: blueprintEfficiency,
      station_id: selectedStation, // Send station_id as selectedStation
    }));

    try {
      const response = await fetch(`${serverIP}/api/product/create_products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formattedData),
      });

      if (response.ok) {
        alert("Успешно");
      } else {
        alert("Ошибка");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Ошибка");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Запись о производстве</h1>
      <form onSubmit={handleSubmit} className="production-form">
        <div className="form-group">
          <label htmlFor="type" className="form-label">Тип продукта</label>
          <select
            id="type"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Выбери тип</option>
            {types.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="station" className="form-label">Станция</label>
          <select
            id="station"
            value={selectedStation}
            onChange={(e) => setSelectedStation(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Выбери станцию</option>
            {stations.map((station) => (
              <option key={station.id} value={station.id}>
                {station.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="date" className="form-label">Дата производства</label>
          <input
            type="datetime-local"
            id="date"
            value={productionDate}
            onChange={(e) => setProductionDate(e.target.value)}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="blueprintEfficiency" className="form-label">Эффективность чертежа</label>
          <input
            type="number"
            id="blueprintEfficiency"
            value={blueprintEfficiency}
            onChange={(e) => setBlueprintEfficiency(e.target.value)}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="quantity" className="form-label">Количество</label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value, 10))}
            className="form-input"
            min="1"
            required
          />
        </div>

        <button type="submit" className="form-button">Записать</button>
      </form>
    </div>
  );
};

export default ProductionForm;
