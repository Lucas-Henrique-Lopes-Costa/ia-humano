import os
import string
from collections import Counter

"""
Programa de Identificação de Autoria
A ideia nessa aula é desenvolvermos um programa que tenta identificar o autor desconhecido de um texto misterioso.

Vamos usar IA para fazer essa predição.
Não vamos perder a oportunidade de usar IA em uma disciplina de Programação com Suporte de IA. 😁
12
Suponha que temos dois trechos de texto.

Trecho 1

I have not yet described to you the most singular part. About six years ago — to be exact, upon the 4th of May 1882 — an advertisement appeared in the Times asking for the address of Miss Mary Morstan and stating that it would be to her advantage to come forward. There was no name or address appended. I had at that time just entered the family of Mrs. Cecil Forrester in the capacity of governess. By her advice I published my address in the advertisement column. The same day there arrived through the post a small card-board box addressed to me, which I found to contain a very large and lustrous pearl. No word of writing was enclosed. Since then, every year upon the same date there has always appeared a similar box, containing a similar pearl, without any clue as to the sender. They have been pronounced by an expert to be of a rare variety and of considerable value. You can see for yourselves that they are very handsome.

13
Trecho 2

It was the Dover Road that lay on a Friday night late in November, before the first of the persons with whom this history has business. The Dover Road lay, as to him, beyond the Dover mail, as it lumbered up Shooter’s Hill. He walked up hill in the mire by the side of the mail, as the rest of the passengers did; not because they had the least relish for walking exercise, under the circumstances, but because the hill, and the harness, and the mud, and the mail, were all so heavy, that the horses had three times already come to a stop, besides once drawing the coach across the road, with the mutinous intent of taking it back to Blackheath. Reins and whip and coachman and guard, however, in combination, had read that article of war which forbade a purpose otherwise strongly in favour of the argument, that some brute animals are endued with Reason; and the team had capitulated and returned to their duty.

14
Suponha que alguém te pergunte se é provável que esses dois trechos tenham sido escritos pelo mesmo autor.

Como você poderia responder a essa pergunta?
Apenas com base nos textos - não vale jogar no Google 😜
Podemos assumir uma premissa razoável de que autores diferentes têm estilo de escrita diferentes.

E que essas diferenças aparecem em métricas que podemos calcular a partir dos textos.
15
Como assim?

Podemos notar, por exemplo, que o primeiro trecho tem frases mais curtas.
E o segundo texto parece mais complexo se repararmos a quantidade de vírgulas e ponto-e-vírgulas.
Com base nessa avaliação poderíamos concluir que os textos, provavelmente, foram escritos por autores diferentes.

O que é verdade nesse caso.
16
O autor do primeiro texto é Sir Arthur Conan Doyle.

Foto de Sir Arthur Conan Doyle. Imagem do filme Sherlock Holmes.

E o autor do segundo texto é Charles Dickens.

Foto de Charles Dickens. Imagem de adaptações de obras de Charles Dickens.

17
Nesse caso acertamos que são autores diferentes, mas o exemplo foi escolhido a dedo 🤭

Pode ser, por exemplo, que um mesmo autor escreva diferente em trechos ou livros diferentes.
Mas, como não vamos fazer um programa perfeito, tudo bem.
18
Ideia Geral
Baseado no princípio desse exemplo, suponha que tenhamos:

um conjunto de textos de autores conhecidos.
e o texto de um autor desconhecido
Poderia ser uma obra nunca publicada, que foi encontrada por acaso com um colecionador, por exemplo.
Ou uma obra publicada com um pseudônimo, que pareça ter sido escrita por um autor conhecido.
Precisamos de uma forma que nos permita comparar o estilo de escrita dos autores conhecidos com o do autor desconhecido.

19
Ideia Geral
Nossa estratégia será construir uma “impressão digital” (ou “assinatura”) do estilo de escrita de cada autor.

Com base em um livro que ele tenha escrito.
Essa impressão digital seria baseada em métricas que conseguimos calcular a partir do texto.
Como o número médio de palavras por frase e a complexidade média das frases.
20
Ideia Geral
Usaríamos o mesmo processo para construir a impressão digital do texto de autor desconhecido.

E compararíamos a impressão digital do autor desconhecido com a dos autores conhecidos.
Aquele que tiver a impressão digital mais próxima, seria o autor mais provável do texto desconhecido.
21
Limitações
Claro que o texto de autor desconhecido pode ser de um autor completamente novo.

Ou pode ser que nossas métricas não capturem bem o estilo de escrita de cada autor.
Ou ainda que um mesmo autor escreva livros diferentes com estilos diferentes.
Portanto, nosso programa não estará pronto para ser lançado no mercado 🙃

De todo modo, dada a dificuldade da tarefa, você ficará surpreso com o resultado que conseguiremos alcançar.
22
A ideia nessa aula é que você mesmo faça o design top-down do programa.

E use o Copilot para ajudar a implementar as funções que você definir.
O livro da disciplina vai construindo o design e, à medida que avança, vai acrescentando mais detalhes sobre como o programa deve funcionar.

Como quais métricas usar, por exemplo.
Mas como aqui é você quem fará o design, é necessário que você conheça esses detalhes antes de começar a fazer o design.
23
Definições para o Programa de Identificação de Autoria
24
Textos disponíveis
O projeto inicial disponibilizado tem uma pasta dados.

Dentro da pasta há uma pasta chamada autores_conhecidos com 5 arquivos de texto.
Cada arquivo é um livro diferente, escrito por um autor diferente.
O título do arquivo é o nome do autor.
Há também 4 arquivos de autores desconhecidos.
Cada arquivo é um trecho de texto, que pode ter sido escrito por qualquer um dos autores conhecidos.
O nome do arquivo não indica o autor.
25
Métricas
A ideia é utilizar as seguintes métricas para construir a impressão digital de cada autor:

tamanho médio das palavras
número de palavras diferentes dividido pelo número total de palavras
número de palavras usadas exatamente uma vez dividido pelo número total de palavras
número médio de palavras por frase
complexidade média das frases
A seguir vamos detalhar como calcular cada uma delas.

26
Tamanho médio das palavras
A ideia aqui é diferenciar autores que usam, em média, palavras mais curtas ou mais longas.

Calculamos o número total de letras das palavras e o número total de palavras do texto.
E dividimos o primeiro pelo segundo.
Exemplo: “A chuva caía. O guarda-chuva tinha ficado em casa.”

São 40 letras e 9 palavras com um total.
Tamanho médio das palavras: 40 / 9 = 4.44
Obs.: para simplificar estamos considerando que o hífen conta como letra.
27
Número de palavras diferentes dividido pelo número total de palavras
A ideia dessa métrica é identificar autores que costumam ser repetitivos ou não.

Calculamos o número de palavras diferentes que aparecem.
E dividimos pelo número total de palavras do texto.
Ex.: Uma pérola! Uma pérola! Uma pérola brilhante! Rara. Que belo achado.

Total de palavras: 10
Palavras diferentes: 7 (uma, pérola, brilhante, rara, que, belo, achado)
Resultado da métrica: 7 / 10 = 0.7
28
Número de palavras usadas exatamente uma vez dividido pelo número total de palavras
Pode ser que alguns autores usem muitas palavras apenas uma vez, enquanto outros tendem a repetir mais as palavras.

Vamos calcular o número de palavras que aparecem exatamente uma vez no texto.
E dividir pelo número total de palavras do texto.
Exemplo: Uma pérola! Uma pérola! Uma pérola brilhante! Rara. Que belo achado.

Número total de palavras: 10
Palavras usadas exatamente uma vez: 5 (brilhante, rara, que, belo, achado)
Resultado da métrica: 5 / 10 = 0.5
29
Número médio de palavras por frase
A ideia dessa métrica é identificar se o autor costuma escrever frases mais longas ou mais curtas.

Calculamos o número total de palavras e o número total de frases do texto.
E dividimos o primeiro pelo segundo.
Exemplo: “A chuva caía. O guarda-chuva tinha ficado em casa.”

Número total de palavras: 9
Número total de frases: 2
Número médio de palavras por frase: 9 / 2 = 4.5
30
Complexidade média das frases
Comentamos no exemplo inicial que um trecho de texto tinha frases mais curtas e outro mais longas.

Uma maneira que temos de medir a complexidade é verificar se as frases têm mais de uma oração.
Exemplo: “No mesmo dia chegou uma carta endereçada a mim, que parecia conter algo importante. Mas não tive coragem de abri-la.”

Veja que a primeira frase tem duas orações, separadas pela vírgula.
Já a segunda frase tem apenas uma oração.
31
Complexidade média das frases
Como seria muito complicado realmente tentar identificar orações, vamos usar uma aproximação simples:

Vamos considerar que toda vírgula, ponto-e-vírgula ou dois-pontos indicam a separação de orações de uma frase.
E vamos calcular o total de orações dividido pelo total de frases do texto.
No exemplo citado, o resultado da métrica seria: 3 / 2 = 1.5
32
A impressão digital de cada autor será então dada pelo conjunto de métricas calculada a partir de um livro que ele tenha escrito.

Ela será uma lista de 5 números, com os valores de cada métrica na ordem que definimos.
Exemplo: [4.44, 0.7, 0.5, 4.5, 1.5]
tamanho médio das palavras
número de palavras diferentes dividido pelo número total de palavras
número de palavras usadas exatamente uma vez dividido pelo número total de palavras
número médio de palavras por frase
complexidade média das frases
Em Aprendizado de Máquina, nós chamaríamos esse conjunto de vetor de características (features).

33
Identificando o autor desconhecido
Para identificar o autor desconhecido de um texto, faremos o seguinte:

Calcularemos a impressão digital de cada autor conhecido.
Calcularemos a impressão digital do texto de autor desconhecido.
E a compararemos com a impressão digital de cada autor conhecido.
O autor conhecido cuja impressão digital for mais próxima, será o autor mais provável do texto desconhecido.
Mas como será feita a comparação entre as impressões digitais?

34
Identificando o autor desconhecido
Suponha que estamos comparando a impressão digital [4.44, 0.7, 0.5, 4.5, 1.5] com uma impressão digital de um autor desconhecido dada por [4.0, 0.5, 0.7, 4.0, 1.9].

Vamos calcular a diferença, em módulo, entre cada métrica.
O resultado seria [0.44, 0.2, 0.2, 0.5, 0.4].
E, em seguida, vamos calcular a soma ponderada dessas diferenças.
Os pesos da soma seria: [11, 33, 50, 0.4, 4].
O resultado seria então (0.44*11 + 0.2*33 + 0.2*50 + 0.5*0.4 + 0.4*4) = 23.24.
35
Identificando o autor desconhecido
Mas de onde veio essa lista de pesos?

Os autores do livro aplicaram esse exercício ao longo do tempo.
E, empiricamente, descobriram que esses pesos funcionam bem para esse problema.
Obs.: em uma aplicação profissional de Aprendizado de Máquina, esses pesos seriam aprendidos a partir de um conjunto de dados de treinamento.

36
Identificando o autor desconhecido
Voltando à identificação do autor desconhecido:

Vimos que a comparação entre duas impressões digitais resulta em um número (score).
E quanto menor esse número, menor a diferença entre as impressões digitais, certo?
Portanto, o autor conhecido cuja comparação resulte no menor score será o autor mais provável do texto desconhecido.
37
Dica para a fase de design
Uma das operações necessárias é a contagem de palavras.

Para isso, podemos usar a função split() da classe str.
Exemplo:
Usando função split() no trecho “A chuva caía. O guarda-chuva tinha ficado em casa.”
Obteríamos as palavras: ["A", "chuva", "caía.", "O", "guarda-chuva", "tinha", "ficado", "em", "casa."]
Mas veja que as palavras “caía.” e “caía” seriam consideradas diferentes.
Precisamos então tratar isso, removendo as pontuações das palavras.
Mas devemos tomar cuidado para não remover o hífen, que faz parte da palavra (como na palavra “guarda-chuva”).
Bastaria remover as pontuações apenas do início e do fim das palavras.
"""


