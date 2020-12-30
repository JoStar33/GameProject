#1. 캐릭터가 공에 맞으면 게임 아웃
#2. 모든 공을 없애면 게임 아웃
#3. 시간제한 99초를 초과하면 게임 아웃

import os
import pygame

#기본 초기화 부분들
pygame.init() #초기화

#화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
current_path = os.path.dirname(__file__) #현재 파일의 위치 변환
image_path = os.path.join(current_path, "images") #images 폴더 위치 변환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.jpg"))


#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지의 높이 위에 캐릭터를 두기위해 사용

#FPS
clock = pygame.time.Clock()

#캐릭터 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size #이미지 크기를 구해온다.
character_width = character_size[0] #캐릭터 가로크기
character_height = character_size[1] #캐릭터 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치.
character_y_pos = screen_height - character_height - stage_height  #화면 세로 크기 가장 아래에 해당하는 곳에 위치.


#이동할 좌표 초기화
character_to_x = 0

#이동속도
character_speed = 5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한 번에 여러 발 발사하므로
weapons = []

#무기 이동 속도
weapon_speed = 10


#공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [pygame.image.load(os.path.join(image_path, "ballon1.png")),
               pygame.image.load(os.path.join(image_path, "ballon2.png")),
               pygame.image.load(os.path.join(image_path, "ballon3.png")),
               pygame.image.load(os.path.join(image_path, "ballon4.png"))]

#공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] #index 0, 1, 2, 3에 해당하는 값

balls = []

#딕셔너리 사용
balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x": 3, #x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6, #y축 이동방향
    "init_spd_y": ball_speed_y[0]#y 최초 속도
})


#사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1


#폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

#게임 종료 메시지
game_result = "Game Over"

#게임내에서 주어지는 총 시간
total_time = 100

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
                character_to_x -=character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x +=character_speed
            elif event.key == pygame.K_SPACE: #무기발사
                weapon_x_pos = character_x_pos + character_width / 2 - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    #게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #무기 위치 조정
    #무기의 x좌표는 그대로 유지되고 y좌표가 줄어들도록 만들어줄 필요가 있다.
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] #웨폰 리스트를 하나씩 불러와서 w라고 치고 하나씩 처리를 해준다.
    #리스트에 0번째 있는값과 첫번째 있는값이 감싸도록.

    #천장에 닿은 무기를 없애도록.
    weapons = [[w[0],w[1]] for w in weapons if w[1] > 0]



    #충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]  # 딕셔너리에 값을 정의
        ball_pos_y = ball_val["pos_y"]  # 딕셔너리에 값을 정의
        ball_img_idx = ball_val["img_idx"]  # 딕셔너리에 값을 정의

        # 공 렉트정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            print("충돌 발생")
            running = False
            break
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #해당 무기를 없애기위한 값 설정
                ball_to_remove = ball_idx #해당 무기를 없애기 위한 값 설정

                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:

                    #현재의 공크기 정보를 가지고 옴.
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),  # 공의 x좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),  # 공의 y좌표
                        "img_idx": ball_img_idx + 1 ,  # 공의 이미지 인덱스
                        "to_x": -3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })
                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + ball_width / 2 - small_ball_width / 2,  # 공의 x좌표
                        "pos_y": ball_pos_y + ball_height / 2 - small_ball_height / 2,  # 공의 y좌표
                        "img_idx": ball_img_idx + 1 ,  # 공의 이미지 인덱스
                        "to_x": 3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })
                break


    #충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #모든 공을 없앤 경우 게임 종료 (성공공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False


    #공 위치 정의. 몇번째 인덱스이며 그 인덱스가 가지고 있는 값을 볼리스트 내에서 꺼내 확인.
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"] #딕셔너리에 값을 정의
        ball_pos_y = ball_val["pos_y"]  # 딕셔너리에 값을 정의
        ball_img_idx = ball_val["img_idx"]  # 딕셔너리에 값을 정의
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        #가로벽에 닿았을 때 공 이동 위치 변경(튕기기)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]* -1
        #세로 위치
        #스테이지에 튕겨서 올라가는 거리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: #그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    screen.blit(background, (0, 0)) #배경 그리기
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height-stage_height)) #스테이지 그리기
    screen.blit(character, (character_x_pos, character_y_pos))  #캐릭터 그리기


    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #경과시간(ms)을 1000으로 나누어서 초 단위로 표시.
    timer =game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255)) #처음은 시간정보(출력할 글자), True, 글자색
    screen.blit(timer, (10,10))

    #만약 시간이 0이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() #게임화면을 다시 그리기
#게임 오버 메시지
msg = game_font.render(game_result,True,(255,255,0)) #노란색
msg_rect = msg.get_rect(center=(int(screen_width/2,), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

#잠시 대기
pygame.time.delay(2000) #2초인데 밀리세컨드라서 1000곱해줘야해

#파이게임 종료
pygame.quit()