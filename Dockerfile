# Usar una imagen de Python como base
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiar el archivo requirements.txt e instalar las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Aplicar migraciones
RUN python InventoryManager/manage.py migrate

# Cargar fixtures (si es necesario)
RUN python InventoryManager/manage.py loaddata InventoryManager/core/users_groups_fixture.json

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "InventoryManager/manage.py", "runserver", "0.0.0.0:8000"]
