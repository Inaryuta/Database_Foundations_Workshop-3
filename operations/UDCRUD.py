import os
import pickle

class UDSQL:
    def __init__(self, db_name='metadata.pkl', tables_dir='tables'):
        self.db_name = db_name
        self.tables_dir = tables_dir
        os.makedirs(self.tables_dir, exist_ok=True)
        self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.db_name):
            with open(self.db_name, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(self.db_name, 'wb') as f:
            pickle.dump(self.metadata, f)

    def insert(self, table, values):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."
        
        columns = self.metadata[table]
        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        
        if len(values) != len(columns) - 1:
            return "Error: Número de valores incorrecto."
        
        last_code = 0
        if os.path.exists(table_path):
            with open(table_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip().split("|")
                    last_code = int(last_line[0])
        
        new_code = str(last_code + 1)
        values.insert(0, new_code)
        
        with open(table_path, 'a', encoding='utf-8') as f:
            f.write("|".join(values) + '\n')
        
        return f"Inserción exitosa. Código asignado: {new_code}"

    def update(self, table, codigo, column, new_value):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."
        
        columns = self.metadata[table]
        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        
        if column not in columns:
            return "Error: La columna no existe."
        
        col_index = columns.index(column)
        codigo_index = 0  
        updated = False
        
        if not os.path.exists(table_path):
            return "Error: No hay datos en la tabla."
        
        with open(table_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(table_path, 'w', encoding='utf-8') as f:
            for line in lines:
                values = line.strip().split("|")
                if values[codigo_index] == codigo:
                    values[col_index] = new_value
                    updated = True
                f.write("|".join(values) + '\n')
        
        return "Actualización exitosa." if updated else "Error: Código no encontrado."

    def delete(self, table, column, value):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."
        
        columns = self.metadata[table]
        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        
        if column not in columns:
            return "Error: La columna no existe."
        
        col_index = columns.index(column)
        deleted = False
        
        if not os.path.exists(table_path):
            return "Error: No hay datos en la tabla."
        
        with open(table_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(table_path, 'w', encoding='utf-8') as f:
            for line in lines:
                values = line.strip().split("|")
                if values[col_index] == value:
                    deleted = True
                else:
                    f.write(line)
        
        return "Eliminación exitosa." if deleted else "Error: Valor no encontrado."
