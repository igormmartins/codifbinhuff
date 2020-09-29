

#=================================================================
#Biblioteca para codificação/descodificação de binários em Huffman
#Codification/decodification library for Huffman binaries
#=================================================================


try:
    #Tenta importar a árvore de huffman presente no arquivo arvore.py
    from arvore import *
except:
    #Caso não cosiga importar...
    decarvore = False #Diz para as fuções desta biblioteca que algo deu errado
    codarvore = False
    print("Erro(codifbinuniv): O arquivo arvore.py não existe, ou esta em outro diretório!\nGere-o ou execute este programa no diretório adequado!") #E imprime esta mensagem de erro



#Função que decodifica um dado binário na arvore de huffman
def parcdec(bit, decarvore):
    if bit in decarvore: #Tenta encontrar alguma correspondência na árvore
        return(decarvore[bit],len(bit)) #Caso encontre, a retorna
    return(False) #Se não conseguir decodificar, diz para as fuções dependentes que não foi possível decodificar



#Função que decodifica/descomprime uma string binária para texto
def decodifica(entrada, decarvore = decarvore, rec1=False, rec2=False):
    if decarvore == False: #Caso não consiga importar a arvore
        print("Erro(codifbinuniv): O arquivo arvore.py não existe!\nGere-o com gerarhuff.py!")
        return(False) #Encerra a função dizendo para as funções dependentes que algo deu errado
    
    listabit = list(entrada) #Transforma a string de entrada em uma lista
    if len(listabit) == 0: #Se a entrada for nula
        return(False) #Retorna False
    
    tentativa = 0 #Contador de tentativas
    caracterebin = listabit[0] #Associa à variavel o primeiro bit da entrada
    caractere = 1 #Contador dos caracteres da entrada, começa em 1 devido à linha anterior. Esta variavel separa os bits que já foram decodificados dos que ainda não foram
    saida = [] #Lista de saída
    
    try: #Tenta decodificar
        while caractere <= len(listabit): #Enquanto a soma dos bits equivalentes aos caracteres decodificados percorridos for menor que a lista dos bits de entrada rode:
                if parcdec(caracterebin, decarvore) == False: #Onde a tentativa ocorre e se der errado...
                    caracterebin = caracterebin+listabit[tentativa+caractere] #Obtém mais um bit seguinte da entrada e tenta novamente decodificar
                    tentativa = tentativa+1
                else: #Se der certo...
                    caracdecodif = parcdec(caracterebin, decarvore) #Obtém o caractere decodificado e a quantidade dos bits do caractere decodificado
                    saida.append(caracdecodif[0]) #Coloca o caractere obtido na lista
                    ulttamanbit = caracdecodif[1] #Obtém a quantidade de bits que o caractere decodificado possui na árvore
                    if tentativa+caractere < len(listabit): #Se ainda tem bits a serem decodificados...
                        caracterebin = listabit[tentativa+caractere] #Associa o próximo bit do próximo caractere à variavel
                    tentativa = 0 #Zera as tentativas
                    caractere = caractere+ulttamanbit #Coloca o inicio da próxima tentativa de decodificação no primeiro que ainda não foi decodificado da lista de etrada
    except: #Se não conseguir decodificar... Aplica um método semelhante ao 'registry shift' a fim de se apagar o primeiro bit da mensagem corrompida e tentar novamente decodificar
        if rec1 == False and rec2 == False: #Verifica se esta função foi chamada dentro da recursividade, a fim de se evitar loops infinitos e informar uma mensagem de ero mais precisa
            print("Erro(codifbinuniv.decodifica): Não há correspondência na árvore! Tentando modo forçado...",end='') #Imprime a mensagem de erro
            nvlistabit = list(caracterebin) #Transforma em lista os bits que não encontraram seu significado
            while len(nvlistabit) > 1: #Enquanto houver bits pra tentar decodificar, rode...
                if decodifica(''.join(nvlistabit),decarvore,True) == False: #tenta decodificar, onde a tentativa ocorre e se der errado...
                    del nvlistabit[0] #Apaga o primeiro bit da lista e tenta novamente
                else: #Se der certo:
                    try: #Há a possibilidade de a string de bits ainda conter erros, por isto tente associar a saida da função a 2 variaveis
                        stringtemp , caracterebintemp  = decodifica(''.join(nvlistabit),decarvore, rec2=True) #o return que devolve estas 2 variaveis se encontra abaixo
                    except: #Se não der certo, não há erros na string de bits
                        stringtemp  = decodifica(''.join(nvlistabit),decarvore, rec2=True) #Então associe apenas uma variavel à saída da função
                    saida.append(stringtemp) #Adiciona-o à saida
                    print(" Sucesso!",end='') #Caso o método consiga encontrar alguma correspondência na árvore, imprima isto
                    sucesso = True #Esta variavel iforma se houve sucesso ao tentar a decodificação forçada. Serve apenas para a organização dos prints das mensagens de erro na tela
                    ahe = True #Esta variavel, assim como a anterior, orgaiza a mensagem de erro, pois algumas terminal com end='', que não pula linha
                    break #Esta rotina so pode ser executada uma única vez. Caso contrário a recursividade cria um loop infinito; além de não haver necessidade de repetir esta tentativa ja que este loop while removeu os primeiros bits que foram recebidos errados
            if decodifica(''.join(nvlistabit),decarvore,True,True) == False: #Caso não encontre nenhuma correspondência
                print(" Tentativa falhou.") #Imprima isto
                ahe = False #Este print não termina com o end=''
            try: #Se existe a variavel caracterebintemp
                if len(caracterebintemp) != 0: #E esta for diferente de 0
                    print(" Ainda sim, erros foram encontrados.") #Houve algum bit desencotrado em que não ha correspondência na árvore, e esta mesagem é exibida
                    ahe = False #Este print tambem não termina com o end=''
            except: #Se não existir
                pass #Ignore
            if ahe and sucesso: #Verifica se o ultimo print termina com end='', a fim de...
                print("") #Terminar a linha e iniciar uma nova, para não escrever mais nada na mesma linha
        if saida == []: #Se a lista de saida estiver vazia:
            return(False) #Retorne False
        else: #Caso contrário:
            string = ''.join(saida) #Agrupa o que já foi decodificado
            if rec1 == True or rec2 == True: #E se estiver sendo executado em modo recursivo
                return(string,caracterebin) #Retorna o texto e o binário que não pode ser decodificado, em caso de erro
            else: #Caso contrário:
                return(string)  #Retorna o texto

    string = ''.join(saida) #Se a codificação ocorrer como o esperado, agrupa a saída e...
    return(string) #A retorna