def leitura_de_textos(caminho_pasta):
    """
    Função que recebe o caminho da pasta onde estão os arquivos de texto.

    Lê todos os arquivos da pasta especificada e retorna um dicionário:
    - chave: nome do arquivo (sem extensão)
    - valor: conteúdo do arquivo
    """
    textos = {}

    if os.path.exists(caminho_pasta):
        for arquivo in os.listdir(caminho_pasta):
            caminho = os.path.join(caminho_pasta, arquivo)
            if os.path.isfile(caminho):
                with open(caminho, "r", encoding="utf-8") as f:
                    textos[os.path.splitext(arquivo)[0]] = f.read()

    return textos


def extracao_de_palavras(texto):
    """
    Recebe um texto em formato de string única e extrai todas as palavras,
    removendo pontuações do início e do fim.
    Retorna uma lista de palavras limpas.
    """
    pontuacoes = string.punctuation.replace("-", "")
    palavras = texto.split()
    palavras_limpa = [
        palavra.strip(pontuacoes) for palavra in palavras if palavra.strip(pontuacoes)
    ]
    return palavras_limpa


def contagem_de_letras(texto):
    """
    Deve realizar a contagem de letras de um determinado texto recebendo o texto em formato
    de uma string única para que assim seja possível extrair quantas letras aquela string contém
    Retorno: Retorna um número inteiro com a quantidade de letras que aquele texto(string)
    contém
    """
    # Remove pontuações do início e fim das palavras, mas mantém hífen
    pontuacoes = string.punctuation.replace("-", "")
    palavras = texto.split()
    total_letras = 0
    for palavra in palavras:
        palavra_limpa = palavra.strip(pontuacoes)
        total_letras += len(palavra_limpa)
    return total_letras


