##################################################
# Archivo: AES
# Lenguaje: Python v.3.10.0
# Autores: García Villegas Daniel y
# Narváez Marqueda Ricardo André Sebastián
# Fecha de creación/modificación: 21/11/21
#Descripción: Encripta un archivo de cualquier tipo de extensión
#generando incicialmente un hash para comparar después del descifrado
#asegurándose así de la integridad del archivo post-cifrado
##################################################

######################################################################
#
# REQUISITOS
#
######################################################################
import sys
import os
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from cryptography.fernet import Fernet



def main():
    if len(sys.argv)<3 or len(sys.argv)>6:
        help()#En caso de que el número de argumentos sea incorrecto, desplegamos las instrucciones al usuario
    else:
        opcion=sys.argv[2]
        if opcion=='-c' and len(sys.argv)==3: #En caso de que se desee cifrar
            cifrado(sys.argv[1])
        else:
            if opcion=='-d' and len(sys.argv)==5: #En caso de que se desee descifrar
                descifrado(sys.argv[1],sys.argv[3],sys.argv[4])
            else:
                help()
                return
            
                

###################################################################
#Función para darle las instrucciones al usuario
#En caso de que ingrese incorrectamente el switch de ruta 
#respectivo
##################################################################
def help(): 
    print("""PARAMETROS INCORRECTOS.
########INSTRUCCIONES#################
Si desea CIFRAR el archivo:    
    >Python AES.py Nombre_De_Su_Archivo.Extension -c 
Si desea DESCIFRAR el archivo:
    >Python AES.py Nombre_De_Su_Archivo.Extension -d Nombre_Del_Archivo_Hash.hash -key
          """)
    return



###################################################################
#
#Proceso principal de cifrado
#
##################################################################

    
def cifrado(ruta):
    if os.path.isfile(ruta)==True:
        print("Obteniendo HASH del archivo",ruta)
        hash_archivo=hash_file(ruta)
        print("Almacenando hash del archivo \n ",hash_archivo)
        h=open(ruta+".hash","w+")
        h.write(hash_archivo)
        write_key()
        key=load_key()
        print("CIFRANDO EL ARCHIVO")
        encrypt(ruta,key)
        print("CIFRADO EXITOSO")
        
    else:
        print("No se ha encontrado el archivo")
            
    return


###################################################################
#
#Proceso principal de descifrado
#
##################################################################
def descifrado(archivo_cifrado,ruta_hash,key):
    
    print("descifrando")
    if os.path.isfile(archivo_cifrado)==True and os.path.isfile(ruta_hash)==True and os.path.isfile(key):
        print("archivos encontrados")
        key=load_key(key)
        decrypt(archivo_cifrado,key)
        print("Archivo descifrado, verificando HASHSUM")
        hash_archivo=hash_file(archivo_cifrado)
        with open(ruta_hash,'r') as file:
            hash_descifrado=file.read()
        print("HASH ARCHIVO: ",hash_archivo," HASH DESCIFRADO", hash_descifrado)
        if (hash_archivo==hash_descifrado):
            print("HASH CORROBORADO")
    else:
        print("Archivos no encontrados, verifique su ruta")
    
    return


###################################################################
#
#Obtención de hash 
#
##################################################################
def hash_file(ruta):
    h=hashlib.sha1()#declaramos el objeto hash
    with open(ruta,'rb') as file: #Abrimos el archivo en modo binario
        chunk=0
        while chunk !=b'': #Leemos hasta llegar al final del archivo
            chunk=file.read(1024) #Leemos de 1024 en 1024 bits por segmento para realizar el hash
            h.update(chunk) #Obtenemos el hashsum hasta ahora
    return h.hexdigest()


###################################################################
#
#Creación de llave durante el cifrado
#
##################################################################
def write_key():

    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

###################################################################
#
#Carga de llave 
#
##################################################################

def load_key(ruta_key="key.key"):
    return open(ruta_key, "rb").read()


###################################################################
#
#Cifrado del archivo
#
##################################################################
def encrypt(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

###################################################################
#
#Descifrado del archivo
#
##################################################################

def decrypt(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

    
    
main()