#Função que cofdifica dada string para binário utilizando a árvore importada
def codifica(entrada, codarvore = codarvore):
    if codarvore == False: #Caso não consiga importar a árvore
        print("Erro(codifbinuniv): O arquivo arvore.py não existe!\nGere-o com gerarhuff.py!")
        return(False) #Encerra a função dizendo para as funções dependentes que algo deu errado
    
    listent = list(entrada)
    bits = [] #Cria uma lista vazia para guardar os bits de saída
    erros = [] #Cria uma lista vazia para guardar os caracteres que não constam na árvore para a codificação

    for ent in listent: #Percorre a entrada
        if (ent in codarvore): #Se a entrada esta contida na arvore...
            bits.append(codarvore[ent]) #Adicione-a à lista
        else: #Caso contrário...
            erros.append(ent) #Adicione-a à lista de caracteres não suportados
    
    if erros == []: #Se não houve erros...
        pass #Não faça nada
    else: #Caso contrário...
        cnc = [] #Cria uma lista vazia a fim de remover as repetições de caracteres não suportados
        for errc in erros: #Percorre a lista contendo os erros
            if errc in cnc: #Se a lista cnc(caractere não consta) já contem o caractere não suportado...
                pass #Não faça nada
            else: #Caso contrário...
                cnc.append(errc) #Adicione-o à lista de erros

        print("\nAlerta(codifbinuniv.codifica): Caracter(es) ({}) não consta(m) na arvore de codificação.\nIgnorando...".format(','.join(cnc))) #Imprime a mensagem de erro informando os caracteres não suportados
    if bits == []: #Se nada foi codificado
        return(False) #Encerra a função dizendo para as funções dependentes que algo deu errado
    else: #Caso contrário
        binstr = ''.join(bits) #Agrupa a saída e...
        return binstr #A retorna