import pygame
import random
import math
import time
# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
	import android
except ImportError:
	android = None
try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer

# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 30

# Color constants.
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
screen = pygame.display.set_mode((800, 480))
moto=pygame.image.load('images/moto3.png').convert_alpha()
crack1_image=pygame.image.load('images/crack.png').convert_alpha()
crack2_image=pygame.image.load('images/crack2.png').convert_alpha()
crack3_image=pygame.image.load('images/crack3.png').convert_alpha()
(w,h)=moto.get_size()
sky=pygame.image.load('images/sky2.png').convert_alpha()
#sky2=pygame.image.load('images/fondo2.png').convert_alpha()
panel_image=pygame.image.load('images/panel.png').convert_alpha()

def coordenadas((x,y),curva=0):
	factor2=(y)**2/10000.
	factor=(y)/100.
	npos_y=factor*480
	try: 
		npos_x=((x*400./100)*factor2+400)*factor**(curva/3.)
	except:
		npos_x=0.
	if y <= 120 and y > 0: 
		return  npos_x, npos_y, factor2
	else: 
		return npos_x, npos_y, False

pygame.font.init()
font = pygame.font.Font("Verdana.ttf", 21)

class Carretera:
	def __init__(self,screen=screen,color=(255,255,255),arco=False):
		self.screen=screen
		self.lineas=[]
		for i in range(110):
			self.lineas.append([-90,i])
		for i in range(110):
			self.lineas.append([90,109-i])
		self.curva=0.
		self.color=color
	def draw(self):
		l2=[]
		for i in self.lineas:
			npos_x,npos_y,factor=coordenadas(i,self.curva)
			l2.append([npos_x,npos_y])
		pygame.draw.polygon(self.screen,(100,100,100),l2,0)
		pygame.draw.lines(self.screen,(255,255,0),False,l2,2)
		
			
class Objeto:
	def __init__(self,screen=screen,pos=[0.,100.],vel=0.,color=(255,255,255),clase=0):
		self.screen=screen
		self.pos=pos
		self.curva=0.
		self.vel=vel
		self.radius=1
		self.clase=clase
	def carga_imagen(self):
		if self.clase == 1:
			self.surf=pygame.image.load('images/arbol.png').convert_alpha()
			(self.w,self.h)=self.surf.get_size()
			#print 'cargado arbol'
	def draw(self):
		npos_x,npos_y,factor=coordenadas(self.pos,self.curva)
		if npos_y > 100:
			if self.clase == 0 :
				pygame.draw.lines(self.screen,(255,255,0),False,[[npos_x-400*factor,npos_y],[npos_x-400*factor,npos_y-500*factor],[npos_x+400*factor,npos_y-500*factor],[npos_x+400*factor,npos_y]],int(20*factor+1))
			elif self.clase == 1 :
				#print 'pintando arbol'
				s=pygame.transform.scale(self.surf,(int(self.w*factor),int(self.h*factor)))
				(w,h)=s.get_size()
				self.screen.blit(s,(int(npos_x-w/2),int(npos_y-h)))#int(factor*100),1)

class Coche:
	def __init__(self,screen=screen,pos=[0.,100.],vel=0.,color=(255,255,255),arco=False):
		self.screen=screen
		self.pos=pos
		self.curva=0.
		self.vel=vel
		self.radius=1
		self.width=1
		self.arco=arco
		self.clase=0
		self.color=color
	def carga_imagen(self):
		if self.clase == 0:
			self.surf=pygame.image.load('images/coche.png').convert_alpha()
			(self.width,self.height)=self.surf.get_size()
		elif self.clase == 1:
			self.surf=pygame.image.load('images/medical_kit.png').convert_alpha()
			(self.width,self.height)=self.surf.get_size()
	def draw(self):
		npos_x,npos_y,factor=coordenadas(self.pos,self.curva)
		if npos_x and npos_y > 100:
			#pygame.draw.circle(self.screen,(255,0,0),(int(npos_x),int(npos_y)),int(self.radius*factor)+1,0)
			s=pygame.transform.scale(self.surf,(int(self.width*factor),int(self.height*factor)))
			screen.blit(s,(int(npos_x-self.width/2*factor),int(npos_y-self.height*factor)))


def panel(screen,panel_image,crack1_image,crack2_image,crack3_image,font,length,time,speed,lives,cracks):
	if cracks == 1:
		screen.blit(crack1_image,(0,0))
	elif cracks == 2:
		screen.blit(crack2_image,(0,0))
	elif cracks == 3:
		screen.blit(crack3_image,(0,0))
	pygame.draw.line(screen,(255,int(255*speed/100),0),[30,450],[30+1.2*speed,450],50)
	if lives >= 0:
		pygame.draw.line(screen,(255,0,0),[610,450],[600+65*lives,450],50)
	else:
		pygame.draw.line(screen,(255,0,0),[610,450],[600+65*0.,450],50)
	screen.blit(panel_image,(0,480-128))
	if time < 10:
		text_s = font.render(str(time)+' s', 1, (255, 255, 0))
		if length > 0:
			text_ss = font.render(str(length)+' m', 1, (255, 0, 0))
		else:
			text_ss = font.render(str(length)+' m', 1, (255, 255, 0))
	else:
		text_s = font.render(str(time)+' s', 1, (0, 255, 0))
		text_ss = font.render(str(length)+' m', 1, (0, 255, 0))
	
	textpos = text_s.get_rect()
	screen.blit(text_s, (textpos[0]+220,textpos[1]+440))
	screen.blit(text_ss, (textpos[0]+421,textpos[1]+440))

