import arcade
from bombas.bomba import Bomba

class Player(arcade.Sprite):
    def __init__(self,arquivo,escala=0.06,velocidade=5,x=0,y=0,bombas=1,forca=1,c=arcade.key.W,b=arcade.key.S,d=arcade.key.D,e=arcade.key.A,bomb=arcade.key.SPACE,ganhou=None,limite_imortal=3.0):
        super().__init__(arquivo,scale=escala,center_x=x,center_y=y)
        self.num_bombas = bombas
        self.forca = 1
        self.velocidade = velocidade
        self.imortal = False
        self.tempo_imortal = 0.0
        self.limite_imortal = limite_imortal
        self.cima = False
        self.baixo = False
        self.esquerda = False
        self.direita = False
        self.c = c
        self.b = b
        self.d = d
        self.e = e
        self.bomb = bomb
        self.plantado = False
        self.som = arcade.sound.load_sound("sound/down.wav")
        self.ganhou = ganhou
        self.vento = 0
        self.fogo = 0
        self.macaco = False
        self.capacete = False

    def mover(self):
        self.change_x = 0
        self.change_y = 0
        if self.cima and not self.baixo:
            self.change_y += self.velocidade
        if self.baixo and not self.cima:
            self.change_y -= self.velocidade
        if self.esquerda and not self.direita:
            self.change_x -= self.velocidade
        if self.direita and not self.esquerda:
            self.change_x += self.velocidade

    def on_key_press(self,key,key_modifiers):
        if key == self.c:
            self.cima = True
        if key == self.b:
            self.baixo = True
        if key == self.d:
            self.direita = True
        if key == self.e:
            self.esquerda = True
        if key == self.bomb and self.num_bombas > 0:
            return True
            
    
    def on_key_release(self,key,key_modifiers):
        if key == self.c:
            self.cima = False
        if key == self.b:
            self.baixo = False
        if key == self.d:
            self.direita = False
        if key == self.e:
            self.esquerda = False

    def plantar_bomba(self):

        pos_x = ((self.center_x // 32) * 32) + 16 
        pos_y = ((self.center_y // 32) * 32) + 16
        bomba = Bomba(0.5, x= pos_x, y= pos_y, forca=self.forca, player=self, limite=3)
        self.num_bombas -= 1
        return bomba
        
    def evitar_fuga(self,largura,altura):
        if self.left < 0:
            self.left = 0
        if self.right > largura:
            self.right = largura-1
        if self.top > altura:
            self.top = altura-1
        if self.bottom < 0:
            self.bottom = 0
    
    def set_num_bombas(self,num_bombas):
        self.num_bombas = num_bombas

    def verificar_sobrevivencia(self,delta_time):
        perdeu = None
        if self.capacete:
            self.imortal = True
            self.capacete = False
        else:
            #print(self.imortal)
            if not self.imortal:
                arcade.sound.play_sound(self.som)
                self.ganhou = False
                perdeu = self.ganhou
                self.kill()
            else:
                #self.atualizar_imortal(delta_time),
                if self.tempo_imortal >= self.limite_imortal:
                    self.tempo_imortal = 0.0
                    self.imortal = False
                else:
                    self.tempo_imortal += delta_time
        return perdeu

    def atualizar_imortal(self,delta_time):
        self.tempo_imortal += delta_time
        if self.tempo_imortal >= self.limite_imortal:
            self.tempo_imortal = 0.0
            self.imortal = False
    