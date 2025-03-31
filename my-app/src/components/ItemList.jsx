import "./ItemList.css";
import ItemRow from "./ItemRow";

const ItemList = ({ data, disableAction }) => {
  const headers = Object.keys(data[0] || {});

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
      {data.map((item, index) => (
        <ItemRow key={index} data={item} index={index} disableAction={disableAction} />
      ))}
    </div>
  );
};

export default ItemList