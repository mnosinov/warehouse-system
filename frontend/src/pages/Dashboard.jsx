import { useState } from "react";
import { useNavigate } from "react-router-dom";
import QRScanner from "../components/QRScanner";
import { productsAPI } from "../services/api";

const Dashboard = () => {
  const [scannedProduct, setScannedProduct] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleScan = async (qrCode) => {
    setLoading(true);
    setError("");

    try {
      // Пока просто ищем продукт по ID (в будущем можно добавить поиск по QR)
      // Для демо используем последнюю часть QR кода как ID
      const productId = qrCode.split(":").pop();
      const response = await productsAPI.getProduct(productId);
      setScannedProduct(response.data);
    } catch (err) {
      setError("Продукт не найден. Убедитесь, что QR-код правильный.");
      setScannedProduct(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    navigate("/login");
  };

  return (
    <div className="dashboard">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "2rem",
        }}
      >
        <h1>Панель оператора склада</h1>
        <button
          onClick={handleLogout}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Выйти
        </button>
      </div>

      <div className="scanner-section">
        <h2>Сканирование QR-кода товара</h2>
        <QRScanner onScan={handleScan} />

        {loading && (
          <p style={{ textAlign: "center", margin: "1rem 0" }}>Загрузка...</p>
        )}
        {error && <div className="error">{error}</div>}
      </div>

      {scannedProduct && (
        <div className="product-info">
          <h3>Информация о товаре:</h3>
          <p>
            <strong>Название:</strong> {scannedProduct.name}
          </p>
          <p>
            <strong>Артикул:</strong> {scannedProduct.sku}
          </p>
          <p>
            <strong>Описание:</strong>{" "}
            {scannedProduct.description || "Нет описания"}
          </p>
          <p>
            <strong>Текущее количество:</strong>{" "}
            {scannedProduct.current_quantity}
          </p>
          <p>
            <strong>Минимальный запас:</strong> {scannedProduct.min_quantity}
          </p>
          <p>
            <strong>Максимальный запас:</strong> {scannedProduct.max_quantity}
          </p>
          <p>
            <strong>QR-код:</strong> {scannedProduct.qr_code}
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
