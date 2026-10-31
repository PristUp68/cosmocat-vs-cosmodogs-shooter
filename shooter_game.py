#Создай собственный Шутер!

from pygame import *
from random import randint, choice
init()
font.init()

WIN_WIDTH = 960
WIN_HEIGHT = 701
FPS = 70
STEP = 3
LEVEL_EARTH = WIN_HEIGHT - 20
lost = 0
MUSIKA = ['Galactic Rap.mp3', 'Mesmerizing Galaxy Loop.mp3', 'Equatorial Complex.mp3', 'Newer Wave.mp3']

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        draw.rect(screen, (255, 0, 0), self.rect, 5)

class Rock_it(GameSprite):
    lives = 5
    pulki = sprite.Group()
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed

    def ogon(self):
        malenkaia_pulia = Bullet('pizza_png.png', self.rect.centerx, self.rect.y, 35, 40, 40)
        self.pulki.add(malenkaia_pulia)

class Zlodei(GameSprite):
    def __init__(self, filename, width, height, speed=5):
        x = randint(0 + width // 2, WIN_WIDTH - width // 2)
        y = randint(-600, - height // 2)
        super().__init__(filename, x, y, width, height, speed)
    def respawn(self):
        self.rect.x = randint(0 + self.rect.width // 2, WIN_WIDTH - self.rect.width // 2)
        self.rect.y = randint(-100, - self.rect.height // 2)
    def update(self):
        self.rect.y += self.speed
    def kill(self):
        return self.respawn()
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()



#print(backround.get_width(), '*', backround.get_height())
def main():
    okoshko = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = time.Clock()
    icon = transform.scale(image.load('image.png'), (32, 32))
    display.set_icon(icon)
    display.set_caption("miau game")
    #mouse.set_visible(0)
    backround = transform.scale(image.load('galaxy.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    okoshko.blit(backround, (0, 0))
    display.update()

    mixer.init()  #подключение музыки
    mixer.music.load(choice(MUSIKA))
    mixer.music.set_volume(0.2) #звууук
    mixer.music.play(loops=-1)
    #money = mixer.Sound('money.ogg')
    #kick = mixer.Sound('kick.ogg')

    rock_it = Rock_it('kotik.png', WIN_WIDTH // 2, WIN_HEIGHT - 50, 100, 110, 10)
    zlodeiskaia_gruppa = sprite.Group()
    for i in range(8):
        filename = choice(('sobaka.png' , 'sobaka2.png'))
        zlodeiskaia_gruppa.add(Zlodei(filename, 75, 80, 1))

    schet = 0
    font2 = font.SysFont('Verdana', 30)
    nadpis_schet = font2.render(
        f'СЧЁТ: {schet}', False, (201, 201, 201)
    )
    nadpis_jizn = font2.render(
        f'ЖИЗНИ: {rock_it.lives}', False, (254, 66, 113)
    )
    user_event = USEREVENT + 1
    time.set_timer(user_event, 500)

    game = True
    while True:
        for e in event.get():
            if e.type == QUIT:
                return
                #elif e.key == game not game:
            elif e.type == MOUSEBUTTONDOWN:
                print(e.pos)
            elif e.type == user_event:
                rock_it.ogon()
            elif not game and e.type == KEYDOWN and e.key == K_SPACE:
                rock_it.lives = Rock_it.lives
                rock_it.pulki.empty()
                for zliuka in zlodeiskaia_gruppa:
                    zliuka.respawn()
                schet = 0
                mixer.music.load(choice(MUSIKA))
                mixer.music.play(loops=-1)
                game = True
                nadpis_jizn = font2.render(
                    f'ЖИЗНИ: {rock_it.lives}', False, (254, 66, 113)
                )
                nadpis_schet = font2.render(
                    f'СЧЁТ: {schet}', False, (201, 201, 201)
                )




        if game:
            rock_it.update()
            zlodeiskaia_gruppa.update()
            rock_it.pulki.update()

            for zliuka in zlodeiskaia_gruppa:
                if zliuka.rect.y > WIN_HEIGHT:
                    rock_it.lives -= 1 
                    nadpis_jizn = font2.render(
                        f'ЖИЗНИ: {rock_it.lives}', False, (254, 66, 113)
                    )
                    zliuka.respawn()
                   
            if sprite.spritecollide(rock_it, zlodeiskaia_gruppa, True):
                rock_it.lives -= 1
                nadpis_jizn = font2.render(
                    f'ЖИЗНИ: {rock_it.lives}', False, (254, 66, 113)
                )

            sbitie = len(sprite.groupcollide(zlodeiskaia_gruppa, rock_it.pulki, True, True))
            if sbitie != 0:
                schet += sbitie
                nadpis_schet = font2.render(
                    f'СЧЁТ: {schet}', False, (201, 201, 201)
                )

            okoshko.blit(backround, (0, 0))
            okoshko.blit(nadpis_schet, (0, 0))
            okoshko.blit(nadpis_jizn, (0, 45))
            rock_it.draw(okoshko)
            zlodeiskaia_gruppa.draw(okoshko)
            rock_it.pulki.draw(okoshko)
            
            
            

            if rock_it.lives <= 0:
                game = False
                font1 = font.SysFont('Verdana', 70)
                nadpis = font1.render(
                    'GAME OVER', False, (201, 1, 55)
                )
                nadpis_rect = nadpis.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                font68 = font.SysFont('Verdana', 40)
                restart_nadpis = font68.render(
                    'нажмите SPACE чтобы начать сначала', False, (201, 201, 201)
                )
                nadpis_rect68 = restart_nadpis.get_rect(midtop=(WIN_WIDTH // 2, nadpis_rect.bottom + 100))
                okoshko.blit(nadpis, nadpis_rect)
                okoshko.blit(restart_nadpis, nadpis_rect68)
                mixer.music.fadeout(3000)



        display.update()     
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    quit()