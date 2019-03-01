
###METER ESTADO __INIT__ LOGO COM AS CLASSES THINGS
from things import *

class Estado:
    def __init__(self,width,height,local_arrumador,local_alvos,local_caixas,local_paredes):
        ###
        self.width = width
        self.height = height
        self.local_caixas = local_caixas
        self.local_alvos = local_alvos
        self.arrumador = local_arrumador
        self.local_paredes = local_paredes
        self.tudo = self.local_caixas+self.local_alvos+self.local_paredes+[self.arrumador]
    
    def in_corner(self,thing):
        percept = self.percept(thing)
        try:   
            assert percept['cima'][0].nome and percept["esq"][0].nome == "#"
            return True
        except:
            pass
        ###################
        try:
            assert percept['cima'][0].nome and percept['direita'][0].nome == "#"
            return True
        except:
            pass
        ###################
        try:
            assert percept['baixo'][0].nome and percept['esq'][0].nome == "#"
            return True
        except:
            pass
        ###################
        try:
            assert percept['baixo'][0].nome and percept['direita'][0].nome == "#"
            return True
        except:
            pass
        ###################
        return False

            
    def percept(self,agent):
        things = {}
        cima = False
        baixo = False
        esq = False
        direita = False
        for thing in self.tudo:
            if thing.width == agent.width and thing.height == agent.height+1:
                if cima is False:
                    things["cima"] = [thing]
                    cima = True
                else:
                    things["cima"].append(thing)
    
            if thing.width == agent.width and thing.height == agent.height-1:
                if baixo is False:
                    things["baixo"] = [thing]
                    baixo = True
                else:
                    things["baixo"].append(thing)
            
            if thing.width == agent.width-1 and thing.height == agent.height:
                if esq is False:
                    things["esq"] = [thing]
                    esq = True
                else:
                    things["esq"].append(thing)
            
            if thing.width == agent.width+1 and thing.height == agent.height:
                if direita is False:
                    things["direita"] = [thing]
                    direita = True
                else:
                    things["direita"].append(thing)
                   
        return things

    def __lt__(self,estado):
        return self.arrumador < estado.arrumador and self.local_caixas < estado.local_caixas
    
    def __eq__(self,estado):
        return self.local_caixas == estado.local_caixas and self.arrumador == estado.arrumador
    
    def __hash__(self):
        caixas = ()
        for each in self.local_caixas:
            caixas+=(each.width,each.height)
        return hash((self.arrumador.width,self.arrumador.height,caixas))
        
    def __str__(self):
        s = ""
        for j in range(self.height,0,-1):
            for i in range(1,self.width):
                lista = []
                for each in self.tudo:
                    if each.width == i and each.height == j:
                        lista.append(each.nome)
                if len(lista) == 0:
                    s+=" . "
                elif len(lista) == 1:
                    s+=" "+str(lista[0])+" "
                else:
                    if "o" in lista and "*" in lista:
                        s+=" @ "
                    elif "o" in lista and "A" in lista:
                        s+=" B "
                
            s+="\n"
            
        return s



