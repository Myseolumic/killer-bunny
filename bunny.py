import sys, pygame
from pygame import *
from numpy import *
from random import *
from math import *

class Player(sprite.Sprite):
	def __init__(self, width, height):
		sprite.Sprite.__init__(self)
		self.stand_imagesR= [image.load("res/Stand_R.png").convert(),
							image.load("res/Stand_R2.png").convert(),
							image.load("res/Stand_R3.png").convert(),
							image.load("res/Stand_R4.png").convert()]
		
		self.stand_imagesL= [image.load("res/Stand_L.png").convert(),
							image.load("res/Stand_L2.png").convert(),
							image.load("res/Stand_L3.png").convert(),
							image.load("res/Stand_L4.png").convert()]
							
		self.run_imagesR= [image.load("res/0R.png").convert(),
							image.load("res/1R.png").convert(),
							image.load("res/2R.png").convert(),
							image.load("res/3R.png").convert(),
							image.load("res/4R.png").convert()]
		
		self.run_imagesL= [image.load("res/0L.png").convert(),
							image.load("res/1L.png").convert(),
							image.load("res/2L.png").convert(),
							image.load("res/3L.png").convert(),
							image.load("res/4L.png").convert()]
							
		self.duck_imagesR= [image.load("res/Ducking_R.png").convert_alpha(),
							image.load("res/Ducking_R.png").convert_alpha(),
							image.load("res/Ducking_R.png").convert_alpha(),
							image.load("res/Ducking_R.png").convert_alpha(),
							image.load("res/Ducking_R.png").convert_alpha(),
							image.load("res/Ducking_R2.png").convert_alpha(),
							image.load("res/Ducking_R3.png").convert_alpha(),
							image.load("res/Ducking_R4.png").convert_alpha(),
							image.load("res/Ducking_R4.png").convert_alpha(),
							image.load("res/Ducking_R4.png").convert_alpha(),
							image.load("res/Ducking_R4.png").convert_alpha(),
							image.load("res/Ducking_R4.png").convert_alpha(),
							image.load("res/Ducking_R3.png").convert_alpha(),
							image.load("res/Ducking_R2.png").convert_alpha()]
		
		self.duck_imagesL= [image.load("res/Ducking_L.png").convert_alpha(),
							image.load("res/Ducking_L.png").convert_alpha(),
							image.load("res/Ducking_L.png").convert_alpha(),
							image.load("res/Ducking_L.png").convert_alpha(),
							image.load("res/Ducking_L.png").convert_alpha(),
							image.load("res/Ducking_L2.png").convert_alpha(),
							image.load("res/Ducking_L3.png").convert_alpha(),
							image.load("res/Ducking_L4.png").convert_alpha(),
							image.load("res/Ducking_L4.png").convert_alpha(),
							image.load("res/Ducking_L4.png").convert_alpha(),
							image.load("res/Ducking_L4.png").convert_alpha(),
							image.load("res/Ducking_L4.png").convert_alpha(),
							image.load("res/Ducking_L3.png").convert_alpha(),
							image.load("res/Ducking_L2.png").convert_alpha()]
							
		self.shoot_imagesR=[image.load("res/charge1.png").convert_alpha(),
							image.load("res/charge2.png").convert_alpha(),
							image.load("res/charge3.png").convert_alpha(),
							image.load("res/charge4.png").convert_alpha(),
							image.load("res/charge5.png").convert_alpha(),
							image.load("res/charge6.png").convert_alpha(),
							image.load("res/charge7.png").convert_alpha(),
							image.load("res/charge8.png").convert_alpha()]
							
		self.shoot_imagesL=[image.load("res/charge1L.png").convert_alpha(),
							image.load("res/charge2L.png").convert_alpha(),
							image.load("res/charge3L.png").convert_alpha(),
							image.load("res/charge4L.png").convert_alpha(),
							image.load("res/charge5L.png").convert_alpha(),
							image.load("res/charge6L.png").convert_alpha(),
							image.load("res/charge7L.png").convert_alpha(),
							image.load("res/charge8L.png").convert_alpha()]
							
		self.charged_imagesR=[image.load("res/charged1.png").convert_alpha(),
							image.load("res/charged2.png").convert_alpha(),
							image.load("res/charged3.png").convert_alpha(),
							image.load("res/charged4.png").convert_alpha()]
							
		self.charged_imagesL=[image.load("res/charged1L.png").convert_alpha(),
							image.load("res/charged2L.png").convert_alpha(),
							image.load("res/charged3L.png").convert_alpha(),
							image.load("res/charged4L.png").convert_alpha()]
							
		self.dict={"standR": self.stand_imagesR, "standL": self.stand_imagesL, "runR":self.run_imagesR, "runL":self.run_imagesL, "duckL":self.duck_imagesL, "duckR":self.duck_imagesR, "shootR":self.shoot_imagesR, "shootL": self.shoot_imagesL, "chargedR": self.charged_imagesR, "chargedL": self.charged_imagesL}
		self.xvel = 0
		self.yvel = 0 
		self.origin = []
		self.hp = 100
		self.maxhp = 100
		self.maxmana = int(84)
		self.mana = int(84)
		self.onGround = False
		self.can_jump = False
		self.jumped = False
		self.charged = False
		self.index = 0
		self.image = self.stand_imagesR[self.index]
		self.rect = self.image.get_rect()
		self.vahe=0
		self.projdmg = 0
		self.ducking = False
		self.jump_sound = pygame.mixer.Sound('res/hupe.wav')
		self.Djump_sound = pygame.mixer.Sound('res/Jumpsound.wav')
		self.firechannel = mixer.Channel(5)
		self.fire_sound = pygame.mixer.Sound('res/fire.wav')
		self.projspawn= pygame.mixer.Sound("res/proj.wav")
		#invincibility jaoks
		self.i_var = 0 
		self.i_time = 0
		self.alpha = 1
		#finish
		self.controlsEnabled = True
		#surm
		self.deathScreen = Surface((802,640))
		self.deathScreen.set_alpha(0)
		self.deathScreen_rect = self.deathScreen.get_rect()
		self.deathvar = 1
		self.dead = False
	
	def update(self, key, up, down, left, right, was_left, was_right, shoot, platforms, anim_state, anim_list, smoke_list, proj_list, CameraX, CameraY):		
		current_state = anim_state
		
		if not shoot:
			if self.mana < self.maxmana:
				self.mana+=0.2
		#self.hp-=(1/30)
		
		#movement
		if up:
			if self.onGround: 
				self.jump_sound.play()
				self.yvel -= 10
				self.can_jump = True
			elif self.can_jump and self.jumped and self.mana >= 30:
				self.mana -=30
				self.can_jump = False
				self.Djump_sound.play()
				smoke = Smoke()
				smoke.rect.x = self.rect.x -50
				smoke.rect.y = self.rect.y +20
				smoke_list.add(smoke)
				self.yvel = -10
		if down:
			if was_right:
				current_state = "duckR"
			elif was_left:
				current_state = "duckL"
		if left:
			self.xvel = -4
		if right:
			self.xvel = 4
		if shoot and not right and not left and not down and self.yvel <= 1 and self.yvel >=-1:
			if self.mana > 0:
				self.mana-=1
				self.projdmg +=2
				if was_left:
					if self.projdmg < 50:
						current_state = "shootL"
					else:
						current_state = "chargedL"
				elif was_right:
					if self.projdmg < 50:
						current_state = "shootR"
					else:
						current_state = "chargedR"
				for i in range(5):
					randx = randint(-100,100)
					randy = randint(-100,100)
					if randx >= -50 and randx <=50 and randy > 50:
						randy +=40
					elif randx >= -50 and randx <=50 and randy < 50:
						randy -=40
					if randy >= -50 and randy <=50 and randx > 50:
						randx +=40
					elif randy >= -50 and randy <=50 and randx < 50:
						randx -=40
					fire = Fire(True, randx / -20, randy / -20)
					fire.rect.x = self.rect.x + 21 +randx
					fire.rect.y = self.rect.y + 40 +randy
					anim_list.add(fire)
					if not self.firechannel.get_busy() and self.mana !=0:
						self.firechannel.play(self.fire_sound)
			else:
				self.fire_sound.fadeout(50)
		else:
			self.fire_sound.fadeout(50)
		if self.charged or self.mana < 1 and self.mana > -1:
			if self.projdmg >=48:
				if was_left:
					speed = -3
				elif was_right:
					speed = 3
				ball = Voidball(speed, self.projdmg)
				ball.rect.x = self.rect.x + 6
				ball.rect.y = self.rect.y + 15
				proj_list.add(ball)
				self.projspawn.play()
				self.charged = False
				self.projdmg = 0
			else:
				self.projdmg = 0
				self.charged = False
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 80: self.yvel = 80
		if not(left or right):
			self.xvel = 0
		self.rect.left += self.xvel
		if self.xvel > 0:
			current_state = "runR"
		elif self.xvel < 0: 
			current_state = "runL"
			
		self.collide(self.xvel, 0, platforms)
		self.rect.top += self.yvel
		self.onGround = False;
		self.collide(0, self.yvel, platforms)
		
		#animation
		self.animate(current_state)
		#update deathscreen alpha
		if self.dead:
			next_alpha = self.deathScreen.get_alpha()+(1*self.deathvar)
			if next_alpha >=255:
				self.deathScreen.set_alpha(255)
			elif next_alpha <=0:
				self.deathScreen.set_alpha(0)
				self.deathvar = 1
				self.dead = False
				self.controlsEnabled = True
				self.hp = 100
			else:
				self.deathScreen.set_alpha(next_alpha)
			
	
	def animate(self, key):
		self.vahe+=1
		if self.vahe == 6:
			self.index+=1
			if self.index >= len(self.dict.get(key)):
				self.index = 0
			temp_alpha = self.image.get_alpha()
			self.image = self.dict.get(key)[self.index]
			self.image.set_colorkey((255,255,255))
			self.image.set_alpha(temp_alpha)
			self.vahe = 0
		self.invincibility()
	
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if xvel > 0:
					self.rect.right = p.rect.left
				if xvel < 0:
					self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.jumped = False
					self.yvel = 0
				if yvel < 0:
					self.rect.top = p.rect.bottom
					self.yvel += 1
	def invincibility(self):
		if self.i_time == 0:
			self.i_var = 255
			self.alpha = 255
			self.image.set_alpha(255)
		if self.i_time > 0:
			if self.vahe == 2 or self.vahe == 4 or self.vahe == 6:
				self.i_var -= 70
				self.alpha = abs(self.i_var)
				if self.alpha >= 255:
					self.i_var = 255
				self.i_time -= 1
				self.image.set_alpha(self.alpha)
	def getHurt(self, dmg):
		if self.hp - dmg > 0:
			self.hp -= dmg
			self.i_time = 45
		else:
			self.controlsEnabled = False
			#death animation
			self.dead = True
			

