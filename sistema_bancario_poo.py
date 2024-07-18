
from abc import ABC,abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self,endereco):
     self.endereco = endereco
     self.contas = []
     
  
    def realizar_transacao(self,conta,transacao):#registrando transacao na classe transacao
     transacao.registrar(conta)
  
    def adicionar_conta(self,conta):#fez o append da conta na lista vazia contas
     self.contas.append(conta)
    
  
class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereco):#definir o nome,cpf,e nascimento normal
     super().__init__(endereco) #receber o endereco da classe cliente
     self.nome = nome
     self.data_nascimento = data_nascimento
     self.cpf = cpf
    

class Conta:
    def __init__(self,numero,cliente):
     self._saldo = 0
     self._numero = numero
     self._agencia = "0001"
     self._cliente = cliente
     self._historico = Historico() #chamar a classe histórico como variável
     

    @classmethod
    def nova_conta(cls,cliente,numero):
     return cls(numero,cliente)
    
    @property
    def saldo(self):#usando o property para retornar os valores privados
      return self._saldo
  
    @property
    def numero(self):
      return self._numero
  
    @property
    def agencia(self):
      return self._agencia
    
    @property
    def cliente(self):
      return self._cliente
  
    @property #histórico vira atributo de conta para ser salva a transação depois
    def historico(self):
      return self._historico


    def sacar(self,valor):
        saldo = self.saldo
        saque_excedido = valor > saldo

        if saque_excedido:
            print("Saldo insuficiente")
  
        elif valor > 0:
            self._saldo -= valor
            print("Saque bem sucedido!")
            return True
        else:
         print("Valor inválido")

        return False
    
    
  
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito bem sucedido!")
        else:
            print("Valor inválido")
            return False
      
        return True
    

class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite = 500,limite_saques = 3):#os dois limites sendo passados por keyword
     super().__init__(numero,cliente)
     self._limite = limite
     self._limite_saques = limite_saques

    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__])#buscando no histórico a quantidade de saques

        limite_por_saque = valor > self._limite
        saques_excedidos = numero_saques >= self._limite_saques

        if limite_por_saque:
         print("Limite de saque excedido!")

        elif saques_excedidos:
         print("Quantidade de saques excedida!")
        else:
         return super().sacar(valor)
    
        return False
   
    def __str__(self):
          return f"""\
              Agência:\t{self.agencia}
              C/C:\t\t{self.numero + 1}
              Titular:\t{self.cliente.nome}
          """

class Historico:
    def __init__(self):
       self._transacoes = [] #transacao vira uma lista dentro do construtor init

    @property #retorno das transações privadas com transacoes sendo um atributo de historico
    def transacoes(self):
       return self._transacoes 


    def adicionar_transacao(self,transacao):
       self.transacoes.append({ #armazenar a transacao usando um dicionário
          "tipo" : transacao.__class__.__name__,
          "valor" : transacao.valor, #valor de transacao é o self da classe ou saque e deposito
          "data" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
       })

class Transacao(ABC): #abc de método abstrato e sendo uma interface
    @property
    @abstractmethod
    def valor(self):
      pass
    
    @classmethod #método de classe abstrata para as classes saque e deposito
    @abstractmethod
    def registrar(self,conta):
      pass
  

class Saque(Transacao):
    def __init__(self,valor):
      self._valor = valor

    @property #valor será um atributo de saque
    def valor(self):
      return self._valor
    

    def registrar(self,conta): #registrar saque na conta e no historico
        transacao_efetuada = conta.sacar(self.valor)
        if transacao_efetuada:
          conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
     self._valor = valor

    @property #valor será um atributo de deposito
    def valor(self):
      return self._valor
    
    def registrar(self,conta): #registrar deposito na conta e no historico
        transacao_efetuada = conta.depositar(self.valor)

        if transacao_efetuada:
          conta.historico.adicionar_transacao(self)
  
def log_transacao(func): #usar esse decorador para mostrar a hora em que a função foi usada
    def envelope(*args, **kwargs):#args e kwargs para funções com mais de um parâmetro
        resultado = func(*args, **kwargs)#usando o args e kwargs caso venha mais de um parâmetro
        print(f"{datetime.now()}: {func.__name__.upper()}")#salvar hora atual e nome da função
        return resultado #salvar o resultado


    return envelope #e retornar a função interna 


def filtrar_clientes(cpf,clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]#buscar na lista de clientes algum cpf igual ao do digitado
  return clientes_filtrados[0] if clientes_filtrados else None
  