def main():
	if android:
			android.init()
			android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
			android.accelerometer_enable(True)
	
	carretera=Carretera()			
	speed=0.
	coches=[]
	bichos=[]
	bichos.append(Objeto())
	bichos[-1].pos=[-150.,15]
	bichos[-1].clase=1
	bichos[-1].carga_imagen()
	bichos.append(Objeto())
	bichos[-1].pos=[-150.,35]
	bichos[-1].clase=1
	bichos[-1].carga_imagen()
	bichos.append(Objeto())
	bichos[-1].pos=[150.,50]
	bichos[-1].clase=1
	bichos[-1].carga_imagen()
	pygame.display.update()
	stage=1
	TIMEREVENT = pygame.USEREVENT
	checkpoint=3000
	FPS=25
	t=0
	l=0
	dt=0.01
	pos=0
	vel=0
	t0=time.time()
	t00=time.time()+60
	last_coche=0
	lives=3
	dcoches=4
	cracks=0
	dentro=True
	if mixer:
		mixer.init()
		mixer.music.load('sound/blues.wav')
		mixer.music.play()
	while dentro:
		if android:
			if mixer.music_channel.get_busy()==False:
				mixer.music.play()
		else:
			if mixer.music.get_busy()==False:
				mixer.music.play()
		for ev in pygame.event.get():
			if pygame.mouse.get_pressed()[0]:
				speed*=0.95
			elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
				dentro=False
		t+=dt
		l+=dt*speed
		curva=math.cos(t)*0.75*math.sin(t/2+3)*math.cos(t/10+12)
		carretera.curva=curva
		n=0
		for i in bichos:
			i.vel=speed
			i.pos[1]+=speed*i.pos[1]*dt+dt
			i.curva=curva
			if i.pos[1] > 100:
				bichos.pop(n)
			n+=1
		n=0
		for i in coches:
			i.vel=speed
			i.pos[1]+=speed*i.pos[1]*dt+dt
			i.curva=curva
			if i.pos[1] > 85 and i.pos[1] < 95:
				#print i.pos[0]-pos
				if i.clase==0:
					if abs(i.pos[0]-pos) < 30:
						if android:
							android.vibrate(2)
						pygame.time.delay(2000)
						lives-=1
						cracks+=1
						if lives < 0:
							dentro=False
						speed*=0
						coches.pop(n)
				elif i.clase==1:
					if abs(i.pos[0]-pos) < 20:
						if lives < 3:
							lives+=1
						if cracks > 0:
							cracks-=1
						if android:
							android.vibrate(1)
						speed*=0
						coches.pop(n)
			if i.pos[1] > 120:
				coches.pop(n)
			n+=1
		if random.random() < 0.05:
			#print 'arbol'
			bichos.append(Objeto())
			if random.random() < 0.5:
				bichos[-1].pos=[150.,0.1]
			else:
				bichos[-1].pos=[-150.,0.1]
			bichos[-1].radius=800
			bichos[-1].clase=1
			bichos[-1].carga_imagen()
		if random.random() < 0.1 and t-last_coche > dcoches:
			coches.append(Coche())
			coches[-1].radius=100
			coches[-1].curva=curva
			if random.random() < 0.05:
				coches[-1].clase=1
			coches[-1].pos=[random.random()*150-75,0.1]
			coches[-1].carga_imagen()
			last_coche=t*1
		speed+=dt
		if pos > 100 or pos < -100:
			speed*=0.9
			if android:
				android.vibrate(0.1)
			if pos > 120:
				pos=120
				speed=0.
			elif pos < -120:
				pos = -120
				speed=0.
		if speed > 5:
			speed=5.
		if android:
			accels=android.accelerometer_reading()
			dpx=accels[1]*100
		else:
			dp=pygame.mouse.get_pos()
			dpx=(dp[0]-400)*2
		pos+=dt*curva*300*speed
		pos+=dpx*dt
		alpha=dpx/2*dt
		carretera.draw()
		screen.blit(sky,(0,0))
		#screen.blit(sky2,(int(-150-curva*150),0))
		for i in range(len(bichos)):
			bichos[-1-i].draw()
		for i in range(len(coches)):
			coches[-1-i].draw()
		motor=pygame.transform.rotate(moto,-int(alpha)*10)
		#(w,h)=motor.get_size()
		xn,yn,f=coordenadas((pos,90),curva)
		screen.blit(motor,(int(xn-w/2),int(yn-h)))
		while 1/(time.time()-t0) > 30:
			time.sleep(0.01)
		#display_text(screen,': '+str(int(speed*20)))
		if (t00-time.time()) < 0:
			lives-=1
			if android:
				android.vibrate(1)
			t00+=60
			if lives < 0:
				dentro=False
		elif l*100 < checkpoint*stage-500 and l*100 > checkpoint*stage-520:
			bichos.append(Objeto())
			bichos[-1].pos=[0.,0.1]
			bichos[-1].radius=800
			bichos[-1].clase=0
			bichos[-1].carga_imagen()
		elif l*100 > checkpoint*stage:
			stage+=1
			if checkpoint < 6000:
				checkpoint+=500
			t00+=60
			dcoches*=0.75
		panel(screen,panel_image,crack1_image,crack2_image,crack3_image,font,int(checkpoint*stage-l*100),int(t00-time.time()),speed*20,lives,cracks)
		pygame.display.update()
		t0=time.time()
		screen.fill((150,255,150))
	ending=pygame.image.load('images/ending.png').convert_alpha()
	screen.blit(ending,(0,0))
	pygame.display.flip()
	pygame.time.delay(5000)	

# This isn't run on Android.
if __name__ == "__main__":
	main()
