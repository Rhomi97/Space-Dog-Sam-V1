import pygame
import sys
from random import randint

slide = 3
endslide = False

def accurate_colision(sprite1, sprite2):
    offset = (sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y)
    return sprite1.mask.overlap(sprite2.mask, offset)

class Menu():
    def __init__(self, color, second_color, shift_x, shift_y, text, x=0, y=0, width=10, height=10, size = 12, colorfont = (0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.fill_color = color
        self.first_color = color
        self.second_color = second_color
        self.text = text
        self.image = pygame.font.SysFont('verdana', size).render(self.text, True, colorfont)

    def color(self):
        if self.fill_color == self.first_color:
            self.fill_color = self.second_color
        else:
            self.fill_color = self.first_color
       
    def fill(self,mw):
       pygame.draw.rect(mw, self.fill_color, self.rect)
       
    def draw(self, mw):#funcion para dibujar la parte de adentro del rectangulo
       self.fill(mw)#llamada a la funcion para dibujar el rectangulo (función heredada de Area)
       mw.blit(self.image, (self.rect.x + self.shift_x, self.rect.y + self.shift_y))
    
    def collidepoint(self, x, y):
       return self.rect.collidepoint(x, y)  
        
class Picture():
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(filename)
        self.lightrectangle = pygame.Rect(x + 28, y+60, 35, 495-60)
        self.lightcenter = pygame.Rect(x + 28+ 16, y+60, 11, 495-60)
        self.fill_color = (252, 250, 227)
        self.switchedlight = 0

    def colliderect(self, rect):
        return self.rect.colliderect(rect)
    
    def resetLight(self):
        self.switchedlight = 0
    
    def fill(self,mw,sam):
        if self.switchedlight < 3:
            pygame.draw.rect(mw, self.fill_color, self.lightrectangle)
            if self.lightcenter.colliderect(sam.rect):
                return True
        self.switchedlight += 1

    def draw(self,mw,sam): #mw main window
        if sam.rect.x >= 125 and not endslide:
            self.rect.x -= slide
        mw.blit(self.image, (self.rect.x, self.rect.y))
        self.lightrectangle.x = self.rect.x + 28
        self.lightcenter.x = self.lightrectangle.x + 16
        

class Ship(Picture):
    def __init__(self, filename, x, y, width, height):
        Picture.__init__(self, filename, x, y, width, height)
        self.shipflag = 0
        self.shipflag2 = 0
    
    def enter(self,mw,color,clock,sam):
        for i in range(20):
            mw.fill(color)
            self.draw(mw,sam)
            self.rect.x += 3
            pygame.display.update()
            clock.tick(30)

class Sam():
    def __init__(self, total_crystals, sam1, sam2, poweredsam1, poweredsam2, healingsam1, healingsam2, power, powerup, x, y, bottom, top, width=44, height=42):
        self.rect = pygame.Rect(x, y, width, height)
        self.normalSam = [pygame.image.load(sam1),pygame.image.load(sam2)]
        self.poweredSam = [pygame.image.load(poweredsam1),pygame.image.load(poweredsam2)]
        self.healingSamImage = [pygame.image.load(healingsam1),pygame.image.load(healingsam2)]
        self.power = pygame.image.load(power)
        self.powerup = pygame.image.load(powerup)
        self.powerupsRect = []
        self.powerRect = pygame.Rect(x+32, y+27, 9, 9)
        self.currentSam = self.normalSam
        self.powered = False
        self.healingSam = False
        self.shoots = []
        self.healingCounter = 0
        self.mask = pygame.mask.from_surface(self.currentSam[0])
        self.poweupMask = pygame.mask.from_surface(self.powerup)
        self.powerMask = pygame.mask.from_surface(self.power)
        self.bottom = bottom - height
        self.top = top
        self.points = 0
        self.pointsrectangle = pygame.Rect(3,3,(15+3)*5,15)
        self.total_crystals = total_crystals
        self.crystals = 0
        self.shipflag = 0
        self.levelmode = True
    
    def drawPoints(self,mw):
        self.image = pygame.font.SysFont('verdana', 15,True).render(str(self.points),True,(255, 255, 255))
        mw.blit(self.image, (self.pointsrectangle.x, self.pointsrectangle.y))
    
    def resetCrystals(self,total_crystals):
        self.crystals = 0
        self.total_crystals = total_crystals
    
    def changeSam(self, type):
        if type == 'normal':
            self.currentSam = self.normalSam
            self.powered = False
        elif type == 'powered':
            self.currentSam = self.poweredSam
            self.powered = True
        elif type == 'healing':
            self.currentSam = self.healingSamImage
            self.powered = False
    
    def setPowerUps(self, powerupList): #powerupListExample: (65,250)
        for i in powerupList:
            self.powerupsRect.append(pygame.Rect(i[0], i[1], 15, 15))
    
    def drawPowerUps(self,mw):
        count = 0
        for i in self.powerupsRect:
            if self.rect.x >= 125 and not endslide:
                self.powerupsRect[count][0] -= slide
            mw.blit(self.powerup,(i[0],i[1]))
            if i.colliderect(self.rect):
                offset = (i[0]-self.rect.x,i[1]-self.rect.y)
                if self.mask.overlap(self.poweupMask, offset) and not self.healingSam:
                    self.changeSam('powered')
                    self.powerupsRect.pop(count)
            count += 1
              
    def move_up(self,mw):
        if self.rect.y > self.top:
            self.rect.y -= 20
        else:
            self.rect.y = self.rect.y
        if self.rect.x < 125 or (self.shipflag >= 1485 and self.rect.x <495-44):
            self.rect.x += 5
        self.powerRect.y = self.rect.y + 27 
        self.powerRect.x = self.rect.x + 32
        mw.blit(self.currentSam[1], (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.currentSam[1])
    
    def fall(self,mw):
        if self.rect.y < self.bottom:
            self.rect.y += 3
        else:
            self.rect.y = self.rect.y
        self.powerRect.y = self.rect.y + 27 
        self.powerRect.x = self.rect.x + 32
        mw.blit(self.currentSam[0], (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.currentSam[0])
    
    def shootings(self,mw,plant = [],bat=[],snail=[]):
        count = 0
        if self.shoots:
            for i in self.shoots:
                if i:
                    mw.blit(self.power, (i[0], i[1]))
                    shootingRect = pygame.Rect(i[0], i[1], 9, 9)
                    count2 = 0
                    for p in plant:
                        if shootingRect.colliderect(p.mouthRectangle):
                            offset = (p.mouthRectangle.x - i[0], p.mouthRectangle.y - i[1]) 
                            if self.powerMask.overlap(p.plantMasks[p.top],offset):
                                plant.pop(count2)
                        count2 += 1
                    count2 = 0 
                    for b in bat:
                        if shootingRect.colliderect(b.rectangles[b.cycle]):
                            offset = (b.rectangles[b.cycle].x - i[0], b.rectangles[b.cycle].y - i[1]) 
                            if self.powerMask.overlap(b.curr_mask,offset):
                                bat.pop(count2)
                        count2 += 1
                    count2 = 0
                    for s in snail:
                        if shootingRect.colliderect(s.rectangles[s.cycle]):
                            offset = (s.rectangles[s.cycle].x - i[0], s.rectangles[s.cycle].y - i[1]) 
                            if self.powerMask.overlap(s.curr_mask,offset):
                                snail.pop(count2)
                        count2 += 1
                    self.shoots[count][0] += 3
                    self.shoots[count][2] += 1
                    if self.shoots[count][2] == 60: 
                        self.shoots.pop(count)
                count += 1              
    
    def shoot(self, mw):
        if self.powered:
            mw.blit(self.power, (self.powerRect.x, self.powerRect.y))
            self.shoots.append([self.powerRect.x, self.powerRect.y, 0])
    
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
    
    def healing(self):
        if self.healingSam:
            self.healingCounter += 1
        if self.healingSam and self.healingCounter == 60:
            self.healingSam = False
            self.healingCounter = 0
            self.changeSam('normal')
    
    def showPoints(self):
        #print(self.points)
        if self.crystals == self.total_crystals:
            return True
    
class Crystal():
    def __init__(self, filename, x, y, width=15, height=15):
        self.image =  pygame.image.load(filename)
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)
        self.points = 15
        
    def draw(self,mw,sam):
        if sam.rect.x >= 125 and not endslide:
            self.rect.x -= slide
        mw.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.colliderect(sam.rect) and not sam.healingSam:
            offset = (self.rect.x - sam.rect.x, self.rect.y - sam.rect.y)
            if sam.mask.overlap(self.mask, offset):
                sam.points += self.points
                sam.crystals += 1
                return True
    
class Lives():
    def __init__(self, filename, life, positions, x=495, y=3, width=15, height=15):
        Picture.__init__(self, filename, x, y, width, height)
        self.lives = 3
        #self.lives = 30
        self.width = width
        self.height = height
        self.x_max = x
        self.y_min = y
        self.lifeImage = pygame.image.load(life)
        self.maskLifeImage = pygame.mask.from_surface(self.lifeImage) 
        self.lifeRects = []
        for i in positions:
            self.lifeRects.append(pygame.Rect(i[0], i[1], width, height))
    
    def updatePositions(self,positions):
        self.lifeRects.clear()
        for i in positions:
            self.lifeRects.append(pygame.Rect(i[0], i[1], self.width, self.height))
        
    def chargeLives(self):
        self.rectangles = []
        self.space = 3
        for i in range(self.lives):
            self.rectangles.append(pygame.Rect(self.x_max-(self.space+self.width)*(i+1), self.y_min, self.width, self.height))
    
    def drawLives(self,mw):
        for i in range(self.lives):
            mw.blit(self.image, (self.rectangles[i].x, self.rectangles[i].y))
        
    def drawLifeUps(self,mw,sam):
        count = 0
        for i in self.lifeRects:
            if sam.rect.x >= 125 and not endslide:
                self.lifeRects[count][0] -= slide
            mw.blit(self.lifeImage,(i.x,i.y))
            if i.colliderect(sam.rect) and not sam.healingSam:
                offset = (i.x - sam.rect.x, i.y - sam.rect.y)
                if sam.mask.overlap(self.maskLifeImage, offset):
                    self.lives += 1
                    self.lifeRects.pop(count)
            count += 1
        
class Plant():
    def __init__(self, stem, open_mouth, mouth, top = 30, x=250, y=485,reverseP = False,staticP = False,width=15, height=15):
        self.rectangles = []
        self.plant = []
        self.plantMasks = []
        self.cycle = 0
        self.up = True
        self.move_mouth = 0
        self.wait_mouth = 0
        self.mouth = [pygame.image.load(open_mouth),pygame.image.load(mouth)]
        self.top = top
        self.reverseP = reverseP
        self.staticP = staticP
        if reverseP:
            y = 0
            height = height*(-1)
            self.mouth = [pygame.transform.flip(self.mouth[0],False,True),pygame.transform.flip(self.mouth[1],False,True)]
        for i in range(self.top):
            self.rectangles.append(pygame.Rect(x, y-height*i, width, height))
            self.plant.append(pygame.image.load(stem))
            self.plantMasks.append(pygame.mask.from_surface(self.plant[i]))
        self.rectangles.append(pygame.Rect(x, y-height*self.top, width, height))
        self.plantMasks.append(pygame.mask.from_surface(self.mouth[0]))
        self.mouthRectangle = self.rectangles[self.top]
    
    def draw(self,mw,i): #mw main window
        mw.blit(self.plant[i], (self.rectangles[i].x, self.rectangles[i].y))
        
    def draw_mouth(self,mw,i,mouth):
        mw.blit(mouth, (self.rectangles[i].x, self.rectangles[i].y))
        
    def delete_plant(self):
        self.rectangles = []
        self.plant = []
        self.cycle = 0
        self.up = True
        self.move_mouth = 0
        self.wait_mouth = 0
        
    def movingPlant(self,mw,sam,lives):
        if self.rectangles and (not self.staticP):
            if sam.rect.x >= 125 and not endslide:
                for i in range(self.top):
                    self.rectangles[i][0] -= slide
                self.rectangles[self.top][0] -= slide
                self.mouthRectangle = self.rectangles[self.top][0]
            for i in range(self.cycle):
                self.draw(mw,i)
                if self.rectangles[i].colliderect(sam.rect) and not sam.healingSam:
                    offset = (self.rectangles[i].x - sam.rect.x, self.rectangles[i].y - sam.rect.y)
                    if sam.mask.overlap(self.plantMasks[i], offset):
                        if not sam.powered:
                            lives.lives -= 1
                        sam.healingSam = True
                        sam.changeSam('healing')
            self.draw(mw,self.cycle)
            if self.rectangles[self.cycle].colliderect(sam.rect) and not sam.healingSam:
                offset = (self.rectangles[self.cycle].x - sam.rect.x, self.rectangles[self.cycle].y - sam.rect.y)
                if sam.mask.overlap(self.plantMasks[self.cycle], offset):
                    if not sam.powered:
                        lives.lives -= 1
                    sam.healingSam = True
                    sam.changeSam('healing')
            if self.cycle <= self.top-1:
                self.draw_mouth(mw,self.cycle+1,self.mouth[self.move_mouth])
                self.mouthRectangle = self.rectangles[self.cycle+1]
                if self.rectangles[self.cycle+1].colliderect(sam.rect) and not sam.healingSam:
                    offset = (self.rectangles[self.cycle+1].x - sam.rect.x, self.rectangles[self.cycle+1].y - sam.rect.y)
                    if sam.mask.overlap(self.plantMasks[self.top-1], offset):
                        if not sam.powered:
                            lives.lives -= 1
                        sam.healingSam = True
                        sam.changeSam('healing')
            if self.cycle == self.top-1:
                self.up = False
            elif self.cycle == 0:
                self.up = True 
            if self.up:
                self.cycle += 1
            else:
                self.cycle -= 1
            
            if self.wait_mouth >= 6:
                if self.move_mouth == 0:
                    self.move_mouth = 1
                    self.plantMasks[self.top] = pygame.mask.from_surface(self.mouth[1])
                else:
                    self.move_mouth = 0
                    self.plantMasks[self.top] = pygame.mask.from_surface(self.mouth[0])
                self.wait_mouth = 0
            self.wait_mouth += 1
        elif self.rectangles and self.staticP:
            for i in range(self.top):
                if sam.rect.x >= 125 and not endslide:
                    self.rectangles[i][0] -= slide
                self.draw(mw,i)
                if self.rectangles[i].colliderect(sam.rect) and not sam.healingSam:
                    offset = (self.rectangles[i].x - sam.rect.x, self.rectangles[i].y - sam.rect.y)
                    if sam.mask.overlap(self.plantMasks[i], offset):
                        if not sam.powered:
                            lives.lives -= 1
                        sam.healingSam = True
                        sam.changeSam('healing')
            if sam.rect.x >= 125 and not endslide:
                self.rectangles[self.top][0] -= slide
            self.draw_mouth(mw,self.top,self.mouth[self.move_mouth])
            if self.wait_mouth >= 6:
                if self.move_mouth == 0:
                    self.move_mouth = 1
                    self.plantMasks[self.top] = pygame.mask.from_surface(self.mouth[1])
                else:
                    self.move_mouth = 0
                    self.plantMasks[self.top] = pygame.mask.from_surface(self.mouth[0])
                self.wait_mouth = 0
            self.wait_mouth += 1

class Bat():
    def __init__(self, flying1, flying2, flying3, flying4, x, y, steps, width=15, height = 15):
        self.bat = [pygame.image.load(flying1),pygame.image.load(flying2),pygame.image.load(flying3),pygame.image.load(flying4)]
        self.flip = False
        self.rectangles = []
        self.cycle = 0
        self.frame = 1
        self.steps = steps
        for i in range(steps):
            self.rectangles.append(pygame.Rect(x-width*i, y, width, height))
        self.masks = [pygame.mask.from_surface(self.bat[0]),pygame.mask.from_surface(self.bat[1]),pygame.mask.from_surface(self.bat[2]),pygame.mask.from_surface(self.bat[3])]
        self.curr_mask = self.masks[0]
        
    def draw_bat(self,mw,i,bat):
        mw.blit(bat, (self.rectangles[i].x, self.rectangles[i].y))
    
    def movingBat(self,mw,sam,lives):
        if sam.rect.x >= 125 and not endslide:
            for i in range(self.steps):
                self.rectangles[i].x -= slide
        if self.flip:
            self.draw_bat(mw,self.cycle,self.bat[1*self.frame+1])
            self.curr_mask = self.masks[1*self.frame+1]
        else:
            self.draw_bat(mw,self.cycle,self.bat[1*self.frame-1])
            self.curr_mask = self.masks[1*self.frame-1]
        if self.rectangles[self.cycle].colliderect(sam.rect) and not sam.healingSam:
            offset = (self.rectangles[self.cycle].x - sam.rect.x, self.rectangles[self.cycle].y - sam.rect.y)
            if sam.mask.overlap(self.curr_mask, offset):
                if not sam.powered:
                    lives.lives -= 1
                sam.healingSam = True
                sam.changeSam('healing')  
        if self.cycle == (self.steps-1) and self.flip == False:
            self.flip = True
        elif self.cycle == 0 and self.flip == True:
            self.flip = False
        if self.flip:
            self.cycle -= 1
        else:
            self.cycle += 1
            
        if self.frame == 1:
            self.frame = 2
        elif self.frame == 2:
            self.frame = 1

class Flame():
    def __init__(self,flame1,flame2,x, y=455, width=15, height = 45):
        self.flame = [pygame.image.load(flame1),pygame.image.load(flame2)]   
        self.rectangle = pygame.Rect(x, y, width, height)
        self.changeFrame = False
        self.ticksxframe = 5
        self.frame = 0
        self.flameMasks = [pygame.mask.from_surface(self.flame[0]),pygame.mask.from_surface(self.flame[1])]

    def draw(self,mw,sam,lives):
        if sam.rect.x >= 125 and not endslide:
            self.rectangle.x -= slide
        mw.blit(self.flame[self.frame], (self.rectangle.x, self.rectangle.y))
        if self.rectangle.colliderect(sam.rect) and not sam.healingSam:
            offset = (self.rectangle.x - sam.rect.x, self.rectangle.y - sam.rect.y)
            if sam.mask.overlap(self.flameMasks[self.frame], offset):
                if not sam.powered:
                    lives.lives -= 1
                sam.healingSam = True
                sam.changeSam('healing')  
        if self.ticksxframe == 0:
            if self.changeFrame:
                self.changeFrame = False
                self.frame = 0
            else:
                self.changeFrame = True
                self.frame = 1
            self.ticksxframe = 5
        self.ticksxframe -= 1

sliding = False       
class Spike():
    
    def __init__(self,picture,x=0, y=480, width=15, height = 15):
        self.picture = pygame.image.load(picture)   
        self.rectangle = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.picture)

    def draw(self,mw,sam,lives):
        global sliding
        if sam.rect.x >= 125 and not endslide:
            self.rectangle.x -= slide
            sliding = True
        mw.blit(self.picture, (self.rectangle.x, self.rectangle.y))
        if self.rectangle.colliderect(sam.rect) and not sam.healingSam:
            offset = (self.rectangle.x - sam.rect.x, self.rectangle.y - sam.rect.y)
            if sam.mask.overlap(self.mask, offset):
                if not sam.powered:
                    lives.lives -= 1
                sam.healingSam = True
                sam.changeSam('healing')
                
class Snail():
    def __init__(self, frame1, frame2, frame3, frame4, turns, x, y=485, width=15, height=15):
        self.snail = [pygame.image.load(frame1), pygame.image.load(frame2), pygame.image.load(frame3), pygame.image.load(frame4)]
        self.snailMasks = [pygame.mask.from_surface(self.snail[0]), pygame.mask.from_surface(self.snail[1]), pygame.mask.from_surface(self.snail[2]), pygame.mask.from_surface(self.snail[3])]
        self.top = 4
        self.turns = turns
        self.cycle = 0
        self.frame = 0
        self.up = True
        self.rectangles = []
        for i in range(self.top * self.turns):
            self.rectangles.append(pygame.Rect(x, y - i * height, width, height))
            #hay hasta el nro 15 y el nro 23
        self.curr_mask = self.snailMasks[0]
    
    def draw(self, mw, frame, i):  # mw main window
        mw.blit(self.snail[frame], (self.rectangles[i].x, self.rectangles[i].y))

    def movingSnail(self, mw, sam, lives):
        # Update snail's horizontal position
        if sam.rect.x >= 125 and not endslide:
            for i in range(self.top * self.turns):
                self.rectangles[i].x -= slide
        #print(self.rectangles[self.cycle].x)
        
        # Draw the snail based on the current frame and cycle
        self.draw(mw, self.frame, self.cycle)
        self.curr_mask = self.snailMasks[self.frame]

        # Collision detection with Sam
        if self.rectangles[self.cycle].colliderect(sam.rect) and not sam.healingSam:
            offset = (self.rectangles[self.cycle].x - sam.rect.x, self.rectangles[self.cycle].y - sam.rect.y)
            if sam.mask.overlap(self.snailMasks[self.frame], offset):
                if not sam.powered:
                    lives.lives -= 1
                sam.healingSam = True
                sam.changeSam('healing')

        # Adjust frame cycling for animation
        if self.frame >= self.top - 1:
            self.frame = 0  # Reset frame to loop the animation

        # Adjust cycle movement logic
        if self.cycle == (self.top * self.turns) - 1:
            self.up = False
        elif self.cycle == 0:
            self.up = True

        if self.up:
            self.cycle += 1
        else:
            self.cycle -= 1

        # Prevent the cycle from going out of bounds
        if self.cycle < 0:
            self.cycle = 0
            self.up = True
        elif self.cycle >= self.top * self.turns:
            self.cycle = self.top * self.turns - 1
            self.up = False
        
        # Smooth frame update to match the animation timing
        self.frame += 1
        if self.frame >= self.top:
            self.frame = 0  # Reset frame if it exceeds the available frames

#def resetObjects(sam,plant,bat,flame,snail,lives,spikes,crystals):
    
def setLevel1(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals):
    lifehearts = []
    powerups = []
    plant_top = 33
    plant_count = 0
    y = 0
    for i in range(bottom_tiles*screens):
        spikes.append(Spike('spike/spike.png',i*tile_size))
        if i >= 6:
            if i%4 == 0 and i<=bottom_tiles:
                plant_count += 1
                plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',plant_top - plant_count,i*tile_size))
                if plant_count <= 6 and len(crystals)<total_crystals:
                    crystals.append(Crystal("crystal.png",i*tile_size + 30,plant_count*tile_size))
            if i == bottom_tiles:
                plant_count = 0
            if i > bottom_tiles and i<=bottom_tiles*2:
                if i%3 == 0 and i%2==0:
                    plant_count += 1
                    if plant_count == 1:
                        powerups.append([(i+2)*tile_size,(y+3)*tile_size])
                    bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,(y+4)*tile_size,4))
                    if plant_count%2 == 0:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,(i*tile_size)+45,485,True))
                        if plant_count == 6:
                            bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',(i*tile_size)+45,140,4))
                    else:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',20,(i*tile_size)+45,485))
                        if len(crystals)<total_crystals and plant_count>1:
                            crystals.append(Crystal("crystal.png",(i*tile_size)+45,150))
            if i == bottom_tiles*2:
                plant_count = 0
            if i > bottom_tiles*2 and i<=bottom_tiles*3:
                if i>(bottom_tiles*2)+5:
                    if i%2 == 0 and i%4 != 0:
                        if plant_count%3 == 0 and len(crystals)<total_crystals:
                            crystals.append(Crystal("crystal.png",i*tile_size,(16-plant_count+3)*tile_size))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10+plant_count,i*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',16-plant_count,i*tile_size,485,True,True))
                        plant_count += 1
            if i == bottom_tiles*3:
                plant_count = 0
                powerups.append([i*tile_size+int(bottom_tiles/2)*tile_size,(screen_height-255)-int((screen_height-255-165)/2)])
            if i > bottom_tiles*3 and i <= bottom_tiles*4:
                if i%7 == 0:
                    bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,255,6))
                    bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,165,6))
                    #if i == 126:
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,(i+1)*tile_size,485,False,True))
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,(i+1)*tile_size,485,True,True))
                if i>126:
                    if i == 127:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,i*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,i*tile_size,485,True,True))
                        if len(lifehearts)<3:
                            lifehearts.append([i*tile_size+tile_size*3, int(screen_height/2)])    
                    if i == 132:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,(i+2)*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,(i+2)*tile_size,485,True,True))
            if i == bottom_tiles * 4:
                plant_count = 0
            if i > bottom_tiles * 4 and i <= bottom_tiles*5:
                if i >= 141:
                    plant_count += 1
                    if i == 141:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,i*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,i*tile_size,485,True,True))
                    if plant_count%16 == 0:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,i*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,i*tile_size,485,True,True))
                    elif plant_count%8 == 0:
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,i*tile_size,485,False,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,True,True))
                    if plant_count == 16:
                        powerups.append([i*tile_size+tile_size*3, int(screen_height/2)])            
            if i == bottom_tiles * 5:
                plant_count = 0
            if i > bottom_tiles * 5 and i <= bottom_tiles*6:
                if i%2 == 0:
                    plant_count += 1
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,True,True))
                    if plant_count%5 == 0 and len(crystals)<total_crystals:
                        crystals.append(Crystal("crystal.png",i*tile_size,285))
                    if plant_count%8 == 0 and plant_count != 16:
                        powerups.append([i*tile_size,300])
                    if plant_count == 16:
                        lifehearts.append([i*tile_size,300])
            if i == bottom_tiles * 6:
                plant_count = 0
            if i > bottom_tiles * 6 and i <= bottom_tiles*7:
                plant_count += 1
                if i == 199:
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,True,True))
                if plant_count%16 == 0:
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,True,True))
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size,300))
                elif plant_count%8 == 0 and plant_count%14 != 0:
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,False,True))
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',8,i*tile_size,485,True,True))
            if i == bottom_tiles * 7:
                plant_count = 0
                bat_count = 0
            if i > bottom_tiles * 7 and i <= bottom_tiles*8:
                if i >= 237:
                    bat_count += 1
                    if i == 237:
                        bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,270,3))
                        bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,360,3))
                    if bat_count%8 == 0:
                        plant_count += 1
                        if plant_count%2 == 0:
                            bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,270,3))
                            bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,360,3))
                        else:
                            bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,180,3))
                            bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,270,3))
                            if len(crystals)<20:
                                crystals.append(Crystal("crystal.png",i*tile_size+15,180+45))
            if i == bottom_tiles * 8:
                plant_count = 0
                bat_count = 0
            if i > bottom_tiles * 8 and i <= bottom_tiles*9:
                if i%4 == 0:
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',11+plant_count,i*tile_size,485,True))
                    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',16-plant_count,i*tile_size,485,False,True))
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size+15*2,(11+plant_count)*15+15+int(45/2)))
                    plant_count += 1
            if i == bottom_tiles * 9:
                plant_count = 0
                bat_count = 0
            if i > bottom_tiles * 9 and i <= bottom_tiles*10:
                if i == 300:
                    bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,255,3))
                    bat.append(Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',i*tile_size,255+45+15*2,3))
                    if len(lifehearts)<3:
                        lifehearts.append([i*tile_size,int(((255+45+15*2)-255)/2)+255])
                if i>300:
                    if i%4 == 0:
                        if i < 324:
                            plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',17,i*tile_size,485,True,True))
                        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,i*tile_size,485))
        if y == (bottom_tiles-1):
            y = 0
        else:
            y += 1  
    #print(len(crystals))
    #print(len(lifehearts))
    lives.append(Lives('lives/lifeTop.png','lives/life.png',lifehearts))
    sam[0].setPowerUps(powerups)
    lives[0].chargeLives()

