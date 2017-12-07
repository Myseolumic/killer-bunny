import sys, pygame
from pygame import *
from numpy import *
from random import *

from npcs import *
from bunny import *

def main():
	mixer.pre_init(44100, -16, 1, 512)
	pygame.mixer.init()
	mixer.set_num_channels(8) # 5 ja 7 kasutuses
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
	generation = gen_world("res/springs1.png")
	world = generation[0] #entities
	player = generation[1]
	W_width = generation[2][0]
	W_height = generation[2][1]
	tokens = generation[3] #chillies
	endblock = generation[5] #4 on vastastele
	endblock.id = 1
	
	CameraX = player.rect.x
	CameraY = player.rect.y - 700#pikslites
	
	background = image.load("res/background.png").convert_alpha()
	background = transform.scale(background, (W_width, W_height))
	
	GUI = pygame.sprite.Group()
	healthport = GUI_portrait("res/healthbarport.png",[10,10])
	manaport = GUI_portrait("res/pentagram.png", [10,60])
	health = GUI_bar((255,0,0), player.maxhp, [36,33])
	mana = GUI_bar((100,0,230), player.maxmana, [52,73])
	GUI.add(healthport)
	GUI.add(health)
	GUI.add(manaport)
	GUI.add(mana)
	
	enemies = generation[4]
	anim_list = pygame.sprite.Group()
	smoke_list = pygame.sprite.Group()
	proj_list = pygame.sprite.Group()
	billybullets= pygame.sprite.Group()
	
	current_state="standR"
	#main game loop
	while 1:
		timer.tick(60)
		#background render
		screen.blit(background,(0-CameraX/4,0-CameraY/4))
		
		#new world loading
		if endblock.next:
			endblock.next = False
			endblock.id += 1
			generation = gen_world("res/springs"+str(endblock.id)+".png")
			world = generation[0]
			player = generation[1]
			W_width = generation[2][0]
			W_height = generation[2][1]
			tokens = generation[3]
			enemies = generation[4]
						
			anim_list.empty()
			smoke_list.empty()
			proj_list.empty()
			billybullets.empty()
			
			endblock_data = generation[5]
			endblock.rect = endblock_data.rect
			CameraX = 0
			CameraY = 200
			while endblock.alpha > 0:
				endblock.blackScreen(-1)
		
		if player.controlsEnabled :
			for e in event.get():
				if e.type == QUIT:
					sys.exit()
				if e.type == KEYUP and e.key == K_SPACE:
					shoot = False
					if player.chargelevel >50:
						player.charged = True
					else:
						player.chargelevel = 0
				if e.type == KEYDOWN and e.key == K_ESCAPE:
					sys.exit()
				if e.type == KEYUP and e.key == K_UP:
					up = False
					player.jumped = True #muidu teeb hüppe kohe ära
				if e.type == KEYUP and e.key == K_DOWN:
					down = False
					player.ducking = False
				if e.type == KEYUP and e.key == K_RIGHT:
					right = False
					was_right= True
					was_left= False
					if not player.charged:
						current_state = "standR"
					else:
						current_state = "chargedR"
				if e.type == KEYUP and e.key == K_LEFT:
					left = False
					was_left= True
					was_right= False
					if not player.charged:
						current_state = "standL"
					else:
						current_state = "chargedL"
				if e.type == KEYDOWN and e.key == K_UP:
					up = True
				if e.type == KEYDOWN and e.key == K_DOWN:
					down = True
					player.ducking = True
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
				if e.type == KEYUP and e.key == K_q:
					player.voidballin = False
				if e.type == KEYDOWN and e.key == K_q:
					player.voidballin = True
				if e.type == KEYUP and e.key == K_w:
					player.blastin = False
				if e.type == KEYDOWN and e.key == K_w:
					player.blastin = True
		elif endblock.loading:
			right = False
			was_right= True
			was_left= False
			current_state = "standR"
			
			#for closing the game
			for e in event.get():
				if e.type == QUIT:
					sys.exit()
		elif player.dead:
			player.deathScreen_rect.x = CameraX
			player.deathScreen_rect.y = CameraY
			
			#same as the comment above
			for e in event.get():
				if e.type == QUIT:
					sys.exit()
		
		
		player.rect = player.rect.move(speed)
		
		#Camera movement
		if player.rect.x > size[0]//2+CameraX and CameraX < W_width-width:
			if player.charged:
				CameraX += 6
			else:
				CameraX += 4
		if player.rect.y > size[1]//2+CameraY and CameraY + height < 32*32:
			CameraY += 4
		if player.rect.x < size[0]//2+CameraX and CameraX > 0:
			if player.charged:
				CameraX -= 6
			else:
				CameraX -= 4
		if player.rect.y < size[1]//2+CameraY and CameraY > 0:
			CameraY -= 4

		for tile in world:
			screen.blit(tile.image,(tile.rect.x -CameraX,tile.rect.y -CameraY))

		for fire in anim_list:
			if fire.lugeja >= 20:
				anim_list.remove(fire)
		

		anim_list.update()
		smoke_list.update()

			
		for enemy in enemies:
			screen.blit(enemy.image,(enemy.rect.x -CameraX,enemy.rect.y -CameraY))
			screen.blit(enemy.aggroArea.image,(enemy.rect.x -CameraX -150,enemy.rect.y -CameraY))
			
		for fire in anim_list:
			screen.blit(fire.image,(fire.rect.x -CameraX,fire.rect.y -CameraY))
			
		for bullet in billybullets:
			screen.blit(bullet.image,(bullet.rect.x -CameraX, bullet.rect.y -CameraY))

		for proj in proj_list:
			screen.blit(proj.image,(proj.rect.x -CameraX,proj.rect.y -CameraY))
			
		for chilly in tokens:
			screen.blit(chilly.image, (chilly.rect.x -CameraX,chilly.rect.y -CameraY))
			
		for smoke in smoke_list:
			screen.blit(smoke.image,(smoke.rect.x -CameraX,smoke.rect.y -CameraY))
			if smoke.imgcount == 6:
				smoke_list.remove(smoke)
		
		#finish
		screen.blit(endblock.image,(endblock.rect.x -CameraX,endblock.rect.y -CameraY))
		
		if not player.dead:
			player.update(current_state, up, down, left, right, was_left, was_right,shoot, world, current_state, anim_list, smoke_list, proj_list, CameraX, CameraY)
		else:
			up = False
			down = False
			left = False
			right = False
			if was_left:
				#death_animation
				player.update("standL", False, False, False, False, True, False, False, world, "standL", anim_list, smoke_list, proj_list, CameraX, CameraY)
			else: #was_right
				#death_animation
				player.update("standR", False, False, False, False, False, True, False, world, "standR", anim_list, smoke_list, proj_list, CameraX, CameraY)
		
		screen.blit(player.image,(player.rect.x -CameraX,player.rect.y -CameraY))		
		GUI.draw(screen)
		health.update(player.hp)
		mana.update(player.mana)
		proj_list.update(anim_list, enemies, proj_list, world)
		enemies.update(world, player,billybullets, enemies)
		tokens.update()
		billybullets.update(world, billybullets, player)
		endblock.update(player, screen, CameraX, CameraY)
		
		if player.dead:
			screen.blit(player.deathScreen, (player.deathScreen_rect.x -CameraX, player.deathScreen_rect.y -CameraY))
			speed = (0,0) #igaks juhuks
			if player.deathScreen.get_alpha() == 255:
				player.rect.x = player.origin[0]
				player.rect.y = player.origin[1]
				player.deathvar = -2
		
		display.flip()
		
