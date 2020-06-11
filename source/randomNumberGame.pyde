import random

bets = 0
spinning = False
betting = False
slowdown = False
gameover = False

pheta = 0
rate = 1
countdown = 0

score = 0
rounds = 0

risky = False

#Ik Pvector exists but shut up
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xy = [x, y]

class Button:
    
    def __init__(self, min_x, max_x, min_y, max_y, value, font_size):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.value = value
        self.font_size = font_size
        self.over = mouseX >= min_x and mouseX <= max_x and mouseY >= min_y and mouseY <= max_y
    
    def sketch(self, col):
        
        colors = {
        "nothing":color(255, 32, 32),
        "highlighted":color(255, 16, 16),
        "blocked":color(128, 16, 16) }
        
        fill(colors[col])
        rect(self.min_x, self.min_y, self.max_x, self.max_y)
        fill(255)
        textSize(self.font_size)
        text(self.value, (self.min_x + self.max_x) // 2, (self.min_y + self.max_y) // 2)
        


def setup():
    global dice_button, bet_button, retry, safe_bet, risky_bet
    # retry = Button(200, 600, 400, 500, "Retry", 32)
    
    # dice_button = Button(300, 500, 450, 500, "Spin the wheel", 24)
    # bet_button = Button(325, 475, 525, 565, "", 14)
    
    
    # safe_bet = Button(550, 750, 400, 450, "Safe, low return bet", 16) 
    # risky_bet = Button(550, 750, 500, 550, "Risky, high return bet", 16)
    
    size(800, 600)
    rectMode(CORNERS)
    textAlign(CENTER, CENTER)
    
    
    
def draw():
    global spinning, rate, slowdown, countdown, replay, gameover, retry, score
    
    retry = Button(200, 600, 400, 500, "Retry", 32)
    
    background(22)
    
    if gameover:
        # retry = Button(200, 600, 400, 500, "Retry", 64)
        if retry.over: retry.sketch("highlighted")
        else: retry.sketch("nothing")
        textSize(64)
        fill(255)
        text("You survived " + str(rounds) + " rounds\n wtih a score of " + str(score), 400, 200)
    else:
        buttons()
        wheel()
        stats()
        bet()
    
        if countdown != 0 and spinning:
            countdown -= 1
        elif countdown == 0 and spinning:
            slowdown = True
    
        if spinning and not slowdown and rate < 7:
            rate += 1
        if slowdown and rate > 0:
            rate -= 1
            if rate <= 0:
                slowdown = False
                spinning = False
                scoring()
            

def bet():
    global betting, bets, score, safe_bet, risky_bet
    
    safe_bet = Button(550, 750, 400, 450, "Safe, low return bet", 16) 
    risky_bet = Button(550, 750, 500, 550, "Risky, high return bet", 16)
    
    if not betting: return

    if spinning: safe_bet.sketch("blocked")
    elif safe_bet.over: safe_bet.sketch("highlighted")
    else: safe_bet.sketch("nothing")
    
    if spinning or score < 12: risky_bet.sketch("blocked")
    elif risky_bet.over: risky_bet.sketch("highlighted")
    else: risky_bet.sketch("nothing")
        
def scoring():
    global pheta, rounds, score, bets, gameover, betting, risky
    boost = abs((pheta // 60) - 6)
    
    if boost == 1:
        gameover = True
    elif betting:
        if risky and boost % 2 == 1 or not risky and boost % 2 == 0:
            score += 6 * (2 ** int(risky))
        elif risky and boost % 2 == 0 or not risky and boost % 2 == 1:
            score -= 6 * (2 ** int(risky))
        if score < 0:
            score = 0
        betting = False
    else:
        if boost == 2:
            bets += 1
        score += boost
        if score >= 99:
            gameover = True
    
    rounds += 1
    
def stats():
    global rounds, score
    textSize(28)
    fill(255)
    text("Rounds: " + str(rounds), 700, 50)
    fill(255, abs(score - 99) * 2.56, abs(score - 99) * 2.56)
    rect(25, 500, 50, 500 - (score * 4))
    text(score, 75, 500 - (score * 4))
    
    
def buttons():
    global dice_button, bet_button, bets, betting, spinning
    
    dice_button = Button(300, 500, 450, 500, "Spin the wheel", 24)
    bet_button = Button(325, 475, 525, 565, "", 14)
    
    if spinning or betting: dice_button.sketch("blocked")
    elif dice_button.over: dice_button.sketch("highlighted")
    else: dice_button.sketch("nothing")
    
    if bets == 0 or score < 6 or betting or spinning: bet_button.sketch("blocked")
    elif bet_button.over: bet_button.sketch("highlighted")
    else: bet_button.sketch("nothing")
    
    fill(255)
    textSize(14)
    text(str(bets) + " bets remaining", 400, 542)
    
def wheel():
    global bets, betting, spinning, pheta, rate, risky
    
    center = Vector2(400, 250)
    r = 150
    
    pushMatrix()
    
    translate(center.x, center.y)
    rotate(radians(pheta))
        
    fill(255)
    ellipse(0, 0, 300, 300)
    for angle in range(90, 211, 60):
        line(r * cos(radians(angle)), r * sin(radians(angle)), r * cos(radians(angle + 180)), r * sin(radians(angle + 180)))
    fill(0)
    textSize(32)
    for i in range(6):
        if spinning and betting and i != 0 and (i + 1) % 2 == int(risky):
            textSize(40)
        else:
            textSize(32)
        pushMatrix()
        rotate(radians((i *60) + 30))
        fill((i % 2) * 255, 0, 0)
        if i == 0: fill(75, 35, 35)
        text(str(i + 1), 0, -100)
        popMatrix() 
    
    if spinning:
        pheta += rate
        pheta = pheta % 360
           
    popMatrix()
    
    fill(255, 40, 40)
    triangle(400, 110, 400 + (75 * cos(radians(300))), 110 + (75 * sin(radians(300))), 400 + (75 * cos(radians(240))), 110 + (75 * sin(radians(240)))) 
    
    
def mouseClicked():
    global dice_button, bet_button, bets, spinning, betting, countdown, retry, score, rounds, gameover, pheta, safe_bet, high_bet, risky
    if dice_button.over and not spinning and not betting and not gameover:
        spinning = True
        countdown = random.randint(75, 435)
    
    if bet_button.over and bets != 0 and not betting and not spinning and score >= 6:
        betting = True
        bets -= 1
        
    if retry.over and gameover:
        bets = 0
        score = 0
        rounds = 0
        pheta = 0
        gameover = False
        
    if safe_bet.over and not spinning and betting:
        spinning = True
        risky = False
        countdown = random.randint(200, 560)
        
    if risky_bet.over and not spinning and score >= 12 and betting:
        spinning = True
        risky = True
        countdown = random.randint(200, 560)
