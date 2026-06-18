import math
import os, platform


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
                        if platform.system() == "Windows":
                            pasta_separada = caminho_completo.split("\\")
                        elif platform.system() == "Linux":
                            pasta_separada = caminho_completo.split("/")
                        else:
                            print("Sistema não suportado")

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

def justificar_texto(texto, tamanho_letra_slide):
        # 1. Criamos o Frame HTML
        # frame_html = HtmlFrame(janela_nova)

        # 2. Seu texto com HTML e CSS para justificar em ambos os lados e centralizar
        largura_slide = "91%"
        tamanho_fonte = f"{tamanho_letra_slide}px"

        codigo_html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <body style="background-color: black; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="
                color: white; 
                font-family: Arial, sans-serif; 
                font-size: {tamanho_fonte}; 
                font-weight: bold; 
                text-align: justify; /* JUSTIFICA AMBOS OS LADOS */
                margin: auto;
                padding-top: 30px;
                max-width: {largura_slide};
                width: 100%;
                line-height: 1.1;
            ">
                {texto.replace('\n', '<br>')}

            </div>
        </body>
        </html>
        """

        return codigo_html