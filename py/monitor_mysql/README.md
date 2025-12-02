# Monitor MySQL QPS

Monitor en tiempo real para medir consultas por segundo en MySQL usando Flask y Chart.js.

## 📋 Requisitos Previos

- Python 3.7+
- pipenv (instalar con `pip install pipenv`)
- MySQL Server 5.7+ o MariaDB
- Usuario MySQL con permisos para consultar estadísticas globales

## 🚀 Instalación

### 1. Instalar dependencias con pipenv
```bash
cd monitor_mysql
pipenv install
```

### 2. Configurar MySQL

#### Crear usuario para monitoreo:
```sql
CREATE USER 'monitor'@'localhost' IDENTIFIED BY 'monitor123';
GRANT PROCESS ON *.* TO 'monitor'@'localhost';
GRANT SELECT ON information_schema.* TO 'monitor'@'localhost';
FLUSH PRIVILEGES;
```

#### O usar usuario existente con permisos:
```sql
GRANT PROCESS ON *.* TO 'web'@'localhost';
GRANT SELECT ON information_schema.* TO 'web'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configurar credenciales

Edita las credenciales en `app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'web',           # Tu usuario MySQL
    'password': '123456789', # Tu contraseña
    'database': 'information_schema'
}
```

## 🏃♂️ Ejecutar la aplicación

```bash
pipenv run python app.py
```

### O activar el entorno virtual:
```bash
pipenv shell
python app.py
```

**Acceder a:** http://localhost:5000

## 🔧 Solución de problemas

### Error de conexión MySQL
```
Error: Access denied for user 'web'@'localhost'
```
**Solución:** Verificar credenciales y permisos del usuario

### Gráfica no se actualiza
1. Verificar logs en la terminal de Flask
2. Abrir consola del navegador (F12) para ver errores
3. Asegurar que hay actividad en MySQL

### Probar conectividad
```bash
mysql -u web -p123456789 -e "SHOW GLOBAL STATUS LIKE 'Queries'"
```

## 📊 Características

- **Gráfica en tiempo real** con Chart.js
- **Métricas separadas**: Total QPS, SELECT, INSERT, UPDATE, DELETE
- **Actualización automática** cada 2 segundos
- **Interfaz responsive** y moderna
- **Estadísticas en vivo** con tarjetas informativas
- **Debug integrado** para diagnóstico

## 🧪 Generar actividad de prueba

Para ver la gráfica en acción, ejecuta consultas en MySQL:

```sql
-- En otra terminal MySQL
USE admindb;
SELECT COUNT(*) FROM empresas;
INSERT INTO empresas (empresa) VALUES ('Test');
UPDATE empresas SET empresa='Test2' WHERE empresa='Test';
DELETE FROM empresas WHERE empresa='Test2';
```

## 📁 Estructura del proyecto

```
monitor_mysql/
├── app.py              # Aplicación Flask principal
├── Pipfile             # Dependencias pipenv
├── Pipfile.lock        # Versiones bloqueadas (generado automáticamente)
├── requirements.txt    # Dependencias Python (alternativo)
├── README.md          # Esta documentación
└── templates/
    └── monitor.html   # Interfaz web con gráfica
```

## 🚨 Comandos de diagnóstico

### Verificar permisos MySQL:
```sql
SHOW GRANTS FOR 'web'@'localhost';
```

### Ver estadísticas actuales:
```sql
SHOW GLOBAL STATUS WHERE Variable_name IN ('Com_select', 'Com_insert', 'Com_update', 'Com_delete', 'Queries');
```

### Logs de Flask:
- Los logs aparecen en la terminal donde ejecutaste `python app.py`
- Busca mensajes como "Stats obtenidas:" y "QPS calculado:"