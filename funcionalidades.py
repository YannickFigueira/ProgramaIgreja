import math
import os


def localizar_arquivo(pasta_raiz, termo_busca):
    print(f"Buscando por '{termo_busca}' em: {pasta_raiz}\n")

    # os.walk percorre pastas e subpastas
    resultado = ""
    for raiz, pastas, arquivos in os.walk(pasta_raiz):
        for arquivo in arquivos:
            # Verifica se o arquivo é .txt
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    # Abre o arquivo com encoding utf-8 para evitar erros de caracteres
                    with open(caminho_completo, 'r', encoding='utf-8') as f:
                        pasta_separada = caminho_completo.split("/")

                        for numero_linha, linha in enumerate(f, 1):
                            if termo_busca.lower() in linha.lower():  # Busca sem diferenciar maiúsculas/minúsculas
                                #print(f"Encontrado em: {pasta_separada[len(pasta_separada) -1]} (Linha {numero_linha})")
                                #print(f"-> {linha.strip()}\n")
                                resultado += f" {pasta_separada[len(pasta_separada) -1]} -> Verso {math.ceil(numero_linha / 3)} -> {linha.strip()}\n"
                except (UnicodeDecodeError, PermissionError):
                    # Ignora arquivos que não podem ser lidos (ex: codificação diferente ou sem permissão)
                    continue
    #print(resultado)
    return resultado.replace(".txt", "")