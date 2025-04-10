FROM python:3.9

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory
# WORKDIR /app

# # Copy requirements.txt and install dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the project files
# COPY . /app/

# # Expose the port
# EXPOSE 8000

# # Start the Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

WORKDIR /app

# 複製依賴清單進來
COPY requirements.txt .

# 安裝依賴
RUN pip install --upgrade pip && pip install -r requirements.txt

# 複製專案程式碼到容器中
COPY . .

# 對外開放埠口（假設用的是8000）
EXPOSE 8000

# 預設啟動指令（你可以根據實際需求更改）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]