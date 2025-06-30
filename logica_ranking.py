import os

vendedores = []

def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]
    maiores = [x for x in lista[1:] if x["vendas"] >= pivo["vendas"]]
    menores = [x for x in lista[1:] if x["vendas"] < pivo["vendas"]]
    return quick_sort(maiores) + [pivo] + quick_sort(menores)

def adicionar_vendedor(nome, vendas_txt):
    try:
        vendas = float(vendas_txt)
        vendedores.append({"nome": nome, "vendas": vendas})
        return True, ""
    except ValueError:
        return False, "Valor inválido para vendas."

def limpar_dados():
    vendedores.clear()

def get_ranking_text():
    if not vendedores:
        return "Nenhum vendedor adicionado ainda."
    texto = ""
    ordenados = quick_sort(vendedores)
    for i, v in enumerate(ordenados, 1):
        texto += f"{i}º lugar: {v['nome']} - R$ {v['vendas']:.2f}\n"
    return texto

def salvar_em_txt():
    if not vendedores:
        return False, "Nada a salvar."
    try:
        caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        caminho_arquivo = os.path.join(caminho_downloads, "relatorio_vendas.txt")
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write("🏆 Relatório de Vendas\n\n")
            ordenados = quick_sort(vendedores)
            for i, v in enumerate(ordenados, 1):
                f.write(f"{i}º lugar: {v['nome']} - R$ {v['vendas']:.2f}\n")
        return True, caminho_arquivo
    except Exception as e:
        return False, str(e)

def get_dados_para_grafico():
    ordenados = quick_sort(vendedores)
    nomes = [v["nome"] for v in ordenados]
    vendas = [v["vendas"] for v in ordenados]
    return nomes, vendas
