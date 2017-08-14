# -*- coding: utf-8 -*-
import pygame
import math
import random
from pygame.locals import *
from sys import exit
import os
import types

from func import *
#*****************************************************************************************
#******************************** base **************************************************
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
#pygame.mixer.pre_init(44100,-16,2,4096)
pygame.mixer.set_num_channels(10)
pygame.mixer.init()

_width,_height=1000,650
_size=(_width,_height)
pygame.display.init()
pygame.display.set_caption("game")
screen = pygame.display.set_mode(_size,0,32)
#screen = pygame.display.set_mode(_size,FULLSCREEN,32)


#********************************* globals ************************************************
lding=j_img('pics/bk/loading.jpg',_width,_height)
screen.blit(lding,(0,0))

Adr 	=	'???'
syss 	=	[]
btns  	= 	[]
txts  	= 	[]
items 	= 	[]
gods  	= 	[0] * 100
flags 	= 	[0] * 100
#*********************************** defs ************************************************
def diag_gon(*args):
	global  moji,sysb
	if sysb.showing==0 and moji.talking and moji.cango:
		moji.goon=1
def chev(*args):
	global  story,btns,txts,sound
	sound.play(10)
	story.last_code=0
	story.event=args[0][0]
	btns,txts=[],[]
def ch_wtf(*args):
	global  story,btns,txts,sound
	story.last_code=0
	sound.play(10)
	story.wtf(args[0][0],0)
	btns,txts=[],[]
def cha_wtf(*args):
	global  story,btns,txts,sound
	story.last_code=0
	sound.play(10)
	story.wtf(args[0][0],args[0][1])
	btns,txts=[],[]
def sys_sho(*args):
	global items,moji,sound,story,btns,txts
	sound.play(8)
	if sysb.showing==0:
		if story.event==0 and args[0][0]<4:
			btns,txts=[],[]
			if story.last_code!=args[0][0]:
				story.code=args[0][0]
			else:
				story.last_code=0
				story.code=0
	if args[0][0]==4:
		sysb.showing^=1

def ch_sho(*args):
	global sysb,sound
	if sysb.showing:
		sound.play(8)
		sysb.pt+=1 if args[0][0]==2 else sysb.n-1
		sysb.pt%=sysb.n
def an_ji(*args):
	global sysb,moji,story
	diag_gon()
	if sysb.showing:
		if args[0][0]==1:
			global items
			moji.zz=items[sysb.pt].id
		else:
			sysb.showing=0
	elif args[0][0]==2:
		story.code=0
		sysb.showing=0

def get_item(x):
	if gods[x]:
		return
	global items,sysb,sound
	if x>0:
		sound.play(6)
	items.append(Item(x))
	sysb.n+=1
	gods[x]=1
def del_item(x):
	global items,sysb
	for i in items:
		if i.id==x:
			items.remove(i)
			sysb.n-=1
			sysb.pt=0
			gods[x]=0
			return
def set_adr(x):
	global Adr
	Adr=x
def ch_flag(x,*args):
	for i in args:
		if x&i==0:
			return 0
	return 1

