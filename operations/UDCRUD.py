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

        return f"Registro insertado con código {new_code}"

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
            return f"Error: Registro con código {code} no encontrado."
        with open(table_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return f"Registro con código {code} actualizado."

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
            return f"Error: Registro con código {code} no encontrado."
        with open(table_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return f"Registro con código {code} eliminado."


    def select(self, table, where_clause=None):
        if table not in self.metadata:
            return f"Error: La tabla '{table}' no existe."

        table_path = os.path.join(self.tables_dir, f"{table}.udsql")
        if not os.path.exists(table_path):
            return f"Error: La tabla '{table}' no existe en el sistema de archivos."

        with open(table_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        columns = self.metadata[table]
        header = lines[0].strip().split("|")
        results = []

        for line in lines[1:]:
            row = line.strip().split("|")
            if len(row) != len(header):  # Handle potential inconsistencies
                continue

            data = dict(zip(header, row))  # Create a dictionary for easy access

            if where_clause is None:  # Select all if no where clause
                results.append(data)
                continue

            try:
                if eval(where_clause, {}, data):
                    results.append(data)
            except (NameError, SyntaxError, TypeError):
                return "Error: Invalid where clause."

        for line in lines[1:]:
            row = line.strip().split("|")
            if len(row) != len(header):
                continue

            data = dict(zip(header, row))

            if where_clause is None:
                results.append(data)
                continue

            try:
                # Utilizamos ast.literal_eval para evaluar expresiones de forma segura
                # y soportar operadores lógicos AND, OR y NOT.
                # Ejemplo: "data['Estado'] == 'Activo' and data['Código'] > 10"
                if ast.literal_eval(where_clause, {}, data):
                    results.append(data)
            except (NameError, SyntaxError, TypeError, ValueError):
                return "Error: Invalid where clause."

        return results
