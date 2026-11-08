import json
from pathlib import Path


ARQUIVO = Path(__file__).with_name("estoque.json")


def carregar_estoque():
    try:
        estoque = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}

    if not isinstance(estoque, dict) or any(
        type(saldo) is not int or saldo < 0 for saldo in estoque.values()
    ):
        raise ValueError("O arquivo precisa conter produtos e saldos inteiros válidos.")
    return estoque


def salvar_estoque(estoque):
    # Grava em um arquivo temporário antes de substituir o anterior.
    temporario = ARQUIVO.with_suffix(".tmp")
    temporario.write_text(
        json.dumps(estoque, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporario.replace(ARQUIVO)


def cadastrar(estoque):
    nome = input("Nome do produto: ").strip().lower()
    if not nome:
        print("Informe um nome.")
    elif nome in estoque:
        print("Produto já cadastrado.")
    else:
        estoque[nome] = 0
        print("Produto cadastrado com saldo zero.")


def listar(estoque):
    if not estoque:
        print("Nenhum produto cadastrado.")
    for nome, saldo in estoque.items():
        print(f"{nome}: {saldo} unidade(s)")


def movimentar(estoque, saida):
    nome = input("Nome do produto: ").strip().lower()
    if nome not in estoque:
        print("Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Digite um número inteiro.")
        return

    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")
        return

    if saida:
        if quantidade > estoque[nome]:
            print("Saldo insuficiente.")
            return
        estoque[nome] -= quantidade
    else:
        estoque[nome] += quantidade

    print(f"Novo saldo de {nome}: {estoque[nome]} unidade(s).")


def main():
    try:
        estoque = carregar_estoque()
    except (OSError, ValueError) as erro:
        print(f"Não foi possível ler o estoque: {erro}")
        return

    while True:
        print("\n=== CONTROLE DE ESTOQUE ===")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Registrar entrada")
        print("4 - Registrar saída")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        # Altera uma cópia para só atualizar o estoque após salvar.
        atualizado = estoque.copy()
        if opcao == "1":
            cadastrar(atualizado)
        elif opcao == "2":
            listar(estoque)
        elif opcao == "3":
            movimentar(atualizado, saida=False)
        elif opcao == "4":
            movimentar(atualizado, saida=True)
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")

        if atualizado != estoque:
            try:
                salvar_estoque(atualizado)
            except OSError as erro:
                print(f"Alteração não salva: {erro}")
            else:
                estoque = atualizado


if __name__ == "__main__":
    main()
