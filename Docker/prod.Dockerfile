# Sử dụng Python image chính thức
FROM python:3.12.4

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện cần thiết
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

# Chạy lệnh migrate và collectstatic
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port để Gunicorn có thể chạy
EXPOSE 8000

# Đảm bảo Gunicorn có thể chạy
RUN which gunicorn

# Chạy ứng dụng Django với Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webbanhang.wsgi:application"]