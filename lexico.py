from os import path

class TipoToken:
    PROGRAM = (1, 'program')
    ID = (2, 'id')
    VAR = (3, 'VAR')
    INT = (4, 'int')
    REAL = (5, 'real')
    BOOL = (6, 'bool')
    CHAR = (7, 'char')
    ABREPAR = (8, '(')
    FECHAPAR = (9, ')')
    IF = (10, 'if')
    ABRECH = (11, '{')
    FECHACH = (12, '}')
    ELSE = (13, 'else')
    WHILE = (14, 'while')
    READ = (15, 'read')
    ATRIB = (16, '=')
    WRITE = (17, 'write')
    CADEIA = (18, 'cadeia')
    CTE = (19, 'cte')
    TRUE = (20, 'true')
    FALSE = (21, 'false')
    OPREL = (22, 'oprel')
    OPAD = (23, 'opad')
    OPMUL = (24, 'opmul')
    OPNEG = (25, '!')
    PVIRG = (26, ';')
    VIRG = (27, ',')
    DPONTOS = (28, ':')
    ERROR = (29, 'erro')
    FIMARQ = (30, 'fim-de-arquivo')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'program': TipoToken.PROGRAM,
                   'VAR': TipoToken.VAR,
                   'int': TipoToken.INT,
                   'real': TipoToken.REAL,
                   'bool': TipoToken.BOOL,
                   'char': TipoToken.CHAR,
                   'if': TipoToken.IF,
                   'else': TipoToken.ELSE,
                   'while': TipoToken.WHILE,
                   'read': TipoToken.READ,
                   'write': TipoToken.WRITE,
                   'false': TipoToken.FALSE,
                   'true': TipoToken.TRUE}

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()
            
    def is_alpha(self,car):
        return 'A' <= car <= 'Z' or 'a' <= car <= 'z'

    def is_alnum(self,car):
        return self.is_alpha(car) or '0' <= car <= '9'

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif self.is_alpha(car):
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'+','-'}:
                    aux = self.getChar()
                    if aux.isdigit():
                        self.ungetChar(aux)
                        estado=3  
                    else:    
                        self.ungetChar(aux)
                        estado=4
                elif car in {'=', ';','*', '(', ')','<','>','!','{','}',':',',','\"'}:
                    estado = 4
                elif car == '/':
                    car = self.getChar()
                    if car == '/' or car == '*':
                        estado=5
                    else:
                        self.ungetChar(car)
                        car='/'
                        estado=4
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not self.is_alnum(car)):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        if len(lexema)>32:
                            return Token(TipoToken.ERROR, '<' + lexema + '>', self.linha)
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car == '.' and '.' not in lexema:
                    continue
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.CTE, lexema, self.linha)

            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':
                    car=self.getChar()
                    if car == '=':
                        lexema += car
                        return Token(TipoToken.OPREL, lexema,self.linha)
                    else:
                        self.ungetChar(car)
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, lexema, self.linha)
                elif car == '+' or car == '-':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '*' or car == '/':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == ':':
                    return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == '<':
                    car = self.getchar()
                    if car == '=' or car == '>':
                        lexema += car
                    else:
                        self.ungetChar(car)
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '>':
                    car = self.getChar()
                    if car == '=':
                        lexema += car
                    else:
                        self.ungetChar(car)
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '!':
                    return Token(TipoToken.OPNEG, lexema, self.linha)
                elif car == '\"':
                    car = self.getChar()
                    while (not car is None) and (car != '\"'):
                        lexema += car
                        car = self.getChar()
                    if car is None:
                        estado = 1
                    else:
                        lexema += car
                        return Token(TipoToken.CADEIA, lexema, self.linha)
            elif estado == 5:
                # consumindo comentario
                if car == '/':
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                else:
                    while (not car is None):
                        car = self.getChar()
                        if car == '*':
                            car = self.getChar()
                            if car == '/':
                                break
                estado = 1
            else:
                return Token(TipoToken.ERROR, '<' + car + '>', self.linha)


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo2.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
