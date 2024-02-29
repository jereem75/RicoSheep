from PIL import Image, ImageTk
from fltk import *
import collections
def superpos(plateau,e):
    '''
    déclare si le mouton qu'on est entrain de faire bouger 
    sort du plateau ou tombe sur un bouisson ou sur un autre
    mouton
    param:plateau:list of list
    e:tuple
    return:boolean
    >>> plateau =   [[None, 'B' , None, 'B' , None],
                    ['B' , 'B' , None, None, None],
                    [None, 'G' , 'B' , 'B' , None],
                    [None, 'B' , 'G' , None, None],
                    [None, None, None, 'B' , None]]
    >>> superpos(plateau,(0,2)))
    True
    >>> superpos(plateau,(3,2)))
    True
    >>> superpos(plateau,(4,3)))
    False
    '''
    a,b = e
    if b >= len(plateau[0])or a >= len(plateau)  or plateau[a][b] == 'B'   :
        return False
    return True

    
def charger(fichier):
    '''
    cette fonction reçoit en parametre le fichier du plateau et le renvoit sous forme de listes de liste avec
    la liste des coordonnées des moutons
    :param:fichier:fichier
    :return :plateau:list of lists
    moutons:list of tuples

    '''
    file=open(fichier,'r')
    plateau = []
    moutons = []
    i=0
    for line in file:
        line1 = line.strip()   
        j = 0
        ligne = []
        for lettre in line1: 
            if lettre == '_':
                ligne.append(None)
            elif lettre=='B':
                ligne.append('B')
            elif lettre=='G':
                ligne.append('G')
            elif lettre=='S':
                moutons.append((i,j))
                ligne.append(None)
            else:
                return None    
            j += 1
        plateau.append(ligne)
        i += 1
    file.close()
    for k in range(len(plateau)-1):
        if len(plateau[k])!=len(plateau[k+1]):
            return "Votre grille n'est pas carré ou rectangulaire"
    return plateau,moutons


def jouer(plateau,moutons,move):
    '''
    cette fonction représente moteur du jeu sa principale fonctionnalité est de mettre à jour les positions des moutons après
une instruction du joueur.
param:plateau:list of lists
mouton :list
move:chaine 
return: moutons
    >>> jouer([[None, 'B' , None, 'B' , None],
            ['B' , 'B' , None, None, None],
            [None, 'G' , 'B' , 'B' , None],
            [None, 'B' , 'G' , None, None],
            [None, None, None, 'B' , None]],[(0,4), (1,3), (2,4), (4,4)],'Right'))
    [(0, 4), (1, 4), (2, 4), (4, 4)]
    >>> jouer([[None, 'B' , None, 'B' , None],
            ['B' , 'B' , None, None, None],
            [None, 'G' , 'B' , 'B' , None],
            [None, 'B' , 'G' , None, None],
            [None, None, None, 'B' , None]],[(0,4), (1,3), (2,4), (4,4)],'Left'))
    [(0, 4), (1, 2), (2, 4), (4, 4)]
    >>> jouer([[None, 'B' , None, 'B' , None],
            ['B' , 'B' , None, None, None],
            [None, 'G' , 'B' , 'B' , None],
            [None, 'B' , 'G' , None, None],
            [None, None, None, 'B' , None]],[(0,4), (1,3), (2,4), (4,4)],'Up'))
    [(0, 4), (1, 3), (2, 4), (4, 4)]
    >>> jouer([[None, 'B' , None, 'B' , None],
            ['B' , 'B' , None, None, None],
            [None, 'G' , 'B' , 'B' , None],
            [None, 'B' , 'G' , None, None],
            [None, None, None, 'B' , None]],[(0,4), (1,3), (2,4), (4,4)],'Up'))
    [(3, 4), (1, 3), (2, 4), (4, 4)]
    '''
    lonlg = len(plateau[0])
    loncol = len(plateau)
    for e in moutons:
        i = moutons.index(e)
        a = e[0]
        b = e[1]
        if move == 'Right':
            while superpos(plateau,(e[0],b+1)) and b+1<lonlg :
                b += 1
            while (a,b) in moutons and b>e[1]:
                b -= 1
            moutons[i] = (e[0],b)
        elif move == 'Left':
            while superpos(plateau,(e[0],b-1)) and b-1>=0 :
                b -= 1
            while (a,b) in moutons and b<e[1]:
                b += 1
            moutons[i] = (e[0],b)
        elif move == 'Up':
            while superpos(plateau,(a-1,e[1]))and a-1>=0:
                a -= 1
            while (a,e[1]) in moutons and a<e[0]:
                a += 1
            moutons[i] = (a,e[1])
        elif move == 'Down':
            while superpos(plateau,(a+1,e[1])) and a+1 < loncol:
                a += 1
            while (a,e[1]) in moutons and a>e[0]:
                a -= 1
            moutons[i] = (a,e[1])
    return moutons


