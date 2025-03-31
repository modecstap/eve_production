import "./ItemRow.css";

const ItemRow = ({ data, index, disableAction }) => {
  return (
    <div className={`item-row ${index % 2 === 0 ? "even" : "odd"}`}>
      {Object.entries(data).map(([key, value]) => (
        <span key={key} className="item-field">
          {value}
        </span>
      ))}
      {!disableAction && <button className="update-button">Update</button>}
    </div>
  );
};
export default ItemRow;