import streamlit as st
import cv2
from PIL import Image
import time
import pandas as pd
import requests
from ultralytics import YOLO

# ================== CONFIGURAÇÃO ==================
VIDEO_PATH = "vision/Data/vid4.mp4"
YOLO_MODEL = "yolov8s.pt"  # YOLOv8
API_URL = "http://localhost:8000/visao/registrar"  # URL da sua API

st.set_page_config(page_title="Mottu Dashboard", layout="wide")
st.title("📊 Dashboard de Monitoramento – Mottu")

# Placeholders
placeholder_video = st.empty()
placeholder_visao = st.empty()
placeholder_ids = st.empty()

# ================== CARREGA MODELO YOLOv8 ==================
model = YOLO(YOLO_MODEL)

# Captura de vídeo
cap = cv2.VideoCapture(VIDEO_PATH)

# ================== HISTÓRICO EM MEMÓRIA ==================
if "historico_motos" not in st.session_state:
    st.session_state.historico_motos = []

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
    motos_ids_frame = []  # lista de IDs das motos no frame atual

    for idx, box in enumerate(motos):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.putText(frame, f"Moto {confidence:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
        contador += 1

        # Cria ID temporário da moto
        motos_ids_frame.append(f"Moto_{idx+1}")

    # Mostra total de motos no frame
    cv2.putText(frame, f"Total Motos: {contador}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # ================== ATUALIZA HISTÓRICO ==================
    st.session_state.historico_motos.append(contador)

    # Envia dados para API
    try:
        payload = {"frame_id": frame_id, "qtd_motos": contador}
        requests.post(API_URL, json=payload, timeout=1)
    except Exception as e:
        st.error(f"Erro ao enviar dados para API: {e}")

    # DataFrame para gráfico
    df_visao = pd.DataFrame({"qtd_motos": st.session_state.historico_motos})

    # ================== MOSTRA NO DASHBOARD ==================
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    placeholder_video.image(img, caption="📹 Visão Computacional", use_container_width=True)

    with placeholder_visao.container():
        st.subheader("📹 Histórico de Motos Detectadas")
        st.metric("Motos Detectadas (último frame)", contador)
        st.line_chart(df_visao["qtd_motos"])

    # ================== IDs das motos no frame ==================
    with placeholder_ids.container():
        st.subheader("🏍️ Motos no Frame Atual")
        if motos_ids_frame:
            st.write(", ".join(motos_ids_frame))
        else:
            st.info("Nenhuma moto detectada neste frame")

    frame_id += 1
    time.sleep(0.05)  # ~20 FPS

cap.release()