def recuperar_conta(cliente):
  if not cliente.contas: #caso o cliente não tenha conta registrada
    print("Cliente não possui conta!")
    return #não permite cliente escolher conta
  
  return cliente.contas[0] #retornar primeira conta do cliente caso ele tenha conta

@log_transacao #usar o @ para chamar o decorador e usando como parâmetro a função de baixo
def depositar(clientes):
    deposito_texto = " MENU DEPOSITO "
    print(deposito_texto.center(38,"#"))
    cpf = input("Informe o cpf do cliente: ")#filtrar o cliente para depósito
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
      print("Cliente não encontrado!")
      return
    
    valor = float(input("Informe o valor do depósito:"))
    transacao = Deposito(valor) #chamar a classe Deposito com o valor digitado

    conta = recuperar_conta(cliente) 
    if not conta:
      return
    
    cliente.realizar_transacao(conta,transacao)#realizar a transacao na classe cliente

@log_transacao
def sacar(clientes):
    saque_texto = " MENU SAQUE "
    print(saque_texto.center(38,"#"))
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
      print("Cliente não encontrado!")
      return
    
    valor = float(input("Informe o valor do saque:"))
    transacao = Saque(valor) #chamar a classe saque com o valor digitado

    conta = recuperar_conta(cliente)
    if not conta:
      return
    
    cliente.realizar_transacao(conta,transacao)

@log_transacao
def mostrar_extrato(clientes):
    extrato_texto = " EXTRATO "
    print(extrato_texto.center(38,"#"))
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
     print("Cliente não encontrado!")
     return

    conta = recuperar_conta(cliente)#verificar se cliente tem conta
    if not conta:
     return
    
    transacoes = conta.historico.transacoes #buscando as transações no histórico 

    extrato = ""
    if not transacoes: #caso não tenha transações salvas
      extrato = ("Não foram realizadas transações")
    else:
      for transacao in transacoes:
        extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"#armazenar tudo no extrato

      print(extrato)
      print(f"\nSaldo:\n\tR${conta.saldo:.2f}")
      print("#"*38)


@log_transacao
def criar_cliente(clientes):
  cliente_texto = " CRIAR CLIENTE "
  print(cliente_texto.center(38,"#"))
  cpf = input("Informe o CPF (somente números): ")
  cliente = filtrar_clientes(cpf,clientes)

  if cliente:
     print("Já existe um cliente com este CPF!")
     return
  
  nome = input("Informe o nome do usuário: ")
  data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
  
  cliente = PessoaFisica(nome=nome,cpf=cpf,data_nascimento=data_nascimento,endereco=endereco)#registrar na pessoa fisica com argumentos por keyword
  clientes.append(cliente)

  print("Cliente registrado com sucesso!")

@log_transacao
def criar_conta(numero_conta,clientes,contas):
  conta_texto = " CRIAR CONTA "
  print(conta_texto.center(38,"#"))
  cpf = input("Informe o CPF do usuário: ")
  cliente = filtrar_clientes(cpf,clientes)

  if not cliente:
     print("Cliente não encontrado!")
     return
  
  conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)#registrar na conta corrente com argumentos por keyword
  contas.append(conta) # append das contas para lista de contas e das contas do cliente
  cliente.contas.append(conta)

  print("Conta criada com sucesso!")


def listar_contas(contas):
  for conta in contas:
    print("*" * 38)
    print(textwrap.dedent(str(conta))) #usar o dedent para apagar qualquer espaço em branco inicial da lista de contas


menu = """
################ MENU ################
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[4]\tCriar usuário
[5]\tCriar conta corrente
[6]\tListar contas
[7]\tSair
=>"""


def main():

    clientes = [] #criando lista de clientes e de contas por cliente
    contas = []
    while True:
        opcao = input(menu)

        if opcao == "1":#depósito não está indo para o extrato
         depositar(clientes)

        elif opcao == "2" :#saque está sendo armazenado no extrato normal,e o numero de saques    também
         sacar(clientes)

        elif opcao == "3":# deu certo
         mostrar_extrato(clientes)

        elif opcao == "4": #está funcionando
          criar_cliente(clientes)

        elif opcao == "5":#está funcionando
          numero_conta = len(contas)
          criar_conta(numero_conta,clientes,contas)

        elif opcao == "6":
          listar_contas(contas)

        elif opcao == "7":
          break

        else:
         print("Operação inválida, por favor selecione novamente a operação desejada.")
main()

