import sys, pygame
from pygame import *
from numpy import *
from random import *


class AggroRect(sprite.Sprite):
	def __init__(self, parent, width, height):
		sprite.Sprite.__init__(self)
		self.width = width
		self.height = height
		self.image = Surface((self.width + parent.rect.width, parent.rect.height+self.height))
		self.image.fill((255,255,0))
		self.image.set_colorkey((255,255,0))
		self.rect = self.image.get_rect().move(parent.rect.x, parent.rect.y)

	def update(self, parent):
		self.rect.x = parent.rect.x-self.width/2
		self.rect.y = parent.rect.y-self.height

class Dog(sprite.Sprite):
	def __init__(self,x,y):
		sprite.Sprite.__init__(self)
		self.imagesR= [image.load("res/dogeRun1R.png").convert_alpha(),
						image.load("res/dogeRun3R.png").convert_alpha(),
						image.load("res/dogeRun5R.png").convert_alpha(),
						image.load("res/dogeRun1R.png").convert_alpha(),
						image.load("res/dogeRun3R.png").convert_alpha(),
						image.load("res/dogeRun5R.png").convert_alpha()]
		
		self.imagesL= [image.load("res/dogeRun1L.png").convert_alpha(),
						image.load("res/dogeRun3L.png").convert_alpha(),
						image.load("res/dogeRun5L.png").convert_alpha(),
						image.load("res/dogeRun1L.png").convert_alpha(),
						image.load("res/dogeRun3L.png").convert_alpha(),
						image.load("res/dogeRun5L.png").convert_alpha()]
						
		self.standimagesR= [image.load("res/dogeStand0R.png").convert_alpha(),
							image.load("res/dogeStand1R.png").convert_alpha(),
							image.load("res/dogeStand0R.png").convert_alpha(),
							image.load("res/dogeStand2R.png").convert_alpha(),
							image.load("res/dogeStand3R.png").convert_alpha(),
							image.load("res/dogeStand2R.png").convert_alpha()]
		
		self.standimagesL= [image.load("res/dogeStand0L.png").convert_alpha(),
							image.load("res/dogeStand1L.png").convert_alpha(),
							image.load("res/dogeStand0L.png").convert_alpha(),
							image.load("res/dogeStand2L.png").convert_alpha(),
							image.load("res/dogeStand3L.png").convert_alpha(),
							image.load("res/dogeStand2L.png").convert_alpha()]
						
		self.imagedict= {"imgR": self.imagesR, "imgL": self.imagesL, "imgRstand": self.standimagesR, "imgLstand": self.standimagesL}
		self.index= 0
		self.lugeja= 0
		self.standing= True
		self.state = "imgR"
		self.image= self.imagedict["imgLstand"][self.index]
		self.rect= self.image.get_rect().move((x,y))
		self.onGround = False
		self.dir = "left"
		self.hp = 40
		self.yvel=0
		self.xvel=0
		self.aggroArea = AggroRect(self, 500, 0)
		self.dying = False
		
	def update(self, platforms, player, billybullets, enemies):
		if self.hp <= 0:
			print("dead doggie")
			#self.dying = True
			#if self.state != "imgRdeath" and self.state != "imgLdeath":
				#self.index = 0
			#if self.dir == "right":
				#self.state = "imgRdeath"
			#elif self.dir == "left":
				#self.state = "imgLdeath"
		self.rect = self.rect.move(self.xvel, self.yvel)
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 80: self.yvel = 80
		self.collide(self.xvel, 0, platforms, player, billybullets)
		self.rect.top += self.yvel
		self.onGround= False
		self.collide(0, self.yvel, platforms, player, billybullets)
		self.aggroArea.update(self)
		self.collide(0, 0, platforms, player, billybullets)
		self.animate(self.state, enemies)
	
	def animate(self, state, enemies):
		if not self.dying:
			self.lugeja+=1
			if self.lugeja == 6:
				if self.index != 5:
					self.index+= 1
				else:
					self.index = 0
				self.lugeja= 0
		elif self.dying:
			self.lugeja+=1
			if self.lugeja == 6:
				if self.index != 4:
					self.index+= 1
					self.lugeja= 0
				else:
					enemies.remove(self)		
		self.image= self.imagedict[state][self.index]
		
	def collide(self, xvel, yvel, platforms, player, billybullets):
		if not self.dying:
			if xvel != 0 or yvel !=0:
				for p in platforms:
					if pygame.sprite.collide_rect(self, p):
						if xvel > 0:
							self.state = "imgL"
							self.dir = "left"
							self.image = self.imagedict[self.state][self.index]
							self.rect.x -= 2
							self.xvel = -1
						if xvel < 0:
							self.state = "imgR"
							self.dir = "right"
							self.image = self.imagedict[self.state][self.index]
							self.xvel = 1
							self.rect.x += 2
						if yvel > 0:
							self.rect.bottom = p.rect.top
							self.onGround = True
							self.yvel = 0
						if yvel < 0:
							self.rect.top = p.rect.bottom
							self.yvel += 1
			else:
				if pygame.sprite.collide_rect(self.aggroArea, player):
					deltax = player.rect.x - self.rect.x-38
					if deltax > 0:
						self.standing = False
						self.xvel = 4
						self.state = "imgR"
						self.dir = "right"
					else:
						self.standing = False
						self.xvel = -4
						self.state = "imgL"
						self.dir = "left"
				else:
					if self.dir == "right":
						self.standing = True
						self.xvel = 0
						self.state = "imgRstand"
					elif self.dir == "left":
						self.standing = True
						self.xvel = 0
						self.state = "imgLstand"
			
			if pygame.sprite.collide_rect(self, player):
				if self.dir == "right":
					player.rect.x+= 3
					player.i_time = 45 #invincibility
				elif self.dir == "left":
					player.rect.x-=3
					player.i_time = 45 #invincibility

