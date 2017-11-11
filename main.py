import sys, pygame
from pygame import *
from numpy import *
from random import randint, uniform

def main():
	mixer.pre_init(44100, -16, 1, 512)#no idea
	init()
	size = width, height = 800, 640
	speed = [0, 0]
	shoot = False
	black = 0, 0, 0
	blue = 110, 110, 255
	zoom = 1 # !=0 
	
	timer = time.Clock()
	screen = display.set_mode(size)
	display.set_caption("Killer Bunny: The Game")
	
	up = down = left = right = running = False
	was_right= True
	was_left= False
	
	
	W_width = 0
	W_height = 0
	generation = gen_world("springs1.png")
	world = generation[0] #entities
	player = generation[1]
	W_width = generation[2][0]
	W_height = generation[2][1]
	tokens = generation[3] #chillies
	CameraX = player.rect.x
	CameraY = player.rect.y - 700#pikslites
	
	GUI = pygame.sprite.Group()
	healthport = GUI_portrait("healthbarport.png",[10,10])
	manaport = GUI_portrait("pentagram.png", [10,60])
	health = GUI_bar((255,0,0), player.maxhp, [36,33])
	mana = GUI_bar((100,0,230), player.maxmana, [52,73])
	GUI.add(healthport)
	GUI.add(health)
	GUI.add(manaport)
	GUI.add(mana)
	
	anim_list = pygame.sprite.Group()
	smoke_list = pygame.sprite.Group()
	
	enemies = pygame.sprite.Group()
	
	hillbilly = Hillbilly()
	enemies.add(hillbilly)
	
	current_state="standR"
	#main game loop
	while 1:
		timer.tick(60)
		for e in event.get():
			if e.type == QUIT:
				sys.exit()
			if e.type == KEYUP and e.key == K_SPACE:
				shoot = False
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				sys.exit()
			if e.type == KEYUP and e.key == K_UP:
				up = False
				player.jumped = True #muidu teeb hüppe kohe ära
			if e.type == KEYUP and e.key == K_DOWN:
				down = False
			if e.type == KEYUP and e.key == K_RIGHT:
				right = False
				was_right= True
				was_left= False
				current_state = "standR"
			if e.type == KEYUP and e.key == K_LEFT:
				left = False
				was_left= True
				was_right= False
				current_state = "standL"
			if e.type == KEYDOWN and e.key == K_UP:
				up = True
			if e.type == KEYDOWN and e.key == K_DOWN:
				down = True
			if e.type == KEYDOWN and e.key == K_LEFT:
				left = True
				was_left= True
				was_right= False
			if e.type == KEYDOWN and e.key == K_RIGHT:
				right = True
				was_right= True
				was_left= False
			if e.type == KEYDOWN and e.key == K_SPACE:
				shoot = True
		
		player.update(current_state, up, down, left, right, was_left, was_right,shoot, world, current_state, anim_list, smoke_list, CameraX, CameraY)
		
		player.rect = player.rect.move(speed)
		if player.rect.x > size[0]//2+CameraX and CameraX < W_width-width: #zoom tuleviku jaoks
			CameraX += 4
		if player.rect.y > size[1]//2+CameraY and CameraY + height < 32*32:
			CameraY += 4
		if player.rect.x < size[0]//2+CameraX and CameraX > 0:
			CameraX -= 4
		if player.rect.y < size[1]//2+CameraY and CameraY > 0:
			CameraY -= 4

		screen.fill(blue)
		for tile in world:
			screen.blit(tile.image,(tile.rect.x -CameraX,tile.rect.y -CameraY))

		for fire in anim_list:

			rand=randint(1,5)
			if rand == 3:
				if fire.lugeja >= 40:
					anim_list.remove(fire)
		
		screen.blit(player.image,(player.rect.x -CameraX,player.rect.y -CameraY))
		anim_list.update()
		smoke_list.update()
		for enemy in enemies:
			screen.blit(enemy.image,(enemy.rect.x -CameraX,enemy.rect.y -CameraY))
			
		for fire in anim_list:
			screen.blit(fire.image,(fire.rect.x -CameraX,fire.rect.y -CameraY))
			
		for chilly in tokens:
			screen.blit(chilly.image, (chilly.rect.x -CameraX,chilly.rect.y -CameraY))
			
		for smoke in smoke_list:
			screen.blit(smoke.image,(smoke.rect.x -CameraX,smoke.rect.y -CameraY))
			if smoke.imgcount == 6:
				smoke_list.remove(smoke)
		
		GUI.draw(screen)
		health.update(player.hp)
		mana.update(player.mana)
		enemies.update(world)
		tokens.update()
		
		display.flip()

