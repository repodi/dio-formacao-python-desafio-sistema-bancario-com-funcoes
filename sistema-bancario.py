SENHA_MANUTENCAO = "1234"
LIMITE_SAQUES = 3
AGENCIA = "0001"
limite = 500

lista_clientes = []
lista_contas = []
numero_ultima_conta = 0

cliente_padrao = {
    "cpf" : "",
    "nome": "",
    "data_nascimento": "", 
    "endereco" : {
        "logradouro": "",
        "numero": "",
        "bairro": "",
        "cidade": "",
        "uf": ""
    }
}

conta_padrao = {
    "cpf" : "", 
    "agencia": AGENCIA,
    "nro_conta": 0,
    "saldo": 0,
    "extrato": "", 
    "numero_saques": 0
}

def busca_cliente_por_cpf(cpf):
    global lista_clientes
    for cliente in lista_clientes: 
        if cliente["cpf"] == cpf:
            return cliente
    else: 
        return None

def listar_clientes(cpf=None):
    global lista_clientes
    print("Lista de clientes:\n")
    for cliente in lista_clientes: 
        print(cliente)

def cadastrar_usuario():
    global cliente_padrao
    global lista_clientes
    print("Cadastrando novo cliente ---> ")
    novo_cliente = cliente_padrao.copy()
    for key in novo_cliente.keys():        
        if key == "cpf":
            campo = input(f"Informe o {key}: ")
            cliente_existente = busca_cliente_por_cpf(campo) 
            if cliente_existente:
                print(cliente_existente)
                print("CPF já esta cadastrado")
                return None
            else:
                novo_cliente[key] = campo
        elif key == "nome":
            campo = input(f"Informe o {key}: ")
            novo_cliente[key] = campo
        elif key == "endereco":
           for key_endereco in novo_cliente[key].keys():
               campo_endereco = input(f"Informe o endereço / {key_endereco}: ")
               novo_cliente[key][key_endereco] = campo_endereco
        else:
           campo = input(f"Informe o {key}: ")
           novo_cliente[key] = campo
    lista_clientes.append(novo_cliente)            
    print(f"Cliente {novo_cliente['cpf']} cadastrado!")

def cadastrar_conta():
    global conta_padrao
    global numero_ultima_conta
    global lista_clientes
    global lista_contas
    cpf = input(f"Informe o CPF do cliente: ")
    cliente = busca_cliente_por_cpf(cpf) 
    if not cliente:
        print("CPF do cliente não esta cadastrado, cadastre o cliente primeiro")
        return None
    else:
        numero_ultima_conta = numero_ultima_conta + 1
        nova_conta = conta_padrao.copy()
        nova_conta["cpf"] = cpf
        nova_conta["nro_conta"] = numero_ultima_conta
        lista_contas.append(nova_conta)
        print(f"Nova conta cadastrada CPF: {nova_conta['cpf']} Agência: {nova_conta['agencia']} Conta Corrente{nova_conta['nro_conta']}")

def listar_contas():
    global lista_contas
    cpf = input(f"Informe o CPF para um cliente em especifico ou pressione enter para todos clientes: ")
    if cpf:
        cliente = busca_cliente_por_cpf(cpf)
        if not cliente:
            print("CPF do cliente não esta cadastrado")
            return None
    print("Lista de contas:\n")
    for conta in lista_contas: 
        if cpf :
            if cpf == conta["cpf"]:
                print(conta)
        else: 
            print(conta)

menu_manutencao = """

[u] Cadastrar Usuário (Cliente)
[l] Listar clientes
[c] Nova Conta
[o] Listar contas
[q] Sair

=> """

def acesso_manutencao():
    senha = input("Informe a senha de manutenção:")
    if (senha == SENHA_MANUTENCAO):        
        while True: 
            opcao_manutencao = input(menu_manutencao)
            if opcao_manutencao == "u":
                cadastrar_usuario()
            elif opcao_manutencao == "l":
                listar_clientes()
            elif opcao_manutencao == "c":
                cadastrar_conta()
            elif opcao_manutencao == "o":
                listar_contas()
            elif opcao_manutencao == "q":
                break
            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
    else: 
        print("Senha de manutenção inválida.")

def buscar_conta(cpf, agencia, nro_conta):    
    global lista_contas
    for conta in lista_contas: 
        if cpf == conta["cpf"] and agencia == conta["agencia"] and int(nro_conta) == conta["nro_conta"]:
            return conta
    else: 
        return None
   
def acessar_conta():
    cpf = input("Informe o cpf para acessar suas contas:")
    cliente_existente = busca_cliente_por_cpf(cpf) 
    if cliente_existente: 
        agencia = input("Informe sua agência: ")
        nro_conta = input("Informe o número da sua conta corrente: ")
        conta_existente = buscar_conta(cpf, agencia, nro_conta)
        if conta_existente:
            acessar_menu_conta(cpf, agencia, nro_conta)
        else:
            print("A conta não existe!")
    else:
        print("Cliente não cadastrado!")

def depositar(cpf, agencia, nro_conta):
    conta = buscar_conta(cpf, agencia, nro_conta)
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        
    else:
        print("Operação falhou! O valor informado é inválido.")

def extrato(cpf, agencia, nro_conta): 
    conta = buscar_conta(cpf, agencia, nro_conta)
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

def saque(cpf, agencia, nro_conta, /):
    conta = buscar_conta(cpf, agencia, nro_conta)
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques"] >= LIMITE_SAQUES
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

menu_conta = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def acessar_menu_conta(cpf, agencia, nro_conta):
    cliente = busca_cliente_por_cpf(cpf).copy()
    print(f"Bem vindo {cliente['nome']} !")
    while True: 
        opcao_menu_conta = input(menu_conta)
        if opcao_menu_conta == "d":
            depositar(cpf, agencia, nro_conta)
        elif opcao_menu_conta == "s": 
            saque(cpf, agencia, nro_conta)
        elif opcao_menu_conta == "e": 
            extrato(cpf, agencia, nro_conta)
        elif opcao_menu_conta == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

menu_geral = """

[a] Acessar conta
[m] Manutenção
[l] Desligar sistema

=> """

while True: 
    opcao = input(menu_geral)
    if opcao == "m":
        acesso_manutencao()
    elif opcao == "a": 
        acessar_conta()
    elif opcao == "l":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
