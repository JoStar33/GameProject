import pygame

pygame.init() #초기화

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Hello Game") #게임이름

background = pygame.image.load("C:/Users/Hose/Desktop/gogo.png")

#이벤트 루프
running = True
while running:
    for event in pygame.event.get(): #이벤트 체크. 마우스에 대해서
        if event.type == pygame.QUIT: #X버튼을 통해 게임을 종료할때에
            running = False
    #screen.fill((0, 0, 255)) 임의로 배경색 설정 가능.
    screen.blit(background, (0, 0)) #배경 그리기
    pygame.display.update() #게임화면을 다시 그리기

#파이게임 종료
pygame.quit()