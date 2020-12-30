import pygame

pygame.init() #초기화

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Hello Game") #게임이름

#배경 이미지 불러오기
background = pygame.image.load("C:/Users/Hose/Desktop/gogo.png")

#캐릭터 불러오기
character = pygame.image.load("C:/Users/Hose/Desktop/character.png")
character_size = character.get_rect().size #이미지 크기를 구해온다.
character_width = character_size[0] #캐릭터 가로크기
character_height = character_size[1] #캐릭터 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치.
character_y_pos = screen_height - character_height  #화면 세로 크기 가장 아래에 해당하는 곳에 위치.


#이벤트 루프
running = True
while running:
    for event in pygame.event.get(): #이벤트 체크. 마우스에 대해서
        if event.type == pygame.QUIT: #X버튼을 통해 게임을 종료할때에
            running = False
    screen.blit(background, (0, 0)) #배경 그리기
    screen.blit(character, (character_x_pos, character_y_pos))  # 배경 그리기
    pygame.display.update() #게임화면을 다시 그리기

#파이게임 종료
pygame.quit()