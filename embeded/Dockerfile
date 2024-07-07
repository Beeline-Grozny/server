# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем зависимости системы
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libopencv-dev \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Nomeroff-net
RUN pip install git+https://github.com/ria-com/nomeroff-net.git

# Устанавливаем зависимости проекта
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем файлы проекта
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт для Flask
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["python", "app.py"]
