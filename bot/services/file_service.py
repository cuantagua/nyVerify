from telegram import Update
from telegram.ext import ContextTypes
import os

class FileService:
    def __init__(self, storage_directory='uploads'):
        self.storage_directory = storage_directory
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    async def guardar_archivo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # 📂 Verifica si hay un archivo en el mensaje
        archivo = update.message.document
        if archivo:
            # 💾 Guarda el archivo en el directorio especificado
            ruta_archivo = os.path.join(self.storage_directory, archivo.file_name)
            await archivo.get_file().download(ruta_archivo)
            return ruta_archivo
        # ❌ No se encontró archivo
        return None

    def listar_archivos(self):
        # 📋 Lista todos los archivos en el directorio
        return os.listdir(self.storage_directory)

    def eliminar_archivo(self, nombre_archivo):
        # 🗑️ Elimina un archivo si existe
        ruta_archivo = os.path.join(self.storage_directory, nombre_archivo)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
            return True
        # ❌ El archivo no existe
        return False

    def obtener_ruta_archivo(self, nombre_archivo):
        # 🔍 Obtiene la ruta completa del archivo si existe
        return os.path.join(self.storage_directory, nombre_archivo) if nombre_archivo in self.listar_archivos() else None