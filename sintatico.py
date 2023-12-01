"""
Nome Discente: Thomas Santos Pollarini
Matrícula: 0064232
Data: 19/11/2023


Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

Código responsável pela parte sintatica do compilador, verifica se os TOKENS da parte lexica estão de acordo com a gramática
estabelecida.

"""


from lexico import TipoToken as tt, Token, Lexico
from tabela import TabelaSimbolos

class Sintatico:
    #construtor da classe
    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.deuErro = False
        # campos utilizados no modo panico
        self.modoPanico = False
        self.tokensDeSincronismo = [tt.PVIRG, tt.FIMARQ]


    #função que inicia a interpretação do arquivo
    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()
            self.tabsimb = TabelaSimbolos()
            self.PROG()   #chama regra inicial da gramática
            self.consome( tt.FIMARQ )
            
            self.lex.fechaArquivo()
            return not self.deuErro

    #função que verifica se o token atual é igual ao token esperado
    def tokenEsperadoEncontrado(self, token):    
        (const, msg) = token
        if self.tokenAtual.const == const:
            return True
        else:
            return False

    #função que consome o token atual, caso seja igual ao token esperado
    def consome(self, token):       
        if not self.modoPanico and self.tokenEsperadoEncontrado( token ):
            # tudo seguindo de acordo
            self.tokenAtual = self.lex.getToken()
            
        elif not self.modoPanico:
            # agora deu erro, solta msg e entra no modo panico
            self.modoPanico = True
            self.deuErro = True
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            #quit()
            procuraTokenDeSincronismo = True
            while procuraTokenDeSincronismo:
                self.tokenAtual = self.lex.getToken()
                for tk in self.tokensDeSincronismo:
                    (const, msg) = tk
                    if self.tokenAtual.const == const:
                        # tokenAtual eh um token de sincronismo
                        procuraTokenDeSincronismo = False
                        self.tokenAtual = self.lex.getToken()
                        break
        elif self.tokenEsperadoEncontrado(token):
            # chegou no ponto de sincronismo :)
            self.tokenAtual = self.lex.getToken()
            self.modoPanico = False
        else:
            # so continua, consumindo e consumindo...
            pass

    """
        Funções abaixo representam as regras da gramática
        
        utilizamos a funçao tokenEsperadoEncontrado para saber qual regra será chamada, em
        casos onde um Não terminal tenha mais de uma regra
        
        caso a função consome não consuma o token esperado ou em casos onde nenhuma
        regra do Não terminal atual seja escolhida, haverá um erro sintatico.
    
    """

    #PROG → program id pvirg DECLS C_COMP
    def PROG(self):                                 
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()

    #DECLS → var LIST_DECLS | λ
    def DECLS(self):
        if self.tokenEsperadoEncontrado(tt.VAR):
            self.consome(tt.VAR)
            self.LIST_DECLS()
        else:
            pass

    #LIST_DECLS → DECL_TIPO D
    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    #D → LIST_DECLS | λ
    def D(self):
        if self.tokenEsperadoEncontrado(tt.ID):
            self.LIST_DECLS()
        else:
            pass
        
    #DECL_TIPO → LIST_ID dpontos TIPO pvirg
    def DECL_TIPO(self):
        nomes=[] #lista de para salvar ids
        self.LIST_ID(nomes)
        self.consome(tt.DPONTOS)
        valor =self.TIPO() #salva o tipo
        self.tabsimb.declaraIdent(nomes, valor,self.tokenAtual.linha) #declara os ids na tabela de simbolos
        self.consome(tt.PVIRG)
        
    #LIST_ID → id E
    def LIST_ID(self, nomes=[]):
        if self.tokenEsperadoEncontrado(tt.ID):   #se for um id
            nomes.append(self.tokenAtual.lexema)  #adiciona na lista de ids
        self.consome( tt.ID )
        self.E(nomes)

    #E → virg LIST_ID | λ
    def E(self,nomes):
        if self.tokenEsperadoEncontrado(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID(nomes)
        else:
            pass

    #TIPO → int | real | bool | char
    def TIPO(self):
        if self.tokenEsperadoEncontrado( tt.INT ):
            self.consome(tt.INT)
            return "int"
        elif self.tokenEsperadoEncontrado(tt.REAL):
            self.consome(tt.REAL)
            return "real"
        elif self.tokenEsperadoEncontrado(tt.BOOL):
            self.consome(tt.BOOL)
            return "bool"
        else:
            self.consome(tt.CHAR)
            return "char"
        

    #C_COMP → abrech LISTA_COMANDOS fechach
    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    #LISTA_COMANDOS → COMANDOS G
    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    #G → LISTA_COMANDOS | λ
    def G(self):
        if self.tokenEsperadoEncontrado( tt.IF ) or self.tokenEsperadoEncontrado( tt.WHILE ) or \
           self.tokenEsperadoEncontrado( tt.READ ) or self.tokenEsperadoEncontrado( tt.WRITE ) or \
           self.tokenEsperadoEncontrado( tt.ID ):
            self.LISTA_COMANDOS()
        else:
            pass
    
    #COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO
    def COMANDOS(self):
        if self.tokenEsperadoEncontrado( tt.IF ):
            self.SE()
        elif self.tokenEsperadoEncontrado( tt.WHILE ):
            self.ENQUANTO()
        elif self.tokenEsperadoEncontrado( tt.READ ):
            self.LEIA()
        elif self.tokenEsperadoEncontrado( tt.WRITE ):
            self.ESCREVA()
        else:
            self.ATRIBUICAO()
        

    #SE → if abrepar EXPR fechapar C_COMP H
    def SE(self):
        self.consome(tt.IF)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        self.H()
        
    #H → else C_COMP | λ
    def H(self):
        if self.tokenEsperadoEncontrado(tt.ELSE):
            self.consome(tt.ELSE)
            self.C_COMP()
        else:
            pass
        
    #ENQUANTO → while abrepar EXPR fechapar C_COMP
    def ENQUANTO(self):
        self.consome(tt.WHILE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        
    #LEIA → read abrepar LIST_ID fechapar pvirg
    def LEIA(self):
        self.consome(tt.READ)
        self.consome(tt.ABREPAR)
        self.LIST_ID()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)
        
    #ATRIBUICAO → id atrib EXPR pvirg
    def ATRIBUICAO(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)
       
    #ESCREVA → write abrepar LIST_W fechapar pvirg 
    def ESCREVA(self):
        self.consome(tt.WRITE)
        self.consome(tt.ABREPAR)
        self.LIST_W()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)
        
    #LIST_W → ELEM_W L
    def LIST_W(self):
        self.ELEM_W()
        self.L()
        
    #L → virg LIST_W | λ
    def L(self):
        if self.tokenEsperadoEncontrado(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass
    
    #ELEM_W → EXPR | cadeia
    def ELEM_W(self):
        if self.tokenEsperadoEncontrado( tt.ID ) or self.tokenEsperadoEncontrado( tt.CTE ) or \
           self.tokenEsperadoEncontrado( tt.ABREPAR ) or self.tokenEsperadoEncontrado( tt.TRUE ) or \
           self.tokenEsperadoEncontrado( tt.FALSE ) or self.tokenEsperadoEncontrado(tt.OPNEG):
            self.EXPR()
        else:
            self.consome(tt.CADEIA)
        
            
    #EXPR → SIMPLES P
    def EXPR(self):
        self.SIMPLES()
        self.P()
        
    #P → oprel SIMPLES | λ
    def P(self):
        if self.tokenEsperadoEncontrado(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass
    
    #SIMPLES → TERMO R
    def SIMPLES(self):
        self.TERMO()
        self.R()
    
    #R → opad SIMPLES | λ
    def R(self):
        if self.tokenEsperadoEncontrado(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass
    
    #TERMO → FAT S
    def TERMO(self):
        self.FAT()
        self.S()
    
    #S → opmul TERMO | λ
    def S(self):
        if self.tokenEsperadoEncontrado(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass
    
    #FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT
    def FAT(self):
        if self.tokenEsperadoEncontrado( tt.OPNEG ):
            self.consome(tt.OPNEG)
            self.FAT()
        elif self.tokenEsperadoEncontrado( tt.CTE ):
            self.consome(tt.CTE)
        elif self.tokenEsperadoEncontrado( tt.ABREPAR ):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.tokenEsperadoEncontrado( tt.TRUE ):
            self.consome(tt.TRUE)
        elif self.tokenEsperadoEncontrado( tt.FALSE ):
            self.consome(tt.FALSE)
        else:
            self.consome(tt.ID)
        

if __name__== "__main__":

    nome = input("Entre com o nome do arquivo: ")
    #nome = 'exemplo1.txt'

    parser = Sintatico()
    parser.interprete(nome)
   
