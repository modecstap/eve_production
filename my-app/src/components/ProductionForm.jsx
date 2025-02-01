import React, { useState, useEffect } from "react";
import "./ProductionForm.css"; // Подключаем стили
import { serverIP } from "../constants/serverIP";

const ProductionForm = () => {
  const [types, setTypes] = useState([]);
  const [selectedType, setSelectedType] = useState("");
  const [productionDate, setProductionDate] = useState("");
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedType || !productionDate || quantity < 1) {
      alert("Please fill all fields correctly.");
      return;
    }

    const formattedData = Array.from({ length: quantity }).map(() => ({
      type_id: parseInt(selectedType, 10),
      production_date: productionDate,
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
        alert("Production data submitted successfully!");
      } else {
        alert("Error submitting production data.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit production data.");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Production Input Form</h1>
      <form onSubmit={handleSubmit} className="production-form">
        <div className="form-group">
          <label htmlFor="type" className="form-label">Product Type</label>
          <select
            id="type"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Select a type</option>
            {types.map((type) => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="date" className="form-label">Production Date</label>
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
          <label htmlFor="quantity" className="form-label">Quantity</label>
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
        <button type="submit" className="form-button">Submit</button>
      </form>
    </div>
  );
};

export default ProductionForm;
