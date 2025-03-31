import React, { useState } from "react";
import OrderForm from "../components/OrderForm";
import ProductionForm from "../components/ProductionForm";
import TransactionForm from "../components/TransactionForm";
import AvailableMaterials from "../components/AvailableMaterials";
import AvailableProducts from "../components/AvailableProducts";
import "./MainPage.css";

const MainPage = () => {
  const [selectedForm, setSelectedForm] = useState("order");
  return (
    <div className="main-container">
      {/* Левая панель выбора формы */}
      <div className="sidebar">
        <h2 className="sidebar-title">Меню</h2>
        <ul className="menu">
          <li
            className={`menu-item ${selectedForm === "order" ? "active" : ""}`}
            onClick={() => setSelectedForm("order")}
          >
            Запись выставления прказа
          </li>
          <li
            className={`menu-item ${selectedForm === "production" ? "active" : ""}`}
            onClick={() => setSelectedForm("production")}
          >
            Запись производства
          </li>
          <li
            className={`menu-item ${selectedForm === "transaction" ? "active" : ""}`}
            onClick={() => setSelectedForm("transaction")}
          >
            Запись транзакций
          </li>
          <li
            className={`menu-item ${selectedForm === "availableMaterials" ? "active" : ""}`}
            onClick={() => setSelectedForm("availableMaterials")}
          >
            таблица доступных материалов
          </li>
          <li
            className={`menu-item ${selectedForm === "availableProducts" ? "active" : ""}`}
            onClick={() => setSelectedForm("availableProducts")}
          >
            таблица доступных продуктов
          </li>
        </ul>
      </div>

      {/* Правая панель отображения формы */}
      <div className="form-display">
        {selectedForm === "order" && <OrderForm />}
        {selectedForm === "production" && <ProductionForm />}
        {selectedForm === "transaction" && <TransactionForm />}
        {selectedForm === "availableMaterials" && <AvailableMaterials />}
        {selectedForm === "availableProducts" && <AvailableProducts />}
      </div>
    </div>
  );
};

export default MainPage;
