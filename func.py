# -*- coding: utf-8 -*-
import pygame
import os
import types

v_dist =lambda x1,y1,x2,y2:(x1-x2)**2+(y1-y2)**2
v_make =lambda x1,y1,x2,y2:((x2-x1),(y2-y1))
v_mak  =lambda x,y:(y[0]-x[0],y[1]-x[1])
v_cha  =lambda x,y:x[0]*y[1]-x[1]*y[0]
v_dan  =lambda x,y:x[0]*x[1]+y[1]*y[0]
v_dis  =lambda x1,y1,x2,y2:math.sqrt(v_dist(x1,y1,x2,y2))
isze   =lambda x:0 if abs(x)<0.000001 else 1 if x>0 else -1
v_cro  =lambda x,y,z:isze(v_cha(v_mak(x,y),v_mak(x,z)))
p_img=lambda x,y,z:pygame.transform.scale(pygame.image.load(x).convert_alpha(),(y,z))
j_img=lambda x,y,z:pygame.transform.scale(pygame.image.load(x).convert(),(y,z))

class Button():
	def __init__(self,x,y,w,h,i,f,k=0,*args):
		self.x,self.y,self.w,self.h,self.f,self.i,self.k=x,y,w,h,f,i,k
		if i>0:
			self.img0=p_img('pics/btn/btn'+str(i)+'_0.png',w,h)
			self.img1=p_img('pics/btn/btn'+str(i)+'_1.png',w,h)
		self.cd=0
		self.args=args
		if type(self.k) is types.StringType:
			self.k=ord(self.k)

	def run(self,timep,mou_pos,moup,keyp,screen):
		self.cd=max(0,self.cd-timep)
		oin=mou_pos[0]>=self.x and mou_pos[0]<=self.x+self.w
		oin&=mou_pos[1]>=self.y and mou_pos[1]<=self.y+self.h
		pud=(oin and moup[0]) or (keyp[self.k] if self.k>0 else 0)
		if pud and self.cd<=0 and type(self.f) is types.FunctionType:
			self.cd=150
			self.f(self.args)
		if self.i:
			screen.blit(self.img1 if oin else self.img0,(self.x,self.y))

class Txt():
	def __init__(self,x,y=30,z=(0,0,0),_x=0,_y=0):
		self.font = pygame.font.Font("font/hanyi.ttf", y)
		self.wen = self.font.render(unicode(x,"utf8"),True,z)
		self._x,self._y=_x,_y
	def run(self,screen):
		screen.blit(self.wen,(self._x,self._y))
		

class Sound:
	def __init__(self):
		self.sd=[]
		src='sound/sd'
		for i in xrange(100):
			if os.path.exists(src+str(i)+'.wav'):
				now=pygame.mixer.Sound(src+str(i)+'.wav')
				now.set_volume(.5)
				if i==6:
					now.set_volume(.15)
				self.sd.append(now)
			else:
				break
	def play(self,x):
		self.sd[x].play()

class Lh():
	def __init__(self):
		self.lhs={}
		src='pics/lh/lh'
		for i in xrange(1,100):
			if os.path.exists(src+self.deal(i)+'_00.png'):
				for j in xrange(100):
					if os.path.exists(src+self.deal(i)+'_'+self.deal(j)+'.png'):
						sr=src+self.deal(i)+'_'+self.deal(j)+'.png'
						if i==3 or i==4 or i==9:
							self.lhs[self.deal(i)+self.deal(j)]=p_img(sr,290,560)
						else:
							self.lhs[self.deal(i)+self.deal(j)]=p_img(sr,310,430)
					else:
						break
			else:
				break

	def deal(self,x):
		return '0'+str(x) if x<10 else str(x)

class Music:
	playing =	0
	musics	=	[]
	def __init__(self):
		src='music/m'
		self.now=-1
		for i in xrange(100):
			if os.path.exists(src+str(i)+'.mid'):
				self.musics.append(src+str(i)+'.mid')
			else:
				break

	def change(self,x):
		if x==self.now:
			return
		self.now=x
		pygame.mixer.music.stop()
		pygame.mixer.music.load(self.musics[x])
		pygame.mixer.music.play(-1)
		self.playing	=	1

	def play(self):
		self.playing	=	1
		pygame.mixer.music.play()

	def pause(self):
		if self.playing==1:
			self.playing=0
			pygame.mixer.music.pause()
		else:
			self.playing=1
			pygame.mixer.music.unpause()
