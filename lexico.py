"""
Nome Discente: Thomas Santos Pollarini
Matrícula: 0064232
Data: 19/11/2023


Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

Código responsável pela parte lexica do compilador, ele lê o arquivo e faz a separação dos TOKENS.

"""

from os import path

class TipoToken:
    PROGRAM = (1, 'program')        #cria os TOKENS utilizados na gramática
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
    def __init__(self, tipo, lexema, linha):  #classe utilizada para armazenar TOKEN
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
            
    def is_alpha(self,car):   #funcao para pegar letras aceitas pela gramática
        return 'A' <= car <= 'Z' or 'a' <= car <= 'z'

    def is_digit(self,car):   #funcao para pegar digitos aceitas pela gramática
        return '0' <= car <= '9'

    def is_alnum(self,car):  #funcao para pegar letras e digitos aceitas pela gramática
        return self.is_alpha(car) or self.is_digit(car)

    # retorna o proximo caracter do arquivo
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

    # retorna o ultimo caracter lido para o arquivo
    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    # retorna o proximo token do arquivo
    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)  #se car está vazio, então retorna token fim de arquivo
                elif car in {' ', '\t', '\n'}:   #ignora espaços
                    if car == '\n':
                        self.linha = self.linha + 1
                elif self.is_alpha(car):   #se car começar com letra manda para estado 2, tratamento de ID
                    estado = 2
                elif self.is_digit(car):  #se car começar com digito manda para estado 3, tratamento de CTE
                    estado = 3
                elif car in {'+','-'}:  # se + ou -, verifica se proximo car é digito
                    aux = self.getChar()    
                    if self.is_digit(aux):  # se for digito manda para estado 3, tratamento de CTE
                        self.ungetChar(aux)
                        estado=3  
                    else:                    #caso contrario manda para estado 4, tratamento de caracteres especiais
                        self.ungetChar(aux)
                        estado=4
                elif car in {'=', ';','*', '(', ')','<','>','!','{','}',':',',','\"'}: 
                    estado = 4            #caso encontre um dos caracteres acima manda para estado 4
                elif car == '/':          
                    car = self.getChar()    #caso encontre barra verifica caso dos comentarios
                    if car == '/' or car == '*':
                        estado=5        #se for comentario manda para estado 5, tratamento de comentarios
                    else:
                        self.ungetChar(car) #caso contrario, manda para estado 4
                        car='/' #recoloca / no car para comparação no estado 4
                        estado=4
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha) #não entrar em nenhum caso caracter não faz parte
            elif estado == 2:                                                  # da gramática, retorna um TOKEN ERRO
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()   
                if car is None or (not self.is_alnum(car)):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:           #verifica se é uma palavra reservada
                        return Token(Lexico.reservadas[lexema], lexema, self.linha) 
                    else:
                        if len(lexema)>32:                  #senão é um ID, caso tenha mais de 32 caracters retorna TOKEN ERRO
                            return Token(TipoToken.ERROR, '<' + lexema + '>', self.linha)
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car == '.' and '.' not in lexema:  #tratemento para aceitar numeros reais
                    continue
                if car is None or (not self.is_digit(car)):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.CTE, lexema, self.linha)

            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':               #em caso de =, >, < verifica proximo car, para pegar ==, >=,<=, <>
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
                    while (not car is None) and (car != '\n'):    #emm caso de comentario de linha, anda até \n
                        car = self.getChar()
                else:
                    while (not car is None):    #em caso de comentario em bloco anda até achar */
                        car = self.getChar()
                        if car == '*':
                            car = self.getChar()
                            if car == '/':
                                break
                estado = 1 #no fim retorna para estado 1, pois nenhum token foi encontrado até então
            else:
                return Token(TipoToken.ERROR, '<' + car + '>', self.linha)


if __name__== "__main__":

   nome = input("Entre com o nome do arquivo: ")
   #nome = 'exemplo1.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

    # le todos os tokens do arquivo e imprime na tela
   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
