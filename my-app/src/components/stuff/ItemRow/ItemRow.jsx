import "./ItemRow.css";

const formatNumber = (value) => {
  if (typeof value === "number") {
    return value
  }
  const num =  parseFloat(value);
  
  if (!isNaN(num)) {
    return num.toLocaleString("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  return value; // Если не число, оставить как есть
};

const ItemRow = ({ data, index, disableAction, onEdit }) => {
  return (
    <div className={`item-row ${index % 2 === 0 ? "even" : "odd"}`}>
      {Object.entries(data).map(([key, value]) => (
        <span key={key} className="item-field">
          {formatNumber(value)}
        </span>
      ))}
      {!disableAction && <button className="update-button" onClick={onEdit}>Изменить</button>}
    </div>
  );
};
export default ItemRow;