class Tile(sprite.Sprite):
	def __init__(self,x,y,img):
		sprite.Sprite.__init__(self)
		self.image = image.load(img).convert_alpha()
		self.rect = self.image.get_rect().move(32*x, 32*y)

class Finish(sprite.Sprite):
	def __init__(self,x,y,img, W_width, W_height):
		sprite.Sprite.__init__(self)
		self.image = image.load(img).convert_alpha()
		self.rect = self.image.get_rect().move(32*x, 32*y)
		
		self.screensaver = Surface((W_width,W_height))
		self.screensaver.fill((0,0,0))
		self.screensaver_rect = self.screensaver.get_rect()
		self.screensaver.set_alpha(70)
		self.alpha = 0
		self.vahe = 0
		self.next = False
		self.loading = False
		self.id = 1
	
	def update(self, player, screen, CameraX, CameraY):
		deltax = player.rect.x - self.rect.x

		if sprite.collide_rect(self, player) and deltax >= 20:
			self.screensaver_rect.x = CameraX
			self.screensaver_rect.y = CameraY
			player.controlsEnabled = False
			self.loading = True
			self.blackScreen(1)
			screen.blit(self.screensaver, (self.screensaver_rect.x-CameraX, self.screensaver_rect.y-CameraY))
			if self.next :
				print("Loading!")
			
	def blackScreen(self, value):
		self.vahe += 1
		if self.vahe == 3:
			self.alpha += 10 * value
			if self.alpha >= 255:
				self.next = True
			if self.alpha <= 0 :
				self.alpha = 0
			self.vahe = 0
			self.screensaver.set_alpha(self.alpha)
				
