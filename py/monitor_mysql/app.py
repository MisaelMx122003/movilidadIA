from flask import Flask, render_template, jsonify
import mysql.connector
import time
from threading import Thread
import json

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'web',
    'password': '123456789',
    'database': 'information_schema'
}

# Variables globales para almacenar métricas
metrics_data = []
max_points = 50

def get_mysql_stats():
    """Obtiene estadísticas de MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Consulta para obtener estadísticas de comandos
        cursor.execute("""
            SHOW GLOBAL STATUS 
            WHERE Variable_name IN ('Com_select', 'Com_insert', 'Com_update', 'Com_delete', 'Queries')
        """)
        
        stats = {}
        for name, value in cursor.fetchall():
            stats[name.lower()] = int(value)
        
        print(f"Stats obtenidas: {stats}")  # Debug
        
        cursor.close()
        conn.close()
        return stats
    except Exception as e:
        print(f"Error: {e}")
        return None

def calculate_qps():
    """Calcula consultas por segundo"""
    global metrics_data
    
    prev_stats = None
    
    while True:
        current_stats = get_mysql_stats()
        current_time = time.time()
        
        if prev_stats and current_stats:
            time_diff = current_time - prev_time
            
            qps_data = {
                'timestamp': current_time * 1000,  # JavaScript usa milisegundos
                'total_qps': (current_stats['queries'] - prev_stats['queries']) / time_diff,
                'select_qps': (current_stats['com_select'] - prev_stats['com_select']) / time_diff,
                'insert_qps': (current_stats['com_insert'] - prev_stats['com_insert']) / time_diff,
                'update_qps': (current_stats['com_update'] - prev_stats['com_update']) / time_diff,
                'delete_qps': (current_stats['com_delete'] - prev_stats['com_delete']) / time_diff
            }
            
            print(f"QPS calculado: {qps_data}")  # Debug
            metrics_data.append(qps_data)
            
            # Mantener solo los últimos N puntos
            if len(metrics_data) > max_points:
                metrics_data.pop(0)
        
        prev_stats = current_stats
        prev_time = current_time
        time.sleep(2)  # Actualizar cada 2 segundos

@app.route('/')
def index():
    return render_template('monitor.html')

@app.route('/api/metrics')
def get_metrics():
    return jsonify(metrics_data)

if __name__ == '__main__':
    # Iniciar el hilo para recopilar métricas
    metrics_thread = Thread(target=calculate_qps, daemon=True)
    metrics_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)