class Hillbilly(sprite.Sprite):
	def __init__(self,x,y):
		sprite.Sprite.__init__(self)
		self.imagesR= [image.load("res/hillyR.png").convert_alpha(),
						image.load("res/hillyR1.png").convert_alpha(),
						image.load("res/hillyR.png").convert_alpha(),
						image.load("res/hillyR2.png").convert_alpha()]
		
		self.imagesL= [image.load("res/hillyL.png").convert_alpha(),
						image.load("res/hillyL1.png").convert_alpha(),
						image.load("res/hillyL.png").convert_alpha(),
						image.load("res/hillyL2.png").convert_alpha()]
						
		self.deathimagesR= [image.load("res/hillyDeathR.png").convert_alpha(),
						image.load("res/hillyDeathR2.png").convert_alpha(),
						image.load("res/hillyDeathR3.png").convert_alpha(),
						image.load("res/hillyDeathR4.png").convert_alpha(),
						image.load("res/hillyDeathR5.png").convert_alpha()]
		
		self.deathimagesL= [image.load("res/hillyDeathL.png").convert_alpha(),
						image.load("res/hillyDeathL2.png").convert_alpha(),
						image.load("res/hillyDeathL3.png").convert_alpha(),
						image.load("res/hillyDeathL4.png").convert_alpha(),
						image.load("res/hillyDeathL5.png").convert_alpha()]
						
		self.standimagesR= [image.load("res/hillyR.png").convert_alpha()]
		
		self.standimagesL= [image.load("res/hillyL.png").convert_alpha()]
						
		self.imagedict= {"imgR": self.imagesR, "imgL": self.imagesL, "imgRstand": self.standimagesR, "imgLstand": self.standimagesL, "imgRdeath": self.deathimagesR, "imgLdeath": self.deathimagesL }
		self.index= 0
		self.lugeja= 0
		self.standing= False
		self.state = "imgR"
		self.image= self.imagedict["imgR"][self.index]
		self.rect= self.image.get_rect().move((x,y))
		self.onGround = False
		self.dir = "right"
		self.hp = 40
		self.yvel=0
		self.xvel=1
		self.aggroArea = AggroRect(self, 500, 0)
		self.dying = False
		self.reload = 0
		self.shootsound = pygame.mixer.Sound('res/Gunshot2.wav')
		
	def update(self, platforms, player, billybullets, enemies):
		if self.hp <= 0:
			self.dying = True
			if self.state != "imgRdeath" and self.state != "imgLdeath":
				self.index = 0
			if self.dir == "right":
				self.state = "imgRdeath"
			elif self.dir == "left":
				self.state = "imgLdeath"
		self.rect = self.rect.move(self.xvel, self.yvel)
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 80: self.yvel = 80
		self.collide(self.xvel, 0, platforms, player, billybullets)
		self.rect.top += self.yvel
		self.onGround= False
		self.collide(0, self.yvel, platforms, player, billybullets)
		self.aggroArea.update(self)
		self.collide(0, 0, platforms, player, billybullets)
		self.animate(self.state, enemies)
	
	def animate(self, state, enemies):
		if not self.standing and not self.dying:
			self.lugeja+=1
			if self.lugeja == 6:
				if self.index != 3:
					self.index+= 1
				else:
					self.index = 0
				self.lugeja= 0
		elif self.standing and not self.dying:
			self.lugeja = 0
			self.index = 0
		elif self.dying:
			self.lugeja+=1
			if self.lugeja == 6:
				if self.index != 4:
					self.index+= 1
					self.lugeja= 0
				else:
					enemies.remove(self)
				
		self.image= self.imagedict[state][self.index]
		
	def collide(self, xvel, yvel, platforms, player, billybullets):
		if not self.dying:
			if xvel != 0 or yvel !=0:
				for p in platforms:
					if pygame.sprite.collide_rect(self, p):
						if xvel > 0:
							self.state = "imgL"
							self.dir = "left"
							self.image = self.imagedict[self.state][self.index]
							self.rect.x -= 2
							self.xvel = -1
						if xvel < 0:
							self.state = "imgR"
							self.dir = "right"
							self.image = self.imagedict[self.state][self.index]
							self.xvel = 1
							self.rect.x += 2
						if yvel > 0:
							self.rect.bottom = p.rect.top
							self.onGround = True
							self.yvel = 0
						if yvel < 0:
							self.rect.top = p.rect.bottom
							self.yvel += 1
			else:
				if pygame.sprite.collide_rect(self.aggroArea, player):
					deltax = player.rect.x - self.rect.x-38
					if deltax > 0:
						self.standing = True
						self.xvel = 0
						self.state = "imgRstand"
						self.dir = "right"
						self.shoot(billybullets)
					else:
						self.standing = True
						self.xvel = 0
						self.state = "imgLstand"
						self.dir = "left"
						self.shoot(billybullets)
				else:
					self.reload = 79
					if self.dir == "right":
						self.standing = False
						self.xvel = 2
						self.state = "imgR"
					elif self.dir == "left":
						self.standing = False
						self.xvel = -2
						self.state = "imgL"
			
			if pygame.sprite.collide_rect(self, player):
				if self.dir == "right":
					player.rect.x+= 3
				elif self.dir == "left":
					player.rect.x-=3
					
	def shoot(self, billybullets): #direction
		if self.dir == "left":
			speed = -3
			offset = 0
		elif self.dir == "right":
			speed = 3
			offset = 64
		if self.reload == 80:
			self.shootsound.play()
			for i in range(-1,2):
				bullet = HillBullet(self.dir, i)
				bullet.rect.x = self.rect.x + offset
				bullet.rect.y = self.rect.y + 66
				billybullets.add(bullet)
			self.reload = 0
		else:
			self.reload+=1	

class HillBullet(sprite.Sprite):
	def __init__(self, dir, ycord):
		sprite.Sprite.__init__(self)
		self.imagelist = [image.load("res/bullet.png").convert_alpha(),
							image.load("res/bulletL.png").convert_alpha()]
		self.index = 0
		self.image = self.imagelist[self.index]
		self.rect = self.image.get_rect()
		self.direction = dir
		self.ymovement = ycord
	
	def update(self, world, billybullets, player):
		if self.direction == "right":
			self.rect.x += 14
			self.rect.y += self.ymovement + randint(-2,2)
			self.image = self.imagelist[0]
		elif self.direction == "left":
			self.rect.x -= 14
			self.rect.y += self.ymovement + randint(-2,2)
			self.image = self.imagelist[1]
		for p in world:
			if pygame.sprite.collide_rect(self, p):
				billybullets.remove(self)
		if pygame.sprite.collide_rect(self, player):
			if not player.ducking:
				if player.hp-2 > 0:
					player.hp -= 2
				else:
					player.hp = 1				