def appuie():
    '''
    simule l'evenement d'appuie sur un bouton du clavier
    :return : tuple
    '''
    while True:
        # print('appuis')
        ev = donne_ev()
        tev = type_ev(ev)

        # Action dépendant du type d'événement reçu :

        if tev =='Touche':
            if touche(ev) in ["Down","Up","Right","Left","r","Escape"]:
                return touche(ev)
        if tev == 'Quitte':
            break
        else:  # dans les autres cas, on ne fait rien
            pass
        
        mise_a_jour()
    ferme_fenetre()


def victoire(plateau,moutons):
    '''
    cette fonction vérifie si le joueur a gagné ou pas
    param:plateau,moutons: list
    return:boolean
    >>> victoire([[None, 'B' , None, 'B' , None],
                ['B' , 'B' , None, None, None],
                [None, 'G' , 'B' , 'B' , None],
                [None, 'B' , 'G' , None, None],
                [None, None, None, 'B' , None]],[(0,4), (1,3), (2,4), (4,4)])
    False
    >>> victoire([[None, 'B' , None, 'B' , None],
                ['B' , 'B' , None, None, None],
                [None, 'G' , 'B' , 'B' , None],
                [None, 'B' , 'G' , None, None],
                [None, None, None, 'B' , None]],[(0,4), (2,1), (3,2), (4,4)])
    True

    '''
    nb_g = 0
    for lg in plateau:
        nb_g += lg.count('G')
    s = 0
    for e in moutons:
        if plateau[e[0]][e[1]]=='G':
            s += 1
    if s == nb_g:
        return True
    return False


def deplacement (plateau,moutons,move):
    '''
    cette fonction est responsable du changement des positions des moutons graphiquement 
    et le changement des images des bouissons
    param:'sheep','herbe_mou',move:chaine
    plateau:list of lists
    moutons:list
    '''
    efface('sheep')
    if move is not None :
        moutons = jouer(plateau,moutons,move)
    efface('herbe_mou')
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if plateau[i][j] == 'G' and (i,j) in moutons :
                image(70*j+45, 70*i+45, 'media/sheep_grass.png', ancrage='center', tag='herbe_mou')
    for e in moutons:
        if plateau[e[0]][e[1]]!='G':
            img=image(70*e[1]+45, 70*e[0]+45, 'media/sheep.png', ancrage='center', tag='sheep')
    
    mise_a_jour()


def charge_jeu(plateau,moutons):
    '''
    cette fonction permet de charger la grille du jeu avec les moutons, les herbes et les bouissons
    param:plateau:list of lists
    moutons:list of tuples
    '''
    taille_fenetre =20+len(plateau[0])*70,20+len(plateau)*70
    cree_fenetre(taille_fenetre[0],taille_fenetre[1])
    ax,ay = 10,10
    bx,by = 10,len(plateau)*70+10
    cx,cy = len(plateau[0])*70+10,10
    x = 0
    y = 0
    while x <= len(plateau[0])*70:
        ligne(ax+x,ay, bx+x,by)
        x += 70
    while y <= len(plateau)*70:
        ligne(ax,ay+y,cx,cy+y)
        y+=70
    for lg in range(len(plateau)):
        for col in range(len(plateau[0])):
            if plateau[lg][col] == 'B':
                image(70*col+45, 70*lg+45, 'media/bush.PNG', ancrage='center', tag='im')
            elif plateau[lg][col] == 'G':
                image(70*col+45, 70*lg+45, 'media/grass.png', ancrage='center', tag='im')
    for e in moutons:
        image(70*e[1]+45, 70*e[0]+45, 'media/sheep.png', ancrage='center', tag='sheep')


