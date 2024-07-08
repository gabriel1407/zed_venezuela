# Usar una imagen base de Python 3.10.4
FROM python:3.10.4-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt y el archivo .env al contenedor
COPY requirements.txt ./
COPY .env ./
COPY wait-for-it.sh ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para correr la aplicación
CMD ["./wait-for-it.sh", "db:3306", "--", "python", "app.py"]
