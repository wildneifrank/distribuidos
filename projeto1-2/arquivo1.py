import threading
import arquivo2  # Importe o módulo que contém as funções

# Variável global compartilhada
minha_variavel_global = 0

# Objeto de trava para sincronização
lock = threading.Lock()

def minha_funcao():
    global minha_variavel_global

    resultado1 = arquivo2.funcao1()  # Chame a função do arquivo1.py
    resultado2 = arquivo2.funcao2()  # Chame outra função do arquivo1.py

    print(resultado1)
    print(resultado2)
    print(minha_variavel_global)

if __name__ == "__main__":
    minha_funcao()  # Chame a função em arquivo2.py quando o arquivo é executado diretamente
