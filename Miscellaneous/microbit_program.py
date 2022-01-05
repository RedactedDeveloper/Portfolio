Keepie-Uppies
from microbit import *
import random
import utime

Paddle = ["00000:00000:00000:00000:90000","00000:00000:00000:00000:09000","00000:00000:00000:00000:00900","00000:00000:00000:00000:00090","00000:00000:00000:00000:00009"]

Column00 = Image("90000:00000:00000:00000:00000")
Column01 = Image("00000:90000:00000:00000:00000")
Column02 = Image("00000:00000:90000:00000:00000")
Column03 = Image("00000:00000:00000:90000:00000")
Column04 = Image("00000:00000:00000:00000:90000")
Column0 = [Column00, Column01, Column02, Column03, Column04]

Column10 = Image("09000:00000:00000:00000:00000")
Column11 = Image("00000:09000:00000:00000:00000")
Column12 = Image("00000:00000:09000:00000:00000")
Column13 = Image("00000:00000:00000:09000:00000")
Column14 = Image("00000:00000:00000:00000:09000")
Column1 = [Column10, Column11, Column12, Column13, Column14]

Column20 = Image("00900:00000:00000:00000:00000")
Column21 = Image("00000:00900:00000:00000:00000")
Column22 = Image("00000:00000:00900:00000:00000")
Column23 = Image("00000:00000:00000:00900:00000")
Column24 = Image("00000:00000:00000:00000:00900")
Column2 = [Column20, Column21, Column22, Column23, Column24]

Column30 = Image("00090:00000:00000:00000:00000")
Column31 = Image("00000:00090:00000:00000:00000")
Column32 = Image("00000:00000:00090:00000:00000")
Column33 = Image("00000:00000:00000:00090:00000")
Column34 = Image("00000:00000:00000:00000:00090")
Column3 = [Column30, Column31, Column32, Column33, Column34]

Column40 = Image("00009:00000:00000:00000:00000")
Column41 = Image("00000:00009:00000:00000:00000")
Column42 = Image("00000:00000:00009:00000:00000")
Column43 = Image("00000:00000:00000:00009:00000")
Column44 = Image("00000:00000:00000:00000:00009")
Column4 = [Column40, Column41, Column42, Column43, Column44]


n = 2
a = ""
score = 0
numberOfBallsOnScreen = 0

if button_a_is_pressed():
    GameStart = True

while GameStart == True:
    display.show(Image(Paddle[n]))
    if button_a_is_pressed():
        if n == 0:
            a = "throwaway"
        else:
            n -= 1
    if button_b_is_pressed():
        if n == 4:
            a = "throwaway"
        else:
            n += 1
    while GameOver == False:
        while numberOfBallsOnScreen == 0:
            Column = random.randint(0,4)
            numberOfBallsOnScreen = 1
            if Column == 0:
                display.show(Image(Column0, delay=200))
                DeadLine = (ticks_add(time.ticks_ms(), 800)
                if paddle[n] == Column0[4] and while ticks_diff(deadline, time.ticks_ms()) == 0:
                    Score += 1
                    numberOfBallsOnScreen = 0
                elif DeadLine < 0:
                    GameOver = True
            elif Column == 1:
                display.show(Image(Column1, delay=200))
                DeadLine = (ticks_add(time.ticks_ms(), 800)
                if paddle[n] == Column1[4] and while ticks_diff(deadline, time.ticks_ms()) == 0:
                    Score += 1
                    numberOfBallsOnScreen = 0
                elif DeadLine < 0:
                    GameOver = True
            elif Column == 2:
                display.show(Image(Column2, delay=200))
                DeadLine = (ticks_add(time.ticks_ms(), 800)
                if paddle[n] == Column2[4] and while ticks_diff(deadline, time.ticks_ms()) == 0:
                    Score += 1
                    numberOfBallsOnScreen = 0
                elif DeadLine < 0:
                    GameOver = True
            elif Column == 3:
                display.show(Image(Column3, delay=200))
                DeadLine = (ticks_add(time.ticks_ms(), 800)
                if paddle[n] == Column3[4] and while ticks_diff(deadline, time.ticks_ms()) == 0:
                    Score += 1
                    numberOfBallsOnScreen = 0
                elif DeadLine < 0:
                    GameOver = True
            elif Column == 4:
                display.show(Image(Column4, delay=200))
                DeadLine = (ticks_add(time.ticks_ms(), 800)
                if paddle[n] == Column4[4] and while ticks_diff(deadline, time.ticks_ms()) == 0:
                    Score += 1
                    numberOfBallsOnScreen = 0
                elif DeadLine < 0:
                    GameOver = True
            
    break
display.show(score)
