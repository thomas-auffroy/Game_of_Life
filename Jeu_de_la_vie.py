from tkinter import *
from random import *

nb_case = 100
height = 700
width = 1400
ratio = round(width/height)

compte_voisin = {}
vivant_empreinte = {}
memoire_trace = {}
memoire_forme_init = {}
		
def position_gauche(event):
	Clique_gauche = [event.x,event.y]	
	vivant(Clique_gauche)

def position_droite(event):
	Clique_droit = [event.x,event.y]
	mort(Clique_droit)
	
def vivant(Clique_gauche):
	y = int(Clique_gauche[1]/(height/nb_case))
	x = int(Clique_gauche[0]/(width/(nb_case*ratio)))
	
	if not (y,x,'vivant') in vivant_empreinte:
		memoire_forme_init[y,x] = False
		creation_vie(y,x)
		
def mort(Clique_droit):
	y = int(Clique_droit[1]/(height/nb_case))
	x = int(Clique_droit[0]/(width/(nb_case*ratio)))
	
	if (y,x,'vivant') in vivant_empreinte:
		del memoire_forme_init[y,x]
		creation_mort(y,x)
		
def creation_vie(i,j):
	for x in range(-1,2):
		for y in range(-1,2):
		
			if ((x == 0) and (y == 0)):
				if (i,j,'empreinte') in vivant_empreinte:
					plateau.delete(vivant_empreinte[i,j,'empreinte'])
					del vivant_empreinte[i,j,'empreinte']
					del memoire_trace[i,j]
			elif not (((i+x,j+y,'vivant') in vivant_empreinte) or ((i+x,j+y,'empreinte') in vivant_empreinte)):
				ecriture_empreinte(i+x,j+y)
				
	ecriture_vie(i,j)
	
def creation_mort(i,j):
	plateau.delete(vivant_empreinte[i,j,'vivant'])
	del vivant_empreinte[i,j,'vivant']
	ecriture_empreinte(i,j)
	
def ecriture_empreinte(i,j):
	memoire_trace[i,j] = False
	if (display.get()) and not((i,j) in memoire_forme_init):
		vivant_empreinte[i,j,'empreinte'] = plateau.create_rectangle(j*width/(nb_case*ratio)+3,i*height/nb_case+3,(j+1)*width/(nb_case*ratio)+3,(i+1)*height/nb_case+3,fill='white',outline='black')
	else:
		vivant_empreinte[i,j,'empreinte'] = False
		
def ecriture_vie(i,j):
	vivant_empreinte[i,j,'vivant'] = plateau.create_rectangle(j*width/(nb_case*ratio)+3,i*height/nb_case+3,(j+1)*width/(nb_case*ratio)+3,(i+1)*height/nb_case+3,fill='red',outline='black')
	
def afficher_trace():
	if display.get():
		for coord in memoire_trace.keys():
			vivant_empreinte[coord[0],coord[1],'empreinte'] = plateau.create_rectangle(coord[1]*width/(nb_case*ratio)+3,coord[0]*height/nb_case+3,(coord[1]+1)*width/(nb_case*ratio)+3,(coord[0]+1)*height/nb_case+3,fill='white',outline='black')
		for coord in memoire_forme_init.keys():
			plateau.delete(memoire_forme_init[coord])
			memoire_forme_init[coord] =  plateau.create_rectangle(coord[1]*width/(nb_case*ratio)+3,coord[0]*height/nb_case+3,(coord[1]+1)*width/(nb_case*ratio)+3,(coord[0]+1)*height/nb_case+3,fill='green',outline='black')	

	else:
		for coord in memoire_forme_init.keys():
			plateau.delete(memoire_forme_init[coord])
		for coord in memoire_trace.keys():
			plateau.delete(vivant_empreinte[coord[0],coord[1],'empreinte'])
			
def calcul_voisin():
	for coord in vivant_empreinte.keys():
		compte_voisin[coord[0],coord[1]] = 0
		
		for x in range (-1,2):
			for y in range (-1,2):
				
				if (((coord[0]+x,coord[1]+y,'vivant') in vivant_empreinte) and not ((x == 0) and (y == 0))):
					compte_voisin[coord[0],coord[1]] += 1
					
def calcul_etat():						
	for coord in compte_voisin.keys():
		
		if ((compte_voisin[coord] == 3) and ((coord[0],coord[1],'empreinte') in vivant_empreinte)):
			creation_vie(coord[0],coord[1])
			
		elif ((compte_voisin[coord] != 3) and (compte_voisin[coord] != 2) and ((coord[0],coord[1],'vivant') in vivant_empreinte)):
			creation_mort(coord[0],coord[1])
			
def cleaner():
	calcul_voisin()
	for coord in compte_voisin.keys():
		if ((compte_voisin[coord] == 0) and ((coord[0],coord[1],'empreinte') in vivant_empreinte)):
			plateau.delete(vivant_empreinte[coord[0],coord[1],'empreinte'])
			del vivant_empreinte[coord[0],coord[1],'empreinte']
			
def quitter():
	fenetre.destroy()
	
def bottomframe():
	bottomframe = Frame(fenetre)

	bouton_GO = Button(bottomframe,text='Lancer',command=fenetre.quit,height=3)
	bouton_GO.pack(side=LEFT,padx=2)
		
	bouton_TRACE = Checkbutton(bottomframe,text='Afficher Trace',command=afficher_trace,height=3,variable=display)
	bouton_TRACE.pack(side=LEFT,padx=50)
	
	frame_MIDDLE = Frame(bottomframe)
	label_STEP = Label(frame_MIDDLE,textvariable=step,height=3,width=5)		
	label_STEP.pack(side=LEFT)
	frame_MIDDLE.pack(side=LEFT,padx=width/3)

	bouton_FIN = Button(bottomframe,text='Quitter',command=fenetre.destroy,height=3)
	bouton_FIN.pack(side=RIGHT,padx=2)
	
	bottomframe.pack(fill=BOTH)	
		
fenetre = Tk()
fenetre.title("LE JEU DE LA VIE")

step = IntVar()
display = IntVar()

topframe = Frame(fenetre)
plateau = Canvas(topframe,bg='black',width=width,height=height,bd=2)
	
plateau.event_add('<<vie>>',"<Button-1>","<B1-Motion>")
plateau.bind('<<vie>>',position_gauche)
plateau.event_add('<<mort>>',"<Button-3>","<B3-Motion>")
plateau.bind('<<mort>>',position_droite)
fenetre.bind("<KeyPress-Return>", lambda lancer: fenetre.quit())

plateau.pack()
topframe.pack()		
bottomframe()

fenetre.mainloop()

plateau.unbind('<<vie>>')
plateau.bind('<<mort>>')

while True:	
	calcul_voisin()
	calcul_etat()
	if not display.get():
		cleaner()	
	step.set(step.get()+1)
	fenetre.update_idletasks()
	fenetre.update()
