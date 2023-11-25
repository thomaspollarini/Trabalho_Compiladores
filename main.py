#
#    Testa o tradutor
#

from sintatico import Sintatico

if __name__ == '__main__':
    print('Tradutor Z \n')

    # nome = input("Entre com o nome do arquivo: ")
    for i in range(1, 5):
        nome = 'exemplo' + str(i) + '.txt'
        print("Testando arquivo: " + nome)
        parser = Sintatico()
        ok = parser.interprete(nome)
        if ok:
            print("Arquivo sintaticamente correto.")
        else:
            print("Arquivo sintaticamente incorreto.")
     
    """     
    nome = 'exemplo.toy'
    parser = Sintatico()
    ok = parser.traduz(nome)
    if ok:
        print("Arquivo sintaticamente correto.")
    else:
        print("Arquivo sintaticamente incorreto.")
    """  