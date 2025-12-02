import csv
import datetime
from src.itsql import Itsql

# ── Conexión SQL ──
itsql = Itsql()

# ── Contadores de consultas SQL ──
sql_counters = {
    'total': 0,
    'select': 0,
    'insert': 0,
    'update': 0,
    'delete': 0,
    'other': 0
}

# ── Función para ejecutar y contar SQL ──
def execute_and_count(sql, counter_type='other'):
    """Ejecuta SQL y cuenta el tipo de consulta"""
    sql_counters['total'] += 1
    sql_counters[counter_type] += 1
    return itsql.execute(sql)

def select_and_count(sql):
    """Ejecuta SELECT y cuenta"""
    sql_counters['total'] += 1
    sql_counters['select'] += 1
    return itsql.select(sql)

# ── CSV a procesar ──
csv_file = 'denue_inegi_46111_.csv'

# ── Tablas a vaciar ──
tablas = [
    'contacto', 'division_territorial', 'personas', 'actividad',
    'direccion_complemento', 'vialidad_referencia', 'vialidad',
    'establecimientos', 'tipo_asentamiento_dic', 'tipo_vial_dic',
    'tipo_unidad_economica'
]

# Desactivar FK temporalmente
execute_and_count("SET FOREIGN_KEY_CHECKS=0;", 'other')

# Ajustar precisión de coordenadas
try:
    execute_and_count("ALTER TABLE test3.establecimientos MODIFY latitud DECIMAL(11,8), MODIFY longitud DECIMAL(11,8);", 'other')
except:
    print("⚠️  Las columnas ya están modificadas o hubo un error")

for tabla in tablas:
    execute_and_count(f"TRUNCATE TABLE test3.{tabla};", 'delete')

execute_and_count("SET FOREIGN_KEY_CHECKS=1;", 'other')

# ── Diccionarios para cachear IDs ──
tipo_unidad_map = {}
tipo_vial_map = {}
tipo_asent_map = {}

# ── Contador y batch para progreso ──
count = 0
batch_size = 1000
total_inserted = 0


# ── Función para validar coordenadas ──
def validar_coordenada(valor, tipo='latitud'):
    if not valor or valor.strip() == '':
        return 'NULL'
    try:
        valor_limpio = valor.strip().replace(' ', '')
        num = float(valor_limpio)
        if tipo == 'latitud' and (-90 <= num <= 90):
            return num
        elif tipo == 'longitud' and (-180 <= num <= 180):
            return num
        else:
            return None
    except:
        return None


# ── Registrar inicio ──
inicio = datetime.datetime.now()
print(f"🚀 Iniciando inserciones a las {inicio}")
print(f"📊 Procesando archivo: {csv_file}")

