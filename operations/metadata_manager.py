import os
import pickle

METADATA_DIR = "metadata"
METADATA_FILE = os.path.join(METADATA_DIR, "metadata.udsql")

def save_metadata(metadata):
    """Guarda la metadata en un archivo usando pickle"""
    os.makedirs(METADATA_DIR, exist_ok=True)
    with open(METADATA_FILE, "wb") as file:
        pickle.dump(metadata, file)

def load_metadata():
    """Carga la metadata desde el archivo, si existe"""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "rb") as file:
            return pickle.load(file)
    return {}

def add_table_metadata(table_name, fields):
    """Agrega una nueva tabla a la metadata y la guarda"""
    metadata = load_metadata()
    if table_name in metadata:
        print(f"Error: La tabla '{table_name}' ya esta en la metadata")
        return
    
    metadata[table_name] = fields
    save_metadata(metadata)
    print(f"Metadata actualizada: Tabla '{table_name}' añadida")

if __name__ == "__main__":
    # Definir las tablas
    tables = {
        "Estudiantes": ["Código", "Nombre", "Documento", "Teléfono", "Dirección", "Correo", "Estado"],
        "Profesores": ["Código", "Nombre", "Documento", "Teléfono", "Correo", "Proyecto Curricular"],
        "Administrativos": ["Código", "Nombre", "Documento", "Teléfono", "Correo", "Cargo"],
        "Espacios_Academicos": ["Código", "Nombre", "Grupo", "Clasificación", "Créditos"],
        "Biblioteca": ["Código", "Título", "Autor", "Año", "Estado"]
    }
    
    # Guardar todas las tablas en la metadata
    for table, fields in tables.items():
        add_table_metadata(table, fields)
