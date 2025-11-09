import streamlit as st
import cv2
from PIL import Image
import time
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from ultralytics import YOLO
import random
import string

# ================== CONFIGURAÇÃO ==================
VIDEO_PATH = "vision/Data/vid4.mp4"
YOLO_MODEL = "yolov8s.pt"
API_HISTORICO = "https://webapp-mottumap.azurewebsites.net/api/historicos"
API_MOTO = "https://webapp-mottumap.azurewebsites.net/api/motos"

# Autenticação
API_USER = "admin@mottu.com"
API_PASS = "123456"

ZONA_ID = 1
SENSOR_ID = 1
POSICAO_BASE = 1

st.set_page_config(page_title="Mottu Dashboard", layout="wide")
st.title("📊 Dashboard de Monitoramento – Mottu")

# ================== PLACEHOLDERS ==================
placeholder_video = st.empty()
placeholder_visao = st.empty()
placeholder_ids = st.empty()

# ================== CARREGA MODELO YOLOv8 ==================
model = YOLO(YOLO_MODEL)
cap = cv2.VideoCapture(VIDEO_PATH)

# ================== HISTÓRICO EM MEMÓRIA ==================
if "historico_motos" not in st.session_state:
    st.session_state.historico_motos = []
if "ultimo_contador" not in st.session_state:
    st.session_state.ultimo_contador = -1

# ================== FUNÇÕES AUXILIARES ==================
def gerar_placa_mercosul():
    """Gera placa no formato Mercosul: AAA1A23"""
    letras = string.ascii_uppercase
    numeros = string.digits
    return f"{random.choice(letras)}{random.choice(letras)}{random.choice(letras)}{random.choice(numeros)}{random.choice(letras)}{random.choice(numeros)}{random.choice(numeros)}"

def gerar_chassi():
    """Gera um chassi alfanumérico com 17 caracteres"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=17))

def verificar_criar_moto(moto_id):
    """Verifica se a moto existe, e cria se não existir."""
    try:
        r = requests.get(f"{API_MOTO}/{moto_id}", auth=HTTPBasicAuth(API_USER, API_PASS), timeout=2)
        if r.status_code == 404:
            # Cria a moto com dados realistas
            payload = {
                "placa": gerar_placa_mercosul(),
                "chassi": gerar_chassi(),
                "modelo": "Pop"
            }
            r_post = requests.post(API_MOTO, json=payload, auth=HTTPBasicAuth(API_USER, API_PASS), timeout=2)
            return r_post.status_code in [200, 201]
        return True
    except requests.exceptions.RequestException:
        return False

# ================== LOOP PRINCIPAL ==================
frame_id = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ================== DETECÇÃO ==================
    results = model(frame, verbose=False)[0]
    motorcycle_id = [k for k, v in results.names.items() if v == "motorcycle"][0]
    motos = [box for box in results.boxes if int(box.cls) == motorcycle_id]

    contador = len(motos)
    motos_ids_frame = []

    for idx, box in enumerate(motos):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
        cv2.putText(frame, f"Moto {confidence:.2f}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
        motos_ids_frame.append(f"Moto_{idx+1}")

    cv2.putText(frame, f"Total Motos: {contador}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    st.session_state.historico_motos.append(contador)

    # ================== ENVIA PARA API COM AUTENTICAÇÃO ==================
    if contador != st.session_state.ultimo_contador and contador > 0:
        st.session_state.ultimo_contador = contador
        for i in range(contador):
            moto_id = i + 1
            if verificar_criar_moto(moto_id):
                payload = {
                    "posicao": POSICAO_BASE + i,
                    "motoId": moto_id,
                    "zonaId": ZONA_ID,
                    "sensorId": SENSOR_ID
                }
                try:
                    response = requests.post(
                        API_HISTORICO,
                        json=payload,
                        auth=HTTPBasicAuth(API_USER, API_PASS),
                        timeout=2
                    )
                    if response.status_code in [200, 201]:
                        st.toast(f"✅ Histórico salvo: Moto {moto_id}", icon="✅")
                    else:
                        st.warning(f"⚠️ Erro {response.status_code} ao salvar histórico.")
                except requests.exceptions.RequestException:
                    st.warning("❌ API não acessível no momento.")
            else:
                st.warning(f"⚠️ Não foi possível criar/verificar Moto {moto_id}.")

    # ================== VISUALIZAÇÃO ==================
    df_visao = pd.DataFrame({"qtd_motos": st.session_state.historico_motos})
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    placeholder_video.image(img, caption="📹 Visão Computacional", use_container_width=True)

    with placeholder_visao.container():
        st.subheader("📊 Histórico de Motos Detectadas")
        st.metric("Motos Detectadas (último frame)", contador)
        st.line_chart(df_visao["qtd_motos"])

    with placeholder_ids.container():
        st.subheader("🏍️ Motos no Frame Atual")
        if motos_ids_frame:
            st.write(", ".join(motos_ids_frame))
        else:
            st.info("Nenhuma moto detectada neste frame")

    frame_id += 1
    time.sleep(0.05)

cap.release()
