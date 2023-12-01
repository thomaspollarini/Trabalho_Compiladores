#
#    Testa o tradutor
#

from sintatico import Sintatico

if __name__ == '__main__':
    print('Tradutor Z \n')

    prompt = input("prompt>")
    
    modulos = prompt.split()
    
    parser = Sintatico()
    ok = parser.interprete(modulos[0])
    if ok:
        print("Arquivo sintaticamente correto.")
    else:
        print("Arquivo sintaticamente incorreto.")
        
    
    if len(modulos) != 1: #verifica se foi passado algum argumento
        if modulos[1]!='-t': #verifica se opção de execução é -t
            print('ERRO: Opção inválida digitada')
            exit()
        else:
            with open(modulos[2], 'w') as arquivo: #abre arquivo    
                for var,tipo in parser.tabsimb.tabela.items():
                    arquivo.write(f"{var}:{tipo}\n") #escreve no arquivo
        
    """ 
    for i in range(2, 3):
        nome = 'exemplo' + str(i) + '.txt'
        print("Testando arquivo: " + nome)
        parser = Sintatico()
        ok = parser.interprete(nome)
        if ok:
            print("Arquivo sintaticamente correto.")
        else:
            print("Arquivo sintaticamente incorreto.")
     
        
    nome = 'exemplo.toy'
    parser = Sintatico()
    ok = parser.traduz(nome)
    if ok:
        print("Arquivo sintaticamente correto.")
    else:
        print("Arquivo sintaticamente incorreto.")
    """  