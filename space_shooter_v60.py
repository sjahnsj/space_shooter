from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import urllib.request as req

import pygame
import sys
import random
from time import sleep


def read_scores():
    try:
        with open("scores.txt", "r") as file:
            all_scores = [int(line.strip()) for line in file.readlines()]

            return all_scores
    except FileNotFoundError:
        return []


def draw_score():
    y = read_scores()
    # print(y)

    x = [i + 1 for i in range(len(y))]

    plt.plot(x, y, marker=".", markerfacecolor="red", markersize=15)
    plt.xticks(range(1, len(y) + 1))
    plt.xlabel("n-th Try")
    plt.ylabel("Score")
    plt.title("Score History")
    plt.show()


def get_weather():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%82%98&qdt=0&ie=utf8&query=%EB%82%A0%EC%94%A8"

    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    # print(soup)
    weather_condition = soup.select_one(
        "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.temperature_info > p"
    )
    return weather_condition.get_text()


BLACK = (0, 0, 0)
padWidth = 480  # 게임화면의 가로크기
padHeight = 640  # 게임화면의 세로크기
rockImage = [
    "PS/rock01.png",
    "PS/rock02.png",
    "PS/rock03.png",
    "PS/rock04.png",
    "PS/rock05.png",
    "PS/rock06.png",
    "PS/rock07.png",
    "PS/rock08.png",
    "PS/rock09.png",
    "PS/rock10.png",
    "PS/rock11.png",
    "PS/rock12.png",
    "PS/rock13.png",
    "PS/rock14.png",
    "PS/rock15.png",
    "PS/rock16.png",
    "PS/rock17.png",
    "PS/rock18.png",
    "PS/rock19.png",
    "PS/rock20.png",
    "PS/rock21.png",
    "PS/rock22.png",
]
explosionSound = [
    "PS/explosion01.wav",
    "PS/explosion02.wav",
    "PS/explosion03.wav",
    "PS/explosion04.wav",
]


############################## scores def start ###################################
scores = 0


def show_end_screen(scores):  # 종료 화면 텍스트 등을 출력하는 코드
    save_scores(scores)  # 현재 게임의 점수를 파일에 저장
    high_scores = read_high_scores()  # 상위 5위 점수 읽어오기
    display_high_scores(high_scores)  # 상위 5위 점수 출력


def save_scores(scores):
    # 현재 게임의 점수를 파일에 저장
    with open("scores.txt", "a") as file:
        file.write(f"{scores}\n")


def read_high_scores():
    try:
        with open("scores.txt", "r") as file:
            all_scores = [int(line.strip()) for line in file.readlines()]
            global end_score, before_score
            end_score = all_scores[-1]
            if len(all_scores) > 1:
                before_score = all_scores[-2]
            else:
                before_score = 0
            return max(all_scores)
    except FileNotFoundError:
        return 0


