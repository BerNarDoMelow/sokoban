from estado import Estado
from search import *
import math, random
import time
from copy import deepcopy  
class Game(Problem):
    def __init__(self,inicial,goal = None):
        super().__init__(inicial)
        self.goal = goal
        self.nos_expandidos = 0



    def actions(self,estado):
        actions = []
        percecao = estado.percept(estado.arrumador)
        if "cima" not in list(percecao.keys()) or percecao["cima"][0].nome == "o":
            actions.append("mover_cima")
    
        elif percecao["cima"][0].nome == "*":
            percecao_caixa = estado.percept(percecao["cima"][0])
            if "cima" not in list(percecao_caixa.keys()) or percecao_caixa["cima"][0].nome == "o":
                actions.append("empurra_cima")
        #########################################
        if "baixo" not in list(percecao.keys()) or percecao["baixo"][0].nome == "o":
            actions.append("mover_baixo")

        elif percecao["baixo"][0].nome == "*":
            percecao_caixa = estado.percept(percecao["baixo"][0])
            if "baixo" not in list(percecao_caixa.keys()) or percecao_caixa["baixo"][0].nome == "o":
                actions.append("empurra_baixo")
        #########################################
        if "esq" not in list(percecao.keys()) or percecao["esq"][0].nome == "o":
            actions.append("mover_esq")
        elif percecao["esq"][0].nome == "*":
            percecao_caixa = estado.percept(percecao["esq"][0])
            if "esq" not in list(percecao_caixa.keys()) or percecao_caixa["esq"][0].nome == "o":
                actions.append("empurra_esq") 
        #########################################
        if "direita" not in list(percecao.keys()) or percecao["direita"][0].nome == "o":
            actions.append("mover_direita")
        elif percecao["direita"][0].nome == "*":
            percecao_caixa = estado.percept(percecao["direita"][0])
            if "direita" not in list(percecao_caixa.keys()) or percecao_caixa["direita"][0].nome == "o":
                actions.append("empurra_direita")
        
        return actions 

    
    def result(self,state,action):
        state = deepcopy(state)
        resultante = state
        percept = state.percept(state.arrumador)
        if action == "mover_baixo":
            resultante = Estado(state.width,state.height,state.arrumador.mover_baixo(),\
                                state.local_alvos,state.local_caixas,state.local_paredes)
        elif action == "mover_cima":
            resultante = Estado(state.width,state.height,state.arrumador.mover_cima(),\
                                state.local_alvos,state.local_caixas,state.local_paredes)
        elif action == "mover_esq":
            resultante = Estado(state.width,state.height,state.arrumador.mover_esq(),\
                                state.local_alvos,state.local_caixas,state.local_paredes)
        elif action == "mover_direita":
            resultante = Estado(state.width,state.height,state.arrumador.mover_direita(),\
                                state.local_alvos,state.local_caixas,state.local_paredes)
        elif action == "empurra_baixo":
            percept = percept['baixo']
            for caixa in state.local_caixas:
                if caixa == percept[0]:
                    caixa.mover_baixo()
            resultante = Estado(state.width,state.height,state.arrumador.mover_baixo(),\
            state.local_alvos,state.local_caixas,state.local_paredes)
        elif action == "empurra_cima":
            percept = percept['cima'][0]
            for caixa in state.local_caixas:
                if caixa == percept:
                    caixa.mover_cima()
            resultante = Estado(state.width,state.height,state.arrumador.mover_cima(),\
            state.local_alvos,state.local_caixas,state.local_paredes)

        elif action == "empurra_esq":
            percept = percept['esq'][0]
            for caixa in state.local_caixas:
                if caixa == percept:
                    caixa.mover_esq()
            resultante = Estado(state.width,state.height,state.arrumador.mover_esq(),\
            state.local_alvos,state.local_caixas,state.local_paredes)

        elif action == "empurra_direita":
            percept = percept['direita'][0]
            for caixa in state.local_caixas:
                if caixa == percept:
                    caixa.mover_direita()
            resultante = Estado(state.width,state.height,state.arrumador.mover_direita(),\
            state.local_alvos,state.local_caixas,state.local_paredes)
        self.nos_expandidos+=1   
        #print(resultante)
        return resultante
    

    def goal_test(self,estado):
        ##E preciso deepcopy
        alvos = deepcopy(estado.local_alvos)
        for caixa in estado.local_caixas:
            for alvo in estado.local_alvos:
                if self.equals(caixa,alvo):
                    alvos.remove(alvo)
        return len(alvos) == 0
            
    def equals(self,caixa,alvo):
        return caixa.width == alvo.width and caixa.height == alvo.height

    def path_cost(self,c,state1,action,state2):
        return 1 if "empurra" in action else 2

    def h1(self,no):
        valor_h = 0
        for each_caixa in no.state.local_caixas:
            lista = []
            dist_alvo = 0
            for each_alvo in no.state.local_alvos:
                nova_dist_alvo = math.sqrt((each_caixa.width-each_alvo.width)**2 + (each_caixa.height-each_alvo.height)**2)
                lista.append(nova_dist_alvo)
            valor_h += min(lista)
        return valor_h
            


    def h2(self,no):
        """
        Esta heuristica desvaloriza por cada caixa que esta no canto
        """
        valor_h = 0
        for each in no.state.local_caixas:
            if no.state.in_corner(each):
                valor_h+=1
        return valor_h


    def h3(self,no):
        """
        Valoriza o que tiver menor distancia entre o arrumador e a primeira caixa que esta state.local_caixas
        """
        caixas = no.state.local_caixas
        lista = []
        arrumador = no.state.arrumador
        for caixa in caixas:
            lista.append(math.sqrt((caixa.width-arrumador.width)**2 + (caixa.height-arrumador.height)**2))
        return min(lista)

    def h4(self,no):
        h1 = self.h1(no)
        h1+= self.h2(no)
        
        return h1
        
        
