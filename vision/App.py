import cv2
import time
import requests
from ultralytics import YOLO

# ================== CONFIGURAÇÃO ==================
VIDEO_PATH = "vision/Data/vid4.mp4"
YOLO_MODEL = "yolov8s.pt"  # YOLOv8
API_URL = "http://localhost:8000/visao/registrar"  # URL da API

# ================== CARREGA MODELO YOLOv8 ==================
model = YOLO(YOLO_MODEL)

# Captura de vídeo
cap = cv2.VideoCapture(VIDEO_PATH)

# ================== HISTÓRICO EM MEMÓRIA ==================
historico_motos = []

# ================== LOOP PRINCIPAL ==================
frame_id = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ================== DETECÇÃO ==================
    results = model(frame, verbose=False)[0]

    # pega o id da classe "motorcycle"
    motorcycle_id = [k for k, v in results.names.items() if v == "motorcycle"][0]
    motos = [box for box in results.boxes if int(box.cls) == motorcycle_id]

    contador = 0
    motos_ids_frame = []

    for idx, box in enumerate(motos):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.putText(frame, f"Moto {confidence:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
        contador += 1
        motos_ids_frame.append(f"Moto_{idx+1}")

    # Mostra total de motos no frame
    cv2.putText(frame, f"Total Motos: {contador}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # ================== ATUALIZA HISTÓRICO ==================
    historico_motos.append(contador)

    # ================== ENVIA DADOS PARA API ==================
    try:
        payload = {"frame_id": frame_id, "qtd_motos": contador}
        requests.post(API_URL, json=payload, timeout=1)
    except Exception as e:
        print(f"Erro ao enviar dados para API: {e}")

    # ================== MOSTRA O VÍDEO ==================
    info_text = f"Total Motos: {contador} | IDs: {', '.join(motos_ids_frame)}"
    cv2.putText(frame, info_text, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("Visão Computacional - Mottu", frame)

    frame_id += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.02)  # ajuste para performance (~50 FPS)

cap.release()
cv2.destroyAllWindows()
