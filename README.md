# Database_Foundations_Workshop-3

## Arquitectura Interna
El proyecto está diseñado por archivos (módulos separados) en lugar de una estructura completamente orientada a clases. Cada archivo tiene una responsabilidad específica, siguiendo un enfoque modular donde cada parte del sistema maneja una función particular.

• create_table.py - Creación de Tablas

Genera archivos .udsql en la carpeta tables/.

Define los nombres de las columnas de cada tabla.

• metadata_manager.py - Manejo de Metadata

Guarda la estructura de las tablas en metadata.pkl usando pickle.

• UDCRUD.py - Implementación de CRUD con la Clase UDSQL

La clase UDSQL encapsula las operaciones sobre los archivos .udsql en tables/.