class Chilly(sprite.Sprite):
	def __init__(self,x,y):
		sprite.Sprite.__init__(self)
		self.imagelist=[image.load("res/chilly.png").convert_alpha(),
						image.load("res/chilly2.png").convert_alpha(),
						image.load("res/chilly3.png").convert_alpha(),
						image.load("res/chilly4.png").convert_alpha(),
						image.load("res/chilly3.png").convert_alpha(),
						image.load("res/chilly2.png").convert_alpha()]
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
	try:
		img = image.load(filename)
	except pygame.error:
		print("Ran out of levels, sorry :(")
		sys.exit()
	rgbarray = surfarray.array3d(img)
	world_width = len(rgbarray)
	world_height = len(rgbarray[0])
	entities = sprite.Group()
	enemies = sprite.Group()
	token_list = sprite.Group()
	
	newlist = []
	
	i = 0
	while i < img.get_height():
		entities.add(Tile(-1,i,"res/wall.png"))
		entities.add(Tile(img.get_width(),i,"res/wall.png"))
		i+=1
	
	for i in range(len(rgbarray)): #y
		for j in range(len(rgbarray[0])): #x
			r = rgbarray[i][j][0]
			g = rgbarray[i][j][1]
			b = rgbarray[i][j][2]
			
			if(r==237): #muruga pealmine osa
				entities.add(Tile(i,j,"res/dirt_top.png"))
			if(r==200): #ilma muruta mulla osa
				entities.add(Tile(i,j,"res/dirt_under.png"))
			if(r==238): #muruga parem pool
				entities.add(Tile(i,j,"res/dirt_top_right.png"))
			if(r==236): #muruga vasak pool
				entities.add(Tile(i,j,"res/dirt_top_left.png"))
			if(g==255 and r!=255):
				player = Player(64,64)
				player.rect = player.rect.move([i*32,j*32])
				player.origin = [i*32,j*32]
			if(g==200 and b==200):
				token_list.add(Chilly(i,j))
			if(r==255 and g==255):
				finish = Finish(i,j,"res/Cave.png",800,640) #screen width, height
			if(b==150):
				hillbilly = Hillbilly(i*32,j*32)
				enemies.add(hillbilly)
			if(r==205 and g==205):
				dog = Dog(i*32,j*32)
				enemies.add(dog)
			
	newlist.append(entities)
	newlist.append(player)
	newlist.append([world_width*32, world_height*32])
	newlist.append(token_list)
	newlist.append(enemies)
	newlist.append(finish)
	
	return newlist

main()