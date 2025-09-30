# Gestão Automatizada de Pátios – Mottu

link do vído no YouTube: https://youtu.be/dWUZyVhUMdw


## 🎯 Apresentação do Problema
A Mottu enfrenta um grande desafio na **gestão e organização de seus pátios**. Atualmente, a localização das motos é feita de forma **manual**, o que gera:
- Processos demorados  
- Alto risco de erros  
- Dificuldade em encontrar rapidamente uma moto específica  

A proposta deste projeto é **automatizar e digitalizar** esse sistema, integrando **visão computacional e sensores RFID** para aumentar a **eficiência operacional** e reduzir falhas.

---

## ✅ Justificativa para o Uso das Tecnologias
- **Câmeras + YOLOv8** → permitem detectar e monitorar motos de forma automática e em tempo real, com baixo custo de instalação  
- **Sensores RFID** → garantem rastreamento preciso de entrada/saída, movimentação entre zonas e histórico de cada moto  
- **Integração API + Dashboard** → centraliza os dados em um sistema único, acessível e confiável  

Essa combinação entrega uma solução **escalável, precisa e de custo viável**.

---

## 🛠 Tecnologias Utilizadas
- **Visão Computacional (YOLOv8 + OpenCV)**: detecção de motos em vídeos/câmeras  
- **Streamlit**: dashboard interativo para monitoramento em tempo real  
- **FastAPI**: API backend para centralizar dados de visão e RFID  
- **SQLite**: banco de dados leve para registro histórico de eventos  
- **RFID**: sensores instalados em pontos estratégicos do pátio  

---

## 🔄 Funcionamento da Solução
1. **Detecção por câmera (YOLOv8)**  
   - Identifica motos nos vídeos e envia dados para a API (`frame_id` + `qtd_motos`)  

2. **Rastreamento por RFID**  
   - Cada moto possui etiqueta RFID  
   - Sensores registram eventos em zonas como: entrada, saída, manutenção, depósito  

3. **Integração via API (FastAPI)**  
   - Recebe eventos da visão computacional e do RFID  
   - Armazena os dados em banco SQLite  

4. **Visualização em Dashboard (Streamlit)**  
   - Exibe vídeo processado em tempo real  
   - Mostra gráfico histórico da quantidade de motos detectadas  
   - Lista eventos de RFID e visão computacional  

---

## 📂 Estrutura do Diretório

``` bash
   ├── dashboard/             # Interface Streamlit
   │   └── dashboard.py
   ├── api/                   # API FastAPI
   │   ├── main.py            # Rotas principais
   │   ├── crud.py            # Operações no banco
   │   ├── database.py        # Conexão e criação de tabelas
   │   ├── models.py          # Modelos Pydantic
   ├── vision/                # Visão computacional
   │   ├── App.py             # Script principal de visão e envio para API
   │   └── Data/              # Vídeos de teste
   │       └── vid4.mp4
   ├── motos.db               # Banco SQLite
   ├── requirements.txt       # Dependências do projeto
   └── yolov8n.pt             # Pesos pré-treinados YOLOv8 (nano)
```

---

## ⚙️ Passos para Configuração e Execução

### 1. Clone o repositório
```bash
   git clone https://github.com/GThomaz03/challenge-IoT
   cd challenge-IoT
```

## 2. Crie e ative um ambiente virtual
Windows:
```bash
   python -m venv venv
   venv\Scripts\activate
```

Linux/macOS:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

## 3. Instale dependências
```bash
   pip install -r requirements.txt
```

## 4. Inicie a API (FastAPI)
```bash
   uvicorn backend-api.main:app --reload
```
A API estará disponível em: http://localhost:8000

## Inicie o Dashboard (Streamlit)
``` bash
   streamlit run dashboard/dashboard.py
```

---

🖼 Observações
   - Certifique-se de ter o modelo yolov8n.pt na raiz do projeto (ou ajuste o caminho no código)
   - O script processa os vídeos da pasta vision/Data e envia os dados para a API
   - O dashboard mostra vídeo, gráfico histórico e lista de motos detectadas em tempo real