def setLevel2(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals):
    lifehearts = []
    powerups = []
    plant_top = 33
    plant_count = 0
    y = 0
    for i in range(bottom_tiles*screens):
        spikes.append(Spike('spike/bluespike.png',i*tile_size))
        if i >= 6:
            if i%4 == 0 and i<=bottom_tiles:
                plant_count += 1
                if plant_count == 1:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',28 - plant_count,i*tile_size,485,True))
                else:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',29 - plant_count,i*tile_size,485,True))
                    if plant_count <= 6 and len(crystals)<total_crystals:
                        crystals.append(Crystal("crystal.png",i*tile_size + 30,465-plant_count*15))
                    if i==32:
                        flame.append(Flame('flame/flame1.png','flame/flame2.png',i*tile_size))
            if i == bottom_tiles:
                plant_count = 0
            if i > bottom_tiles and i<=bottom_tiles*2:
                if i%2 == 0 and i<36:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',25,i*tile_size,485,True,True))
                    flame.append(Flame('flame/flame1.png','flame/flame2.png',i*tile_size))
                if i%3 == 0 and i%2==0:
                    plant_count += 1
                    if plant_count == 1:
                        powerups.append([i*tile_size,450])
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,(y+4)*tile_size,4))
                    if plant_count%2 == 0:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',6,(i*tile_size)+45,485))
                        bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',(i*tile_size)+45+15*2,325,4))
                        #105
                        #if plant_count == 6:
                        #    bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',(i*tile_size)+45,140,4))
                    else:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',26,(i*tile_size)+45,485,True))
                        flame.append(Flame('flame/flame1.png','flame/flame2.png',(i*tile_size)+45))
                        if len(crystals)<total_crystals and plant_count>1:
                            crystals.append(Crystal("crystal.png",(i*tile_size)+45,435))
            if i == bottom_tiles*2:
                plant_count = 0
            if i > bottom_tiles*2 and i<=bottom_tiles*3:
                if i>(bottom_tiles*2)+5:
                    if i%2 == 0 and i%4 != 0:
                        if plant_count%3 == 0 and len(crystals)<total_crystals:
                            crystals.append(Crystal("crystal.png",i*tile_size,(20-plant_count+3)*tile_size))#4
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',6+plant_count,i*tile_size,485,False,True))#4
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',20-plant_count,i*tile_size,485,True,True))#4
                        plant_count += 1
            if i == bottom_tiles*3:
                plant_count = 0
                powerups.append([i*tile_size+int(bottom_tiles/2)*tile_size,((screen_height-255)-int((screen_height-255-165)/2)+120)])
                crystals.append(Crystal("crystal.png",(i*tile_size+int(bottom_tiles/2)*tile_size)-15,((screen_height-255)-int((screen_height-255-165)/2)+120)))
                crystals.append(Crystal("crystal.png",(i*tile_size+int(bottom_tiles/2)*tile_size)+15,((screen_height-255)-int((screen_height-255-165)/2)+120)))
            if i > bottom_tiles*3 and i <= bottom_tiles*4:
                flame.append(Flame('flame/flame1.png','flame/flame2.png',i*tile_size))
                if i%7 == 0:
                    bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',(i+1)*tile_size,300,3))
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,165,6))
                    #if i == 126:
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,(i+1)*tile_size,485,False,True))
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,(i+1)*tile_size,485,True,True))
                if i>126:
                    if i == 127:
                        #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',15,i*tile_size,485,False,True))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',25,i*tile_size+15*3,485,True,True))
                        if len(lifehearts)<3:
                            lifehearts.append([i*tile_size+tile_size*3, 435])    
                    #if i == 132:
                    #    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,(i+2)*tile_size,485,False,True))
                    #    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,(i+2)*tile_size,485,True,True))
            if i == bottom_tiles * 4:
                plant_count = 0
            if i > bottom_tiles * 4 and i <= bottom_tiles*5:
                if i >= 141:
                    plant_count += 1
                    if i == 141:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',12,i*tile_size,485,False))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',13,i*tile_size,485,True))
                    if plant_count%16 == 0:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',12,i*tile_size,485,False))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',13,i*tile_size,485,True))
                    elif plant_count%8 == 0:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',9,i*tile_size,485,False))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',19,i*tile_size,485,True))
                    if plant_count == 16:
                        powerups.append([i*tile_size+tile_size*3, int(screen_height/2)])            
            if i == bottom_tiles * 5:
                plant_count = 0
            if i > bottom_tiles * 5 and i <= bottom_tiles*6:
                if i%2 == 0:
                    plant_count += 1
                    if plant_count == 1:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,i*tile_size,485,False,True))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,i*tile_size,485,True,True))    
                    else:
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',9,i*tile_size,485,False,True))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',19,i*tile_size,485,True,True))
                        if plant_count%5 == 0 and len(crystals)<total_crystals:
                            crystals.append(Crystal("crystal.png",i*tile_size,285+15*2))
                        if plant_count%8 == 0 and plant_count != 16:
                            powerups.append([i*tile_size,300])
                        if plant_count == 16:
                            lifehearts.append([i*tile_size,300])
            if i == bottom_tiles * 6:
                plant_count = 0
            if i > bottom_tiles * 6 and i <= bottom_tiles*7:
                flame.append(Flame('flame/flame1.png','flame/flame2.png',i*tile_size))
                plant_count += 1
                if i == 199:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,i*tile_size,485,True,True))
                if plant_count%16 == 0:
                    #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17+8,i*tile_size,485,True,True))
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size-15*5,300))
                elif plant_count%8 == 0 and plant_count%14 != 0:
                    #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,i*tile_size,485,False,True))
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8+8,i*tile_size,485,True,True))
            if i == bottom_tiles * 7:
                plant_count = 0
                bat_count = 0
                bat_count2 = 0
            if i > bottom_tiles * 7 and i <= bottom_tiles*8:
                plant_count += 1
                if plant_count == 7:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',27,i*tile_size,485,True,True))
                if plant_count == 18:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',27,i*tile_size,485,True,True))
                if plant_count == 23:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',27,i*tile_size,485,True,True))
                if i >= 237:
                    bat_count += 1
                    if i == 237:
                        bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,270,3))
                        bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,360,3))
                    if bat_count%8 == 0:
                        bat_count2 += 1
                        if bat_count2%2 == 0:
                            bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,270,3))
                            bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,360,3))
                        else:
                            bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,180,3))
                            bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,270,3))
                            if len(crystals)<20:
                                crystals.append(Crystal("crystal.png",i*tile_size+15,370))
            if i == bottom_tiles * 8:
                plant_count = 0
                bat_count = 0
                bat_count2 = 0
            if i > bottom_tiles * 8 and i <= bottom_tiles*9:
                if i%4 == 0:
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',15+plant_count,i*tile_size,485,True,True))
                    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',12-plant_count,i*tile_size,485,False,True))
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size+15*2,(15+plant_count)*15+15+int(45/2)))
                    plant_count += 1
            if i == bottom_tiles * 9:
                plant_count = 0
                bat_count = 0
            if i > bottom_tiles * 9 and i <= bottom_tiles*10:
                if i == 300:
                    bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,255,3))
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,255+45+15*2,3))
                    if len(lifehearts)<3:
                        lifehearts.append([i*tile_size,int(((255+45+15*2)-255)/2)+255])
                if i>300:
                    if i%4 == 0:
                        if i < 324:
                            plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17-plant_count,i*tile_size,485,True,True))
                        plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',10+plant_count,i*tile_size,485,False,True))
                        plant_count += 1
        if y == (bottom_tiles-1):
            y = 0
        else:
            y += 1  
    #print(len(crystals))
    #print(len(lifehearts))
    #lives.append(Lives('lives/lifeTop.png','lives/life.png',lifehearts))
    lives[0].updatePositions(lifehearts)
    sam[0].setPowerUps(powerups)
    lives[0].chargeLives()
    
