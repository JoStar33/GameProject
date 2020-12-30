import pygame

#기본 초기화 부분들
pygame.init() #초기화

#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Hello Game") #게임이름

#FPS
clock = pygame.time.Clock()
#배경 이미지 불러오기
background = pygame.image.load("C:/Users/Hose/Desktop/gogo.png")

#캐릭터 불러오기
character = pygame.image.load("C:/Users/Hose/Desktop/character.png")
character_size = character.get_rect().size #이미지 크기를 구해온다.
character_width = character_size[0] #캐릭터 가로크기
character_height = character_size[1] #캐릭터 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치.
character_y_pos = screen_height - character_height  #화면 세로 크기 가장 아래에 해당하는 곳에 위치.


#이동할 좌표 초기화
to_x = 0
to_y = 0

#이동속도
character_speed = 0.6

#적 캐릭터
enemy = pygame.image.load("C:/Users/Hose/Desktop/enemy.png")
enemy_size = enemy.get_rect().size #이미지 크기를 구해온다.
enemy_width = enemy_size[0] #캐릭터 가로크기
enemy_height = enemy_size[1] #캐릭터 세로크기
enemy_x_pos = (screen_width / 2) - (enemy_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치.
enemy_y_pos = (screen_height / 2)- (enemy_height / 2)  #화면 세로 크기 가장 아래에 해당하는 곳에 위치.

#폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

#게임내에서 주어지는 총 시간
total_time = 10

#시작 시간 정보
start_ticks = pygame.time.get_ticks()

#이벤트 루프
running = True
while running:
    dt = clock.tick(30) #게임화면 초당 프레임 수
    #이벤트 처리과정
    #print("fps:"+ str(clock.get_fps()))
    #10fps는 1초동안에 10번 동작 -> 1번에 10만큼 이동
    #20fps는 1초동안에 20번 동작 -> 1번에 5만큼 이동
    for event in pygame.event.get(): #이벤트 체크. 마우스에 대해서
        if event.type == pygame.QUIT: #X버튼을 통해 게임을 종료할때에
            running = False #게임이 진행중이 아니라는 의미
        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -=character_speed #to_x = to_x -5
            elif event.key == pygame.K_RIGHT:
                to_x +=character_speed
            elif event.key == pygame.K_UP:
                to_y -=character_speed
            elif event.key == pygame.K_DOWN:
                to_y +=character_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x=0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y=0

    #게임 캐릭터 위치 정의
   character_x_pos += to_x * dt
   character_y_pos += to_y * dt

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height


    #충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    #충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌 발생")
        running = False

    screen.blit(background, (0, 0)) #배경 그리기
    screen.blit(character, (character_x_pos, character_y_pos))  # 배경 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))  # 배경 그리기

    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #경과시간(ms)을 1000으로 나누어서 초 단위로 표시.
    timer =game_font.render(str(int(total_time - elapsed_time)),True,(255,255,255)) #처음은 시간정보(출력할 글자), True, 글자색
    screen.blit(timer, (10,10))

    #만약 시간이 0이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False

    pygame.display.update() #게임화면을 다시 그리기

#잠시 대기
pygame.time.delay(2000) #2초인데 밀리세컨드라서 1000곱해줘야해

#파이게임 종료
pygame.quit()