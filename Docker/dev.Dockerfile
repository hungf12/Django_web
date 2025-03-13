# Sử dụng Python image chính thức
FROM python:3.12.4

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Expose port để Django có thể chạy
EXPOSE 8000

# Chạy ứng dụng Django ở chế độ development với reload
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]