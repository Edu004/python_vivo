
from abc import ABC,abstractclassmethod,abstractproperty
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
  def __init__(self,nome,cpf,data_nascimento,endereco):#definir o nome,cpf,e nascimento normal
    super().__init__(endereco) #receber o endereco da classe cliente
    self.nome = nome
    self.cpf = cpf
    self.data_nascimento = data_nascimento
    

class Conta:
  def __init__(self,numero,cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
     

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

  @property
  def historico(self):
    return self._historico


  def sacar(self,valor):
    saldo = self.saldo
    saque_excedido = valor > saldo

    if saque_excedido:
      print("Saldo insuficiente")


    elif valor > 0:
      saldo -= valor
      print("Saque bem sucedido!")
      return True
    else:
      print("Valor inválido")
      return False
    
    
  
  def depositar(self,valor):
    saldo = self.saldo
    if valor > 0:
      saldo += valor
      print("Depósito bem sucedido!")
      return True
    else:
      print("Valor inválido")
      return False
    

class ContaCorrente(Conta):
  def __init__(self,numero,cliente,limite = 500,limite_saques = 3):
    super().__init__(numero,cliente)
    self._limite = limite
    self._limite_saques = limite_saques

  def sacar(self,valor):
    numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

    limite_excedido = valor > self._limite
    saque_excedido = numero_saques >= self._limite

    if limite_excedido:
      print("Limite de saque excedido!")
    
    elif saque_excedido:
      print("Quantidade de saques excedida!")
    else:
      return super().sacar(valor)

    return False
  
  def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
  def __init__(self):
    self._transacoes = [] #transacao vira uma lista dentro do construtor init

  @property
  def transacoes(self):
    return self._transacoes


  def adicionar_transacao(self,transacao):
    self.transacoes.append({ #armazenar a transacao no dicionário
        "tipo" : transacao.__class__.__name__,
        "valor" : transacao.valor,
        "data" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    

  
class Transacao(ABC):

  @property
  @abstractclassmethod
  def valor(self):
    pass
  
  @abstractclassmethod
  def registrar(self,conta):
    pass
  

class Saque(Transacao):

  def __init__(self,valor):
    self._valor = valor

  @property #valor será um atributo de saque
  def valor(self):
    return self._valor
  
  #@valor.setter
  #def valor(self,saldo):
   # self.valor -= saldo

  def registrar(self,conta,valor):
    transacao_efetuada = conta.sacar(valor)
    if transacao_efetuada:
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self,valor):
    self._valor = valor

  @property #valor será um atributo de deposito
  def valor(self):
    return self._valor
  
  #@valor.setter
  #def valor(self,saldo):
   # self.valor += saldo

  def registrar(self,conta,valor):
    transacao_efetuada = conta.depositar(valor)
    if transacao_efetuada:
      conta.historico.adicionar_transacao(self)
  


def filtrar_clientes(cpf,clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None
  
def recuperar_conta(cliente):
  if not cliente.contas:
    print("Cliente não possui conta!")
    return #não permite cliente escolher conta
  
  return cliente.contas[0]

def depositar(clientes):
  cpf = input("Informe o cpf do cliente: ")
  cliente = filtrar_clientes(cpf,clientes)

  if not cliente:
    print("Cliente não encontrado!")
    return
  
  valor = float(input("Informe o valor do depósito:"))
  transacao = Deposito(valor)

  conta = recuperar_conta(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta,transacao)


def sacar(clientes):
  cpf = input("Informe o cpf do cliente: ")
  cliente = filtrar_clientes(cpf,clientes)

  if not cliente:
    print("Cliente não encontrado!")
    return
  
  valor = float(input("Informe o valor do saque:"))
  transacao = Saque(valor)

  conta = recuperar_conta(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta,transacao)


def mostrar_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
     print("Cliente não encontrado!")
     return

    conta = recuperar_conta(cliente)
    if not conta:
     return
    
    extrato_texto = "Extrato"
    print(extrato_texto.center(22,"#"))
    transacoes = conta.historico.transacoes #buscando as transações no histórico 

    extrato = ""
    if not transacoes:
      extrato = ("Não foram realizadas transações")
    else:
      for transacao in transacoes:
        extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

      print(extrato)
      print(f"\nSaldo:\n\tR${conta.saldo:.2f}")
      print("########################")



def criar_usuario(clientes):
  cpf = input("Informe o CPF (somente números): ")
  cliente = filtrar_clientes(cpf,clientes)

  if cliente:
     print("Cliente com cpf repetido!")
     return
  
  nome = input("Informe o nome do usuário: ")
  data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
  
  cliente = PessoaFisica(nome=nome,cpf=cpf,data_nascimento=data_nascimento,endereco=endereco)
  clientes.append(cliente)

  print("Cliente registrado com sucesso!")


def criar_conta(numero_conta,clientes,contas):
  print("Criar conta")
  cpf = input("Informe o CPF do usuário: ")
  cliente = filtrar_clientes(cpf,clientes)

  if not cliente:
     print("Cliente não encontrado!")
     return
  
  conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
  contas.append(conta) # append das contas para lista de contas do cliente 
  cliente.contas.append(conta)

  print("Conta criada com sucesso!")


def listar_contas(contas):
  for conta in contas:
    print("*" * 100)
    print(textwrap.dedent(str(conta)))




menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar usuário
[5] Criar conta corrente
[6] Listar contas
[7] Sair
"""

def main():

    clientes = []
    contas = []
    while True:
      opcao = input(menu)

      if opcao == "1":#depósito não está indo para o extrato
       depositar(clientes)


      elif opcao == "2" :#saque está sendo armazenado no extrato normal,e o numero de saques também
       sacar(clientes)

      elif opcao == "3":# deu certo
       mostrar_extrato(clientes)

      elif opcao == "4": #está funcionando
        criar_usuario(clientes)

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

  

