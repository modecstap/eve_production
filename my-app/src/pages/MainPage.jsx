import React, { useState } from "react";
import OrderForm from "../components/OrderForm";
import ProductionForm from "../components/ProductionForm";
import TransactionForm from "../components/TransactionForm";
import "./MainPage.css";

const MainPage = () => {
  const [selectedForm, setSelectedForm] = useState("order");

  return (
    <div className="main-container">
      {/* Левая панель выбора формы */}
      <div className="sidebar">
        <h2 className="sidebar-title">Select a Form</h2>
        <ul className="menu">
          <li
            className={`menu-item ${selectedForm === "order" ? "active" : ""}`}
            onClick={() => setSelectedForm("order")}
          >
            Order Form
          </li>
          <li
            className={`menu-item ${selectedForm === "production" ? "active" : ""}`}
            onClick={() => setSelectedForm("production")}
          >
            Production Form
          </li>
          <li
            className={`menu-item ${selectedForm === "transaction" ? "active" : ""}`}
            onClick={() => setSelectedForm("transaction")}
          >
            Transaction Form
          </li>
        </ul>
      </div>

      {/* Правая панель отображения формы */}
      <div className="form-display">
        {selectedForm === "order" && <OrderForm />}
        {selectedForm === "production" && <ProductionForm />}
        {selectedForm === "transaction" && <TransactionForm />}
      </div>
    </div>
  );
};

export default MainPage;