class Smoke(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.imagelist = [image.load("res/cloud1.png").convert_alpha(),
						image.load("res/cloud2.png").convert_alpha(),
						image.load("res/cloud3.png").convert_alpha(),
						image.load("res/cloud4.png").convert_alpha(),
						image.load("res/cloud5.png").convert_alpha(),
						image.load("res/cloud6.png").convert_alpha(),
						image.load("res/cloud6.png").convert_alpha()]
		self.imgcount=0
		self.image = self.imagelist[self.imgcount]
		self.rect = self.image.get_rect()
		self.indexcounter=0
		
	def update(self):
		self.indexcounter+=1
		if self.indexcounter == 4:
			self.indexcounter = 0
			if self.imgcount < 6:
				self.imgcount+=1
				self.image = self.imagelist[self.imgcount]

class Voidball(sprite.Sprite):
	def __init__(self, speed, dmg):
		sprite.Sprite.__init__(self)
		self.imagelist = [image.load("res/proj1b.png").convert_alpha(),
						image.load("res/proj5b.png").convert_alpha(),
						image.load("res/proj2b.png").convert_alpha(),
						image.load("res/proj4b.png").convert_alpha(),
						image.load("res/proj6b.png").convert_alpha(),
						image.load("res/proj3b.png").convert_alpha()]
						
		self.decayimage=[image.load("res/fade1.png").convert_alpha(),
						image.load("res/fade2.png").convert_alpha(),
						image.load("res/fade3.png").convert_alpha()]
						
		self.index = 0
		self.damage = dmg
		self.image = self.imagelist[self.index]
		self.rect = self.image.get_rect().inflate(0,-10)
		self.lugeja = 0
		self.decaytimer=0
		self.speed = speed
		self.blastsound = pygame.mixer.Sound("res/vortex.wav")
		self.blastchannel = mixer.Channel(7)
		self.blastsound.set_volume(0.4)
		
	def update(self, anim_list, enemylist, proj_list, platforms):
		self.decaytimer+=1
		randmovey = randint(-2,2)
		randmovex = randint(-2,2)
		self.rect.x += self.speed + randmovex
		fire = Fire(True, randmovex, randmovey)
		fire.rect.x = self.rect.x + 24
		fire.rect.y = self.rect.y + 24
		anim_list.add(fire)
		if self.lugeja == 4:
			if self.decaytimer < 125:
				if self.index != 5:
					self.index +=1
					self.image = self.imagelist[self.index]
				else:
					self.index = 0
					self.image = self.imagelist[self.index]
				self.lugeja = 0
			elif self.decaytimer == 125:
				self.index = 0
				self.image = self.decayimage[self.index]
				self.lugeja = 0
			else:
				if self.index != 2:
					self.index +=1
					self.image = self.decayimage[self.index]
				else:
					self.index = 0
					self.image = self.decayimage[self.index]
					proj_list.remove(self)
				self.lugeja = 0
		else:
			self.lugeja+=1
		self.collision(enemylist, anim_list, proj_list, platforms)

	def collision(self, enemies, anim_list, proj_list, platforms):
		for en in enemies:
			if pygame.sprite.collide_rect(self, en):
				en.rect.inflate(0, -80)
				en.xvel -= (en.rect.x -self.rect.x) / 20
				en.yvel -= 3
				proj_list.remove(self)
				blast = Voidblast()
				blast.rect.x = self.rect.x-48
				blast.rect.y = self.rect.y-48
				proj_list.add(blast)
				en.hp -= self.damage
				if not self.blastchannel.get_busy():
					self.blastchannel.play(self.blastsound)
		
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				proj_list.remove(self)
				blast = Voidblast()
				blast.rect.x = self.rect.x-48
				blast.rect.y = self.rect.y-48
				proj_list.add(blast)
				if not self.blastchannel.get_busy():
					self.blastchannel.play(self.blastsound)

class Voidblast(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.imagelist = [image.load("res/blast0.png").convert_alpha(),
						image.load("res/blast01.png").convert_alpha(),
						image.load("res/blast1.png").convert_alpha(),
						image.load("res/blast2.png").convert_alpha(),
						image.load("res/blast3.png").convert_alpha(),
						image.load("res/blast4.png").convert_alpha(),
						image.load("res/blast5.png").convert_alpha(),
						image.load("res/blast6.png").convert_alpha()]
		self.index = 0
		self.image = self.imagelist[self.index]
		self.lugeja = 0
		self.rect = self.image.get_rect()
	
	def update(self, list, list2, proj_list, list3):
		if self.lugeja == 5:
			self.lugeja = 0
			if self.index != 7:
				self.index+=1
				self.image = self.imagelist[self.index]
			else:
				proj_list.remove(self)
		else:
			self.lugeja +=1

class Fire(sprite.Sprite):
	def __init__(self, speed, xx, yy):
		sprite.Sprite.__init__(self)
		self.imagelist=[image.load("res/fire.png").convert_alpha(),
						image.load("res/fire2.png").convert_alpha(),
						image.load("res/fire3.png").convert_alpha(),
						]
		self.image_index=0
		self.image = self.imagelist[self.image_index]
		self.rect = self.image.get_rect()
		self.lugeja=0
		self.xspeed= xx
		self.yspeed = yy

	
	def update(self):
		self.rect.y += self.yspeed
		self.rect.x += self.xspeed
		self.lugeja+=1
		self.animate()
		
	def animate(self):
			image_rand=randint(1,5)
			if image_rand == 4 and self.image_index != 2:	
				self.image_index +=1
			self.image = self.imagelist[self.image_index]