#*********************************** sys ************************************************
syss.append(Button(50,510,900,140,0,diag_gon))
syss.append(Button(0,0,0,0,0,sys_sho,'q',1))
syss.append(Button(0,0,0,0,0,sys_sho,'w',2))
syss.append(Button(0,0,0,0,0,sys_sho,'e',3))
syss.append(Button(0,0,0,0,0,sys_sho,'r',4))
syss.append(Button(0,0,0,0,0,an_ji,K_z,1))
syss.append(Button(0,0,0,0,0,an_ji,K_x,2))
syss.append(Button(0,0,0,0,0,ch_sho,K_LEFT,1))		
syss.append(Button(0,0,0,0,0,ch_sho,K_a,1))		
syss.append(Button(0,0,0,0,0,ch_sho,K_RIGHT,2))		
syss.append(Button(0,0,0,0,0,ch_sho,K_d,2))		
#********************************** class ************************************************
class Moji():
	def __init__(self):
		self.talking = 0
		self.pt 	 = 1
		self.cd 	 = 0
		self.zz 	 = -1
		self.now 	 = 0
		self.sta 	 = 0
		self.cango 	 = 1
		self.goon 	 = 0
		self.lens = [0] * 1000
		self.diag = [0] * 1000
		self.font = pygame.font.Font("font/hanyi.ttf", 25)
		self.fon2 = pygame.font.Font("font/hanyi.ttf", 45)
		self.color= (0,0,0)
		self.c2	  = (45,150,50)
		self.c3	  = (65,90,200)
		self.bd	  = p_img('pics/diag_board.png',900,140)
		self.px,self.py=50,510
		src='diags/da'

		for i in xrange(1000):
			if os.path.exists(src+str(i)):
				mm=open(src+str(i),'r').read()
				mm=unicode(mm,"utf8").split('###\n')
				for k in mm:
					if len(k)<2:
						continue
					k=k.split('\n')
					now_id=int(k[0])
					self.diag[now_id]=[0]
					for j in k[1:]:
						if len(j)<2:
							continue
						self.diag[now_id][0]+=1
						now=j.split(' ')
						now.append(1 if now[5][0]=='#' else 2 if now[5][0]=='*' else 0)
						xx=now[5][1:] if now[5][0]=='#' or now[5][0]=='*' else now[5]
						self.diag[now_id].append([now[0],now[1],now[2],now[3],int(now[4]),xx,now[6]])
			else:
				break
	def rd(self,x,y):
		return self.font.render(x,True,self.c2 if y==1 else self.color)
	def rdd(self,x):
		return self.fon2.render(x,True,self.c3)
	def set(self,x):
		global story
		story.last_code=0
		self.talking = 1
		self.pt 	 = 1
		self.cd 	 = 500
		self.now 	 = x
		self.zz 	 = -1
		self.cango 	 = 1
		self.sta 	 = 0
		self.goon 	 = 0
	def work(self):
		global Adr,screen,story
		if story.event==0:
			tt='-调查' if self.sta==1 else '-移动' if self.sta==2 else '-交谈' if self.sta==3 else ''
			screen.blit(self.rdd(unicode(Adr+tt,"utf8")),(5,0))

	def run(self):
		self.work()
		if not self.talking:
			return
		global timep
		self.cd=max(0,self.cd-timep)
		if self.cango and self.cd<=0 and self.goon:
			self.pt+=1
			self.zz=-1
			self.cd=300
			self.goon=0
		if self.pt>self.diag[self.now][0]:
			self.talking=0
			return
		global screen,lh,sound
		now=self.diag[self.now][self.pt]
		for i in xrange(1,4):
			if len(now[i])>1:
				if now[i][1] in ['3','4','9']:
					screen.blit(lh.lhs[now[i]],(self.px+290*(i-1),self.py-390))
				else:
					screen.blit(lh.lhs[now[i]],(self.px+290*(i-1),self.py-290))
		screen.blit(self.bd,(self.px,self.py))
		screen.blit(self.rd(now[0],0),(self.px+50,self.py+15))
		j=0
		ds=[]
		if now[6]==2:
			self.cango=0
		while j<len(now[5]):
			ds.append(self.rd(now[5][j:j+31],now[6]))
			j+=31
		for i in xrange(len(ds)):
			screen.blit(ds[i],(self.px+50,self.py+40+25*i))
		if now[4]!=0:
			if now[4]<0:
				get_item(-now[4])
			elif now[4]<1000:
				sound.play(now[4])
			else:
				flags[now[4]/1000]|=now[4]%1000
			now[4]=0


class Item():
	def __init__(self,x):
		global moji
		it=open('item/i'+str(x)+'.txt').read().split(' ')
		self.id=x
		self.img=j_img(it[0],150,130)
		self.ds=[]
		j,ku=0,13
		it[1]=unicode(it[1],'utf8')
		while j<len(it[1]):
			self.ds.append(moji.rd(it[1][j:j+ku],0))
			j+=ku
class Sysb():
	def __init__(self):
		self.pt=0
		self.showing=0
		self.n=0
		self.shoimg=p_img('pics/shogo.png',650,190)

	def run(self):
		global screen,items,story
		if self.showing:
			if self.n<=0:
				return
			screen.blit(self.shoimg,(180,150))
			screen.blit(items[self.pt].img,(238,180))
			dsp=items[self.pt].ds
			for i in xrange(len(dsp)):
				screen.blit(dsp[i],(420,200+25*i))

#********************************** rule & story ************************************
class Rule():
	def __init__(self):
		pass
	
	def run(self):
		global timep,btns,moji,screen,keyp,story
		screen.blit(story.bk,(0,0))
		moji.run()

		map(lambda x:x.run(timep,mou_pos,moup,keyp,screen),btns)
		map(lambda x:x.run(screen),txts)
		map(lambda x:x.run(timep,mou_pos,moup,keyp,screen),syss)
		sysb.run()
		pygame.display.update()

