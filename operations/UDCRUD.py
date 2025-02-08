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
        if len(values) != len(columns) - 1:
            return "Error: Número de valores incorrecto."

        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        last_code = 0

        if os.path.exists(table_path):
            with open(table_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Recorremos todas las líneas para obtener el último código válido
            for line in lines:
                parts = line.strip().split("|")
                if not parts:
                    continue
                if parts[0] == "Código":
                    continue
                try:
                    code = int(parts[0])
                    last_code = code
                except ValueError:
                    continue

        new_code = last_code + 1

        # Si el archivo no existe o está vacío, se crea y se escribe la cabecera
        if not os.path.exists(table_path) or os.path.getsize(table_path) == 0:
            with open(table_path, "w", encoding="utf-8") as f:
                f.write("|".join(columns) + "\n")
                f.write("|".join([str(new_code)] + values) + "\n")
        else:
            with open(table_path, "a", encoding="utf-8") as f:
                f.write("|".join([str(new_code)] + values) + "\n")

        return f"Registro insertado con ID {new_code}"

    def update(self, table, code, new_values):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."
        columns = self.metadata[table]
        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        if not os.path.exists(table_path):
            return f"Error: La tabla '{table}' no existe en el sistema de archivos."

        with open(table_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        header = lines[0]
        updated = False
        new_lines = [header]

        for line in lines[1:]:
            parts = line.strip().split("|")
            try:
                current_code = int(parts[0])
            except ValueError:
                new_lines.append(line)
                continue
            if current_code == code:
                new_lines.append("|".join([str(code)] + new_values) + "\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            return f"Error: Registro con ID {code} no encontrado."
        with open(table_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return f"Registro con ID {code} actualizado."

    def delete(self, table, code):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."
        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        if not os.path.exists(table_path):
            return f"Error: La tabla '{table}' no existe en el sistema de archivos."

        with open(table_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        header = lines[0]
        deleted = False
        new_lines = [header]

        for line in lines[1:]:
            parts = line.strip().split("|")
            try:
                current_code = int(parts[0])
            except ValueError:
                new_lines.append(line)
                continue
            if current_code == code:
                deleted = True
                continue  # Omite la línea
            new_lines.append(line)

        if not deleted:
            return f"Error: Registro con ID {code} no encontrado."
        with open(table_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return f"Registro con ID {code} eliminado."


    def select(self, table, where_clause=None):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."

        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        if not os.path.exists(table_path):
            return f"Error: La tabla '{table}' no existe en el sistema de archivos."

        with open(table_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            return []

        header = lines[0].strip().split("|")
        results = []

        # Función segura para evaluar condiciones
        def evaluate_condition(row, where_clause):
            safe_globals = {
                "__builtins__": None
            }
            safe_locals = {col: row[col] for col in header}

            try:
                return eval(where_clause, safe_globals, safe_locals)
            except Exception:
                return False

        for line in lines[1:]:
            row = line.strip().split("|")
            if len(row) != len(header):
                continue

            data = dict(zip(header, row))

            # Convertir valores numéricos para comparación correcta
            for key in data:
                if data[key].isdigit():
                    data[key] = int(data[key])

            if where_clause is None or evaluate_condition(data, where_clause):
                results.append(data)

        return results