def tamanho_medio_palavras(texto):
    """
    Recebe um texto em formato de string única e calcula o tamanho médio das palavras.
    Retorna um float com a média do tamanho das palavras.
    """
    palavras = extracao_de_palavras(texto)
    if not palavras:
        return 0.0
    total_letras = contagem_de_letras(texto)
    return total_letras / len(palavras)


def contagem_de_frases(texto):
    """
    Contabiliza o número de frases em um texto, recebendo o texto como parâmetro
    e calculando quantas frases aquele texto possui.
    Retorno: Retorna um número inteiro com a quantidade de frases que aquele texto possui.
    """
    delimitadores = [".", "!", "?"]
    frases = 0
    for caractere in texto:
        if caractere in delimitadores:
            frases += 1
    return frases if frases > 0 else 1


def contagem_de_oracoes(texto):
    """
    Recebe um texto e conta o número de orações no texto (aproximação usando vírgulas, ponto-e-vírgula, dois-pontos).
    Retorna um inteiro com o número de orações.
    """
    delimitadores = [",", ";", ":"]
    oracoes = 1  # Começa com 1 para contar a primeira oração
    for caractere in texto:
        if caractere in delimitadores:
            oracoes += 1
    return oracoes


def contagem_palavras_diferentes(texto):
    """
    Chama a função "extracao_de_palavras" para obter a lista de palavras do texto.
    Cria um conjunto (set) a partir da lista de palavras para eliminar duplicatas.
    Retorna o tamanho do conjunto, que representa o número de palavras diferentes no texto.
    """
    palavras = extracao_de_palavras(texto)
    palavras_diferentes = set(palavras)
    return len(palavras_diferentes)


