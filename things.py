from agents import Agent,Thing

class Arrumador(Agent):
    def __init__(self,posicao):
        self.width = posicao[0]
        self.height = posicao[1]
        self.nome = "A"
        
    def mover_baixo(self):
        return Arrumador((self.width,self.height-1))
    
    def mover_cima(self):
        return Arrumador((self.width,self.height+1))
    
    def mover_esq(self):
        return Arrumador((self.width-1,self.height))
    
    def mover_direita(self):
        return Arrumador((self.width+1,self.height))

    def __lt__(self,agent):
        return self.width <= agent.width and self.height < agent.height\
               or self.width < agent.width and self.height <= agent.height

    def __eq__(self,state):
        return self.width == state.width and self.height == state.height
    
    def __repr__(self):
        return "A"

class Caixa(Thing):
    def __init__(self,local):
        self.width = local[0]
        self.height = local[1]
        self.nome = "*"
        
    def mover_baixo(self):
        #return Caixa((self.width,self.height-1))
        self.height-=1
    def mover_cima(self):
        self.height+=1
    
    def mover_esq(self):
        self.width-=1
    
    def mover_direita(self):
        self.width+=1

    def __lt__(self,agent):
        return self.width <= agent.width and self.height < agent.height\
               or self.width < agent.width and self.height <= agent.height

    def __eq__(self,state):
        return self.width == state.width and self.height == state.height

    def __repr__(self):
        return "*"

class Alvo(Thing):
    def __init__(self,posicao):
        self.width = posicao[0]
        self.height = posicao[1]
        self.nome = "o"

    def __eq__(self,state):
        return self.width == state.width and self.height == state.height
      
    def __repr__(self):
        return "o"
    

class Parede(Thing):
    def __init__(self,posicao):
        self.width = posicao[0]
        self.height = posicao[1]
        self.nome = "#"

    def __eq__(self,state):
        return self.width == state.width and self.height == state.height
        
    def __repr__(self):
        return "#";