def setLevel3(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals):
    lifehearts = []
    powerups = []
    plant_top = 33
    plant_count = 0
    y = 0
    for i in range(bottom_tiles*screens):
        spikes.append(Spike('spike/orangespike.png',i*tile_size))
        if i >= 6:
            if i%4 == 0 and i<=bottom_tiles:
                plant_count += 1
                for t in range(plant_count):
                    flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size,455+t*45-(plant_count-1)*5))
                for e in range(9):
                    flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size,350-(e*45)-plant_count*5))
            if i == bottom_tiles:
                plant_count = 0
            if i > bottom_tiles and i<=bottom_tiles*2:
                if i%2 == 0:
                    if i == 34:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',23,i*tile_size,485,True,True))
                    else:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',25,i*tile_size,485,True,True))
                    flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size))
                if i%3 == 0 and i%2==0:
                    plant_count += 1
                    if plant_count == 1:
                        powerups.append([i*tile_size,430])
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,(y+4)*tile_size,4))
                    if plant_count%2 == 0:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',6,(i*tile_size)+45,485))
                        if plant_count == 6:
                            powerups.append([(i*tile_size)+45+15*8,340])
                        #bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',(i*tile_size)+45+15*2,325,4))
                        #105
                        #if plant_count == 6:
                        #    bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',(i*tile_size)+45,140,4))
                    else:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',26,(i*tile_size)+45,485,True))
                        flame.append(Flame('flame/redflame1.png','flame/redflame2.png',(i*tile_size)+45))
                        if len(crystals)<total_crystals and plant_count>1:
                            crystals.append(Crystal("crystal.png",(i*tile_size)+45,435))
            if i == bottom_tiles*2:
                plant_count = 0
            if i > bottom_tiles*2 and i<=bottom_tiles*3:
                if i>(bottom_tiles*2)+5:
                    if i%2 == 0 and i%4 != 0:
                        if plant_count%3 == 0 and len(crystals)<total_crystals:
                            crystals.append(Crystal("crystal.png",i*tile_size,(20-plant_count+3)*tile_size))#4
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',9+plant_count,i*tile_size,485))#4
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',20-plant_count,i*tile_size,485,True,True))#4
                        if plant_count == 6:
                            powerups.append([i*tile_size+15*3,((screen_height-255)-int((screen_height-255-165)/2)+120)])
                        plant_count += 1
            if i == bottom_tiles*3:
                plant_count = 0
                #powerups.append([i*tile_size+int(bottom_tiles/2)*tile_size,((screen_height-255)-int((screen_height-255-165)/2)+120)])
                crystals.append(Crystal("crystal.png",(i*tile_size+int(bottom_tiles/2)*tile_size)-15,((screen_height-255)-int((screen_height-255-165)/2)+120)))
                crystals.append(Crystal("crystal.png",(i*tile_size+int(bottom_tiles/2)*tile_size)+15,((screen_height-255)-int((screen_height-255-165)/2)+120)))
            if i > bottom_tiles*3 and i <= bottom_tiles*4:
                flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size))
                flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size,455-45))
                if i%7 == 0:
                    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',(i+1)*tile_size,300,3))
                    snail.append(Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',8,(i+1)*tile_size))
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,165,6))
                    #if i == 126:
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',15,(i+1)*tile_size,485,False,True))
                    #    plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,(i+1)*tile_size,485,True,True))
                if i>126:
                    if i == 127:
                        #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',15,i*tile_size,485,False,True))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',22,i*tile_size+15*3,485,True,True))
                        if len(lifehearts)<3:
                            lifehearts.append([i*tile_size+tile_size*3, 435])    
                    #if i == 132:
                    #    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,(i+2)*tile_size,485,False,True))
                    #    plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,(i+2)*tile_size,485,True,True))
            if i == bottom_tiles * 4:
                plant_count = 0
            if i > bottom_tiles * 4 and i <= bottom_tiles*5:
                if i >= 141:
                    plant_count += 1
                    if i == 141:
                        powerups.append([i*tile_size-tile_size*5, screen_height-tile_size*7])  
                        #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',12,i*tile_size,485,False))
                        snail.append(Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',8,i*tile_size))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',13,i*tile_size,485,True,True))
                    if plant_count%16 == 0:
                        #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',12,i*tile_size,485,False))
                        snail.append(Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',8,i*tile_size))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',13,i*tile_size,485,True,True))
                    elif plant_count%8 == 0:
                        #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',9,i*tile_size,485,False))
                        snail.append(Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',8,i*tile_size))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',19,i*tile_size,485,True,True))          
                    if plant_count == 24:
                        powerups.append([i*tile_size-5*tile_size, screen_height-tile_size*7])
            if i == bottom_tiles * 5:
                plant_count = 0
            if i > bottom_tiles * 5 and i <= bottom_tiles*6:
                if i%2 == 0:
                    plant_count += 1
                    if plant_count == 1:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',2,i*tile_size,485,False,True))#6
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',23,i*tile_size,485,True,True))    
                    else:
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',4,i*tile_size,485,False))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',25,i*tile_size,485,True,True))
                        if plant_count%5 == 0 and len(crystals)<total_crystals:
                            crystals.append(Crystal("crystal.png",i*tile_size,285+15*2+15*6))#6
                        if plant_count%8 == 0 and plant_count != 16:
                            powerups.append([i*tile_size,300+15*7])
                        if plant_count == 16:
                            lifehearts.append([i*tile_size,300+15*7])
            if i == bottom_tiles * 6:
                plant_count = 0
            if i > bottom_tiles * 6 and i <= bottom_tiles*7:
                flame.append(Flame('flame/redflame1.png','flame/redflame2.png',i*tile_size))
                plant_count += 1
                if i == 199:
                    powerups.append([i*tile_size,415])
                    #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',8,i*tile_size,485,False,True))
                    #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',17,i*tile_size,485,True,True))
                if plant_count%16 == 0:
                    #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',8,i*tile_size,485,False,True))
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',17+12,i*tile_size,485,True))#4
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size-15*13,415))
                elif plant_count%8 == 0 and plant_count%14 != 0:
                    #plant.append(Plant('plant/blueplant3.png','plant/blueplant1.png','plant/blueplant2.png',17,i*tile_size,485,False,True))
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',8+12,i*tile_size,485,True))
            if i == bottom_tiles * 7:
                plant_count = 0
                bat_count = 0
                bat_count2 = 0
            if i > bottom_tiles * 7 and i <= bottom_tiles*8:
                plant_count += 1
                if plant_count == 7:
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',32,i*tile_size,485,True))
                if plant_count == 18:
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',32,i*tile_size,485,True))
                if plant_count == 23:
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',32,i*tile_size,485,True))
                if i >= 237:
                    bat_count += 1
                    if bat_count%8 == 0:
                        #bat_count2 += 1
                        #if bat_count2%2 == 0:
                        #    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size,270,3))
                        #    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size,360,3))
                        #else:
                        #    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size,180,3))
                        #    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size,270,3))
                        if len(crystals)<20:
                            crystals.append(Crystal("crystal.png",i*tile_size+15,415))
            if i == bottom_tiles * 8:
                plant_count = 0
                bat_count = 0
                bat_count2 = 0
            if i > bottom_tiles * 8 and i <= bottom_tiles*9:
                if i%4 == 0:
                    if plant_count == 0:
                        powerups.append([i*tile_size-15*3,415])
                    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',20+plant_count,i*tile_size,485,True,True))
                    #plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',12-plant_count,i*tile_size,485,False,True))
                    snail.append(Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',12-plant_count,i*tile_size))
                    if len(crystals)<20:
                        crystals.append(Crystal("crystal.png",i*tile_size+15*2,(15+plant_count)*15+15+int(45/2)+15*5))
                    plant_count += 1
            if i == bottom_tiles * 9:
                plant_count = 0
                bat_count = 0
            if i > bottom_tiles * 9 and i <= bottom_tiles*10:
                if i == 300:
                    bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size,255,3))
                    #bat.append(Bat('bat/bluebat1.png','bat/bluebat2.png','bat/bluebat3.png','bat/bluebat4.png',i*tile_size,255+45+15*2,3))
                    if len(lifehearts)<3:
                        lifehearts.append([i*tile_size,int(((255+45+15*2)-255)/2)+255])
                if i>300:
                    if i%4 == 0:
                        bat_count += 1
                        if i < 324:
                            bat.append(Bat('bat/redbat1.png','bat/redbat2.png','bat/redbat3.png','bat/redbat4.png',i*tile_size+8*15,255-60*bat_count,8))
                        #    plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',17-plant_count,i*tile_size,485,True,True))
                        plant.append(Plant('plant/orangeplant3.png','plant/orangeplant1.png','plant/orangeplant2.png',10+plant_count,i*tile_size,485))
                        plant_count += 1
        if y == (bottom_tiles-1):
            y = 0
        else:
            y += 1  
    #print(len(crystals))
    #print(len(lifehearts))
    #lives.append(Lives('lives/lifeTop.png','lives/life.png',lifehearts))
    lives[0].updatePositions(lifehearts)
    sam[0].setPowerUps(powerups)
    lives[0].chargeLives()

