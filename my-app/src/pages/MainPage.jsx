import React, { useState } from "react";
import OrderForm from "../components/forms/OrderForm/OrderForm";
import ProductionForm from "../components/forms/ProductionForm/ProductionForm";
import TransactionForm from "../components/forms/TransactionForm/TransactionForm";
import AvailableMaterials from "../components/tables/AvailableMaterials/AvailableMaterials";
import AvailableProducts from "../components/tables/AvailableProducts/AvailableProducts";
import Stations from "../components/tables/Stations/Stations"
import Transactions from "../components/tables/Transactions/Transactions"
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
            Запись выставления приказа
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
            className={`menu-item ${selectedForm === "stations" ? "active" : ""}`}
            onClick={() => setSelectedForm("stations")}
          >
            Станции
          </li>
          <li
            className={`menu-item ${selectedForm === "transactions" ? "active" : ""}`}
            onClick={() => setSelectedForm("transactions")}
          >
            Транзакции
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
        {selectedForm === "stations" && <Stations />}
        {selectedForm === "transactions" && <Transactions />}
        {selectedForm === "availableMaterials" && <AvailableMaterials />}
        {selectedForm === "availableProducts" && <AvailableProducts />}
      </div>
    </div>
  );
};

export default MainPage;
