

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
  opcao = input(menu)

  if opcao == "1":
    print("Depósito")
    valor = float(input("Valor do depósito: "))
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"

  elif opcao == "2":
    print("Saque")
    saque = float(input("Valor do saque: "))

    limite_saldo = saque > saldo
    limite_por_saque = saque > limite
    qtd_saques = numero_saques >= LIMITE_SAQUES

    if limite_saldo or limite_por_saque or qtd_saques:
      print("Erro na operação")
    else:
      valor -= saque
      extrato += f"Saque: R$ {saque:.2f}\n"
      numero_saques += 1


  elif opcao == "3":
    print("\n================ EXTRATO ================")
    print(extrato)
    print(f"Saldo: R$ {valor:.2f}")
    print("===========================================")



  elif opcao == "4":
    break

  else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")
