import { useEffect, useRef, useState } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";

const QRScanner = ({ onScan }) => {
  const [isScanning, setIsScanning] = useState(false);
  const scannerRef = useRef(null);

  const startScanning = () => {
    setIsScanning(true);
  };

  const stopScanning = () => {
    setIsScanning(false);
    if (scannerRef.current) {
      scannerRef.current.clear().catch((error) => {
        console.error("Failed to clear scanner", error);
      });
      scannerRef.current = null;
    }
  };

  useEffect(() => {
    if (!isScanning) return;

    const scanner = new Html5QrcodeScanner(
      "qr-reader",
      {
        qrbox: {
          width: 250,
          height: 250,
        },
        fps: 2, // Уменьшаем FPS для производительности
      },
      false,
    );

    let isComponentMounted = true;

    scanner.render(
      (decodedText) => {
        if (!isComponentMounted) return;
        console.log("QR Code scanned:", decodedText);
        onScan(decodedText);
        stopScanning();
      },
      (error) => {
        if (!isComponentMounted) return;
        // Игнорируем обычные ошибки "не найден QR-код"
        if (!error?.message?.includes("NotFoundException")) {
          console.log("QR Scan error:", error);
        }
      },
    );

    scannerRef.current = scanner;

    return () => {
      isComponentMounted = false;
      if (scannerRef.current) {
        scannerRef.current.clear().catch((error) => {
          console.error("Failed to clear scanner on unmount", error);
        });
      }
    };
  }, [isScanning, onScan]);

  return (
    <div className="qr-scanner">
      <h3>Сканирование QR-кода товара</h3>

      {isScanning ? (
        <div>
          <div
            id="qr-reader"
            style={{ width: "100%", maxWidth: "500px", margin: "0 auto" }}
          ></div>
          <div style={{ textAlign: "center", marginTop: "1rem" }}>
            <button
              onClick={stopScanning}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#dc3545",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              Остановить сканирование
            </button>
          </div>
          <p style={{ textAlign: "center", marginTop: "1rem", color: "#666" }}>
            Наведите камеру на QR-код товара
          </p>
        </div>
      ) : (
        <div style={{ textAlign: "center" }}>
          <button
            onClick={startScanning}
            style={{
              padding: "0.75rem 1.5rem",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              fontSize: "1rem",
              cursor: "pointer",
            }}
          >
            Начать сканирование
          </button>
        </div>
      )}
    </div>
  );
};

export default QRScanner;
