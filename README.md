# restaurante
Aplicación web para gestionar el menú, pedidos y órdenes de un restaurant

## Crear entorno virtual
```bash
python -m venv venv
```

## Activar entorno virtual

- Linux/Mac: 
```bash
source venv/bin/activate
```
- Windows: 
```bash
source venv/Scripts/activate
```
- Windows (alternativa): 
```bash
./venv/Scripts/activate
```

## Instalar dependencias
```bash
pip install -r requirements.txt
```

## Hacer migraciones
```bash
python manage.py makemigrations
python manage.py migrate 
```

## Llenar base de datos con fixture
```bash
python manage.py loaddata products.json
```

## Correr app
```bash
python manage.py runserver
```