plant1 = randint(0,26)
plant2 = 26 - plant1
move = 1
down = 1
plantstep = 0
spikessize = 0
plantsize = 0
crystalsize = 0
def setInfiniteMode(spikes,lives,plant,crystals):
    global plantstep
    global plant1
    global plant2
    global move
    global down
    global spikessize
    global plantsize
    global crystalsize
    plantstep = 0
    plant1 = randint(0,26)
    plant2 = 26 - plant1
    move = 1
    down = 1
    for i in range(-240,735,15):
        spikes.append(Spike('spike/spike.png',i))
        if i > 75 and i < 495:
            if i == 90 or plantstep == 5:
                plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',plant1,i,485,True,True))
                plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',plant2,i,485,False,True))
                crystals.append(Crystal("crystal.png",i,(plant1*15)+15*randint(1,5)))
                if plant1 >= 25:
                    move = randint(1,2)
                    if move == 1:
                        plant1 = plant1 - 5
                        plant2 = plant2 + 5
                elif plant1 <= 1:
                    move = randint(1,2)
                    if move == 1:
                        plant1 = plant1 + 5
                        plant2 = plant2 - 5
                else:
                    move = randint(1,2)
                    if move == 1:
                        down = randint(1,2)
                        if down == 1:
                            plant1 = plant1 + 1
                            plant2 = plant2 - 1
                plantstep = 0
            if i >= 90:
                plantstep += 1
    lives.append(Lives('lives/lifeTop.png','lives/life.png',[]))
    lives[0].chargeLives()
    spikessize = len(spikes)
    plantsize = len(plant)
    crystalsize = len(crystals)
    