def med_palavras_por_frase(texto):
    """
    Dado um texto, calcula o número médio de palavras por frase.
    Retorna um float com a média.
    """
    total_palavras = len(extracao_de_palavras(texto))
    total_frases = contagem_de_frases(texto)
    if total_frases == 0:
        return 0.0
    return total_palavras / total_frases


def complexidade_media_frases(texto):
    """
    Dado um texto, calcula a complexidade média das frases,
    definida como o número total de orações dividido pelo número total de frases.
    Retorna um float com a complexidade média.
    """
    total_oracoes = contagem_de_oracoes(texto)
    total_frases = contagem_de_frases(texto)
    if total_frases == 0:
        return 0.0
    return total_oracoes / total_frases


def extracao_de_metricas(texto):
    """
    Extrai as métricas do texto conforme especificado:
    1. Tamanho médio das palavras
    2. Número de palavras diferentes dividido pelo número total de palavras
    3. Número de palavras usadas exatamente uma vez dividido pelo número total de palavras
    4. Número médio de palavras por frase
    5. Complexidade média das frases
    Retorna uma lista com as métricas na ordem definida.
    """
    palavras = extracao_de_palavras(texto)
    total_palavras = len(palavras)
    if total_palavras == 0:
        return [0.0, 0.0, 0.0, 0.0, 0.0]

    # 1. Tamanho médio das palavras
    tamanho_medio = tamanho_medio_palavras(texto)

    # 2. Número de palavras diferentes dividido pelo número total de palavras
    palavras_diferentes = len(set(palavras))
    proporcao_diferentes = palavras_diferentes / total_palavras

    # 3. Número de palavras usadas exatamente uma vez dividido pelo número total de palavras
    contagem = Counter(palavras)
    palavras_unicas = sum(1 for v in contagem.values() if v == 1)
    proporcao_unicas = palavras_unicas / total_palavras

    # 4. Número médio de palavras por frase
    media_palavras_frase = med_palavras_por_frase(texto)

    # 5. Complexidade média das frases
    complexidade = complexidade_media_frases(texto)

    return [
        tamanho_medio,
        proporcao_diferentes,
        proporcao_unicas,
        media_palavras_frase,
        complexidade,
    ]


