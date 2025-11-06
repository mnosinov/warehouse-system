import { useEffect, useRef } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";

const QRScanner = ({ onScan }) => {
  const scannerRef = useRef(null);

  useEffect(() => {
    const scanner = new Html5QrcodeScanner(
      "qr-reader",
      {
        qrbox: {
          width: 250,
          height: 250,
        },
        fps: 5,
      },
      false,
    );

    scanner.render(
      (decodedText) => {
        onScan(decodedText);
        // Останавливаем сканер после успешного сканирования
        scanner.clear();
      },
      (error) => {
        // Ошибки можно логировать, но не показывать пользователю
        console.log("QR Scan error:", error);
      },
    );

    scannerRef.current = scanner;

    return () => {
      if (scannerRef.current) {
        scannerRef.current.clear().catch((error) => {
          console.error("Failed to clear html5QrcodeScanner.", error);
        });
      }
    };
  }, [onScan]);

  return <div id="qr-reader" style={{ width: "100%" }}></div>;
};

export default QRScanner;