class Hillbilly(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.imagesR= [image.load("hillyR.png").convert_alpha(),
						image.load("hillyR1.png").convert_alpha(),
						image.load("hillyR.png").convert_alpha(),
						image.load("hillyR2.png").convert_alpha()]
		self.imagesL= [image.load("hillyL.png").convert_alpha(),
						image.load("hillyL1.png").convert_alpha(),
						image.load("hillyL.png").convert_alpha(),
						image.load("hillyL2.png").convert_alpha()]
		self.imagedict= {"imgR": self.imagesR, "imgL": self.imagesL}
		self.index= 0
		self.lugeja= 0
		self.standing= False
		self.image= self.imagedict["imgR"][self.index]
		self.rect= self.image.get_rect()
		self.onGround = False
		self.yvel=0
		self.xvel=0
	
	def update(self, platforms):
		self.rect.x +=1
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 80: self.yvel = 80
		self.collide(self.xvel, self.yvel, platforms)
		self.rect.top += self.yvel
		self.onGround= False
		self.collide(0, self.yvel, platforms)
		self.animate()
	
	def animate(self):
		if not self.standing:
			self.lugeja+=1
			if self.lugeja == 6:
				if self.index != 3:
					self.index+= 1
				else:
					self.index= 0
				self.lugeja= 0
			self.image= self.imagedict["imgR"][self.index]
		
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
					self.yvel = 0
				if yvel < 0:
					self.rect.top = p.rect.bottom
					self.yvel += 1
		
class Player(sprite.Sprite):
	def __init__(self, width, height):
		sprite.Sprite.__init__(self)
		self.stand_imagesR= [image.load("Stand_R.png").convert_alpha(),
							image.load("Stand_R2.png").convert_alpha(),
							image.load("Stand_R3.png").convert_alpha(),
							image.load("Stand_R4.png").convert_alpha()]
		
		self.stand_imagesL= [image.load("Stand_L.png").convert_alpha(),
							image.load("Stand_L2.png").convert_alpha(),
							image.load("Stand_L3.png").convert_alpha(),
							image.load("Stand_L4.png").convert_alpha()]
							
		self.run_imagesR= [image.load("0R.png").convert_alpha(),
							image.load("1R.png").convert_alpha(),
							image.load("2R.png").convert_alpha(),
							image.load("3R.png").convert_alpha(),
							image.load("4R.png").convert_alpha()]
		
		self.run_imagesL= [image.load("0L.png").convert_alpha(),
							image.load("1L.png").convert_alpha(),
							image.load("2L.png").convert_alpha(),
							image.load("3L.png").convert_alpha(),
							image.load("4L.png").convert_alpha()]
							
		self.duck_imagesR= [image.load("Ducking_R.png").convert_alpha(),
							image.load("Ducking_R.png").convert_alpha(),
							image.load("Ducking_R.png").convert_alpha(),
							image.load("Ducking_R.png").convert_alpha(),
							image.load("Ducking_R.png").convert_alpha(),
							image.load("Ducking_R2.png").convert_alpha(),
							image.load("Ducking_R3.png").convert_alpha(),
							image.load("Ducking_R4.png").convert_alpha(),
							image.load("Ducking_R4.png").convert_alpha(),
							image.load("Ducking_R4.png").convert_alpha(),
							image.load("Ducking_R4.png").convert_alpha(),
							image.load("Ducking_R4.png").convert_alpha(),
							image.load("Ducking_R3.png").convert_alpha(),
							image.load("Ducking_R2.png").convert_alpha()]
		
		self.duck_imagesL= [image.load("Ducking_L.png").convert_alpha(),
							image.load("Ducking_L.png").convert_alpha(),
							image.load("Ducking_L.png").convert_alpha(),
							image.load("Ducking_L.png").convert_alpha(),
							image.load("Ducking_L.png").convert_alpha(),
							image.load("Ducking_L2.png").convert_alpha(),
							image.load("Ducking_L3.png").convert_alpha(),
							image.load("Ducking_L4.png").convert_alpha(),
							image.load("Ducking_L4.png").convert_alpha(),
							image.load("Ducking_L4.png").convert_alpha(),
							image.load("Ducking_L4.png").convert_alpha(),
							image.load("Ducking_L4.png").convert_alpha(),
							image.load("Ducking_L3.png").convert_alpha(),
							image.load("Ducking_L2.png").convert_alpha()]
							
		self.shoot_imagesR=[image.load("Shoot_R.png").convert_alpha(),
							image.load("Shoot_R2.png").convert_alpha()]
							
		self.shoot_imagesL=[image.load("Shoot_L.png").convert_alpha(),
							image.load("Shoot_L2.png").convert_alpha()]
							
		self.dict={"standR": self.stand_imagesR, "standL": self.stand_imagesL, "runR":self.run_imagesR, "runL":self.run_imagesL, "duckL":self.duck_imagesL, "duckR":self.duck_imagesR, "shootR":self.shoot_imagesR, "shootL": self.shoot_imagesL}
		self.xvel = 0
		self.yvel = 0
		self.hp = 100
		self.maxhp = 100
		self.maxmana = 84
		self.mana = 84
		self.onGround = False
		self.can_jump = False
		self.jumped = False
		self.index = 0
		self.image = self.stand_imagesR[self.index]
		self.rect = self.image.get_rect()
		self.vahe=0
		self.jump_sound = pygame.mixer.Sound('hupe.wav')
		self.Djump_sound = pygame.mixer.Sound('Jumpsound.wav')
		self.fire_sound = pygame.mixer.Sound('jumperoo.wav')
	
	def update(self, key, up, down, left, right, was_left, was_right, shoot, platforms, anim_state, anim_list, smoke_list, CameraX, CameraY):		
		current_state = anim_state
		
		#movement
		if up:
			if self.onGround: 
				self.jump_sound.play()
				self.yvel -= 10
				self.can_jump = True
			elif self.can_jump and self.jumped:
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
		if shoot and not right and not left and not down:
			if self.mana > 0:
				self.mana-=1
				if was_left:
					current_state = "shootL"
					for i in range(5):
						rand = randint(1,2)
						if rand == 2:
							fire = Fire(False)
							fire.rect.x = self.rect.x +8
							fire.rect.y = self.rect.y +37
							anim_list.add(fire)
					if not mixer.get_busy():
						self.fire_sound.play()
				elif was_right:
					current_state = "shootR"
					for i in range(5):
						rand = randint(1,2)
						if rand == 2:
							fire = Fire(True)
							fire.rect.x = self.rect.x +28
							fire.rect.y = self.rect.y +37
							anim_list.add(fire)
					if not mixer.get_busy():
						self.fire_sound.play()
		else:
			self.fire_sound.fadeout(500)
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
	
	def animate(self, key):
		self.vahe+=1
		if self.vahe == 6:
			self.index+=1
			if self.index >= len(self.dict.get(key)):
				self.index = 0
			self.image = self.dict.get(key)[self.index]
			self.vahe = 0
	
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

class Smoke(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.imagelist = [image.load("cloud1.png").convert_alpha(),
						image.load("cloud2.png").convert_alpha(),
						image.load("cloud3.png").convert_alpha(),
						image.load("cloud4.png").convert_alpha(),
						image.load("cloud5.png").convert_alpha(),
						image.load("cloud6.png").convert_alpha(),
						image.load("cloud6.png").convert_alpha()]
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

class Tile(sprite.Sprite):
	def __init__(self,x,y,img):
		sprite.Sprite.__init__(self)
		self.image = image.load(img).convert_alpha()
		self.rect = self.image.get_rect().move(32*x, 32*y)

class Chilly(sprite.Sprite):
	def __init__(self,x,y):
		sprite.Sprite.__init__(self)
		self.imagelist=[image.load("chilly.png").convert_alpha(),
						image.load("chilly2.png").convert_alpha(),
						image.load("chilly3.png").convert_alpha(),
						image.load("chilly4.png").convert_alpha(),
						image.load("chilly3.png").convert_alpha(),
						image.load("chilly2.png").convert_alpha()]
		self.image_index = 0
		self.image = self.imagelist[self.image_index]
		self.rect = self.image.get_rect().move(32*x,32*y)
		self.lugeja = 0
	
	def update(self):
		self.animate()
	
	def animate(self):
		if self.lugeja == 6:
			self.lugeja = 0
			self.image_index+=1
			if self.image_index > 5:
				self.image_index = 0
			self.image = self.imagelist[self.image_index]
		else:
			self.lugeja +=1
		
class Fire(sprite.Sprite):
	def __init__(self, speed):
		sprite.Sprite.__init__(self)
		self.imagelist=[image.load("fire.png").convert_alpha(),
						image.load("fire2.png").convert_alpha(),
						image.load("fire3.png").convert_alpha(),
						image.load("fire4.png").convert_alpha(),
						image.load("fire5.png").convert_alpha()]
		self.image_index=0
		self.image = self.imagelist[self.image_index]
		self.rect = self.image.get_rect()
		self.lugeja=0
		self.vp=speed
		if self.vp == True:
			self.speed = randint(3,5)
		elif self.vp == False:
			self.speed = randint(-5,-3)
	
	def update(self):
		dest = randint(-4,4)
		self.rect.y += dest
		self.rect.x +=self.speed
		self.lugeja+=1
		self.animate()
		
	def animate(self):
			image_rand=randint(1,8)
			if image_rand == 4 and self.image_index != 4:	
				self.image_index +=1
			self.image = self.imagelist[self.image_index]
			
class GUI_portrait(sprite.Sprite):
	def __init__(self, img, offset):
		sprite.Sprite.__init__(self)
		self.image = image.load(img).convert_alpha()
		self.rect = self.image.get_rect().move(offset)

class GUI_bar(sprite.Sprite):
	def __init__(self, color, maxvalue, offset):
		sprite.Sprite.__init__(self)
		self.width = maxvalue
		self.color = color
		self.image = Surface([self.width,12])
		self.rect = self.image.get_rect().move(offset)
		self.image.fill(color)
	
	def update(self, value):
		self.width = value
		self.image = Surface([self.width,12])
		self.image.fill(self.color)
			
def gen_world(filename):
	img = image.load(filename)
	rgbarray = surfarray.array3d(img)
	world_width = len(rgbarray)
	world_height = len(rgbarray[0])
	entities = sprite.Group()
	token_list = sprite.Group()
	
	newlist = []
	
	i = 0
	while i < img.get_height():
		entities.add(Tile(-1,i,"wall.png"))
		entities.add(Tile(img.get_width(),i,"wall.png"))
		i+=1
	
	for i in range(len(rgbarray)): #y
		for j in range(len(rgbarray[0])): #x
			r = rgbarray[i][j][0]
			g = rgbarray[i][j][1]
			b = rgbarray[i][j][2]
			
			if(r==237): #muruga pealmine osa
				entities.add(Tile(i,j,"dirt_top.png"))
			if(r==200): #ilma muruta mulla osa
				entities.add(Tile(i,j,"dirt_under.png"))
			if(r==238): #muruga parem pool
				entities.add(Tile(i,j,"dirt_top_right.png"))
			if(r==236): #muruga vasak pool
				entities.add(Tile(i,j,"dirt_top_left.png"))
			if(g==255):
				player = Player(64,64)
				player.rect=player.rect.move([i*32,j*32])
			if(g==200 and b==200):
				token_list.add(Chilly(i,j))
			
	newlist.append(entities)
	newlist.append(player)
	newlist.append([world_width*32, world_height*32])
	newlist.append(token_list)
			
	return newlist

main()