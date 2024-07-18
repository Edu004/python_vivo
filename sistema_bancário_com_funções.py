

def deposito(saldo,valor,extrato):
  if valor > 0:
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print("Depósito bem sucedido!")

  else:
    print("Erro na operação")
  return saldo, extrato


def saque(*,saldo,valor_saque,extrato,limite,numero_saques,LIMITE_SAQUES):

    limite_saldo = valor_saque > saldo
    limite_por_saque = valor_saque > limite
    qtd_saques = numero_saques >= LIMITE_SAQUES

    if limite_saldo:
      print("Saldo insuficiente")# deu certo

    elif limite_por_saque:
      print("Limite por saque excedido")#deu certo

    elif qtd_saques:
      print("Limite de saques excedido")#deu certo

    elif valor_saque > 0:
      saldo -= valor_saque
      extrato += f"Saque: R$ {valor_saque:.2f}\n"
      numero_saques += 1
      print("Saque bem sucedido!")

    return saldo,extrato,numero_saques




def mostrar_extrato(saldo,extrato):
    print("\n================ EXTRATO ================")
    extrato += f"Saldo: R$ {saldo}\n"
    print(extrato)
    print("===========================================")


def criar_usuario(usuarios):
  nome = input("Informe o nome do usuário: ")
  data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
  cpf = input("Informe o CPF (somente números): ")
  for usuario in usuarios:
    if usuario.get('CPF') == cpf:
      print("CPF já cadastrado")
      return
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")



  dados_usuario = {'Nome' : nome,
                    'Data de nascimento': data_nascimento,
                    'CPF': cpf,
                    'Endereço': endereco}
  usuarios.append(dados_usuario.copy())


def criar_conta(contas,usuarios,AGENCIA):
  print("Criar conta")
  cpf = input("Informe o CPF do usuário: ")
  usuario = None
  id_usuario = 0
  for user in usuarios:
    if user['CPF'] == cpf:
      id_usuario  += 1
      usuario = user

      dados_conta = {'Agência' : AGENCIA,
                    'Id': id_usuario,
                    'Usuário': usuario,}
      contas.append(dados_conta.copy())
      print("Conta criada com sucesso!")
      return contas
  else:
    print("Usuário não encontrado,não é possível criar a conta")
    return

def listar_contas(contas):
  print('------------------------------------------------------')
  print("Listar contas")

  for conta in contas:

    contas_info = {
      'Agência': conta['Agência'],
      'Id': conta['Id'],
      'Titular': conta['Usuário']['Nome']}

    for chave,valor in contas_info.items():
      print('{}: {}'.format(chave,valor))
  print('------------------------------------------------------')



menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar usuário
[5] Criar conta corrente
[6] Listar usuarios
[7] Listar contas
[8] Sair
"""

def main():

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    contas = []
    usuarios = []
    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ""
    while True:
      opcao = input(menu)

      if opcao == "1":#depósito não está indo para o extrato
       print("Depósito")
       valor = float(input("Valor do depósito: "))

       saldo,extrato = deposito(saldo,valor,extrato)


      elif opcao == "2" :#saque está sendo armazenado no extrato normal,e o numero de saques também
       print("Saque")
       valor_saque = float(input("Valor do saque: "))
       saldo, extrato,numero_saques = saque(saldo=saldo,valor_saque=valor_saque,extrato=extrato,limite=limite,numero_saques=numero_saques,LIMITE_SAQUES=LIMITE_SAQUES)


      elif opcao == "3":# deu certo
       mostrar_extrato(saldo,extrato)

      elif opcao == "4": #está funcionando
        criar_usuario(usuarios)

      elif opcao == "5":#está funcionando
        criar_conta(contas,usuarios,AGENCIA)

      elif opcao == "6": #está funcionando
        print('------------------------------------------------------')
        print("Listar usuarios")
        for usuario in usuarios:

          for chave,valor in usuario.items():
            print('{}: {}'.format(chave,valor))
        print('------------------------------------------------------')


      elif opcao == "7":
        listar_contas(contas)


      elif opcao == "8":
        break


      else:
       print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
