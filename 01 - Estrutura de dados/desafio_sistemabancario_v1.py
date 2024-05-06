depositos = []
saques = []
saldo = 0
total_saques_dia = 0
limite_diario = 1500
total_saques_realizados = 0

def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        depositos.append(valor)
        print(f'Depósito de R$ {valor:.2f} realizado com sucesso.')
        print(f'Saldo atual: R$ {saldo:.2f}')
    else:
        print('Erro: O valor do depósito deve ser positivo.')

def sacar(valor):
    global saldo, total_saques_dia, limite_diario, total_saques_realizados
    if total_saques_realizados < 3:
        if saldo >= valor:
            if valor <= 500 and total_saques_dia + valor <= limite_diario:
                saldo -= valor
                saques.append(valor)
                total_saques_dia += valor
                total_saques_realizados += 1
                print(f'Saque de R$ {valor:.2f} realizado com sucesso.')
                print(f'Saldo atual: R$ {saldo:.2f}')
            elif valor > 500:
                print('Erro: O valor do saque excede o limite de R$ 500,00 por saque.')
            elif total_saques_dia + valor > limite_diario:
                print('Erro: O limite diário de saque de R$ 1500,00 foi atingido.')
        else:
            print('Erro: Saldo insuficiente para realizar o saque.')
    else:
        print('Erro: Limite máximo de saques diários atingido.')

def extrato():
    print('\nExtrato detalhado:')
    print('Depósitos:')
    for i, deposito in enumerate(depositos, start=1):
        print(f'{i}. R$ {deposito:.2f}')
    print('Saques:')
    for i, saque in enumerate(saques, start=1):
        print(f'{i}. R$ {saque:.2f}')
    print(f'\nSaldo atual: R$ {saldo:.2f}')
    print(f'Total de depósitos diário: R$ {sum(depositos):.2f}')
    print(f'Total de saques diário: R$ {sum(saques):.2f}')

# Menu de operações
while True:
    print("\n======= Menu =======")
    print("1. Sacar")
    print("2. Depositar")
    print("3. Extrato")
    print("4. Sair")
    escolha = input("Escolha a operação desejada (1/2/3/4): ")

    if escolha == '1':
        valor = float(input("Digite o valor a ser sacado: "))
        sacar(valor)
    elif escolha == '2':
        valor = float(input("Digite o valor a ser depositado: "))
        depositar(valor)
    elif escolha == '3':
        extrato()
    elif escolha == '4':
        print("Saindo...")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
