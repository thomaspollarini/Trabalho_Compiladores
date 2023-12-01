"""
Nome Discente: Thomas Santos Pollarini
Matrícula: 0064232
Data: 30/11/2023


Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

Código responsável por executar o programa principal, que recebe como argumento o nome do arquivo a ser analisado e a opção
de execução -t, que gera um arquivo com a tabela de símbolos.

"""

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