import React, { useState, useEffect } from "react";
import "./TransactionForm.css"; // Подключаем стили
import { serverIP } from "../constants/serverIP";

const TransactionForm = () => {
  const [transactionsInput, setTransactionsInput] = useState("");
  const [materials, setMaterials] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // Загружаем материалы при монтировании компонента
    const fetchMaterials = async () => {
      try {
        const response = await fetch(`${serverIP}/api/type_info/get_types`);
        const data = await response.json();
        setMaterials(data);
      } catch (err) {
        setError("Ошибка загрузки списка материалов.");
      }
    };
    fetchMaterials();
  }, []);

  const parseTransactions = (input) => {
    const lines = input.split("\n");
    const transactions = [];

    lines.forEach((line, index) => {
      const parts = line.split(/\s{4,}/);

      if (parts.length < 9) return;

      const [date, count, materialName, pricePerUnit, allPrice] = parts;
      const material = materials.find((mat) => mat.name.toLowerCase() === materialName.trim().toLowerCase());

      if (!material) {
        console.warn(`Материал "${materialName}" не найден в строке ${index + 1}.`);
        return;
      }

      const release_date = `${date.replaceAll(".", "-")}:00.000`;
      const countParsed = parseInt(count.replace(/\s/g, ""), 10);
      const priceParsed = parseFloat(allPrice.replace(/[^0-9,.-]/g, "").replace(",", ".").replace("-", ""))/countParsed;

      if (!isNaN(countParsed) && !isNaN(priceParsed)) {
        transactions.push({
          release_date,
          count: countParsed,
          material_id: material.id,
          price: priceParsed,
          remains: countParsed
        });
      } else {
        console.warn(`Ошибка в данных строки ${index + 1}: не удалось обработать.`);
      }
    });

    return transactions;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!materials.length) {
      alert("Список материалов не загружен. Попробуйте позже.");
      return;
    }

    const transactions = parseTransactions(transactionsInput);

    if (transactions.length > 0) {
      try {
          console.log(JSON.stringify(transactions))
        const response = await fetch(`${serverIP}/api/transaction/add_transactions`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(transactions),
        });

        if (response.ok) {
          alert("Транзакции успешно отправлены!");
        } else {
          alert("Ошибка при отправке транзакций.");
        }
      } catch {
        alert("Ошибка сети.");
      }
    } else {
      alert("Не удалось обработать транзакции. Проверьте ввод.");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Ввод транзакций</h1>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit} className="transaction-form">
        <div className="form-group">
          <label htmlFor="transactions" className="form-label">Список транзакций:</label>
          <textarea
            id="transactions"
            value={transactionsInput}
            onChange={(e) => setTransactionsInput(e.target.value)}
            rows={20}
            cols={50}
            placeholder="Введите транзакции..."
            className="form-textarea"
          />
        </div>
        <button type="submit" className="form-button" disabled={!materials.length}>
          Записать
        </button>
      </form>
    </div>
  );
};

export default TransactionForm;
