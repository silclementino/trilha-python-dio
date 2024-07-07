# Funções de operações bancárias

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    return saldo, extrato

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def extrato_bancario(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=========================================")

# Funções para gerenciamento de usuários e contas

usuarios = []
contas = []
numero_conta = 1

def validar_cpf(cpf):
    if len(cpf) != 11:
        print("O CPF no Brasil contém 11 dígitos! Verifique o número do documento antes de tentar novamente.")
        return False
    return True

def criar_usuario(nome, data_nascimento, cpf, endereco):
    if not validar_cpf(cpf):
        return
    global usuarios
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("Usuário já cadastrado.")
            return
    novo_usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")

def criar_conta(cpf_usuario):
    if not validar_cpf(cpf_usuario):
        return
    global contas, numero_conta
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf_usuario:
            usuario_encontrado = usuario
            break
    if usuario_encontrado:
        nova_conta = {
            'agencia': '0001',
            'numero_conta': numero_conta,
            'usuario': usuario_encontrado
        }
        contas.append(nova_conta)
        numero_conta += 1
        print("Conta criada com sucesso!")
        print("\n==== Detalhes da Conta Corrente ====")
        print(f"Agência: {nova_conta['agencia']}")
        print(f"Número da conta: {nova_conta['numero_conta']}")
        print(f"Nome do usuário: {nova_conta['usuario']['nome']}")
        print("====================================")
    else:
        print("O CPF informado não está vinculado a um usuário. Por favor, crie primeiro o Usuário e em seguida Crie a Conta Corrente.")

def listar_conta(cpf_usuario):
    if not validar_cpf(cpf_usuario):
        return
    conta_encontrada = False
    for conta in contas:
        if conta['usuario']['cpf'] == cpf_usuario:
            print("\n========== Detalhes da Conta Corrente ==========")
            print(f"Agência: {conta['agencia']}")
            print(f"Número da conta: {conta['numero_conta']}")
            print(f"Nome do usuário: {conta['usuario']['nome']}")
            print("==================================================")
            conta_encontrada = True
            break
    if not conta_encontrada:
        print("O CPF informado não está vinculado a um usuário. Por favor, crie primeiro o Usuário e em seguida Crie a Conta Corrente.")

# Menu principal

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[cu] Criar Usuário
[cc] Criar Conta Corrente
[lc] Listar Conta Corrente
[q] Sair

=> """

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

    elif opcao == "e":
        extrato_bancario(saldo, extrato=extrato)

    elif opcao == "cu":
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento (dd/mm/yyyy): ")
        cpf = input("CPF (somente números): ")
        endereco = input("Endereço (logradouro, número - bairro - cidade / sigla estado): ")
        criar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao == "cc":
        cpf_usuario = input("Informe o CPF do usuário (somente números): ")
        criar_conta(cpf_usuario)

    elif opcao == "lc":
        cpf_usuario = input("Informe o CPF do usuário (somente números): ")
        listar_conta(cpf_usuario)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
