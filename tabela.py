"""
Nome Discente: Thomas Santos Pollarini
Matrícula: 0064232
Data: 30/11/2023


Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

Código responsável pela criação da tabela de símbolos e verificação de identificadores já declarados.

"""

class TabelaSimbolos:

    def __init__(self):
        self.tabela = dict()

    def existeIdent(self, nome):
        if nome in self.tabela:
            return True
        else:
            return False

    def declaraIdent(self, nomes, valor,linha):
        for nome in nomes: #para cada nome na lista de nomes
            if not self.existeIdent(nome):
                self.tabela[nome] = valor #adiciona na tabela, o nome e o tipo
            else:
                print('ERRO SEMÂNTICO [linha %d]: identificador "%s" já declarado.'
                    % (linha, nome))
                    
                