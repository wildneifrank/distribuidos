#import ArCondicionado_pb2

class ArCondicionadoController:
    def __init__(self):
        #self.ar_condicionado = ArCondicionado_pb2.ArCondicionado()
        self.ar_condicionado = {
            "ligado": False, 
            "temperatura": 20 
        }

    def ligar(self):
        self.ar_condicionado["ligado"] = True

    def desligar(self):
        self.ar_condicionado["ligado"] = False

    def aumentar_temperatura(self):
        if self.ar_condicionado["ligado"] and self.ar_condicionado["temperatura"] < 27:
            self.ar_condicionado["temperatura"] += 1
        elif self.ar_condicionado["temperatura"] >= 27:
            print("\nMáximo atingido.")
        else:
            print("\nDesligado\n")

    def diminuir_temperatura(self):
        if self.ar_condicionado["ligado"] and self.ar_condicionado["temperatura"] > 16:
            self.ar_condicionado["temperatura"] -= 1
        elif self.ar_condicionado["temperatura"] <= 16:
            print("\nMínimo atingido.")
        else:
            print("O ar condicionado está desligado. Não é possível diminuir a temperatura.")

    def mostrar_estado(self):
        if self.ar_condicionado["ligado"]:
            estado = "ligado"
            print(f"\nTemperatura: {self.ar_condicionado['temperatura']} graus Celsius\n")
        else:
            print("\nDesligado\n")    


controller = ArCondicionadoController()

while True:
    comando = input("Digite: \n'ligar' para ligar \n 'desligar' para desligar \n '+' para aumentar a temperatura \n '-' para diminuir a temperatura \n 'sair' para sair: \n ")

    if comando == "ligar":
        controller.ligar()
    elif comando == "desligar":
        controller.desligar()
    elif comando == "+":
        controller.aumentar_temperatura()
    elif comando == "-":
        controller.diminuir_temperatura()
    elif comando == "sair":
        break
    else:
        print("Não foi possível realizar a ação")
        continue

    controller.mostrar_estado()
