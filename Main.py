import random
import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


# Definindo as dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600


movimentoHorizontal = 2.5


# Parâmetros da nave
nave_tamanho = 0.8
nave_x, nave_y = 0.0, -1.5
nave_velocidade = 0.05


# Parâmetros dos inimigos
inimigos = []
num_inimigos = 3
inimigo_tamanho = 0.6
inimigo_velocidade = 0.02
inimigo_direcao = 1


# Parâmetros dos tiros
tiros = []
tiro_velocidade = 0.1
tiro_tamanho = 0.1


# Parâmetros das partículas
particulas = []


# Inicializando a lista de inimigos
for i in range(num_inimigos):
    inimigos.append([i * 1 - 1, 1.4])


# Função para carregar a textura
def carregar_textura(caminho_imagem):
    imagem = pygame.image.load(caminho_imagem)
    imagem = pygame.transform.flip(imagem, True, False)
    dados_imagem = pygame.image.tostring(imagem, "RGBA", 1)
    largura, altura = imagem.get_size()

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados_imagem)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return textura_id


# Inicializando o pygame e a janela
pygame.init()
display = (LARGURA_TELA, ALTURA_TELA)
pygame.display.set_caption("Space Invaders")
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluPerspective(45, (LARGURA_TELA / ALTURA_TELA), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)


# Configurando a fonte de luz
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
light_position = [1.0, 1.0, 1.0, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [0.0, 0.0, 0.0, 0.0]
glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


# Configurando o material para a nave
material_diffuse = [1.0, 1.0, 1.0, 1.0]
material_specular = [1.0, 1.0, 1.0, 1.0]
material_shininess = [50.0]
glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)


# Carregando a textura da nave
textura = carregar_textura("nave.png")  


glEnable(GL_TEXTURE_2D)


# Função para desenhar a nave
def desenhar_nave():
    glPushMatrix()
    glTranslatef(nave_x, nave_y, 0.0)
        
    glBindTexture(GL_TEXTURE_2D, textura)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-nave_tamanho / 2, -nave_tamanho / 2, 0.0)
    glTexCoord2f(1, 0); glVertex3f(nave_tamanho / 2, -nave_tamanho / 2, 0.0)
    glTexCoord2f(1, 1); glVertex3f(nave_tamanho / 2, nave_tamanho / 2, 0.0)
    glTexCoord2f(0, 1); glVertex3f(-nave_tamanho / 2, nave_tamanho / 2, 0.0)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    glPopMatrix()


# Função para desenhar inimigos 3D sem textura
def desenhar_inimigos_3d():

    for inimigo in inimigos:
        glPushMatrix()
        glTranslatef(inimigo[0] + inimigo_tamanho / 2, inimigo[1] - inimigo_tamanho / 2, 0.0)  
        glBegin(GL_QUADS)

        # Frente
        glVertex3f(-inimigo_tamanho / 2, -inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, -inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(-inimigo_tamanho / 2, inimigo_tamanho / 2, inimigo_tamanho / 2)

        # Trás
        glVertex3f(-inimigo_tamanho / 2, -inimigo_tamanho / 2, -inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, -inimigo_tamanho / 2, -inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, inimigo_tamanho / 2, -inimigo_tamanho / 2)
        glVertex3f(-inimigo_tamanho / 2, inimigo_tamanho / 2, -inimigo_tamanho / 2)

        # Laterais
        glVertex3f(-inimigo_tamanho / 2, -inimigo_tamanho / 2, -inimigo_tamanho / 2)
        glVertex3f(-inimigo_tamanho / 2, -inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(-inimigo_tamanho / 2, inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(-inimigo_tamanho / 2, inimigo_tamanho / 2, -inimigo_tamanho / 2)

        glVertex3f(inimigo_tamanho / 2, -inimigo_tamanho / 2, -inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, -inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, inimigo_tamanho / 2, inimigo_tamanho / 2)
        glVertex3f(inimigo_tamanho / 2, inimigo_tamanho / 2, -inimigo_tamanho / 2)

        glEnd()
        glPopMatrix()


# Função para mover os inimigos
def mover_inimigos():
    global inimigo_direcao
    for inimigo in inimigos:
        inimigo[0] += inimigo_velocidade * inimigo_direcao
    for inimigo in inimigos:
        if inimigo[0] <= -movimentoHorizontal or inimigo[0] + inimigo_tamanho >= movimentoHorizontal:
            inimigo_direcao *= -1


# Função para disparar tiros
def disparar_tiro():
    tiros.append([nave_x, nave_y + nave_tamanho / 2])


# Função para mover os tiros
def mover_tiros():
    global tiros
    for tiro in tiros[:]:
        tiro[1] += tiro_velocidade
        if tiro[1] > 2: 
            tiros.remove(tiro)


# Função para verificar colisão entre tiros e inimigos
def verificar_colisao():
    global inimigos, tiros, particulas
    for tiro in tiros[:]:
        for inimigo in inimigos[:]:
            distancia = math.sqrt((tiro[0] - inimigo[0]) ** 2 + (tiro[1] - inimigo[1]) ** 2)

            if distancia < (inimigo_tamanho / 2 + tiro_tamanho / 2):
                inimigos.remove(inimigo)
                tiros.remove(tiro)
                gerar_particulas(tiro[0], tiro[1])  


# Função para gerar partículas com direções aleatórias
def gerar_particulas(x, y):
    for _ in range(50):  
        particulas.append([x, y, random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)])


# Função para desenhar as partículas
def desenhar_particulas():
    for particula in particulas[:]:
        particula[0] += particula[2]  
        particula[1] += particula[3]  
        
        particula[2] *= 0.98  
        particula[3] *= 0.98  

        glPushMatrix()
        glTranslatef(particula[0], particula[1], 0.0)
        glPointSize(5.0)  
        glBegin(GL_POINTS)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()
        glPopMatrix()


# Função para desenhar os tiros
def desenhar_tiros():
    for tiro in tiros:
        glPushMatrix()
        glTranslatef(tiro[0], tiro[1], 0.0)
        glBegin(GL_QUADS)
        glVertex3f(-tiro_tamanho / 2, -tiro_tamanho / 2, 0.0)
        glVertex3f(tiro_tamanho / 2, -tiro_tamanho / 2, 0.0)
        glVertex3f(tiro_tamanho / 2, tiro_tamanho / 2, 0.0)
        glVertex3f(-tiro_tamanho / 2, tiro_tamanho / 2, 0.0)
        glEnd()
        glPopMatrix()


# Função principal de controle
def jogo():
    global nave_x, nave_y, tiros
    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    disparar_tiro()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > -movimentoHorizontal + nave_tamanho / 2:
            nave_x -= nave_velocidade
        if teclas[pygame.K_RIGHT] and nave_x < movimentoHorizontal - nave_tamanho / 2:
            nave_x += nave_velocidade

        mover_inimigos()

        mover_tiros()

        verificar_colisao()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        desenhar_nave()
        desenhar_inimigos_3d()
        desenhar_tiros()
        desenhar_particulas()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Inicia o jogo
jogo()
