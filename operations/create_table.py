import os

def create_table(table_name, fields):
    # Asegurar que la carpeta tables existe
    tables_dir = "tables"
    os.makedirs(tables_dir, exist_ok=True)
    
    # Ruta del archivo de la tabla
    table_path = os.path.join(tables_dir, f"{table_name}.udsql")
    
    # Verificar si la tabla ya existe
    if os.path.exists(table_path):
        print(f"Error: La tabla '{table_name}' ya existe")
        return
    
    # Escribir la cabecera con los nombres de los campos
    with open(table_path, "w", encoding="utf-8") as file:
        file.write("|".join(fields) + "\n")
    
    print(f"Tabla '{table_name}' creada con exito")

# Crear todas las tablas
def create_all_tables():
    tables = {
        "Estudiantes": ["ID","Codigo", "Nombre", "Documento", "Telefono", "Direccion", "Correo", "Estado"],
        "Profesores": ["ID", "Nombre", "Documento", "Telefono", "Correo", "Proyecto Curricular"],
        "Administrativos": ["ID", "Nombre", "Documento", "Telefono", "Correo", "Cargo"],
        "Espacios_Academicos": ["ID", "Nombre", "Grupo", "Clasificacion", "Creditos"],
        "Biblioteca": ["ID", "Titulo", "Autor", "Año", "Estado"],
        "Carrera": ["ID", "Codigo", "Nombre", "Facultad"]
    }
    
    for table, fields in tables.items():
        create_table(table, fields)

if __name__ == "__main__":
    create_all_tables()
