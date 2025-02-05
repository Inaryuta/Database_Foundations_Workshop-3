import os
import pickle

def save_metadata(metadata):
    metadata_path = "metadata.pkl"
    with open(metadata_path, "wb") as file:
        pickle.dump(metadata, file)

def load_metadata():
    metadata_path = "metadata.pkl"
    if os.path.exists(metadata_path):
        with open(metadata_path, "rb") as file:
            return pickle.load(file)
    return {}

def add_table_to_metadata(table_name, fields):
    metadata = load_metadata()
    
    if table_name in metadata:
        print(f"Error: La tabla '{table_name}' ya está en la metadata")
        return
    
    metadata[table_name] = fields
    save_metadata(metadata)
    print(f"Metadata actualizada: Tabla '{table_name}' añadida")

# Crear todas las tablas en la metadata
def create_all_tables_metadata():
    tables = {
        "Estudiantes": ["Código", "Nombre", "Documento", "Teléfono", "Dirección", "Correo", "Estado"],
        "Profesores": ["Código", "Nombre", "Documento", "Teléfono", "Correo", "Proyecto Curricular"],
        "Administrativos": ["Código", "Nombre", "Documento", "Teléfono", "Correo", "Cargo"],
        "Espacios_Academicos": ["Código", "Nombre", "Grupo", "Clasificación", "Créditos"],
        "Biblioteca": ["Código", "Título", "Autor", "Año", "Estado"]
    }
    
    for table, fields in tables.items():
        add_table_to_metadata(table, fields)

if __name__ == "__main__":
    create_all_tables_metadata()
