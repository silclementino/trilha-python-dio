from datetime import date
from typing import List

# Funções de operações bancárias

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        return saldo, extrato, numero_saques, "Operação falhou! Você não tem saldo suficiente."
    elif valor > limite:
        return saldo, extrato, numero_saques, "Operação falhou! O valor do saque excede o limite."
    elif numero_saques >= limite_saques:
        return saldo, extrato, numero_saques, "Operação falhou! Número máximo de saques excedido."
    elif valor <= 0:
        return saldo, extrato, numero_saques, "Operação falhou! O valor informado é inválido."
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return saldo, extrato, numero_saques, f"Saque de R$ {valor:.2f} realizado com sucesso!"

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato, f"Depósito de R$ {valor:.2f} realizado com sucesso!"
    else:
        return saldo, extrato, "Operação falhou! O valor informado é inválido."

def extrato_bancario(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=========================================")

# Classe base para transações
class Transacao:
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: 'Conta'):
        raise NotImplementedError("Método deve ser implementado nas subclasses")

# Classe para depósitos, herda de Transacao
class Deposito(Transacao):
    def registrar(self, conta: 'Conta'):
        conta.saldo, conta.extrato, msg = depositar(conta.saldo, self.valor, conta.extrato)
        conta.historico.adicionarTransacao(self)
        print(msg)

# Classe para saques, herda de Transacao
class Saque(Transacao):
    def registrar(self, conta: 'Conta'):
        conta.saldo, conta.extrato, conta.numero_saques, msg = sacar(
            saldo=conta.saldo,
            valor=self.valor,
            extrato=conta.extrato,
            limite=conta.limite,
            numero_saques=conta.numero_saques,
            limite_saques=conta.limite_saques
        )
        conta.historico.adicionarTransacao(self)
        print(msg)

# Classe para histórico de transações
class Historico:
    def __init__(self):
        self.transacoes: List[Transacao] = []

    def adicionarTransacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

# Classe para contas bancárias
class Conta:
    def __init__(self, numero: int, agencia: str, cliente: 'Cliente'):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        self.extrato = ""
        self.numero_saques = 0
        self.limite = 500
        self.limite_saques = 3

    def saldo(self) -> float:
        return self.saldo

    @classmethod
    def novaConta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        return cls(numero, "0001", cliente)

    def sacar(self, valor: float) -> bool:
        saque = Saque(valor)
        saque.registrar(self)
        return True

    def depositar(self, valor: float) -> bool:
        deposito = Deposito(valor)
        deposito.registrar(self)
        return True

# Classe para clientes
class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

# Classe para conta corrente, herda de Conta
class ContaCorrente(Conta):
    def __init__(self, numero: int, agencia: str, cliente: Cliente, limite: float, limiteSaques: int):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limiteSaques = limiteSaques

# Classe para pessoas físicas, herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, dataNascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.dataNascimento = dataNascimento

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
        saldo, extrato, msg = depositar(saldo, valor, extrato)
        print(msg)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques, msg = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        print(msg)

    elif opcao == "e":
        extrato_bancario(saldo, extrato=extrato)

    elif opcao == "cu":
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento (dd/mm/yyyy): ")
        cpf = input("CPF (somente números): ")
        endereco = input("Endereço (logradouro, número - bairro - cidade / sigla estado): ")
        criar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao == "cc":
        cpf_usuario = input("Informe o CPF do usuário: ")
        criar_conta(cpf_usuario)

    elif opcao == "lc":
        cpf_usuario = input("Informe o CPF do usuário: ")
        listar_conta(cpf_usuario)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
