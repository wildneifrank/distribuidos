# arquivo1.py

import arquivo1  # Importe o arquivo2.py para acessar sua variável global

def funcao1():
    return "Função 1 em arquivo1.py"

def funcao2():

    # Use a trava para proteger o acesso à variável global em arquivo2.py
    with arquivo1.lock:
        arquivo1.minha_variavel_global += 1

    return "Função 2 em arquivo1.py modificou a variável global"