class Story():
	def __init__(self,x=1):
		self.event=x
		self.cond=0
		self.code=0
		self.b_ss=5
		self.b_ev=0
		self.now_st=0
		self.jmp=0
		self.cx,self.cy=250,85
		self.t,self.arg=0,0
		self.set(0)
		self.cod=[0]*1000
		self.last=0
		self.last_code=0
		self.kod=[{}]*4
		self.kod[1]=[0]*100
		self.kod[2]=[0]*100
		self.kod[3]=[0]*100
		kods=open('kods','r').readlines()
		j=0
		for i in kods:
			j+=1
			i=i.split(' ')
			self.kod[1][j]=int(i[0])
			self.kod[3][j]=int(i[1])
			self.kod[2][j]=int(i[2])
		cods=open('scp','r').read().split('end')
		for i in cods:
			if len(i)>2:
				i=i.split('onf')
				i[0],i[1]=filter(lambda x:len(x),i[0].split('\n')),filter(lambda x:len(x),i[1].split('\n'))
				self.cod[int(i[0][0])]=(i[0][1:],i[1])

	def set(self,x):
		self.bk=j_img('pics/bk/bk'+str(x)+'.jpg',_width,_height)
	def wtf(self,x,y):
		global moji
		moji.set(x)
		self.event=-1
		self.b_ev=y
	def cnm(self,x):
		self.now_st=x
		self.event=-2

	def trans(self,x):
		if len(x)<2:
			return
		global moji,bgm,btns,ch_wtf,cha_wtf,flags,sound,sysb
		x=x.split(' ')
		if x[0]=='set_event':
			self.event=int(x[1])
		elif x[0]=='set_diag':
			moji.set(int(x[1]))
		elif x[0]=='set_adr':
			set_adr(x[1])
		elif x[0]=='ch_talking':
			if not moji.talking:
				self.event=int(x[1])
		elif x[0]=='set_t':
			self.t=int(x[1])
		elif x[0]=='set_bgm':
			bgm.change(int(x[1]))
		elif x[0]=='set_bk':
			self.set(int(x[1]))
		elif x[0]=='set_cond':
			self.cond=int(x[1])
		elif x[0]=='set_wtf':
			if len(x)==2:
				self.wtf(int(x[1]),0)
			else:
				self.wtf(int(x[1]),int(x[2]))
		elif x[0]=='set_wof':
			self.wtf(int(x[1]),int(x[2]))
		elif x[0]=='set_wh':
			set_adr(x[1])
			self.set(int(x[2]))
			self.cond=int(x[3])
		elif x[0]=='set_go':
			j=0
			self.event=0
			for i in x[1:]:
				i=i.split('#')
				if int(i[1])>=0:
					btns.append(Button(self.cx,self.cy+65*j,500,60,2,chev,0,int(i[1])))
				else:
					btns.append(Button(self.cx,self.cy+65*j,500,60,2,ch_wtf,0,-int(i[1])))
				txts.append(Txt(i[0],_x=self.cx+200,_y=self.cy+15+65*j))
				j+=1
		elif x[0]=='get_item':
			get_item(int(x[1]))
		elif x[0]=='del_item':
			del_item(int(x[1]))
		elif x[0]=='set_loop':
			if moji.pt==int(x[1]):
				moji.pt=int(x[2])
		elif x[0]=='ch_z':
			if moji.pt==int(x[1]) and moji.zz!=-1:
				sysb.showing=0
				if moji.zz==int(x[2]):
					self.event=int(x[3])
					self.jmp=1
				else:
					moji.goon=1
				moji.zz=-1
		elif x[0]=='ch_zz':
			if moji.pt==int(x[1]) and moji.zz!=-1:
				sysb.showing=0
				if moji.zz==int(x[2]):
					moji.cango=1
					moji.pt+=1
				else:
					sound.play(0)
				moji.zz=-1
		elif x[0]=='ch_zzz':
			if moji.pt==int(x[1]) and moji.zz!=-1:
				sysb.showing=0
				if moji.zz==int(x[2]):
					moji.pt=int(x[3])
				else:
					sound.play(0)
				moji.zz=-1
		elif x[0]=='ch_flag':
			if flags[int(x[1])]&int(x[2])==int(x[2]):
				if int(x[3])>=0:
					self.event=int(x[3])
				else:
					self.wtf(-int(x[3]),0)
				self.jmp=1
		elif x[0]=='set_cha':
			if int(x[5])>0:
		 		btns.append(Button(int(x[1]),int(x[2]),int(x[3]),int(x[4]),0,ch_wtf,0,int(x[5])))
			else:
		 		btns.append(Button(int(x[1]),int(x[2]),int(x[3]),int(x[4]),0,chev,0,-int(x[5])))


	def run(self):
		global timep,moji,btns,chev,txts,bgm,sound,flags,ch_wtf
		if self.t>0:
			self.t=max(0,self.t-timep)
			return
		if self.event==-1:
			self.last=-1
			if not moji.talking:
				self.event=self.b_ev
			return
		if self.event==0:
			self.last=0
			if self.code:
				if self.code!=self.last_code:
					moji.sta=self.code
					if self.kod[self.code][self.cond]>=0:
						self.event=self.kod[self.code][self.cond]
					else:
						self.wtf(-self.kod[self.code][self.cond],0)
				self.last_code=self.code
				self.code=0
			return

		for i in self.cod[self.event][1 if self.last==self.event else 0]:
			self.last=self.event
			self.trans(i)
			if self.jmp:
				self.jmp=0
				return

#*****************************************************************************************
clock 		= 	pygame.time.Clock()
lh 			=	Lh()
sound 		=	Sound()
moji 		= 	Moji()
bgm 		=	Music()
rule 		=	Rule()
story 		=	Story()
sysb 		=	Sysb()
#********************************** main *************************************************
while True:
	keyp=pygame.key.get_pressed()
	moup=pygame.mouse.get_pressed()
	mou_pos=pygame.mouse.get_pos()
	timep = clock.tick(60)
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	rule.run()
	story.run()