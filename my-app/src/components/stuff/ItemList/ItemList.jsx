import { useState } from "react";
import "./ItemList.css";
import ItemRow from "../ItemRow/ItemRow";
import Pagination from "../Pagination/Pagination";

const ITEMS_PER_PAGE = 15;

const ItemList = ({ data, disableAction }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);

  const headers = Object.keys(data[0] || {});
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const currentItems = data.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  return (
    <div className="item-list">
      {/* Заголовки таблицы */}
      <div className="item-row header">
        {headers.map((header) => (
          <span key={header} className="item-field">
            {header.toUpperCase()}
          </span>
        ))}
        {!disableAction && <span className="item-field">Actions</span>}
      </div>

      {/* Список элементов */}
      {currentItems.map((item, index) => (
        <ItemRow key={index} data={item} index={index} disableAction={disableAction} />
      ))}

      {/* Кнопка "Добавить" */}
      {!disableAction && <button className="add-button">+</button>}

      {/* Пагинация */}
      <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
    </div>
  );
};

export default ItemList