def gerar_array_proximidade(autores_conhecidos, autor_desconhecido):
    """
    Receber dois dicionários contendo autores e textos conhecidos e desconhecidos.
    Cada dicionário tem como chave o nome do autor e como valor o texto escrito por ele.
    Deve calcular a impressão digital através de extrair métricas de cada autor conhecido e do autor desconhecido.
    Deve retornar um dicionário onde a chave é o nome do texto e o um conjunto de dados de metricas
    para cada um dos textos.
    """
    metricas_conhecidos = {
        autor: extracao_de_metricas(texto)
        for autor, texto in autores_conhecidos.items()
    }
    metricas_desconhecidos = {
        autor: extracao_de_metricas(texto)
        for autor, texto in autor_desconhecido.items()
    }
    return {"conhecidos": metricas_conhecidos, "desconhecidos": metricas_desconhecidos}


def identificar_autor_desconhecido(metricas_conhecidos, metrica_desconhecido):
    """
    Recebe um dicionário contendo autores e textos conhecidos e desconhecidos.
    Identifica o autor mais provável de um texto desconhecido.
    Para isso compara a impressão digital do autor desconhecido com a dos autores conhecidos.
    Retorna o nome do autor conhecido cuja impressão digital for mais próxima.
    """
    pesos = [11, 33, 50, 0.4, 4]
    menor_score = float("inf")
    autor_mais_provavel = None

    for autor, metrica_conhecido in metricas_conhecidos.items():
        score = sum(
            abs(metrica_conhecido[i] - metrica_desconhecido[i]) * pesos[i]
            for i in range(5)
        )
        if score < menor_score:
            menor_score = score
            autor_mais_provavel = autor

    return autor_mais_provavel


def main():
    autores_conhecidos = {}
    autores_desconhecidos = {}
    autores_desconhecidos = leitura_de_textos("../dados")
    autores_conhecidos = leitura_de_textos("../dados/autores_conhecidos")

    metricas = gerar_array_proximidade(autores_conhecidos, autores_desconhecidos)
    for autor_desconhecido, metrica_desconhecido in metricas["desconhecidos"].items():
        autor_mais_provavel = identificar_autor_desconhecido(
            metricas["conhecidos"], metrica_desconhecido
        )
        print(
            f"O autor mais provável de '{autor_desconhecido}' é: {autor_mais_provavel}"
        )


if __name__ == "__main__":
    main()

