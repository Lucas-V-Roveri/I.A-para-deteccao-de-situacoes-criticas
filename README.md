# Detecção de Fogo e Fumaça - Aplicativo Web


## Propósito



Este projeto é um aplicativo web construído com Flask que utiliza um modelo de detecção de objetos YOLO (You Only Look Once) para detectar fogo e fumaça em fluxos de vídeo. Ele suporta dois modos de entrada:

- Carregamento de um arquivo de vídeo MP4 para análise.

- Uso de uma webcam para detecção em tempo real.



O aplicativo processa os quadros de vídeo, anota as detecções com caixas delimitadoras (para confidências ≥ 55%) e aciona alertas com base na lógica de detecção: um alerta é ativado se pelo menos duas detecções ocorrerem dentro de 2,5 segundos e persiste por 25 segundos a partir da última detecção, estendendo-se com novas detecções. Isso o torna adequado para um sistema de alarme simples para monitoramento de fogo/fumaça.



A interface é amigável para dispositivos móveis, com texto em português para títulos, botões e alertas.


## Requisitos



### Software

- Python 3.8 ou superior

- Uma webcam (para o modo em tempo real; opcional, mas necessária para a funcionalidade da webcam)

- Navegador com permissões de acesso à webcam (para o modo em tempo real)



### Bibliotecas

Instale os seguintes pacotes Python usando pip:

```

pip install flask opencv-python ultralytics

```



### Modelo

- Um modelo YOLO pré-treinado para detecção de fogo/fumaça. Coloque o arquivo de pesos do modelo (`best.pt`) em um diretório `weights/` na raiz do projeto.

&nbsp; - Você pode treinar seu próprio modelo usando Ultralytics YOLO ou usar um pré-treinado adequado para as classes de fogo/fumaça.



### Estrutura de Diretórios

Certifique-se da seguinte estrutura:

```

projeto/

├── app.py                # Código principal do aplicativo Flask

├── weights/

│   └── best.pt           # Pesos do modelo YOLO

├── templates/

│   ├── index.html        # Página de seleção de carregamento/webcam

│   └── stream.html       # Página de fluxo e exibição de alertas

├── static/               # Opcional: para arquivos estáticos (ex.: CSS/JS se adicionados)

└── uploads/              # Criado automaticamente para vídeos carregados

```



## Como Executar



1. **Clonar ou Configurar o Projeto**:

&nbsp;  - Salve o código principal em um arquivo chamado `app.py`.

&nbsp;  - Crie a pasta `templates/` e adicione `index.html` e `stream.html` com o conteúdo HTML fornecido (das instruções anteriores).

&nbsp;  - Coloque os pesos do YOLO em `weights/best.pt`.



2. **Instalar Dependências**:

&nbsp;  ```

&nbsp;  pip install flask opencv-python ultralytics

&nbsp;  ```



3. **Executar o Aplicativo**:

&nbsp;  ```

&nbsp;  python app.py

&nbsp;  ```

&nbsp;  - O aplicativo será iniciado no modo de depuração em `http://127.0.0.1:5000/` (ou `http://localhost:5000/`).



4. **Acessar o Aplicativo**:

&nbsp;  - Abra um navegador web e vá para `http://127.0.0.1:5000/`.

&nbsp;  - Escolha carregar um vídeo MP4 ou usar a webcam.

&nbsp;  - Para o modo webcam, conceda permissões ao navegador quando solicitado.

&nbsp;  - A página de fluxo mostrará o feed de vídeo anotado e alertas em tempo real.



5. **Notas**:

&nbsp;  - Vídeos carregados são salvos temporariamente em `uploads/` e podem ser excluídos após o processamento (descomente `os.remove(video\_path)` se desejado).

&nbsp;  - Limiar de detecção definido para ≥55% de confiança.

&nbsp;  - Lógica de alerta: Aciona com ≥2 detecções em 2,5s, dura 25s a partir da última detecção.

&nbsp;  - Para produção, desative o modo de depuração (`app.run(debug=False)`) e considere hospedar com um servidor WSGI como Gunicorn.

&nbsp;  - Testado em ambientes locais; certifique-se de que o OpenCV pode acessar sua webcam (ex.: índice 0; ajuste se necessário).





