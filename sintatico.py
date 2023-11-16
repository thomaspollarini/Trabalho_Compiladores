"""

 Linguagem Toy

    Gramatica::

    F* --> C Rf
    Rf --> C Rf | lambda
    C  --> A | R | P
    A --> ident = E ;
    R --> read ( ident ) ;
    P --> print ( ident ) ;

    E --> M Rs
    Rs --> + M Rs | lambda
    M --> Op Rm
    Rm --> * Op Rm | lambda
    Op --> ( E ) | num

    Tokens::

    IDENT ATRIB READ PTOVIRG PRINT ADD MULT OPENPAR CLOSEPAR NUM ERROR FIMARQ

    Comentarios::

    iniciam com # ate o fim da linha

"""

from lexico import TipoToken as tt, Token, Lexico

class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.F()
            self.consome( tt.FIMARQ )

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def F(self):
        self.C()
        self.Rf()

    def Rf(self):
        if self.atualIgual( tt.FIMARQ ):
            pass
        else:
            self.C()
            self.Rf()

    def C(self):
        if self.atualIgual( tt.READ ):
            self.R()
        elif self.atualIgual( tt.PRINT ):
            self.P()
        else:
            self.A()

    def A(self):
        self.consome( tt.IDENT )
        self.consome( tt.ATRIB )
        self.E()
        self.consome( tt.PTOVIRG )

    def R(self):
        self.consome( tt.READ )
        self.consome( tt.OPENPAR )
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )

    def P(self):
        self.consome( tt.PRINT )
        self.consome( tt.OPENPAR )
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )

    def E(self):
        self.M()
        self.Rs()

    def Rs(self):
        if self.atualIgual( tt.ADD ):
            self.consome( tt.ADD )
            self.M()
            self.Rs()
        else:
            pass

    def M(self):
        self.Op()
        self.Rm()

    def Rm(self):
        if self.atualIgual( tt.MULT ):
            self.consome( tt.MULT )
            self.Op()
            self.Rm()
        else:
            pass

    def Op(self):
        if self.atualIgual( tt.OPENPAR ):
            self.consome( tt.OPENPAR )
            self.E()
            self.consome( tt.CLOSEPAR )
        else:
            self.consome( tt.NUM )

if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo.toy'
   parser = Sintatico()
   parser.interprete(nome)