def display_high_scores(high_scores):
    writeMessage3_2("★SCORE★")
    font = pygame.font.Font("PS/font.ttf", 20)
    text_y = padHeight / 2 + 130
    # for i, score in enumerate(high_scores, start=1):
    score_text = font.render(f"최고 점수 : {high_scores}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(padWidth / 2, text_y))
    gamePad.blit(score_text, score_rect)
    text_y += 25

    score_text = font.render(f"현재 점수 : {end_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(padWidth / 2, text_y))
    gamePad.blit(score_text, score_rect)
    text_y += 25

    score_text = font.render(f"이전 점수 : {before_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(padWidth / 2, text_y))
    gamePad.blit(score_text, score_rect)
    text_y += 25

    score_text = font.render(f"점수 이력 그래프 보기 : G", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(padWidth / 2, text_y))
    gamePad.blit(score_text, score_rect)
    text_y += 25

    pygame.display.update()


############################## scores def end ###################################
# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def show_level(level):
    font = pygame.font.Font("PS/font.ttf", 20)
    level_text = font.render("레벨:" + str(level), True, (255, 255, 255))
    gamePad.blit(level_text, (10, 30))  # Adjusted position


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound, bg_y, background_near, bgnear_y, laser, laser_rect, shoot_laser, shooter_life, special, lvup, missile1, missile2, expl, hpbar, hpbar_rect, weather
    weather = get_weather()
    pygame.init()
    pygame.mixer.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("PyShooting")  # 게임 이름
    expl = pygame.mixer.Sound("PS/expl1.mp3")
    ############################
    shooter_life = 10
    shoot_laser = False
    background = pygame.image.load("PS/space_bg.png")  # 배경 그림
    bg_y = 0
    background_near = pygame.image.load("PS/near_bg.jpeg")  # 배경 그림
    background_near.set_alpha(160)
    bgnear_y = 0
    laser = pygame.image.load("PS/laser.jpg")
    laser_rect = laser.get_rect(topleft=(0, padHeight))
    hpbar = pygame.image.load("PS/hp_bar.png")  # hp bar draw
    hpbar_rect = laser.get_rect(topleft=(0, 0))
    pygame.mixer.music.load("PS/music2.mp3")  # 배경 음악
    pygame.mixer.music.play(-1)  # 배경 음악 재생
    missileSound = pygame.mixer.Sound("PS/missile.wav")  # 미사일 사운드
    gameOverSound = pygame.mixer.Sound("PS/gameover.wav")  # 게임 오버 사운드
    fighter = pygame.image.load("PS/f4.png")  # 전투기 그림
    missile = pygame.image.load("PS/m2.png")  # 미사일 그림
    missile1 = pygame.image.load("PS/m1.png")
    missile2 = pygame.image.load("PS/m3.png")
    explosion = pygame.image.load("PS/e1.png")  # 폭발 그림
    clock = pygame.time.Clock()
    #######################################
    special = pygame.mixer.Sound("PS/s2.mp3")  # 필살기 사운드
    lvup = pygame.mixer.Sound("PS/lvup.mp3")  # 레벨업 사운드
    lvup.set_volume(1)


# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad
    global shootCount
    shootCount = count  ######### scores ######## 점수를 scores 리스트에 추가
    font = pygame.font.Font("PS/font.ttf", 20)
    text = font.render("점수:" + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 2))


# 운석을 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font("PS/font.ttf", 20)
    text = font.render("놓친 운석:" + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 2))


# 게임 메시지 출력
########################요기###########################
def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font("PS/font.ttf", 105)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2 - 150)
    gamePad.blit(text, textpos)
    pygame.display.update()


def writeMessage2(text):
    global gamePad
    textfont = pygame.font.Font("PS/font.ttf", 25)
    text = textfont.render(text, True, (0, 250, 250))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2 - 40)
    gamePad.blit(text, textpos)
    pygame.display.update()


def writeMessage3(text):
    global gamePad
    textfont = pygame.font.Font("PS/font.ttf", 25)
    text = textfont.render(text, True, (0, 150, 250))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2 - 15)
    gamePad.blit(text, textpos)
    pygame.display.update()


def writeMessage4(text):
    global gamePad
    textfont = pygame.font.Font("PS/font.ttf", 25)
    text = textfont.render(text, True, (0, 150, 250))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2 + 10)
    gamePad.blit(text, textpos)
    pygame.display.update()


def writeMessage3_2(text):
    global gamePad
    textfont = pygame.font.Font("PS/font.ttf", 30)
    text = textfont.render(text, True, (30, 150, 100))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2 + 80)
    gamePad.blit(text, textpos)
    pygame.display.update()


# 전투기가 운석과 충돌했을 때 메시지 출력
def crash():
    global gamePad, shooter_life
    shooter_life = 10
    pygame.mixer.music.stop()  # 배경 음악 정지
    gameOverSound.play()  # 게임 오버 사운드 재생
    writeMessage("GAME OVER")
    writeMessage2("다시시작 : ENTER")
    writeMessage3("나가기 : Q")
    scores = shootCount  ######### scores ######## 점수를 scores 리스트에 추가
    show_end_screen(scores)  ######### scores ########
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.play(-1)  # 배경 음악 재생
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_g:
                    draw_score()