slides = 0
slideplants = 0
meters = 0

def updateInfiniteMode(spikes,lives,plant,crystals):
    global slides
    global sliding
    global spikessize
    global slideplants
    global plant1
    global plant2
    global move
    global down
    global plantsize
    global crystalsize
    global meters
    if meters > 35:
        topplant = 25
    else:
        topplant = 35
    if sliding and slides == 5:
        spikes.append(Spike('spike/spike.png',spikes[spikessize-1].rectangle.x+15))
        spikes.pop(0)
        slides = 0
    if sliding and slideplants == topplant:
        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',plant1,plant[10].rectangles[0].x+15*5,485,True,True))
        plant.append(Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',plant2,plant[11].rectangles[0].x+15*5,485,False,True))
        crystals.append(Crystal("crystal.png",plant[10].rectangles[0].x+15*5,(plant1*15)+15*randint(1,5)))
        if plant1 >= 25:
            move = randint(1,2)
            if move == 1:
                plant1 = plant1 - 5
                plant2 = plant2 + 5
        elif plant1 <= 1:
            move = randint(1,2)
            if move == 1:
                plant1 = plant1 + 5
                plant2 = plant2 - 5
        else:
            move = randint(1,2)
            if move == 1:
                down = randint(1,2)
                if down == 1:
                    plant1 = plant1 + 1
                    plant2 = plant2 - 1
        plant.pop(0)
        plant.pop(0)
        slideplants = 0
        
def resetAll(total_crystals, sam, ship, plant, bat, flame, snail, lives, spikes, crystals,screen_height,top):
    sam.clear()
    sam.append(Sam(total_crystals,'normalSam/sam1.png','normalSam/sam2.png','poweredSam/sam3.png','poweredSam/sam4.png', 'normalSam/sam1H.png', 'normalSam/sam2H.png','poweredSam/power.png','poweredSam/powerup.png',23,0,screen_height,top))
    #sam = Sam(total_crystals,'normalSam/sam1.png','normalSam/sam2.png','poweredSam/sam3.png','poweredSam/sam4.png', 'normalSam/sam1H.png', 'normalSam/sam2H.png','poweredSam/power.png','poweredSam/powerup.png',23,0,screen_height,top)
    ship.clear()
    ship.append(Ship('ship.png', -55, 0, 88, 64))
    #ship = Ship('ship.png', -55, 0, 88, 64)
    #plant = []
    plant.clear()
    #plant = [Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,180),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',5,270,0,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,295,0,True,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',20,310,485,False,True)]
    bat.clear()
    #bat = [Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',450,250,6),Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',235,300,6)]
    flame.clear()
    #flame = Flame('flame/flame1.png','flame/flame2.png',280)
    snail.clear()
    #snail = [Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',4,300),Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',6,350)]
    lives.clear()
    #lives = Lives('lives/lifeTop.png','lives/life.png',([75,100],[260,95]))
    spikes.clear()
    crystals.clear()

def resetLevel(total_crystals, sam, ship, plant, bat, flame, snail, lives, spikes, crystals,screen_height,top):
    #sam = Sam(total_crystals,'normalSam/sam1.png','normalSam/sam2.png','poweredSam/sam3.png','poweredSam/sam4.png', 'normalSam/sam1H.png', 'normalSam/sam2H.png','poweredSam/power.png','poweredSam/powerup.png',23,0,screen_height,top)
    ship.clear()
    ship.append(Ship('ship.png', -55, 0, 88, 64))
    sam[0].rect.x = 23
    sam[0].rect.y = 0
    sam[0].powerRect.x = 23 + 32 
    sam[0].powerRect.y = 0 + 27 
    sam[0].shipflag = 0
    #ship = Ship('ship.png', -55, 0, 88, 64)
    #plant = []
    #plant = []
    plant.clear()
    #plant = [Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,180),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',5,270,0,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,295,0,True,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',20,310,485,False,True)]
    bat.clear()
    #bat = [Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',450,250,6),Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',235,300,6)]
    flame.clear()
    #flame = Flame('flame/flame1.png','flame/flame2.png',280)
    snail.clear()
    #snail = [Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',4,300),Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',6,350)]
    #lives.clear()
    #lives = Lives('lives/lifeTop.png','lives/life.png',([75,100],[260,95]))
    spikes.clear()
    crystals.clear()
    
game_over = False
def levelMode(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top,mw,back,clock,startpoint,screen_width,bottom_tiles,screens,tile_size,shipstop):
    global game_over
    levelpass = False
    level = 1
    resetAll(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top)
    while not game_over:
        global endslide
        resetLevel(total_crystals, sam, ship, plant, bat, flame, snail, lives, spikes, crystals,screen_height,top)
        if level == 1:
            setLevel1(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals)
            levelpass = False
            endslide = False
            shipstop = screen_width*screens-ship[0].rect.width-tile_size
        elif level == 2:
            back = (242, 182, 145)
            setLevel2(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals)
            levelpass = False
            endslide = False
            shipstop = screen_width*screens-ship[0].rect.width-tile_size
        elif level == 3:
            back = (0, 0, 0)
            setLevel3(total_crystals,startpoint,screen_width,screen_height,bottom_tiles,screens,tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals)
            levelpass = False
            endslide = False
            shipstop = screen_width*screens-ship[0].rect.width-tile_size
        else:
            return sam[0].points 
        sam[0].resetCrystals(total_crystals)
        ship[0].enter(mw,back,clock,sam[0])
        while not levelpass and not game_over:
            sam[0].shipflag = ship[0].shipflag2
            if ship[0].shipflag2 == 1485:
                endslide = True
            mw.fill(back)
            #self.screen.blit(self.backcover,(0,0))
            ship[0].draw(mw,sam[0])
            sam[0].drawPowerUps(mw)
            lives[0].drawLifeUps(mw,sam[0])
            lives[0].chargeLives()
            ccount = 0
            for i in crystals:
                touchedCrystal = i.draw(mw,sam[0])
                if touchedCrystal:
                    crystals.pop(ccount)
                ccount += 1
                
            for i in spikes:
                i.draw(mw,sam[0],lives[0])
            for i in plant:
                i.movingPlant(mw,sam[0],lives[0])
            for i in bat:
                i.movingBat(mw,sam[0],lives[0])
            for i in flame:
                i.draw(mw,sam[0],lives[0])
            for i in snail:
                i.movingSnail(mw,sam[0],lives[0])
            sam[0].shootings(mw,plant,bat,snail)
            sam[0].healing()
            ship[0].shipflag += 1
            if sam[0].rect.x >= 125:
                if not endslide:
                    shipstop -= slide
                ship[0].shipflag2 += 1
                if ship[0].shipflag2 >= 57:
                    ship[0].rect.x = shipstop
            move_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move_up = True
                    if event.key == pygame.K_SPACE:
                        sam[0].shoot(mw)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        move_up = False
                if endslide:
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_x:
                            levelpass = ship[0].fill(mw,sam[0]) 
                            if sam[0].crystals >= int(total_crystals*0.7):
                                level += 1
                            #resetLevel(total_crystals, sam, ship, plant, bat, flame, snail, lives, spikes, crystals,screen_height,top)
                            if levelpass:
                                sam[0].rect.x = -70
                                sam[0].rect.y = 0
                                sam[0].powerRect.x = -70 + 32 
                                sam[0].powerRect.y = 0 + 27 
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            None             

            if move_up:
                if(ship[0].shipflag) >= 26:
                    sam[0].move_up(mw)
                if(ship[0].shipflag) < 26:
                    ship[0].draw(mw,sam[0])
            else:
                sam[0].fall(mw)
                if(ship[0].shipflag) < 26:
                    ship[0].draw(mw,sam[0])

            lives[0].drawLives(mw)
            sam[0].drawPoints(mw)
            totalCrystalCollected = sam[0].showPoints()
            
            if sam[0].rect.x >= 447:
                game_over = True
                resetAll(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top)
            #    print('Perdiste')
            
            #if totalCrystalCollected:
            #    game_over = True
            #    print('Gano')
            #    pygame.quit()
            #    sys.exit()
            
            if lives[0].lives <= 0:
                game_over = True  
                resetAll(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top)        
            if game_over:
                return 0
            pygame.display.update()
            clock.tick(15)
            
def infiniteMode(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top,mw,back,clock,startpoint,screen_width,bottom_tiles,screens,tile_size,shipstop):
    global game_over
    resetAll(total_crystals,sam,ship,plant,bat,flame,snail,lives,spikes,crystals,screen_height,top)
    setInfiniteMode(spikes,lives,plant,crystals)
    ship[0].enter(mw,back,clock,sam[0])
    while not game_over:
        global slides
        global sliding
        global slideplants
        global meters
        mw.fill(back)
        ship[0].draw(mw,sam[0])

        if sliding:
            slides += 1
            slideplants += 1
            meters += 1
        updateInfiniteMode(spikes,lives,plant,crystals)

        ccount = 0
        for i in crystals:
            touchedCrystal = i.draw(mw,sam[0])
            if touchedCrystal:
                crystals.pop(ccount)
            ccount += 1
            
        for i in spikes:
            i.draw(mw,sam[0],lives[0])
        for i in plant:
            i.movingPlant(mw,sam[0],lives[0])

        sam[0].healing()
        ship[0].shipflag += 1

        move_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_up = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False

        if move_up:
            if(ship[0].shipflag) >= 26:
                sam[0].move_up(mw)
            if(ship[0].shipflag) < 26:
                ship[0].draw(mw,sam[0])
        else:
            sam[0].fall(mw)
            if(ship[0].shipflag) < 26:
                ship[0].draw(mw,sam[0])

        lives[0].drawLives(mw)
        sam[0].drawPoints(mw)
        
        if lives[0].lives <= 0:
            game_over = True

        if game_over:
            return sam[0].points
        pygame.display.update()
        clock.tick(20)
        
class Game():
    def __init__(self):
        pygame.init()
        self.screen_width = 495
        self.screen_height = 495
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.backcover = pygame.image.load('cover.png')
        self.back = (107, 109, 247)
        self.back2 = (242, 182, 145)
        self.back3 = (0, 0, 0)
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.total_crystals = 0
        
        self.movement = [False, False]
        
        self.tile_size = 15
        self.bottom_tiles = int(self.screen_width/self.tile_size)
        self.startpoint = self.tile_size * 7
        self.screens = 10
        self.top = 0
        self.menu_color = (252,238,117)
        self.menu_color2 = (241,122,122)
        self.pointscolor = (159,244,251)
        self.instructions_p = "Sam's planet is running out of energy...\nHelp sam collect crystals to get more energy\n*Press UP to move Sam\n*Press SPACE to shoot at monsters\n*Press X to turn on the ship's light to pick up Sam\nTo pass each level, Sam must get at least\n70 percent of the crystals\nPress SPACE to continue"
        self.instructions = Menu(self.menu_color,self.menu_color2,15,15,"Sam's planet is running out of energy...",0,0,495,495,24,(173,4,187))
        self.instructions2 = Menu(self.menu_color,self.menu_color2,10,10,"Sam needs crystals to get more energy",0,50,495,50,24,(173,4,187))
        self.instructions3 = Menu(self.menu_color,self.menu_color2,10,10,"Help her by:",0,100,495,50,24,(173,4,187))
        self.instructions4 = Menu(self.menu_color,self.menu_color2,10,10,"* Pressing UP to move her",0,150,495,50,24,(173,4,187))
        self.instructions5 = Menu(self.menu_color,self.menu_color2,10,10,"* Pressing SPACE to shoot at monsters",0,200,495,50,24,(173,4,187))
        self.instructions6 = Menu(self.menu_color,self.menu_color2,10,10,"* Pressing X to turn on the ship's light",0,250,495,50,24,(173,4,187))
        self.instructions7 = Menu(self.menu_color,self.menu_color2,10,10,"to pick up Sam",0,300,495,50,24,(173,4,187))
        self.instructions8 = Menu(self.menu_color,self.menu_color2,10,10,"PRESS SPACE TO RETURN...",0,350,495,50,24,(173,4,187))
        self.help = Menu(self.menu_color,self.menu_color2,8,0,"?",15,15,30,30,24,(173,4,187))
        self.lm = Menu(self.pointscolor,self.menu_color2,8,0,"LM  0",158,15,150,30,24,(173,4,187))
        self.infinite = Menu(self.pointscolor,self.menu_color2,8,0,"∞  0",323,15,150,30,24,(173,4,187))
        self.play = Menu(self.menu_color,self.menu_color2,8,0,"Play Level Mode",265,380,208,30,24,(173,4,187))
        self.playinfinite = Menu(self.menu_color,self.menu_color2,30,0,"Play ∞ Mode",265,425,208,30,24,(173,4,187))
        self.max_points_levelmode = 0
        self.max_points_infi = 0
        self.clicked_instructions = False
    def run(self):
#----------------------------------Ship enters and variables------------------------------------
        self.total_crystals = 20
        self.sam = []
        self.ship = []
        self.sam.append(Sam(self.total_crystals,'normalSam/sam1.png','normalSam/sam2.png','poweredSam/sam3.png','poweredSam/sam4.png', 'normalSam/sam1H.png', 'normalSam/sam2H.png','poweredSam/power.png','poweredSam/powerup.png',23,0,self.screen_height,self.top))
        #self.sam = Sam(self.total_crystals,'normalSam/sam1.png','normalSam/sam2.png','poweredSam/sam3.png','poweredSam/sam4.png', 'normalSam/sam1H.png', 'normalSam/sam2H.png','poweredSam/power.png','poweredSam/powerup.png',23,0,self.screen_height,self.top)
        self.ship.append(Ship('ship.png', -55, 0, 88, 64))
        #self.ship = Ship('ship.png', -55, 0, 88, 64)
        self.plant = []
        #plant = [Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,180),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',5,270,0,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',10,295,0,True,True),Plant('plant/plant3.png','plant/plant1.png','plant/plant2.png',20,310,485,False,True)]
        self.bat = []
        #bat = [Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',450,250,6),Bat('bat/bat1.png','bat/bat2.png','bat/bat3.png','bat/bat4.png',235,300,6)]
        self.flame = []
        #flame = Flame('flame/flame1.png','flame/flame2.png',280)
        self.snail = []
        #snail = [Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',4,300),Snail('snail/snail1.png','snail/snail2.png','snail/snail3.png','snail/snail4.png',6,350)]
        self.lives = []
        #lives = Lives('lives/lifeTop.png','lives/life.png',([75,100],[260,95]))
        self.spikes = []
        self.crystals = []
        #crystals = [Crystal("crystal.png",70,83),Crystal("crystal.png",100,71),Crystal("crystal.png",110,225)]
        self.shipstop = self.screen_width*self.screens-self.ship[0].rect.width-self.tile_size
        #for i in range(self.bottom_tiles*self.screens):
        #    spikes.append(Spike('spike/spike.png',i*self.tile_size))
        #sam.setPowerUps([[125,250],[375,250]])
        #lives.chargeLives()
#        setLevel1(self.total_crystals,self.startpoint,self.screen_width,self.screen_height,self.bottom_tiles,self.screens,self.tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals)     
#        #setLevel3(self.total_crystals,self.startpoint,self.screen_width,self.screen_height,self.bottom_tiles,self.screens,self.tile_size,sam,plant,bat,flame,snail,lives,spikes,crystals)
#        ship.enter(self.screen,self.back,self.clock,sam)
#
#        #setInfiniteMode(spikes,lives,plant,crystals)
        self.clock = pygame.time.Clock()
#        ship.shipflag = 0
#        self.game_over = False
#----------------------Level Mode---------------------------------------------------------
#        while True:
#            global endslide
#            sam.shipflag = ship.shipflag2
#            if ship.shipflag2 == 1485:
#                endslide = True
#            self.screen.fill(self.back)
#            #self.screen.blit(self.backcover,(0,0))
#            ship.draw(self.screen,sam)
#            sam.drawPowerUps(self.screen)
#            lives[0].drawLifeUps(self.screen,sam)
#            lives[0].chargeLives()
#            ccount = 0
#            for i in crystals:
#                touchedCrystal = i.draw(self.screen,sam)
#                if touchedCrystal:
#                    crystals.pop(ccount)
#                ccount += 1
#                
#            for i in spikes:
#                i.draw(self.screen,sam,lives[0])
#            for i in plant:
#                i.movingPlant(self.screen,sam,lives[0])
#            for i in bat:
#                i.movingBat(self.screen,sam,lives[0])
#            for i in flame:
#                i.draw(self.screen,sam,lives[0])
#            for i in snail:
#                i.movingSnail(self.screen,sam,lives[0])
#            sam.shootings(self.screen,plant,bat,snail)
#            sam.healing()
#            ship.shipflag += 1
#            if sam.rect.x >= 125:
#                if not endslide:
#                    shipstop -= slide
#                ship.shipflag2 += 1
#                if ship.shipflag2 >= 57:
#                    ship.rect.x = shipstop
#            move_up = False
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    game_over = True
#                    pygame.quit()
#                    sys.exit()
#                if event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_UP:
#                        move_up = True
#                    if event.key == pygame.K_SPACE:
#                        sam.shoot(self.screen)
#                elif event.type == pygame.KEYUP:
#                    if event.key == pygame.K_UP:
#                        move_up = False
#                if endslide:
#                    if event.type == pygame.KEYDOWN: 
#                        if event.key == pygame.K_x:
#                            ship.fill(self.screen,sam) 
#                    elif event.type == pygame.KEYDOWN:
#                        if event.key == pygame.K_x:
#                            None             
#
#            if move_up:
#                if(ship.shipflag) >= 26:
#                    sam.move_up(self.screen)
#                if(ship.shipflag) < 26:
#                    ship.draw(self.screen,sam)
#            else:
#                sam.fall(self.screen)
#                if(ship.shipflag) < 26:
#                    ship.draw(self.screen,sam)
#
#            lives[0].drawLives(self.screen)
#            sam.drawPoints(self.screen)
#            totalCrystalCollected = sam.showPoints()
#            
#            if sam.rect.x >= 447:
#                print('Perdiste')
#            
#            if totalCrystalCollected:
#                game_over = True
#                print('Gano')
#                pygame.quit()
#                sys.exit()
#            
#            if lives[0].lives <= 0:
#                game_over = True
#                pygame.quit()
#                sys.exit()            
#            
#            pygame.display.update()
#            self.clock.tick(15)#va a aumentar de 15 en 15
#----------------------Infinite mode-------------------------------------------------------
#        while True:
#            #global endslide
#            #sam.shipflag = ship.shipflag2
#            #if ship.shipflag2 == 1485:
#            #    endslide = True
#            global slides
#            global sliding
#            global slideplants
#            global meters
#            self.screen.fill(self.back)
#            ship.draw(self.screen,sam)
#            #print(slides)
#            #print(sliding)
#            if sliding:
#                slides += 1
#                slideplants += 1
#                meters += 1
#            updateInfiniteMode(spikes,lives,plant,crystals)
#            #sam.drawPowerUps(self.screen)
#            #lives[0].drawLifeUps(self.screen,sam)
#            #lives[0].chargeLives()
#            ccount = 0
#            for i in crystals:
#                touchedCrystal = i.draw(self.screen,sam)
#                if touchedCrystal:
#                    crystals.pop(ccount)
#                ccount += 1
#                
#            for i in spikes:
#                i.draw(self.screen,sam,lives[0])
#            for i in plant:
#                i.movingPlant(self.screen,sam,lives[0])
#            #for i in bat:
#            #    i.movingBat(self.screen,sam,lives[0])
#            #for i in flame:
#            #    i.draw(self.screen,sam,lives[0])
#            #for i in snail:
#            #    i.movingSnail(self.screen,sam,lives[0])
#            #sam.shootings(self.screen,plant,bat,snail)
#            sam.healing()
#            ship.shipflag += 1
#            #if sam.rect.x >= 125:
#            #    if not endslide:
#            #        shipstop -= slide
#            #    ship.shipflag2 += 1
#            #    if ship.shipflag2 >= 57:
#            #        ship.rect.x = shipstop
#            move_up = False
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    game_over = True
#                    pygame.quit()
#                    sys.exit()
#                if event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_UP:
#                        move_up = True
#                #    if event.key == pygame.K_SPACE:
#                #        sam.shoot(self.screen)
#                elif event.type == pygame.KEYUP:
#                    if event.key == pygame.K_UP:
#                        move_up = False
#                #if endslide:
#                #    if event.type == pygame.KEYDOWN: 
#                #        if event.key == pygame.K_x:
#                #            ship.fill(self.screen,sam) 
#                #    elif event.type == pygame.KEYDOWN:
#                #        if event.key == pygame.K_x:
#                #            None             
#
#            if move_up:
#                if(ship.shipflag) >= 26:
#                    sam.move_up(self.screen)
#                if(ship.shipflag) < 26:
#                    ship.draw(self.screen,sam)
#            else:
#                sam.fall(self.screen)
#                if(ship.shipflag) < 26:
#                    ship.draw(self.screen,sam)
#
#            lives[0].drawLives(self.screen)
#            sam.drawPoints(self.screen)
#            totalCrystalCollected = sam.showPoints()
#            
#            #if sam.rect.x >= 447:
#            #    print('Perdiste')
#            
#            #if totalCrystalCollected:
#            #    game_over = True
#            #    print('Gano')
#            #    pygame.quit()
#            #    sys.exit()
#            
#            if lives[0].lives <= 0:
#                game_over = True
#                pygame.quit()
#                sys.exit()            
#            
#            pygame.display.update()
#            self.clock.tick(20)#va a aumentar de 15 en 15
#---------------------------------------------------------------------------
        while True:
            global game_over
            game_over = False
            resetAll(self.total_crystals,self.sam,self.ship,self.plant,self.bat,self.flame,self.snail,self.lives,self.spikes,self.crystals,self.screen_height,self.top)
            #print(self.plant)
            self.screen.blit(self.backcover,(0,0))
            self.help.draw(self.screen)
            self.play.draw(self.screen)
            self.playinfinite.draw(self.screen)
            self.lm = Menu(self.pointscolor,self.menu_color2,8,0,"LM  "+str(self.max_points_levelmode),158,15,150,30,24,(173,4,187))
            self.infinite = Menu(self.pointscolor,self.menu_color2,8,0,"∞  "+str(self.max_points_infi),323,15,150,30,24,(173,4,187))
            self.lm.draw(self.screen)
            self.infinite.draw(self.screen)
            if self.clicked_instructions:
                self.instructions.draw(self.screen)
                self.instructions2.draw(self.screen)
                self.instructions3.draw(self.screen)
                self.instructions4.draw(self.screen)
                self.instructions5.draw(self.screen)
                self.instructions6.draw(self.screen)
                self.instructions7.draw(self.screen)
                self.instructions8.draw(self.screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #game_over = True
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.clicked_instructions = False
            #max_points_levelmode = 0
            #max_points_infinitemode = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #game_over = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if self.help.collidepoint(x,y):
                        #self.help.color()
                        self.clicked_instructions = True
                    if self.play.collidepoint(x,y) and not self.clicked_instructions:
                        #self.play.color()
                        points = levelMode(self.total_crystals,self.sam,self.ship,self.plant,self.bat,self.flame,self.snail,self.lives,self.spikes,self.crystals,self.screen_height,self.top,self.screen,self.back,self.clock,self.startpoint,self.screen_width,self.bottom_tiles,self.screens,self.tile_size,self.shipstop)
                        if points > self.max_points_levelmode:
                            self.max_points_levelmode = points
                    if self.playinfinite.collidepoint(x,y) and not self.clicked_instructions:
                        #self.playinfinite.color()
                        points = infiniteMode(self.total_crystals,self.sam,self.ship,self.plant,self.bat,self.flame,self.snail,self.lives,self.spikes,self.crystals,self.screen_height,self.top,self.screen,self.back,self.clock,self.startpoint,self.screen_width,self.bottom_tiles,self.screens,self.tile_size,self.shipstop)
                        if points > self.max_points_levelmode:
                            self.max_points_infi = points
            pygame.display.update()
            self.clock.tick(15)
Game().run()