def menu(taille_fenetre):
    '''
    cette fonction charge le menu du jeu
    :param:taille_fenetre :tuple
    return: tuple
    '''
    x = taille_fenetre[0]
    y = taille_fenetre[1]
    cree_fenetre(x,y)
    texte(x/3.6,y/25, "RICOSHEEP", couleur="green", taille=50, police='Courier')
    texte(x/2,y*4/5, "start game", couleur="green", taille=30, police='Courier',ancrage='center')
    longueur1,hauteur1 = taille_texte('start game','Courier',30)
    rectangle(x/2-longueur1//2,y*4/5-hauteur1//2,x/2+longueur1//2,y*4/5+hauteur1//2,couleur='red',epaisseur=3)
    texte(x/25,y/7, "type of the game :", couleur="black", taille=20, police='halvetica')
    texte(x*3/8,y/7, "player", couleur="black", taille=20, police='halvetica')
    texte(x*3/4,y/7, "solver", couleur="black", taille=20, police='halvetica')
    rectangle(x/2,y/7,x/2+hauteur1,y/7+hauteur1,remplissage='black')
    rectangle(x*6/7,y/7,x*6/7+hauteur1,y/7+hauteur1,remplissage='white')
    texte(x/25,y*2/7, "chose your map :", couleur="black", taille=20, police='halvetica')
    
    x=x/4
    y=y*2/7
    rectangle((x+taille_fenetre[0]/6)-50,y-50,(x+taille_fenetre[0]/6)+50,y+50,couleur='red',epaisseur=5,tag='rect')
    for cle in dict:
        x+=taille_fenetre[0]/6
        if x >= taille_fenetre[0]-70:
            x = x/12
            y += taille_fenetre[1]/7
        image(x,y,'media/'+cle, ancrage='center', tag='im') 

    
    return 'joueur','map1.txt'


def appuie_souris():
    '''
    simule l'evenement du click droit ou gauche
    :return : tuple
    '''
    while True:
        ev = donne_ev()
        tev = type_ev(ev)

        # Action dépendant du type d'événement reçu :

        if tev == "ClicDroit":
            return(abscisse(ev), ordonnee(ev))

        elif tev == "ClicGauche":
            return(abscisse(ev), ordonnee(ev))

        elif tev == 'Quitte':
            return tev

        else:  # dans les autres cas, on ne fait rien
            pass

        mise_a_jour()


def manip_menu(dict,taille_fenetre):
    '''
    cette fonction sert à manipuler tous les evenements qui se passe dans le menu du jeu reçoit un dictionnaire des images des grilles et la taille 
    de la fenetreet renvoit le type du jeu le nom du fichier de la grille et un test
    param:dict:dictionnaire
    taille_fenetre:tuple
    return :chaine,chaine,boolean
    '''
    x,y=taille_fenetre
    longueur1,hauteur1=taille_texte('start game','Courier',30)
    map = 'map1.txt'
    type ='joueur'
    xev,yev = 0,0
    while x/2-longueur1//2>xev or xev>x/2+longueur1//2 or y*4/5-hauteur1//2 >yev or yev>y*4/5+hauteur1//2:
        move = appuie_souris()
        if move == 'Quitte':
            return None,None,False
        else :
            xev,yev =move
            if x*6/7<= xev<=x*6/7+50 and y/7 <= yev<= y/7+50 :
                rectangle(x/2,y/7,x/2+hauteur1,y/7+hauteur1,remplissage='white')
                rectangle(x*6/7,y/7,x*6/7+hauteur1,y/7+hauteur1,remplissage='black')
                type = 'solveur'
            elif x/2<= xev<=x/2+50 and y/7 <= yev<= y/7+50 :
                rectangle(x/2,y/7,x/2+hauteur1,y/7+hauteur1,remplissage='black')
                rectangle(x*6/7,y/7,x*6/7+hauteur1,y/7+hauteur1,remplissage='white')
                type = 'joueur'
            elif x/12-60<= xev<=taille_fenetre[0] and y*2/7-50<= yev<= y*4/5+hauteur1//2-20:
                x = x/4
                y = y*2/7
                for cle in dict:
                    x += taille_fenetre[0]/6
                    if x>= taille_fenetre[0]-70:
                        x = x/12
                        y += taille_fenetre[1]/7
                    img = Image.open( 'media/'+cle )
                    tkimage =  ImageTk.PhotoImage(img)
                    h = tkimage.height()
                    w = tkimage.width()
                    if x-(w//2) <=xev<= x+(w//2) and y-(h//2) <= yev <= y+(h//2) :
                        efface('rect')
                        rectangle(x-(w//2),y-(h//2),x+(w//2),y+(h//2),couleur='red',epaisseur=2,tag='rect')
                        map = 'maps/'+dict[cle]
            x,y = taille_fenetre
    return type,map,True
def solveur(plateau,moutons0,visite=set(),moutons_set=set()):
    
    if victoire(plateau,moutons0)==True:
        deque = collections.deque()
        return deque
    elif moutons_set in visite :
        return None
    else:
        moutons_set = set()
        for x in range(len(moutons0)):
            moutons_set.add(moutons0[x])
        moutons_set = frozenset(moutons_set)
        visite.add(moutons_set)
        moutons_var = moutons0.copy()
        for coup in ['Left', 'Right', 'Up', 'Down']:
            pos_moutons = jouer(plateau,moutons0,coup)
            l = solveur(plateau,pos_moutons,visite,frozenset(pos_moutons))
            if l is not None:
                l.appendleft(coup)
                return l
            moutons0 = moutons_var.copy()


if __name__ == "__main__":
    taille_fenetre = 800 , 800
    dict = {'map1.png':'map1.txt','map2.png':'map2.txt','map3.png':'map3.txt','big1.png':'big1.txt',
    'big2.png':'big2.txt','big3.png':'big3.txt','huge.png':'huge.txt','one_sheep.png':'one_sheep.txt',
    'one_sheep2.png':'one_sheep2.txt','onegrass.png':'onegrass.txt','wide1.png':'wide1.txt','wide2.png':'wide2.txt',
    'wide3.png':'wide3.txt','wide4.png':'wide4.txt','losable.png':'losable.txt','test_move.png':'test_move.txt'}
    menu(taille_fenetre)
    type,fichier,test = manip_menu(dict,taille_fenetre)
    ferme_fenetre()
    detect_perte = 0
    if test == True:
        plateau,moutons = charger(fichier) 
        charge_jeu(plateau,moutons)
        while not(victoire(plateau,moutons)) and type =='joueur':
            # print(lst_moutons)
            move=appuie()
            if move in ["Down","Up","Right","Left"]:
                deplacement(plateau,moutons,move)
                # print(moutons)
                moutons0 = moutons.copy()
                detect_perte = solveur(plateau,moutons0,visite=set(),moutons_set=set())
                if detect_perte == None:
                    break
                # print(moutons0)
                mise_a_jour() 
            elif move =='r':
                efface('sheep')
                plateau,moutons = charger(fichier)
                deplacement(plateau,moutons,None)
                
            elif move =='Escape':
                ferme_fenetre()
                menu(taille_fenetre)
                type,fichier,test = manip_menu(dict,taille_fenetre)
                if test == True:
                    ferme_fenetre()
                    plateau,moutons = charger(fichier) 
                    charge_jeu(plateau,moutons)
            else:
                break
        if type=='solveur':
            solution = solveur(plateau,moutons,visite=set(),moutons_set=set())
            print(solution)
            for coup in solution:
                eve = appuie_souris()
                deplacement(plateau,moutons,coup)
                print(moutons)
                
                if eve =='Quitte' :
                    ferme_fenetre()
                    break
        if victoire(plateau,moutons):
            image(40+len(plateau[0])//2*70,len(plateau)*(4/9)*70, 'media/shaun.png', ancrage='center', tag='im')
            attend_ev()
            donne_ev()
            print('félicitation vous avez réussi')
        elif detect_perte ==None :
            image(40+len(plateau[0])//2*70,len(plateau)*(4/9)*70, 'media/sad.png', ancrage='center', tag='im')
            attend_ev()
            donne_ev()
            print('vous avez perdu')