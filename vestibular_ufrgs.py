# Place the names in the 'nomes' list, and the script will search for them in
# the UFRGS' vestibular (college entrance exam) list of names, and output the
# names of those that it found, and for each of those that it didn't find, a
# list with all the names with the same first name, for you to manually search.
# URL substitution may be necessary.

# Coloque os nomes na lista 'nomes', e o script vai buscar por eles no listão
# do vestibular da UFRGS, e devolver os nomes que ele achou (passaram), e para
# cada um que não foi achado, devolve uma lista de nomes com o mesmo primeiro
# nome, para fazer uma busca manual. Substituição da URL pode ser necessária.

from bs4 import BeautifulSoup
import requests

nomes = ["Example Name One",
         "Example Name Two"]

nomes_dicionario = []
for nome in nomes:
    src = 'https://vestibular.ufrgs.br/cv2019/listao/arquivo_' + nome[0].lower() + '.html'
    page = requests.get(src)
    soup = BeautifulSoup(page.content, 'html.parser')
    nomes_letra = []
    for tr in soup.select('div.listao tr'):
        if(tr.find_all('td') != []):
            nomes_letra.append(tr.find_all('td')[1].text)

    nomes_dicionario.append((nome,(nome in nomes_letra)))

passaram = []
nao_passaram = []
for nome in nomes_dicionario:
    if nome[1]:
        passaram.append(nome[0])
    else:
        nao_passaram.append(nome[0])

possiveis_nomes_total = []
for nome in nao_passaram:
    primeiro_nome = nome.split()[0]

    src = 'https://vestibular.ufrgs.br/cv2019/listao/arquivo_' + primeiro_nome[0].lower() + '.html'
    page = requests.get(src)
    soup = BeautifulSoup(page.content, 'html.parser')
    nomes_letra = []
    for tr in soup.select('div.listao tr'):
        if(tr.find_all('td') != []):
            nomes_letra.append(tr.find_all('td')[1].text)

    possiveis_nomes = []
    for nome_aleatorio in nomes_letra:
        if primeiro_nome in nome_aleatorio:
            possiveis_nomes.append(nome_aleatorio)

    possiveis_nomes_total.append((nome,possiveis_nomes))

print("\nPASSARAM:")
for nome in passaram:
    print(" -" + nome)
print("\nNÃO PASSARAM: (se tiver passado vai estar entre esses nomes)")
for nome in possiveis_nomes_total:
    print(nome[0] + ":")
    for possivel_nome in nome[1]:
        print("  -" + possivel_nome)
