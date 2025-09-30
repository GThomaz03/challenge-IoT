import cv2
import requests
from ultralytics import YOLO

# Carregar modelo YOLOv5u
model = YOLO("yolov5su.pt")

# Fonte do vídeo
PATH_DATA = 'vision/Data/vid4.mp4'
cap = cv2.VideoCapture(PATH_DATA)

# URL da API FastAPI
API_URL = "http://127.0.0.1:8000/visao/registrar"

frame_counter = 0  # contador de frames

def detect_and_track_motos(frame, frame_id):
    results = model(frame, verbose=False)[0]

    # pega o id da classe "motorcycle"
    motorcycle_id = [k for k, v in results.names.items() if v == "motorcycle"][0]

    motos = [box for box in results.boxes if int(box.cls) == motorcycle_id]

    contador = 0

    for box in motos:
        x1, y1, x2, y2 = map(int, box.xyxy[0])   # coordenadas da bounding box
        confidence = float(box.conf[0])          # confiança da predição

        # Desenha no frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'Moto {confidence:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        contador += 1

    # Mostra contador na tela
    cv2.putText(frame, f'Total Motos: {contador}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Envia os dados para a API
    try:
        payload = {
            "frame_id": frame_id,
            "qtd_motos": contador
        }
        requests.post(API_URL, json=payload, timeout=1)
    except Exception as e:
        print("Falha ao enviar para API:", e)

    return frame


# Loop do vídeo
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1
    frame = detect_and_track_motos(frame, frame_counter)

    cv2.imshow('Mottu Moto Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
