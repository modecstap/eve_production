import React, { useState } from "react";

import OrderForm from "../components/forms/OrderForm/OrderForm";
import ProductionForm from "../components/forms/ProductionForm/ProductionForm";
import TransactionForm from "../components/forms/TransactionForm/TransactionForm";

import Table from "../components/stuff/Table/Table";

import "./MainPage.css";

const MainPage = () => {
  const [selectedForm, setSelectedForm] = useState("order");
  return (
    <div className="main-container">
      {/* Левая панель выбора формы */}
      <div className="sidebar">
        <h2 className="sidebar-title">Меню</h2>
        <ul className="menu">
          {/* Формы ввода */}
          <details className="dropdown">
            <summary className="menu-item">Формы ввода</summary>
            <ul className="submenu">
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
            </ul>
          </details>

          {/* Сводные таблицы */}
          <details className="dropdown">
            <summary className="menu-item">Сводные таблицы</summary>
            <ul className="submenu">
              <li
                className={`menu-item ${selectedForm === "availableMaterials" ? "active" : ""}`}
                onClick={() => setSelectedForm("availableMaterials")}
              >
                Таблица доступных материалов
              </li>
              <li
                className={`menu-item ${selectedForm === "availableProducts" ? "active" : ""}`}
                onClick={() => setSelectedForm("availableProducts")}
              >
                Таблица доступных продуктов
            </li>
            </ul>
          </details>

          {/* Базовые */}
          <details className="dropdown">
            <summary className="menu-item">Базовые таблицы</summary>
            <ul className="submenu">
              <li
                className={`menu-item ${selectedForm === "materialList" ? "active" : ""}`}
                onClick={() => setSelectedForm("materialList")}
              >
                Требуемые материалы
              </li>
              <li
                className={`menu-item ${selectedForm === "orders" ? "active" : ""}`}
                onClick={() => setSelectedForm("orders")}
              >
                Приказы
              </li>
              <li
                className={`menu-item ${selectedForm === "products" ? "active" : ""}`}
                onClick={() => setSelectedForm("products")}
              >
                Продукты
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
                className={`menu-item ${selectedForm === "types" ? "active" : ""}`}
                onClick={() => setSelectedForm("types")}
              >
                Типы
              </li>
              <li
                className={`menu-item ${selectedForm === "usedTransactions" ? "active" : ""}`}
                onClick={() => setSelectedForm("usedTransactions")}
              >
                Использованные транзакции
              </li>
            </ul>
          </details>
        </ul>
      </div>

      {/* Правая панель отображения формы */}
      <div className="form-display">
        {selectedForm === "order" && <OrderForm />}
        {selectedForm === "production" && <ProductionForm />}
        {selectedForm === "transaction" && <TransactionForm />}
        {selectedForm === "materialList" && <Table endPoint="api/material_list" title="требуемые материалы"  />}
        {selectedForm === "orders" && <Table endPoint="api/orders" title="Заказы" />}
        {selectedForm === "products" && <Table endPoint="api/products" title="Приказы" />}
        {selectedForm === "stations" && <Table endPoint="api/stations" title="Станции" />}
        {selectedForm === "transactions" && <Table endPoint="api/transactions" title="Транзакции" />}
        {selectedForm === "types" && <Table endPoint="api/types" title="Типы" />}
        {selectedForm === "usedTransactions" && <Table endPoint="api/used_transaction" title="Использованные транзакции" />}
        {selectedForm === "availableMaterials" && <Table endPoint="api/available_materials" title="Доступные материалы" />}
        {selectedForm === "availableProducts" && <Table endPoint="api/available_products" title="Доступные продукты" />}
      </div>
    </div>
  );
};

export default MainPage;
