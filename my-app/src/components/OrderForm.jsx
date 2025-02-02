import React, { useState, useEffect } from "react";
import "./OrderForm.css"; // Подключаем стили
import { serverIP } from "../constants/serverIP";

const OrderForm = () => {
  const [itemTypes, setItemTypes] = useState([]);
  const [selectedItemType, setSelectedItemType] = useState("");
  const [releaseDate, setReleaseDate] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    // Fetch available order types and item types
    const fetchData = async () => {
      try {
        const [typesResponse, itemTypesResponse] = await Promise.all([
          fetch(`${serverIP}/api/type_info/get_types`),
          fetch(`${serverIP}/api/type_info/get_types`),
        ]);

        if (typesResponse.ok && itemTypesResponse.ok) {
          const itemTypesData = await itemTypesResponse.json();
          setItemTypes(itemTypesData);
        } else {
          console.error("Failed to fetch types or item types");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedItemType || !releaseDate || price <= 0 || quantity < 1) {
      alert("Please fill all fields correctly.");
      return;
    }

    const formattedData = [
      {
        price: parseFloat(price),
        release_date: releaseDate + ".000",
        product_count: parseInt(quantity, 10),
        type_id: parseInt(selectedItemType, 10),
      },
    ];

    try {
      const response = await fetch(`${serverIP}/api/order/add_order`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formattedData),
      });

      if (response.ok) {
        alert("Успешно");
      } else {
        alert("Ошибка создания приказа");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Ошибка создания приказа");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Форма ввода приказа </h1>
      <form onSubmit={handleSubmit} className="order-form">
        <div className="form-group">
          <label htmlFor="item-type" className="form-label">Тип предмета</label>
          <select
            id="item-type"
            value={selectedItemType}
            onChange={(e) => setSelectedItemType(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Выбери тип предмета</option>
            {itemTypes.map((itemType) => (
              <option key={itemType.id} value={itemType.id}>
                {itemType.name}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="date" className="form-label">Дата выпуска</label>
          <input
            type="datetime-local"
            id="date"
            value={releaseDate}
            onChange={(e) => setReleaseDate(e.target.value)}
            className="form-input"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="price" className="form-label">Цена</label>
          <input
            type="number"
            id="price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="form-input"
            min="0.01"
            step="0.01"
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

export default OrderForm;
