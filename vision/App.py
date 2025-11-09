import cv2
import time
import requests
import random
import string
from ultralytics import YOLO

# ================== CONFIGURAÇÃO ==================
VIDEO_PATH = "vision/Data/vid4.mp4"
YOLO_MODEL = "yolov8s.pt"
API_BASE = "http://webapp-mottumap.azurewebsites.net/api"
AUTH = ("admin@mottu.com", "123456")

ZONA_ID = 1
SENSOR_ID = 1
POSICAO_BASE = 1

# ================== FUNÇÕES AUXILIARES ==================
def gerar_placa_mercosul():
    letras = string.ascii_uppercase
    numeros = string.digits
    return f"{random.choice(letras)}{random.choice(letras)}{random.choice(letras)}{random.choice(numeros)}{random.choice(letras)}{random.choice(numeros)}{random.choice(numeros)}"

def gerar_chassi():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=17))

def registrar_moto(placa, chassi, modelo):
    moto = {"placa": placa, "chassi": chassi, "modelo": modelo}
    try:
        response = requests.post(f"{API_BASE}/motos", json=moto, auth=AUTH, timeout=3)
        if response.status_code in (200, 201):
            data = response.json()
            print(f"[API] Moto registrada: {data}")
            return data.get("id")
        else:
            print(f"[API] Erro ao registrar moto: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[API] Falha ao registrar moto: {e}")
    return None

def registrar_historico(moto_id, posicao):
    historico = {
        "posicao": posicao,
        "motoId": moto_id,
        "zonaId": ZONA_ID,
        "sensorId": SENSOR_ID
    }
    try:
        response = requests.post(f"{API_BASE}/historicos", json=historico, auth=AUTH, timeout=3)
        print(f"[API] Histórico registrado: {response.status_code}")
    except Exception as e:
        print(f"[API] Falha ao registrar histórico: {e}")

# ================== CARREGA MODELO YOLOv8 ==================
model = YOLO(YOLO_MODEL)
cap = cv2.VideoCapture(VIDEO_PATH)

# ================== CONTROLE DE MOTOS DETECTADAS ==================
motos_ativas = {}  # {label: {"id": moto_id, "posicao": posicao}}
frame_id = 0

# ================== LOOP PRINCIPAL ==================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, verbose=False)[0]
    motorcycle_id = [k for k, v in results.names.items() if v == "motorcycle"][0]
    motos = [box for box in results.boxes if int(box.cls) == motorcycle_id]

    motos_ids_frame = []
    for idx, box in enumerate(motos):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        label = f"Moto_{idx+1}"
        motos_ids_frame.append(label)

        # Se é uma nova moto detectada
        if label not in motos_ativas:
            placa = gerar_placa_mercosul()
            chassi = gerar_chassi()
            modelo = random.choice(["Pop", "Sport"])
            moto_id = registrar_moto(placa, chassi, modelo)
            if moto_id:
                posicao = POSICAO_BASE + idx
                motos_ativas[label] = {"id": moto_id, "posicao": posicao}
                registrar_historico(moto_id, posicao)

        # Desenha retângulo
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"Moto {confidence:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

    # Remove motos que sumiram
    for label in list(motos_ativas.keys()):
        if label not in motos_ids_frame:
            print(f"[API] Moto removida da tela: {label}")
            del motos_ativas[label]

    # ================== MOSTRA TOTAL ==================
    contador = len(motos_ids_frame)
    info_text = f"Total Motos: {contador} | IDs: {', '.join(motos_ids_frame)}"
    cv2.putText(frame, info_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Visão Computacional - MottuMap", frame)

    frame_id += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()
