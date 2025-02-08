import os
from operations.UDCRUD import UDSQL

if __name__ == "__main__":
    db = UDSQL()

    while True:
        print("\nOptions:")
        print("1. Insert record")
        print("2. Update record")
        print("3. Delete record")
        print("4. Select records")
        print("5. Exit")

        option = input("Select an option: ")

        if option == "1":
            table = input("Enter the table name: ")
            if table not in db.metadata:
                print(f"Error: Table '{table}' does not exist.")
                continue
            fields = db.metadata[table]
            values = []
            for field in fields[1:]:  # Exclude the code
                value = input(f"Enter the value for {field}: ")
                values.append(value)
            result = db.insert(table, values)
            print(result)

        elif option == "2":
            table = input("Enter the table name: ")
            if table not in db.metadata:
                print(f"Error: Table '{table}' does not exist.")
                continue
            code = int(input("Enter the code of the record to update: "))
            fields = db.metadata[table][1:]  # Exclude the code
            new_values = []
            for field in fields:
                new_value = input(f"Enter the new value for {field}: ")
                new_values.append(new_value)
            result = db.update(table, code, new_values)
            print(result)

        elif option == "3":
            table = input("Enter the table name: ")
            if table not in db.metadata:
                print(f"Error: Table '{table}' does not exist.")
                continue
            code = int(input("Enter the code of the record to delete: "))
            result = db.delete(table, code)
            print(result)

        elif option == "4":
            table = input("Enter the table name: ")
            if table not in db.metadata:
                print(f"Error: Table '{table}' does not exist.")
                continue
            where_clause = input("Enter the WHERE clause (or press Enter to select all): ")
            if where_clause:
                results = db.select(table, where_clause)
            else:
                results = db.select(table)

            if isinstance(results, str):  # Check if there was an error
                print(results)
            else:
                if results:
                    for result in results:
                        print(result)
                else:
                    print("No records found.")

        elif option == "5":
            break

        else:
            print("Invalid option. Try again.")
