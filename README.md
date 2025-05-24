# Gestão Automatizada de Pátios Mottu

## Apresentação do Problema Real
A Mottu enfrenta um desafio considerável na organização e gestão eficiente de seus pátios. Atualmente, a localização das motos é monitorada manualmente, o que representa um processo demorado e sujeito a erros. Automatizar e digitalizar este sistema é essencial para melhorar a eficiência operacional, reduzir o tempo de busca de motos específicas e minimizar os erros de localização.

## Justificativa para o Uso das Tecnologias
Escolhemos usar câmeras e sensores RFID devido ao equilíbrio favorável que essas tecnologias oferecem entre custo e precisão. Na análise de custo-benefício, essas soluções se destacaram não apenas pelo investimento inicial relativamente baixo, mas também pela facilidade de implementação em relação às necessidades complexas do pátio da Mottu. Considerando-se esses fatores, essa combinação oferece uma solução robusta e eficiente.

## Tecnologias Utilizadas

- Visão Computacional: Utilizada para identificar motos estacionadas em diferentes áreas do pátio e para monitorar se as vagas estão ocupadas, garantindo precisão no mapeamento digital do pátio.
- Etiquetas e Sensores RFID: Os sensores serão posicionados em zonas estratégicas do pátio, como entradas, saídas, áreas designadas para reparos leves, depósitos de carcaças, e zonas para motos sem placa. Eles permitirão um controle granular do movimento e localização das motos.

## Funcionamento dos Componentes-Chave
A solução opera integrando diferentes tecnologias para um resultado coeso:

- *Rastreamento através de RFID:* As etiquetas RFID, associadas a sensores localizados em pontos-chave, fornecem um histórico detalhado da movimentação das motos no pátio, facilitando o rastreamento eficiente.
- *Integração Câmera-Sensor:* Quando uma moto passa por uma sensor de estacionamento, seu ID é registrado e enviado para o sistema integrado à câmera. Isso permite identificar e registrar qual moto é estacionada em determinada vaga, atualizando seu status no mapa digital com dados como {ID:X, Vaga:X, Zona:X}. Assim, cada ação de ocupação e desocupação de vagas é automaticamente registrada e atualizada no sistema.

## Viabilidade Técnica Inicial do Projeto
Nossa solução se destaca por sua viabilidade técnica. A instalação de câmeras e sensores em locais estratégicos configura um processo relativamente simples. A instalação de dispositivos RFID em todas as motos é um desafio, mas absolutamente crucial para garantir precisão e eficácia no rastreamento automatizado. O alcance dessa precisão otimiza a gestão operacional do pátio e reduz significadamente erros de localização. Acreditamos que, com os passos adequados de implementação, esta solução proporcionará benefícios significativos para a operação da Mottu.


## Estrutura do diretótrio

```
├── App.py # Script principal para execução
├── dados/ # Diretório contendo os vídeos para processamento
│ └── vid1.mp4 # Exemplo de vídeo
├── requirements.txt # Arquivo de dependências
└── yolov5s.pt # Pesos pré-treinados do modelo YOLOv5
```

## Passos para Configuração e Execução
### Instalação de Dependências:
Clone o repositório
```
   git clone https://github.com/GThomaz03/challenge-IoT
   cd challenge-IoT
```

Crie e ative um ambiente virtual

Windows:
```
   python -m venv venv
   venv/Scripts/activate
```

Linux/macOS
```
   python3 -m venv venv
   source venv/bin/activate
```

Assegure que você está no diretório raiz do projeto e execute:
```
   pip install -r requirements.txt
```

Caso não tenha o Yolov5s intalado em sua máquina, execute:
```
   git clone https://github.com/ultralytics/yolov5
   cd yolov5
   pip install -r requirements.txt
```

Executar o Programa:

Para rodar a aplicação principal, utilize o comando:
```
   cd ..
   python App.py
```

Certifique-se de que o arquivo de vídeo vid4.mp4 está presente na pasta dados, ou ajuste o código no App.py para utilizar qualquer outro vídeo de sua escolha.

### Observações:

Certifique-se de que o arquivo yolov5s.pt está no mesmo diretório para que o modelo possa ser carregado corretamente.

O script processará o vídeo e apresentará a detecção de motos em tempo real.