###############################
from things import *
def examples(filename):
    local_paredes = []
    local_alvos = []
    local_caixas = []
    local_arrumador = Arrumador((0,0))
    x = 0
    with open(filename,'r') as fich:
        mapa = fich.readlines()
        y = len(mapa)   
        for each_line in mapa:
            x = 1
            for each in each_line:
                if each == "#":
                    local_paredes.append(Parede((x,y)))
                elif each == 'o':
                    local_alvos.append(Alvo((x,y)))
                elif each == 'A':
                    local_arrumador = Arrumador((x,y))
                elif each == '*':
                    local_caixas.append(Caixa((x,y)))
                x+=1
            y-=1

    width = x
    height = width


    return {'width':width,'height':height,'local_arrumador':local_arrumador,'local_caixas':local_caixas,\
                'local_alvos':local_alvos,'local_paredes':local_paredes}


#######A ir buscar ao ficheiro   
example = examples('puzzle1.txt')
local_alvos = example['local_alvos']
parede = example['local_paredes']
arrumador = example['local_arrumador']
local_caixas = example['local_caixas']
width = example['width']
height = example['height']
###########
#########Teste
#local_alvos = [Alvo((0,2)),Alvo((1,2))]
#parede = []
#arrumador = Arrumador((2,2))
#local_caixas = [Caixa((4,2))]

#width = 5
#height = 5
#############
amb = Estado(width,height,arrumador,local_alvos,local_caixas,parede)
game = Game(amb)
tempo_inicial = time.time()
#res = depth_first_tree_search(game)
#res = depth_first_graph_search(game)
#res = uniform_cost_search(game)
#res = breadth_first_search(game)
#res = iterative_deepening_search(game)
#res = depth_limited_search(game,1)
res = best_first_graph_search(game,game.h2)
#res = best_first_graph_search(game,game.h3)
#res = astar_search(game,game.h3)
print(res.solution())
#Para correr tem descomentar o algoritmo que quer



