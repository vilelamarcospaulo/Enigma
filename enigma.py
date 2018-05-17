#REPRESENTA UM ROTOR DA MAQUINA
class Rotor:
    def __init__(self, Key, StartAt=0):
        #VETOR DE CHAVE
        self.Key = Key
        #POSICAO ATUAL DO VETOR
        self.Pos = StartAt
        #INDICADOR SE JÁ HOUVE ALGUMA ROTAÇÃO
        self.IndRotate = False
        #Tamanho do alfabeto
        self.N = len(self.Key)

    #Movimenta o ponteiro uma casa para frente
    def Rotate(self):
        #indicador de que houve uma rotação
        self.IndRotate = True
        #ROTACIONAR O ROTOR É ADICIONAR 1 AO PONTEIRO DA CHAVE.
        #utilizamos '% len(self.Key)' pois a chave tem o mesmo tamanho que o alfabeto
        self.Pos =  (self.Pos + 1) % self.N

    #Recebe o simbolo a ser criptografado
    #e um marcador indicando se deve ou não rotacionar após a cifra
    #Retorna o resultado da cifra
    def cipher(self, Symbol, Rotate=True):
        #sempre indica que nao houve rotação, caso haja o metodo self.Rotate() irá atualizar
        #esse valor
        self.IndRotate = False

        #A cada rotação é subtraido 1 de toda a chave e também a chave atual passa a ser a ultima
        #equivalente a isso é dizer que com o vetor fixo,
        #na rotação 'r' a chave correspontende sera (self.key[(entrada + r)%alfabeto] - r) % alfabeto
        #self.Key[(entrada + r)%alfabeto], essa parte da equação garante que a cada 'rotação' o indice será redirecionado ao proximo
        # - r, garante que a cada rotação o valor correspondende é reajustado
        
        #A variavel self.Pos contem a posição atual do ponteiro que é o mesmo que o numero de rotações
        result = (self.Key[(Symbol + self.Pos) % self.N] - self.Pos) % self.N
        
        #SE FOR SOLICITADO QUE FAÇA UMA ROTAÇÃO
        if Rotate:
            self.Rotate()
            
        return result

    def decipher(self, Symbol, Rotate=True):
        self.IndRotate = False

        result = (self.Key.index((Symbol + self.Pos) % self.N) - self.Pos) % self.N 
        if Rotate:
            self.Rotate()

        return result

    #Retorna se esse rotor fechou um ciclo NA ULTIMA ROTAÇÃO
    #Um ciclo acontece quando já houve alguma rotação e a posição atual é 0
    def cycle(self):
        return self.IndRotate and self.Pos == 0

#REPRESENTA A MAQUINA ENIGMA EM SI
class Enigma:
    def __init__(self, Rotors, AlphabetLength):
        self.Rotors = Rotors
        self.AlphabetLength = AlphabetLength

        for r in Rotors:
            assert len(r.Key) == self.AlphabetLength
        
    def cipher(self, Symbol):
        if len(self.Rotors) <= 0: 
            return

        #Entrada passa pelo primeiro rotor, com o parametro padrao de rotaçãp
        ciphered = self.Rotors[0].cipher(Symbol)
        #Para os proximos rotores passa a cifra em cascada, passando como parametro de rotação
        #Se o rotor anterior deve uma rotação
        for i in range(1, len(self.Rotors)):
            ciphered = self.Rotors[i].cipher(ciphered, self.Rotors[i - 1].cycle())

        return ciphered

    def decipher(self, Symbol):
        if len(self.Rotors) <= 0: 
            return
        
        #Entra o simbolo no ultimo rotor, com o indicador de não rotação
        deciphered = self.Rotors[len(self.Rotors) - 1].decipher(Symbol, len(self.Rotors) == 1) 
        #Entra o resultado em cascada nos rotores no sentido inverso
        # 'i == 0' faz com que apenas o primeiro rotor gire
        for i in range(len(self.Rotors) - 2, -1, -1):
             deciphered = self.Rotors[i].decipher(deciphered, i == 0)  

        #propaga as rotações no sentido correto, como o primeiro rotor ja foi solicitado
        #a rotação no laço anterior, não é feita a rotação desse novamente.
        for i in range(1, len(self.Rotors)):
            if(self.Rotors[i - 1].cycle()):
                self.Rotors[i].Rotate()

        return deciphered

def teste1():
    print("TESTE 1")
    key = [[4, 2, 8, 0, 6, 5, 3, 1, 7, 9]]

    machineE = Enigma([Rotor(key[0])], 10)
    machineD = Enigma([Rotor(key[0])], 10)

    word = [0]*5

    encrypted = [machineE.cipher(letter) for letter in word] # Palavra encriptada
    decrypted = [machineD.decipher(letter) for letter in encrypted] # Palavra decriptografada

    print (encrypted)
    print (decrypted)

    assert word == decrypted # Confere se a palavra original é igual a palavra decriptografada
    print("------------------------")
    #SAIDA
    #[4, 1, 6, 7, 2]
    #[0, 0, 0, 0, 0]


def teste2():
    print("TESTE 2")
    ##
    ##TESTE COM TRÊS ROTORES, AS SEGUITES CHAVES COMEÇANDO COM DESLOCAMENTOS 5,3 e 4
    key = [[5, 6, 1, 8, 2, 0, 7, 3, 4, 9], 
        [9, 3, 8, 5, 0, 6, 1, 2, 4, 7],
        [7, 9, 5, 8, 0, 1, 2, 4, 3, 6]]

    #Define a maquina usada para ciframento e deciframento ambas devem ser iguais
    #Não pode ser a mesma para não haver duplicação nas rotações

    machineE = Enigma([Rotor(key[0], 5), Rotor(key[1], 3), Rotor(key[2], 4)], 10)
    machineD = Enigma([Rotor(key[0], 5), Rotor(key[1], 3), Rotor(key[2], 4)], 10)

    word = [0,1,2,3,4,5,6,7,8,9] #Palavra a ser criptografada

    encrypted = [machineE.cipher(letter) for letter in word] #Palavra encriptada
    decrypted = [machineD.decipher(letter) for letter in encrypted] #Palavra decriptografada

    assert word == decrypted #Confere se a palavra original é igual a palavra decriptografada

    print(encrypted)
    print(decrypted)
    #SAIDA
    #[7, 3, 0, 6, 2, 3, 5, 4, 1, 6]
    #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

teste1()
teste2()