# ── Leer todo el archivo una sola vez ──
print("📖 Leyendo archivo CSV...")
with open(csv_file, newline='', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    todas_las_filas = list(reader)  # Guardar todas las filas en memoria

print(f"📚 Total de filas leídas: {len(todas_las_filas):,}")

# ── Procesar diccionarios primero ──
print("📝 Procesando diccionarios...")
for row in todas_las_filas:
    # Tipo unidad económica
    tipo_uni = row['tipoUniEco'].strip()
    if tipo_uni and tipo_uni not in tipo_unidad_map:
        execute_and_count(f"INSERT IGNORE INTO test3.tipo_unidad_economica (nombre_tipo) VALUES ('{tipo_uni}');", 'insert')
        res = select_and_count(f"SELECT id FROM test3.tipo_unidad_economica WHERE nombre_tipo='{tipo_uni}';")
        tipo_unidad_map[tipo_uni] = res['id'] if res else 1

    # Tipo asentamiento
    tipo_asent = row['tipo_asent'].strip()
    if tipo_asent and tipo_asent not in tipo_asent_map:
        execute_and_count(f"INSERT IGNORE INTO test3.tipo_asentamiento_dic (descripcion) VALUES ('{tipo_asent}');", 'insert')
        res = select_and_count(f"SELECT id FROM test3.tipo_asentamiento_dic WHERE descripcion='{tipo_asent}';")
        tipo_asent_map[tipo_asent] = res['id'] if res else 1

    # Tipos vialidad
    for vial_col in ['tipo_vial', 'tipo_v_e_1', 'tipo_v_e_2', 'tipo_v_e_3']:
        tipo_vial = row[vial_col].strip()
        if tipo_vial and tipo_vial not in tipo_vial_map:
            execute_and_count(f"INSERT IGNORE INTO test3.tipo_vial_dic (descripcion) VALUES ('{tipo_vial}');", 'insert')
            res = select_and_count(f"SELECT id FROM test3.tipo_vial_dic WHERE descripcion='{tipo_vial}';")
            tipo_vial_map[tipo_vial] = res['id'] if res else 1

print(
    f"✅ Diccionarios procesados: {len(tipo_unidad_map)} tipos unidad, {len(tipo_vial_map)} tipos vial, {len(tipo_asent_map)} tipos asentamiento")

# ── Procesar datos principales ──
print("📥 Insertando datos principales...")
for row in todas_las_filas:
    count += 1
    try:
        # IDs de diccionarios
        tipo_uni = row['tipoUniEco'].strip()
        id_tipo_uni = tipo_unidad_map.get(tipo_uni, 'NULL')

        tipo_asent = row['tipo_asent'].strip()
        id_tipo_asent = tipo_asent_map.get(tipo_asent, 'NULL')

        tipo_vial = row['tipo_vial'].strip()
        id_tipo_vial = tipo_vial_map.get(tipo_vial, 'NULL')

        # Validar coordenadas
        latitud_val = validar_coordenada(row['latitud'], 'latitud')
        longitud_val = validar_coordenada(row['longitud'], 'longitud')
        latitud = latitud_val if latitud_val is not None else 'NULL'
        longitud = longitud_val if longitud_val is not None else 'NULL'

        # ── Establecimientos ──
        id_estab = int(row['id'] or 0)
        clee = row['clee'].strip().replace("'", "''")
        nom_estab = row['nom_estab'].strip().replace("'", "''")
        raz_social = row['raz_social'].strip().replace("'", "''")
        fecha_alta = row['fecha_alta'].strip()

        execute_and_count(
            f"INSERT INTO test3.establecimientos "
            f"(id, clee, nom_estab, raz_social, tipoUniEco_id, fecha_alta, latitud, longitud) "
            f"VALUES ({id_estab}, '{clee}', '{nom_estab}', '{raz_social}', "
            f"{id_tipo_uni}, '{fecha_alta}', {latitud}, {longitud});",
            'insert'
        )

        # ── Vialidad principal ──
        nom_vial = row['nom_vial'].strip().replace("'", "''")
        numero_ext = row['numero_ext'].strip()
        letra_ext = row['letra_ext'].strip()

        execute_and_count(
            f"INSERT INTO test3.vialidad "
            f"(establecimiento_id, tipo_vial_id, nom_vial, numero_ext, letra_ext) "
            f"VALUES ({id_estab}, {id_tipo_vial}, '{nom_vial}', '{numero_ext}', '{letra_ext}');",
            'insert'
        )

        # ── Vialidades de referencia ──
        for i in range(1, 4):
            tipo_v_e = row[f'tipo_v_e_{i}'].strip()
            nom_v_e = row[f'nom_v_e_{i}'].strip().replace("'", "''")

            if tipo_v_e and nom_v_e:
                id_tipo_v_e = tipo_vial_map.get(tipo_v_e, 'NULL')
                execute_and_count(
                    f"INSERT INTO test3.vialidad_referencia "
                    f"(establecimiento_id, tipo_v_e_id, nom_v_e, numero_orden) "
                    f"VALUES ({id_estab}, {id_tipo_v_e}, '{nom_v_e}', {i});",
                    'insert'
                )

        # ── Dirección complemento ──
        edificio = row['edificio'].strip().replace("'", "''")
        edificio_e = row['edificio_e'].strip().replace("'", "''")
        numero_int = row['numero_int'].strip()
        letra_int = row['letra_int'].strip()
        nomb_asent = row['nomb_asent'].strip().replace("'", "''")
        tipoCenCom = row['tipoCenCom'].strip().replace("'", "''")
        nom_CenCom = row['nom_CenCom'].strip().replace("'", "''")
        num_local = row['num_local'].strip()
        cod_postal = row['cod_postal'].strip()

        execute_and_count(
            f"INSERT INTO test3.direccion_complemento "
            f"(establecimiento_id, edificio, edificio_e, numero_int, letra_int, "
            f"tipo_asent_id, nomb_asent, tipoCenCom, nom_CenCom, num_local, cod_postal) "
            f"VALUES ({id_estab}, '{edificio}', '{edificio_e}', '{numero_int}', '{letra_int}', "
            f"{id_tipo_asent}, '{nomb_asent}', '{tipoCenCom}', '{nom_CenCom}', '{num_local}', '{cod_postal}');",
            'insert'
        )

        # ── Actividad ──
        codigo_act = row['codigo_act'].strip()
        nombre_act = row['nombre_act'].strip().replace("'", "''")
        execute_and_count(
            f"INSERT INTO test3.actividad (establecimiento_id, codigo_act, nombre_act) "
            f"VALUES ({id_estab}, '{codigo_act}', '{nombre_act}');",
            'insert'
        )

        # ── Personas ──
        per_ocu = row['per_ocu'].strip()
        execute_and_count(
            f"INSERT INTO test3.personas (establecimiento_id, per_ocu) "
            f"VALUES ({id_estab}, '{per_ocu}');",
            'insert'
        )

        # ── División territorial ──
        cve_ent = row['cve_ent'].strip()
        entidad = row['entidad'].strip().replace("'", "''")
        cve_mun = row['cve_mun'].strip()
        municipio = row['municipio'].strip().replace("'", "''")
        cve_loc = row['cve_loc'].strip()
        localidad = row['localidad'].strip().replace("'", "''")
        ageb = row['ageb'].strip()
        manzana = row['manzana'].strip()

        execute_and_count(
            f"INSERT INTO test3.division_territorial "
            f"(establecimiento_id, cve_ent, entidad, cve_mun, municipio, cve_loc, localidad, ageb, manzana) "
            f"VALUES ({id_estab}, '{cve_ent}', '{entidad}', '{cve_mun}', '{municipio}', "
            f"'{cve_loc}', '{localidad}', '{ageb}', '{manzana}');",
            'insert'
        )

        # ── Contacto ──
        telefono = row['telefono'].strip()
        correo = row['correoelec'].strip().replace("'", "''")
        www = row['www'].strip().replace("'", "''")
        execute_and_count(
            f"INSERT INTO test3.contacto (establecimiento_id, telefono, correoelec, www) "
            f"VALUES ({id_estab}, '{telefono}', '{correo}', '{www}');",
            'insert'
        )

        total_inserted += 1

        # ── Mostrar progreso ──
        if count % batch_size == 0:
            print(f"📊 Procesadas {count} filas | Insertadas: {total_inserted} registros")
            print(f"📈 Consultas SQL ejecutadas hasta ahora: {sql_counters['total']:,}")

    except Exception as e:
        print(f"❌ Fila {row.get('id', 'N/A')} NO insertada: {str(e)[:100]}...")
        continue

# ── Commit final ──
itsql.commit()

# ── Verificar datos insertados ──
print("🔍 Verificando datos insertados...")
res_estab = select_and_count("SELECT COUNT(*) as total FROM test3.establecimientos;")
res_vial = select_and_count("SELECT COUNT(*) as total FROM test3.vialidad;")
res_act = select_and_count("SELECT COUNT(*) as total FROM test3.actividad;")

print(f"📊 Establecimientos insertados: {res_estab['total']:,}")
print(f"📊 Vialidades insertadas: {res_vial['total']:,}")
print(f"📊 Actividades insertadas: {res_act['total']:,}")

# ── Estadísticas de consultas SQL ──
print(f"\n📊 ESTADÍSTICAS DE CONSULTAS SQL EJECUTADAS:")
print(f"🔢 TOTAL de consultas: {sql_counters['total']:,}")
print(f"📥 INSERT: {sql_counters['insert']:,}")
print(f"🔍 SELECT: {sql_counters['select']:,}")
print(f"🗑️  DELETE/TRUNCATE: {sql_counters['delete']:,}")
print(f"⚙️  OTHER: {sql_counters['other']:,}")

# ── Calcular consultas por tabla aproximadas ──
print(f"\n📈 CONSULTAS POR OPERACIÓN:")
print(f"• Diccionarios: ~{len(tipo_unidad_map) + len(tipo_vial_map) + len(tipo_asent_map)} INSERT + SELECT")
print(f"• Establecimientos: {count:,} INSERT")
print(f"• Vialidad principal: {count:,} INSERT")
print(f"• Vialidad referencia: ~{count * 3} INSERT (máximo)")
print(f"• Dirección complemento: {count:,} INSERT")
print(f"• Actividad: {count:,} INSERT")
print(f"• Personas: {count:,} INSERT")
print(f"• División territorial: {count:,} INSERT")
print(f"• Contacto: {count:,} INSERT")

# ── Fin del proceso ──
fin = datetime.datetime.now()
duracion = fin - inicio
print(f"\n🎉 PROCESO COMPLETADO")
print(f"⏰ Hora inicio: {inicio}")
print(f"⏰ Hora fin: {fin}")
print(f"⏱️  Duración total: {duracion}")
print(f"📈 Filas procesadas: {count:,}")
print(f"✅ Registros insertados: {total_inserted:,}")
print(f"❌ Errores: {count - total_inserted:,}")
print(f"📊 Consultas SQL totales: {sql_counters['total']:,}")