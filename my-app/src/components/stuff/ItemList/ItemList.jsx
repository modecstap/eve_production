import { useState } from "react";
import "./ItemList.css";
import ItemRow from "../ItemRow/ItemRow";
import Modal from "../Modal/Modal";
import Pagination from "../Pagination/Pagination";

const ITEMS_PER_PAGE = 15;

const ItemList = ({ data, disableAction, apiUrl }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const openModal = (item) => {
    setSelectedItem(item);
    setIsModalOpen(true);
  };

  const headers = Object.keys(data[0] || {}).map(key => key.replace(/_/g, ' '));;
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
        {!disableAction && <span className="item-field">ACTIONS</span>}
      </div>

      {/* Список элементов */}
      {currentItems.map((item, index) => (
        <ItemRow key={index} data={item} index={index} disableAction={disableAction} onEdit={() => openModal(item)} />
      ))}

      {/* Кнопка "Добавить" */}
      {!disableAction && <button className="add-button" onClick={() => openModal({})}>
        +
      </button>}
      {isModalOpen && <Modal item={data[0]} onClose={() => setIsModalOpen(false)} apiUrl={apiUrl} isAdd={true} />}
    
      {/* Пагинация */}
      <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
    </div>
  );
};

export default ItemList