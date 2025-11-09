# 🚀 Gestão Automatizada de Pátios – MottuMap

🎥 **Demonstração:** [https://youtu.be/OXw7AyHvTEk](https://youtu.be/OXw7AyHvTEk)

---

## 👥 Integrantes

- **Eduardo Guilherme Dias** – RM557886
- **Gabriel Alves Thomaz** – RM558637
- **Luiz Sadao Kamada** – RM557652

---

## 🎯 Desafio

A **Mottu** enfrenta dificuldades na **gestão manual dos pátios de motos**, gerando:

- Processos lentos e imprecisos
- Alto risco de erro humano
- Dificuldade em localizar rapidamente uma moto específica

O projeto **MottuMap** automatiza esse processo, combinando:

- **Visão computacional** (detecção automática de motos)
- **Sensores inteligentes** (RFID e visão)
- **API central Java + Dashboard interativo**

Essa integração permite o **monitoramento em tempo real**, com **registro e exclusão automáticos de motos** conforme entram e saem do campo de visão.

---

## 🧠 Solução Proposta

| Componente                    | Função                                            |
| ----------------------------- | ------------------------------------------------- |
| **YOLOv8 + OpenCV**           | Detecta motos em vídeo ao vivo e envia para a API |
| **API Java (Spring Boot)**    | Centraliza o registro, histórico e autenticação   |
| **Dashboard (Streamlit)**     | Monitora em tempo real o vídeo e os dados da API  |
| **Banco Oracle**              | Armazena motos, históricos, sensores e zonas      |
| **Autenticação (Basic Auth)** | Define permissões de acesso entre ADMIN e USER    |

---

## 🔒 Perfis e Permissões

| Email           | Senha  | Role (permissão)      |
| --------------- | ------ | --------------------- |
| admin@mottu.com | 123456 | ADMIN (CRUD completo) |
| user@mottu.com  | 123456 | USER (apenas GET)     |

Todas as requisições da visão e do dashboard passam por autenticação **Basic Auth** antes de acessar a API.

---

## ⚙️ Fluxo de Funcionamento

1. **Detecção por câmera (YOLOv8)**

   - O script `App.py` identifica motos no vídeo e gera dados realistas:

     - Placa no formato Mercosul (`ABC1D23`)
     - Chassi com 17 caracteres alfanuméricos
     - Modelo (ex: “CG 160”, “Pop 110”, “YBR 125”)

2. **Integração com API MottuMap**

   - Quando uma moto é detectada:

     - Envia requisição `POST /api/motos` → cria a moto no banco Oracle
     - Envia `POST /api/historicos` → registra o evento e posição atual

   - Quando a moto sai da tela, ela é removida automaticamente do banco via `DELETE /api/motos/{id}`

3. **Visualização no Dashboard (Streamlit)**

   - Mostra vídeo com detecção em tempo real
   - Exibe gráficos e lista de motos detectadas
   - Atualiza contadores e status de cada zona do pátio

---

## 🧩 Estrutura do Projeto

```bash
challenge-iot
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

## 🛠 Tecnologias Utilizadas

### 🧠 Inteligência Artificial

- **YOLOv8 (Ultralytics)** – detecção de motos em tempo real
- **OpenCV** – processamento de frames

### 🌐 Backend

- **Java (Spring Boot)**
- **JPA / Hibernate**
- **Banco Oracle**
- **Autenticação Basic Auth**

### 📊 Frontend / Dashboard

- **Streamlit** – interface de monitoramento
- **Python (requests, matplotlib)**

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/GThomaz03/challenge-IoT
cd mottumap
```

### 2️⃣ Crie e ative o ambiente Python

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

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Inicie a visão computacional

```bash
python vision/App.py
```

> As motos detectadas serão automaticamente registradas e removidas na API.

### 5️⃣ Execute o dashboard

```bash
streamlit run dashboard/dashboard.py
```

> Acesse no navegador: [http://localhost:8501](http://localhost:8501)

---

## 🧾 Exemplo de Registro Automático

| Evento               | Endpoint          | Método | Exemplo                                                                     |
| -------------------- | ----------------- | ------ | --------------------------------------------------------------------------- |
| Moto detectada       | `/api/motos`      | POST   | `{ "placa": "BRA2A19", "chassi": "9C2JC4110LR000001", "modelo": "CG 160" }` |
| Histórico registrado | `/api/historicos` | POST   | `{ "motoId": 1, "posicao": 3, "zonaId": 1, "sensorId": 2 }`                 |
| Moto removida        | `/api/motos/{id}` | DELETE | —                                                                           |

---

## 📈 Benefícios

- Redução de erros humanos
- Monitoramento em tempo real
- Integração direta com o banco de dados da Mottu
- Automação completa do registro de entrada e saída
- Arquitetura escalável e segura com autenticação

---

## 🔮 Possíveis Extensões Futuras

- Implementar reconhecimento de placas reais (OCR)
- Integrar com câmeras IP ao vivo
- Mapa interativo do pátio com posições em tempo real
- Relatórios analíticos de fluxo de motos

---

## 🧩 Conclusão

O **MottuMap** integra **IA, visão computacional e APIs corporativas** para oferecer uma **gestão de pátio 100% automatizada**, com dados centralizados, segurança e escalabilidade — alinhada à visão de eficiência e tecnologia da Mottu.