# 게임 오버 메시지 보이기
def gameOver():
    pygame.mixer.music.stop()  # 배경 음악 정지
    gameOverSound.play()  # 게임 오버 사운드 재생
    global gamePad, shooter_life
    shooter_life = 10
    writeMessage("GAME OVER")
    writeMessage2("다시시작 : ENTER")
    writeMessage3("나가기 : Q")
    scores = shootCount  ######### scores ######## 점수를 scores 리스트에 추가
    show_end_screen(scores)  ######### scores ########
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.play(-1)  # 배경 음악 재생
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_g:
                    draw_score()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, bg_y, background_near, bgnear_y, laser, laser_rect, shoot_laser, shooter_life, special, lvup, missile1, missile2, expl, hpbar, hpbar_rect, weather

    isPause = False
    pygame.font.init()
    font = pygame.font.Font("PS/font.ttf", 70)  # 폰트와 크기 설정
    font2 = pygame.font.Font("PS/font.ttf", 20)

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_SPACE:
                    onGame = True

        drawObject(background, 0, bg_y - padHeight)
        drawObject(background, 0, bg_y)
        bg_y += 2
        if bg_y > padHeight:
            bg_y = 0
        drawObject(background_near, 0, bgnear_y - padHeight)
        drawObject(background_near, 0, bgnear_y)
        bgnear_y += 3
        if bgnear_y > padHeight:
            bgnear_y = 0

        welcome_text = font.render("Space Shooter", True, (250, 50, 50))
        welcome_rect = welcome_text.get_rect(center=(padWidth / 2, padHeight / 2 - 160))
        gamePad.blit(welcome_text, welcome_rect)
        welcome_text = font2.render(weather, True, (250, 250, 50))
        welcome_rect = welcome_text.get_rect(center=(padWidth / 2, padHeight / 2 - 90))
        gamePad.blit(welcome_text, welcome_rect)
        welcome_text = font2.render("게임하기 좋은 날이네요 ^^", True, (250, 250, 50))
        welcome_rect = welcome_text.get_rect(center=(padWidth / 2, padHeight / 2 - 65))
        gamePad.blit(welcome_text, welcome_rect)

        press_text = font2.render("스페이스바를 누르면 시작합니다.", True, (255, 255, 255))
        press_rect = press_text.get_rect(center=(padWidth / 2, padHeight / 2))
        gamePad.blit(press_text, press_rect)

        instruction_text = font2.render(
            "운석을 부술 시 점수가 올라갑니다.",
            True,
            (255, 255, 255),
        )
        instruction_rect = instruction_text.get_rect(
            center=(padWidth / 2, padHeight / 2 + 50)
        )
        gamePad.blit(instruction_text, instruction_rect)

        instruction_text2 = font2.render(
            "우주를 지켜주세요!",
            True,
            (255, 255, 255),
        )
        instruction_rect2 = instruction_text2.get_rect(
            center=(padWidth / 2, padHeight / 2 + 80)
        )
        gamePad.blit(instruction_text2, instruction_rect2)

        instruction_text3 = font2.render(
            "←↑↓→ 방향키로 움직입니다",
            True,
            (255, 255, 255),
        )
        instruction_rect3 = instruction_text3.get_rect(
            center=(padWidth / 2, padHeight / 2 + 120)
        )
        gamePad.blit(instruction_text3, instruction_rect3)

        instruction_text4 = font2.render(
            "발사 : SPACEBAR  일시정지 : P  필살기: S",
            True,
            (255, 255, 255),
        )
        instruction_rect4 = instruction_text4.get_rect(
            center=(padWidth / 2, padHeight / 2 + 160)
        )
        gamePad.blit(instruction_text4, instruction_rect4)

        pygame.display.update()
        clock.tick(60)
    # 전투기 미사일에 운석이 맞았을 경우 True
    level = 1
    isShot = False
    isShot2 = False
    isShot3 = False
    shotCount = 0
    rockPassed = 0
    rotation_angle = random.randint(1, 20)
    rotation_angle1 = random.randint(1, 20)

    # 무기 좌표 리스트
    missileXY = []
    lv = True
    lv2 = True
    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rock2 = pygame.image.load(random.choice(rockImage))
    rock3 = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size  # 운석 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockSize2 = rock2.get_rect().size  # 운석 크기
    rockWidth2 = rockSize2[0]
    rockHeight2 = rockSize2[1]
    rockSize3 = rock2.get_rect().size  # 운석 크기
    rockWidth3 = rockSize2[0]
    rockHeight3 = rockSize2[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockX2 = random.randrange(0, padWidth - rockWidth)
    rockX3 = random.randrange(0, padWidth - rockWidth)
    rockY = -10
    rockY2 = -10
    rockY3 = -10
    rockSpeed = 3

    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치(x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  # 전투기 왼쪽으로 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:  # 전투기 오른쪽으로 이동
                    fighterX += 5
                elif event.key == pygame.K_UP:
                    fighterY -= 5  # Move up (backward)
                elif event.key == pygame.K_DOWN:
                    fighterY += 5  # Move down (forward)

                elif event.key == pygame.K_SPACE:  # 미사일 발사
                    if level <= 1:
                        missileSound.play()  # 미사일 사운드 재생
                        missileX = x + fighterWidth / 2.5
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth / 7.5
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                    #######
                    if level == 2:
                        missileSound.play()  # 미사일 사운드 재생
                        missileX = x + fighterWidth / 2
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                    #######
                    if level == 3:
                        missileSound.play()  # 미사일 사운드 재생
                        missileX = x + fighterWidth / 2
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x - 20
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missileX = x + 20 + fighterWidth
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])

                elif event.key == pygame.K_s:  # 필살기 Laser
                    shoot_laser = True
                elif event.key == pygame.K_p:  # pause
                    isPause = True

            if event.type in [pygame.KEYUP]:  # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0  # Stop vertical movement

        #######################################################
        drawObject(background, 0, bg_y - padHeight)
        drawObject(background, 0, bg_y)
        bg_y += 2
        if bg_y > padHeight:
            bg_y = 0
        drawObject(background_near, 0, bgnear_y - padHeight)
        drawObject(background_near, 0, bgnear_y)
        bgnear_y += 4
        if bgnear_y > padHeight:
            bgnear_y = 0
        # 배경 화면 그리기        # gamePad.fill(BLACK) 게임 화면 (검은색)으로 만들어주는 초기화면
        # drawObject 때문에 필요없음
        if shoot_laser:  # collision
            drawObject(laser, 0, laser_rect.y)
            special.play()
            laser_rect.y -= 3
            if laser_rect.y < rockY:
                isShot = True
                shotCount += 1
            if level == 2 or level == 3:
                if laser_rect.y < rockY2:
                    isShot2 = True
                    shotCount += 1
                if laser_rect.y < rockY3:
                    isShot3 = True
                    shotCount += 1
            if laser_rect.y < 0:
                shoot_laser = False
                laser_rect.y = padHeight
                special.stop()
        ###########################################################
        if lv == True:
            if shotCount >= 10:
                level += 1
                rockSpeed += 1
                lvup.play()
                lv = False
        if lv2 == True:
            if shotCount >= 40:
                level += 1
                rockSpeed += 1
                lvup.play()
                lv2 = False

        show_level(level)

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소에 대해 반복함
                bxy[1] -= 10  # 총알의 y좌표 -10(위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if level == 2 or level == 3:
                    if bxy[1] < rockY2:
                        if (
                            bxy[0] > rockX2
                            and bxy[0] < rockX2 + rockWidth2
                            # and missileXY != []
                        ):
                            if bxy in missileXY:
                                missileXY.remove(bxy)
                            isShot2 = True
                            shotCount += 1
                    if bxy[1] < rockY3:
                        if (
                            bxy[0] > rockX3
                            and bxy[0] < rockX3 + rockWidth3
                            # and missileXY != []
                        ):
                            if bxy in missileXY:
                                missileXY.remove(bxy)
                            isShot3 = True
                            shotCount += 1

                ###########################################################################################
                if bxy[1] <= 0:  # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)  # 미사일 제거
                    except:
                        pass
        ag = random.randint(1, 10)
        rotation_angle = (rotation_angle + ag) % 360
        rotation_angle1 = -((rotation_angle + ag) % 360)
        if len(missileXY) != 0:
            if level == 1:
                for bx, by in missileXY:
                    drawObject(missile2, bx, by)
            if level == 2:
                for bx, by in missileXY:
                    drawObject(missile, bx, by)
            if level == 3:
                for bx, by in missileXY:
                    drawObject(missile1, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        rockY += rockSpeed  # 운석 아래로 움직임

        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            # 새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
            shooter_life -= 1

        if level == 2:
            if rockY2 > padHeight:
                # 새로운 운석 (랜덤)
                rock2 = pygame.image.load(random.choice(rockImage))
                rockSize2 = rock2.get_rect().size
                rockWidth2 = rockSize[0]
                rockHeight2 = rockSize[1]
                rockX2 = random.randrange(0, padWidth - rockWidth2)
                rockY2 = -30
                rockPassed += 1
                shooter_life -= 1
            if rockY3 > padHeight:
                # 새로운 운석 (랜덤)
                rock3 = pygame.image.load(random.choice(rockImage))
                rockSize3 = rock3.get_rect().size
                rockWidth3 = rockSize[0]
                rockHeight3 = rockSize[1]
                rockX3 = random.randrange(0, padWidth - rockWidth2)
                rockY3 = -30
                rockPassed += 1
                shooter_life -= 1
            if isShot2:
                # 운석 폭발
                drawObject(explosion, rockX2, rockY2)  # 운석 폭발 그리기
                rock2 = pygame.image.load(random.choice(rockImage))
                rockSize2 = rock2.get_rect().size
                rockWidth2 = rockSize2[0]
                rockHeight2 = rockSize2[1]
                rockX2 = random.randrange(0, padWidth - rockWidth2)
                rockY2 = -30
                isShot2 = False
                # 운석 맞추면 속도 증가
                rockSpeed += 0.1
                if rockSpeed >= 10:
                    rockSpeed = 10
            if isShot3:
                # 운석 폭발
                drawObject(explosion, rockX3, rockY3)  # 운석 폭발 그리기
                rock3 = pygame.image.load(random.choice(rockImage))
                rockSize3 = rock3.get_rect().size
                rockWidth3 = rockSize3[0]
                rockHeight3 = rockSize3[1]
                rockX3 = random.randrange(0, padWidth - rockWidth2)
                rockY3 = -30
                isShot3 = False
                # 운석 맞추면 속도 증가
                rockSpeed += 0.15
                if rockSpeed >= 10:
                    rockSpeed = 10
            rotated_rock2 = pygame.transform.rotate(
                rock2, rotation_angle
            )  # Adjust the rotation angle as needed
            rotated_rock2_rect = rotated_rock2.get_rect(
                center=(rockX2 + rockWidth2 / 2, rockY2 + rockHeight2 / 2)
            )
            gamePad.blit(rotated_rock2, rotated_rock2_rect.topleft)
            rotated_rock3 = pygame.transform.rotate(
                rock3, rotation_angle1
            )  # Adjust the rotation angle as needed
            rotated_rock3_rect = rotated_rock3.get_rect(
                center=(rockX3 + rockWidth3 / 2, rockY3 + rockHeight3 / 2)
            )
            gamePad.blit(rotated_rock3, rotated_rock3_rect.topleft)
            rockY2 += rockSpeed
            rockY3 += rockSpeed

        if level == 3:
            if rockY2 > padHeight:
                # 새로운 운석 (랜덤)
                rock2 = pygame.image.load(random.choice(rockImage))
                rockSize2 = rock2.get_rect().size
                rockWidth2 = rockSize[0]
                rockHeight2 = rockSize[1]
                rockX2 = random.randrange(0, padWidth - rockWidth2)
                rockY2 = -30
                rockPassed += 1
                shooter_life -= 1
            if rockY3 > padHeight:
                # 새로운 운석 (랜덤)
                rock3 = pygame.image.load(random.choice(rockImage))
                rockSize3 = rock3.get_rect().size
                rockWidth3 = rockSize[0]
                rockHeight3 = rockSize[1]
                rockX3 = random.randrange(0, padWidth - rockWidth2)
                rockY3 = -30
                rockPassed += 1
                shooter_life -= 1
            if isShot2:
                # 운석 폭발
                drawObject(explosion, rockX2, rockY2)  # 운석 폭발 그리기
                rock2 = pygame.image.load(random.choice(rockImage))
                rockSize2 = rock2.get_rect().size
                rockWidth2 = rockSize2[0]
                rockHeight2 = rockSize2[1]
                rockX2 = random.randrange(0, padWidth - rockWidth2)
                rockY2 = -30
                isShot2 = False
                # 운석 맞추면 속도 증가
                rockSpeed += 0.15
                if rockSpeed >= 10:
                    rockSpeed = 10
            if isShot3:
                # 운석 폭발
                drawObject(explosion, rockX3, rockY3)  # 운석 폭발 그리기
                rock3 = pygame.image.load(random.choice(rockImage))
                rockSize3 = rock3.get_rect().size
                rockWidth3 = rockSize3[0]
                rockHeight3 = rockSize3[1]
                rockX3 = random.randrange(0, padWidth - rockWidth2)
                rockY3 = -30
                isShot3 = False
                # 운석 맞추면 속도 증가
                rockSpeed += 0.2
                if rockSpeed >= 10:
                    rockSpeed = 10
            rotated_rock2 = pygame.transform.rotate(
                rock2, rotation_angle
            )  # Adjust the rotation angle as needed
            rotated_rock2_rect = rotated_rock2.get_rect(
                center=(rockX2 + rockWidth2 / 2, rockY2 + rockHeight2 / 2)
            )
            gamePad.blit(rotated_rock2, rotated_rock2_rect.topleft)
            rotated_rock3 = pygame.transform.rotate(
                rock3, rotation_angle1
            )  # Adjust the rotation angle as needed
            rotated_rock3_rect = rotated_rock3.get_rect(
                center=(rockX3 + rockWidth3 / 2, rockY3 + rockHeight3 / 2)
            )
            gamePad.blit(rotated_rock3, rotated_rock3_rect.topleft)
            rockY2 += rockSpeed
            rockY3 += rockSpeed

        if shooter_life < 1:  # 운석 3개 놓치면 게임오버
            gameOver()

        # 놓친 운석 수 표시
        writePassed(rockPassed)

        # 운석을 맞춘 경우
        if isShot:
            # 운석 폭발
            drawObject(explosion, rockX, rockY)  # 운석 폭발 그리기
            destroySound.play()  # 운석 폭발 사운드 재생

            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            # 운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        # 전투기 위치 재조정
        x += fighterX
        y += fighterY
        # 가로 경계 처리
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 세로 경계 처리
        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight

        # 전투기가 운석과 충돌했는지 체크 collision
        if y < rockY + rockHeight:
            if (
                (rockX > x and rockX < x + fighterWidth)
                or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth)
                or (rockX <= x and rockX + rockWidth >= x + fighterWidth)
            ):
                if shooter_life < 1:
                    crash()
                # expl.play()
                # rock = pygame.image.load(random.choice(rockImage))
                shooter_life -= 1
                # rockSize = rock.get_rect().size
                # rockWidth = rockSize[0]
                # rockHeight = rockSize[1]
                # rockX = random.randrange(0, padWidth - rockWidth)
                # rockY = -30
                isShot = True

        if level == 2 or level == 3:
            if y < rockY2 + rockHeight2:
                if (
                    (rockX2 > x and rockX2 < x + fighterWidth)
                    or (
                        rockX2 + rockWidth2 > x
                        and rockX2 + rockWidth2 < x + fighterWidth
                    )
                    or (rockX2 <= x and rockX2 + rockWidth >= x + fighterWidth)
                ):
                    if shooter_life < 1:
                        crash()
                    shooter_life -= 1
                    isShot2 = True

                    # expl.play()
                    # rock2 = pygame.image.load(random.choice(rockImage))
                    # rockSize2 = rock2.get_rect().size
                    # rockWidth2 = rockSize[0]
                    # rockHeight2 = rockSize[1]
                    # rockX2 = random.randrange(0, padWidth - rockWidth2)
                    # rockY2 = -30
                    # rotated_rock2 = pygame.transform.rotate(
                    #     rock2, rotation_angle
                    # )  # Adjust the rotation angle as needed
                    # rotated_rock2_rect = rotated_rock2.get_rect(
                    #     center=(rockX2 + rockWidth2 / 2, rockY2 + rockHeight2 / 2)
                    # )
                    # gamePad.blit(rotated_rock2, rotated_rock2_rect.topleft)

            if y < rockY3 + rockHeight3:
                if (
                    (rockX3 > x and rockX3 < x + fighterWidth)
                    or (
                        rockX3 + rockWidth3 > x
                        and rockX3 + rockWidth3 < x + fighterWidth
                    )
                    or (rockX3 <= x and rockX3 + rockWidth >= x + fighterWidth)
                ):
                    if shooter_life < 1:
                        crash()
                    shooter_life -= 1
                    isShot3 = True

                    # expl.play()
                    # rock3 = pygame.image.load(random.choice(rockImage))
                    # rockSize3 = rock3.get_rect().size
                    # rockWidth3 = rockSize[0]
                    # rockHeight3 = rockSize[1]
                    # rockX3 = random.randrange(0, padWidth - rockWidth2)
                    # rockY3 = -30
                    # rotated_rock3 = pygame.transform.rotate(
                    #     rock3, rotation_angle
                    # )  # Adjust the rotation angle as needed
                    # rotated_rock3_rect = rotated_rock3.get_rect(
                    #     center=(rockX3 + rockWidth3 / 2, rockY3 + rockHeight3 / 2)
                    # )
                    # gamePad.blit(rotated_rock3, rotated_rock3_rect.topleft)

        ############# Drawing life energy bar
        hpbar_rect.x = int(x) - 3
        hpbar_rect.y = int(y + fighterHeight + 1)

        drawObject(hpbar, hpbar_rect.x, hpbar_rect.y)

        pygame.draw.rect(
            gamePad,
            (100, 230, 100),
            [x + 1, y + fighterHeight + 3, float(shooter_life / 10) * fighterWidth, 5],
            5,
        )
        #####################################
        drawObject(fighter, x, y)  # 비행기를 게임 화면의 (x,y) 좌표에 그림

        rotated_rock = pygame.transform.rotate(
            rock, rotation_angle
        )  # Adjust the rotation angle as needed
        rotated_rock_rect = rotated_rock.get_rect(
            center=(rockX + rockWidth / 2, rockY + rockHeight / 2)
        )
        gamePad.blit(rotated_rock, rotated_rock_rect.topleft)

        pygame.display.update()  # 게임화면을 다시그림

        clock.tick(60)  # 게임화면의 초당 프레임수를 60으로 설정
        ######################################
        ########################################
        while isPause:
            for event in pygame.event.get():
                # if event.type in [pygame.QUIT]:  # 게임 프로그램 종료
                #     pygame.quit()
                #     sys.exit()

                if event.type in [pygame.KEYDOWN]:
                    if event.key == pygame.K_p:
                        isPause = False
            pygame.time.delay(100)
            press_text = font.render("Game Paused", True, (255, 255, 0))
            press_rect = press_text.get_rect(center=(padWidth / 2, padHeight / 2))
            gamePad.blit(press_text, press_rect)
            press_text = font2.render("계속 플레이 하려면 p를 누르세요", True, (255, 255, 255))
            press_rect = press_text.get_rect(center=(padWidth / 2, padHeight / 2 + 60))
            gamePad.blit(press_text, press_rect)
            pygame.display.update()
        #########################################
        ##############################
    pygame.quit()  # pygame 종료


if __name__ == "__main__":
    initGame()
    runGame()
