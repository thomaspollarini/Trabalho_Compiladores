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

class Sintatico:
    #construtor da classe
    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    #função que inicia a interpretação do arquivo
    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.PROG()   #chama regra inicial da gramática
            self.consome( tt.FIMARQ )
            print("PALAVRA ACEITA")
            
            self.lex.fechaArquivo()

    #função que verifica se o token atual é igual ao token esperado
    def atualIgual(self, token):    
        (const, msg) = token
        return self.tokenAtual.const == const

    #função que consome o token atual, caso seja igual ao token esperado
    def consome(self, token):       
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    """
        Funções abaixo representam as regras da gramática
        
        utilizamos a funçao atualIgual para saber qual regra será chamada, em
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
        if self.atualIgual(tt.VAR):
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
        if self.atualIgual(tt.ID):
            self.LIST_DECLS()
        else:
            pass
        
    #DECL_TIPO → LIST_ID dpontos TIPO pvirg
    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PVIRG)
        
    #LIST_ID → id E
    def LIST_ID(self):
        self.consome( tt.ID )
        self.E()

    #E → virg LIST_ID | λ
    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID()
        else:
            pass

    #TIPO → int | real | bool | char
    def TIPO(self):
        if self.atualIgual( tt.INT ):
            self.consome(tt.INT)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL)
        elif self.atualIgual(tt.CHAR):
            self.consome(tt.CHAR)
        else:
            print('ERRO DE SINTAXE [linha %d]: era esperado %s mas veio "%s"'
               % (self.tokenAtual.linha, '"int" | "real" | "bool" | "char"', self.tokenAtual.lexema))

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
        if self.atualIgual( tt.IF ) or self.atualIgual( tt.WHILE ) or \
           self.atualIgual( tt.READ ) or self.atualIgual( tt.WRITE ) or \
           self.atualIgual( tt.ID ):
            self.LISTA_COMANDOS()
        else:
            pass
    
    #COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO
    def COMANDOS(self):
        if self.atualIgual( tt.IF ):
            self.SE()
        elif self.atualIgual( tt.WHILE ):
            self.ENQUANTO()
        elif self.atualIgual( tt.READ ):
            self.LEIA()
        elif self.atualIgual( tt.WRITE ):
            self.ESCREVA()
        elif self.atualIgual( tt.ID ):
            self.ATRIBUICAO()
        else:
            print('ERRO DE SINTAXE [linha %d]: era esperado %s mas veio "%s"'
               % (self.tokenAtual.linha, '"if" | "while" | "read" | "write" | "id"', self.tokenAtual.lexema))

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
        if self.atualIgual(tt.ELSE):
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
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass
    
    #ELEM_W → EXPR | cadeia
    def ELEM_W(self):
        if self.atualIgual( tt.ID ) or self.atualIgual( tt.CTE ) or \
           self.atualIgual( tt.ABREPAR ) or self.atualIgual( tt.TRUE ) or \
           self.atualIgual( tt.FALSE ) or self.atualIgual(tt.OPNEG):
            self.EXPR()
        elif self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            print('ERRO DE SINTAXE [linha %d]: era esperado %s mas veio "%s"'
               % (self.tokenAtual.linha, '"id" | "cte" | "(" | "true" | "false" | "!" | "cadeia"', self.tokenAtual.lexema))
            
    #EXPR → SIMPLES P
    def EXPR(self):
        self.SIMPLES()
        self.P()
        
    #P → oprel SIMPLES | λ
    def P(self):
        if self.atualIgual(tt.OPREL):
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
        if self.atualIgual(tt.OPAD):
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
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass
    
    #FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT
    def FAT(self):
        if self.atualIgual( tt.ID ):
            self.consome(tt.ID)
        elif self.atualIgual( tt.CTE ):
            self.consome(tt.CTE)
        elif self.atualIgual( tt.ABREPAR ):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.atualIgual( tt.TRUE ):
            self.consome(tt.TRUE)
        elif self.atualIgual( tt.FALSE ):
            self.consome(tt.FALSE)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()
        else:
            print('ERRO DE SINTAXE [linha %d]: era esperado %s mas veio "%s"'
               % (self.tokenAtual.linha, '"id" | "cte" | "(" | "true" | "false" | "!"', self.tokenAtual.lexema))

if __name__== "__main__":

    nome = input("Entre com o nome do arquivo: ")
    #nome = 'exemplo1.txt'

    parser = Sintatico()
    parser.interprete(nome)
   
