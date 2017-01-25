# -*- encoding: utf-8 -*-
'''
#importo el modulo de systema
import sys
import maya.cmds as mc
#pregunto si ya existe la ruta en memoria y si no existe la agrego, asi puede buscar mi archivo
if not 'G:/Dropbox/scripts/E_TOOLS' in sys.path:
	sys.path.append('G:/Dropbox/scripts/E_TOOLS')

#aqui coloco el nombre de mi archivo a importar
import E_TOOLS
#recargo mi archivo si esta en memoria
reload(E_TOOLS)
#asi se usan las funciones que creo en mi archivo
E_TOOLS.emanTools()
#elimino la ruta para volver a evaluarla despues
#sys.path.remove('F:/Emma/Dropbox/scripts/E_TOOLS')
'''
#-----------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------
import sys
import maya.cmds as mc
import random as rm
import os
from functools import partial
#-----------------------------------------------------------------------------------------------
# END Imports
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Global Variables and definitions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# END Global Varables and definitions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Main functions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# END Main functions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Utility functions
#-----------------------------------------------------------------------------------------------
#Generated comment lines in console
def printFuncion(input='something'):

	r = len(input)
	asterix=''

	for index in range(r):

		asterix=asterix+'#'

	print asterix
	print (input).upper()
	print asterix
#Generated comment lines in windons
def printFuncionWin(input='something'):

	if mc.window('errorWin',ex=True):
		mc.deleteUI('errorWin')

	# Make a new window
	mc.window('errorWin', title=" FAIL ", s=False, iconName='Short Name', widthHeight=(200, 100), bgc=(0.1,0.5,0.8))
	mc.columnLayout()
	mc.text(label='')
	mc.text(label=(input).upper())
	mc.text(label='')
	mc.button('  OK  ', command = 'mc.deleteUI("errorWin")',al=True)
	mc.showWindow('errorWin')
#-----------------------------------------------------------------------------------------------
# END Utility functions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# UI functions
#-----------------------------------------------------------------------------------------------
#Window NameToRename
def windowRename(arg):

	nWin='NameToRename'
	nota='Name and Suffix'
	nota2='Rename'
	if mc.window( nWin,ex=True ):
		mc.deleteUI(nWin)
	mc.window( nWin, title=nota,s=False, width= 300, height=100, bgc=(0.25,0.27,0.29) )
	mc.columnLayout( adjustableColumn=True )
	mc.textFieldGrp( nWin + 'FieldsN' , label='Name Objects:', ann='Here you put the name of the object' )
	mc.textFieldGrp( nWin + 'FieldS', label='Suffix Objets:',ann='Here you put the name of the suffix' )
	mc.columnLayout( adjustableColumn=True )
	mc.button ( nWin + 'btn', label=nota2, command=rename, annotation=nota2,w=50, h=50 )
	mc.showWindow( nWin )

def rename(arg):

	if len( mc.ls(sl=True) )== 0 :
		printFuncionWin( 'Select something' )
		return

	nameObject = str( mc.textFieldGrp('NameToRenameFieldsN', q = True, text=True ))
	suffixObjects = str( mc.textFieldGrp('NameToRenameFieldS', q = True, text=True) )
	if nameObject != '' and suffixObjects != '':
		funcionRename(nameObject, suffixObjects.upper())
	else:
		printFuncionWin('You need write something.')

	printFuncion('new names of the objects are:')

	print 'The Object is: ' + nameObject
	print 'The Suffix is: ' + suffixObjects
#----------------------------------------------------------------------------------------------
#Window deleteNodes
def deletingNodeType(arg):

	dWin='deletingNodeType_'

	if mc.window(dWin,ex=True):
		mc.deleteUI(dWin)

	mc.window(dWin+'ntr', title='Type Node',s=1, widthHeight=(60, 60), bgc=(0.25,0.27,0.29))
	mc.columnLayout(adjustableColumn=True)
	mc.textFieldGrp('deletingNodeType_FieldsN', label='Nodo:', ann='Here you put the name node to delete')
	mc.columnLayout(adjustableColumn=True)
	mc.button (dWin+'btn', label='DELETES NODES', command=getNameNode, annotation='Delete the Node',w=20, h=50)
	mc.showWindow(dWin+'ntr')
#----------------------------------------------------------------------------------------------
#Funcion para renombrar y colocar sufijo
def funcionRename(nameObj, sufijoObj):
	lista=mc.ls(sl=True, r=True)
	contador=00

	for obj in lista:
		try:
			mc.rename(obj, nameObj+str(contador)+'_'+sufijoObj)
			contador+=01
		except:
			printFuncionWin('I can not rename the object')
#----------------------------------------------------------------------------------------------
def getNameNode(arg):

	nameNode = mc.textFieldGrp('deletingNodeType_FieldsN', q = True, text=True)

	deletingNodeTypeSet(nameNode)
#----------------------------------------------------------------------------------------------
#Put the material texture and alpha
def fixAlphaEyeSlash():

	if not mc.objExists('pestanas__MAT'):
		mc.file('C:/Users/pdeleo/Desktop/pdeleo/EMAN_TOOLS/TOOL_CTRLS/pestanas.ma', i=True)

	else:
		printFuncion('and the material was created earlier')

	try:
		mc.connectAttr('pestanas_MAT.outColor', 'pestanas_MATSG.surfaceShader', f=True)

	except: 0
#----------------------------------------------------------------------------------------------
#Visibilida de los atributos y lock
def OnOffAttr(chBoxv=True,lock=True,keyable=True,trf=False,rot=False,scal=False,v=False):
	sel=mc.ls(sl=1)
	for o in sel:
		if trf:
			mc.setAttr(o+'.tx',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.ty',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.tz',lock=lock,channelBox=chBoxv,keyable=keyable )
		if rot:
			mc.setAttr(o+'.rx',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.ry',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.rz',lock=lock,channelBox=chBoxv,keyable=keyable )
		if scal:
			mc.setAttr(o+'.sx',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.sy',lock=lock,channelBox=chBoxv,keyable=keyable )
			mc.setAttr(o+'.sz',lock=lock,channelBox=chBoxv,keyable=keyable )
		if v:
			mc.setAttr(o+'.v',lock=lock,channelBox=chBoxv,keyable=keyable )
#----------------------------------------------------------------------------------------------
#Change color randomly
def publicAttrCntr():
	cnts=mc.ls('*__CNT',type='transform')
	attr=['tx','ty','tz','rx','ry','rz','v']
	mc.select(cnts)
	for cnt in cnts:
	    currentContainer=mc.container( q=1,findContainer=cnt)
	    for at in attr:
	        attrConect=''
	        if '|' in cnt:
	            name=cnt.split('|')[-1]
            else:
                name=cnt
	        attrConect=mc.container(currentContainer,edit=True,publishName=str(name)+at)
	        mc.container(currentContainer,edit=True,bindAttr=[str(cnt)+'.'+at, attrConect])
	        mc.container(currentContainer,edit=True,publishAsChild=[str(cnt), attrConect])
#----------------------------------------------------------------------------------------------
#Change color randomly
def openCloseContainer():
    cntr=str(mc.ls(sl=1)[0])
    if cntr:
        cntr=mc.container( q=1,findContainer=cntr)
        if mc.getAttr(cntr+'.blackBox')==False:
            mc.setAttr(cntr+'.blackBox',1)
        else:
            mc.setAttr(cntr+'.blackBox',0)
    else:
        print 'Selecciona algo'
#----------------------------------------------------------------------------------------------
#Change color randomly
def changeColor():

	if len(mc.ls(sl=True))== 0 :
		printFuncionWin('  Select something  ')
		return

	numcolor = rm.randrange(1, 21, 1)

	sel=mc.ls(sl=True)

	for o in sel:
		mc.setAttr (o+'.overrideEnabled', True)
		mc.setAttr (o+'.overrideColor', numcolor)
	printFuncion('changed')
#----------------------------------------------------------------------------------------------
#Cambios de colorer a rojo
def ColorRed(arg):

	if len(mc.ls(sl=True))== 0 :
			printFuncionWin('Select something')
			return

	sel=mc.ls(sl=1)

	for o in sel:
		mc.setAttr (o+'.overrideEnabled', True)
		mc.setAttr (o+'.overrideColor', 13)
		printFuncion('cambio el color rojo')
#----------------------------------------------------------------------------------------------
#Cambios de colorer a amarillo
def ColorYellow(arg):

	if len(mc.ls(sl=True))== 0 :
			printFuncionWin('Select something')
			return

	sel=mc.ls(sl=1)

	for o in sel:
		mc.setAttr (o+'.overrideEnabled', True)
		mc.setAttr (o+'.overrideColor', 22)
		printFuncion('cambio el color amarillo')
#----------------------------------------------------------------------------------------------
#Cambios de colorer a verde
def ColorGreen(arg):

	if len(mc.ls(sl=True))== 0 :
			printFuncionWin('Select something')
			return

	sel=mc.ls(sl=1)

	for o in sel:
		mc.setAttr (o+'.overrideEnabled', True)
		mc.setAttr (o+'.overrideColor', 14)
		printFuncion('cambio el color verde')
#----------------------------------------------------------------------------------------------
#Pasa de L a R o de R a L.
def CambiaLado(arg):

	if len(mc.ls(sl=True)) == 0 :
			printFuncionWin('Select something')
			return

	sel= mc.ls(sl=True)


	for obj in sel:
		# Variables
		lado = obj[0]
		nombre = obj[1:]
		# Averiguar el lado
		if lado[0] == 'L':
			lado = 'R'
			mc.rename (obj, lado+nombre)
			return printFuncion('Switch letter L in') + lado

		if lado[0] == 'R':
			lado = 'L'
			mc.rename (obj, lado+nombre)
			return printFuncion('Switch letter R in') + lado
'''
sel= mc.ls(sl=True)

for obj in sel:
	if obj[0] == 'L': mc.rename(obj, 'R_'+obj.split('L_')[1])
	else: mc.rename(obj, 'L_'+obj.split('R_')[1])

'''
#----------------------------------------------------------------------------------------------
#Borra todos los tipos de nodos que quieras pasandolo por parametro.
def deletingNodeTypeSet(input=''):

	#listo todo los tipos de nodos que necesito
	nodoLista = mc.ls (typ=input)
	try:
		#Pregunto a que esta conectado
		for Nodo in nodoLista:
			fuente = mc.listConnections (Nodo, s=1, d=1)
			mc.delete(Nodo)
			print 'Se borro el nodo<',Nodo,'>del objeto<',fuente[4],'>'
	except:
		print 'Cant delete '+ str(Nodo)
#-----------------------------------------------------------------------------------------------
#Mirror de partes dependiendo de la nomenclatura L o R
def mirrorPieces(arg):

    L=mc.radioButton(buttomL, q=1,select=True)
    R=mc.radioButton(buttomR, q=1,select=True)
    C=mc.radioButton(buttomC, q=1,select=True)
    if L:
        side='L'
    elif R:
        side='R'
    elif C:
        side='C'
    sel = mc.ls(sl=True)
    for o in sel:# Mirror the piece
        if mc.nodeType(mc.listRelatives(o)[0])=='mesh':
            if mc.objExists(o+'_mirror')==False:
                mirroredGeo = ''
                attrs=mc.listAttr (o, keyable=1)
                for attr in attrs:
                    mc.setAttr (o+"."+attr, lock=0)
                mc.xform(o, ws=True, piv=(0, 0,0))
                mc.makeIdentity (o,translate=1,rotate=1,scale=True, apply=True)
                mirroredGeo = mc.duplicate(o,n=o+'_mirror')[0]
                mc.setAttr (mirroredGeo +'.scaleX',-1)
                mc.makeIdentity (mirroredGeo,translate=1,rotate=1,scale=True, apply=True)
                mc.polyNormal (mirroredGeo, normalMode=0, userNormalMode=0)
                if 'L_' in mirroredGeo:
                    mc.rename(mirroredGeo, o.replace('L_','R_'))
                elif 'R_' in mirroredGeo:
                    mc.rename(mirroredGeo, o.replace('R_','L_'))
                elif 'Left' in mirroredGeo:
                    mc.rename(mirroredGeo, o.replace('Left','Right'))
                elif 'Right' in mirroredGeo:
                    mc.rename(mirroredGeo, o.replace('Right','Left'))
                elif 'Mid' or 'C_' or 'mid' in mirroredGeo or None == mirroredGeo:
                    mc.polyUnite(o, mirroredGeo, name=str(o), constructionHistory=1, mergeUVSets=1,caching=True)
                    mc.delete(mirroredGeo,ch = True)
                    mc.rename(mirroredGeo,str(o))
                    mc.polyMergeVertex (mirroredGeo,d= 0.379)
            else:
                print 'Ya existe el mirror.'
        else:
            print 'No es una geometria'
#-----------------------------------------------------------------------------------------------
#MIRROR DE TRFS
def mirrorTRF(arg):

	sel = mc.ls(sl=True)
	for o in sel:# Mirror the piece
	    if mc.objExists(o+'_mirror')==False:
	        child=[]
	        currentTRF=mc.xform(o, query=True,translation=True)
	        currentROT=mc.xform(o, query=True,rotation=True)
	        currentSCA=mc.getAttr(o+'.scaleX')
	        mirroredGeo = ''
	        mirroredGeo = mc.duplicate(o,n=o+'_mirror',renameChildren=True)[0]
	        mc.setAttr (mirroredGeo +'.scaleX',currentSCA*-1)
	        mc.setAttr (mirroredGeo +'.translateX',currentTRF[0]*-1)
	        mc.setAttr (mirroredGeo +'.translateZ',currentTRF[2]*-1)
	        mc.setAttr (mirroredGeo +'.rotateY',currentROT[1]*-1)
	        mc.setAttr (mirroredGeo +'.rotateZ',currentROT[2]*-1)
	        mc.makeIdentity (mirroredGeo,scale=True, apply=True)
	        child=mc.listRelatives(mirroredGeo,allDescendents=True,type='transform')
	        if 'L_' in mirroredGeo:
	            if child:
	                for chd in child:
	                    mc.rename(chd, chd.replace('L_','R_'))
	            mc.rename(mirroredGeo, o.replace('L_','R_'))
	        elif 'R_' in mirroredGeo:
	            if child:
	                for chd in child:
	                     mc.rename(chd, chd.replace('R_','L_'))
	            mc.rename(mirroredGeo, o.replace('R_','L_'))
	        elif 'Left' in mirroredGeo:
	            if child:
	                for chd in child:
	                    mc.rename(chd, chd.replace('Left','Right'))
	            mc.rename(mirroredGeo, o.replace('Left','Right'))
	        elif 'Right' in mirroredGeo:
	            if child:
	                for chd in child:
	                    mc.rename(chd, chd.replace('Right','Left'))
	            mc.rename(mirroredGeo, o.replace('Right','Left'))
	    else:
	        print 'Ya existe el mirror.'
#-----------------------------------------------------------------------------------------------
#Copia el nombre de la primera seleccion a la segunda seleccion con un nuevo tag
def copyName(arg):
    try:
        name = mc.ls( sl=1 )
        if len(name) == 2:
            sourceName = name[0]
            targetName = name[1]
            onlyName = sourceName.split( '_jnt' )[0]
            newName = mc.rename( targetName , onlyName + '_SLC' )
            print 'Source Name: ' + sourceName
            print 'Target Name: ' + targetName
            print 'New Name: ' + str(newName)

        else:
        	print 'Seleccionar source y luego target para copiar su nombre nuevo'
    except:
        pass
#-----------------------------------------------------------------------------------------------
#Coloca el el shape o control dentro del transform. Selecciona primero el objeto y luego el shape.
def cntToShape(arg):

	obj = mc.ls( sl=1 )
	shapes=mc.listRelatives(obj,s=1)

	for sh in shapes:
		mc.parent( sh, obj[1], s=True, r=True )


#-----------------------------------------------------------------------------------------------
#Coloca un transform y lo emparenta donde esta a un shape
def zeroTransform(node,sufix='__ZTR'):

	if len(mc.ls(sl=True)) == 2:


		#get the parent of the node
		parentNode=mc.listRelatives(node,p=1)
		zeroTransform=mc.createNode('transform',n=node.split('__')[0]+sufix)
		mc.parent(zeroTransform,node)
		mc.xform(zeroTransform,t=[0,0,0],ro=[0,0,0],s=[1,1,1],sh=[0,0,0])
		mc.parent(zeroTransform,parentNode) if mc.listRelatives(node,p=1)!=None else mc.parent(zeroTransform,w=1)
		mc.parent(node,zeroTransform)

		#check if the node is in a container and add if so, the zero to it
		container=mc.container(q=1,fc=node)
		if container:
			mc.container(container,e=1,an=zeroTransform)


		return zeroTransform

		for obj in mc.ls(sl=1):
			zeroTransform(obj)

	else:
		print 'Porfavor selecciona primero un mesh y luego una curva para usar de control'
#-----------------------------------------------------------------------------------------------
#Crea un parent constrian entre los husos y el rig con los SLC para proxy de personaje.
#Los huesos tienen que tener el mismo nombre que el SLC sino no lo creara.
def parentSLCtoJoint(arg):
    global onOff
    SLCS=[]
    SLCS=mc.ls('*:*_SLC',type='transform')
    if SLCS:
        for slc in SLCS:
            #switch (False,slc)
            jointName=slc.split('_SLC')[0]
            if mc.objExists(jointName) and mc.nodeType(jointName)=='joint':
				if not mc.objExists(str(jointName)+'__PCNS'):
					mc.parentConstraint(jointName,slc,name=str(jointName)+'__PCNS',maintainOffset=True)
				if not mc.objExists(str(jointName)+'__SCNS'):
					mc.scaleConstraint(jointName,slc,name=str(jointName)+'__SCNS',maintainOffset=True)
            #switch (True,slc)
    else:
		mc.warning('La escena tiene que contener SLC para poder ejecutarce')
#-----------------------------------------------------------------------------------------------
#crea un circle y lo emparenta a un transform y lo borra luego.
def createCIRCLEinTRF(arg):
    sel=mc.ls(sl=1)
    for o in sel:
        cnt=mc.circle(name=o.split('__')[0]+'__CNT', r=1,object=1)[0]
        hcns=mc.parentConstraint(o,cnt)
        mc.delete(hcns)
#-----------------------------------------------------------------------------------------------
#Genera un control midiendo el joint padre al hijo. solo hay que colocar el caracter correspondiente al axi principal. x,y,z .....
def cntjoint( axis='x' ):

	radius = 1.0
	dirX=dirY=dirZ=centerX=centerY=centerZ = 0
	if axis == "x":
		dirZ = 1
	if axis == "y":
		dirZ = 1
	if axis == "z":
		dirX = 1

	sel= mc.ls( sl=1 )

	if len(sel) == 0 and mc.nodeType(sel[0]) != 'joint':
		print 'Select a joint before creating the control'

	rel = mc.listRelatives( sel[0], c=1, type='joint' )

	if rel:
		radius = mc.getAttr ((str(rel[0]) + '.t' + axis)) / 2.0

	if axis == 'x':
		centerX = radius
	if axis == 'y':
		centerY = radius
	if axis == 'z':
		centerZ = radius

	cnt = mc.circle( n=sel[0].split('__')[0]+'__CNT', c=[centerX, centerY, centerZ], nr=[dirX, dirY, dirZ], r=radius )

	rel = mc.listRelatives( cnt[0], c=1, s=1 )
	mc.parent( rel[0], sel[0], s=1, r=1 )
	mc.delete( cnt[0] )

#-----------------------------------------------------------------------------------------------
def createClusterInVertex(arg):#Crea un cluster con la seleccion de VERTICES
	sel=mc.ls(sl=1)[0]
	vtxs= mc.filterExpand(sm=28)
	for v in vtxs:
	    n,nV= v.split('.cv[')
	    cls=mc.cluster(v)
	    s=mc.select(sel)
	    if '__' in n:
	        mc.rename(cls[1],str(n).split('__')[0]+str(nV[:-1])+'_CLS')
	    else:
	        mc.rename(cls[1],str(n)+str(nV[:-1])+'_CLS')
#-----------------------------------------------------------------------------------------------
def createJointInVertex(arg):#Crea un JOINT con la seleccion de VERTICES
	objs = mc.ls(sl=1)
	sel=[]
	if '.vtx[' in objs[0]:
	    for v in objs:
	        pos=mc.pointPosition(v)
	        mc.select(cl=1)
	        jnt=mc.joint(name=str(o)+'_JNT',p=pos)
	        sel.append(jnt)
	else:
	    for o in objs:
	        mc.select(cl=1)
	        jnt=mc.joint(name=str(o)+'_JNT',rad=0.5)
	        mc.select(cl=1)
	        mc.delete( mc.parentConstraint( o, jnt ) )
	        sel.append(jnt)
	mc.select(sel)

#-----------------------------------------------------------------------------------------------
#Crea una serie de condiciones para lograr un driven key programable.
def setDrivenKeyCondition(source='',target='',axiX='x',axiY='y',axiZ='z'):
    if mc.nodeType(source)=='joint' and mc.nodeType(target)=='transform':
    #X
        #CREO Y SETEO NODO X
        xMDNDIV=mc.createNode('multiplyDivide',shared=True,n=str(source)+'_X'+'DIV'+'__MDN')
        xCND=mc.createNode('condition',shared=True,n=str(source)+'_X'+'__CND')
        mc.setAttr(xMDNDIV+'.operation', 2)
        mc.setAttr(xMDNDIV+'.input2X', 8)
        mc.setAttr(xCND+'.operation', 2)
        #Conectando SOURCE to MDN
        mc.connectAttr(source+'.rx',xMDNDIV+'.input1X')
        #conectando SOURCE to CND
        mc.connectAttr(source+'.rx',xCND+'.colorIfTrueR')
        mc.connectAttr(source+'.rx',xCND+'.firstTerm')
        #coenctando MDN to CND
        mc.connectAttr(xMDNDIV+'.outputX',xCND+'.colorIfFalseR')
        #conectadno CND to TARGET
        mc.connectAttr(xCND+'.outColorR',target+'.r'+axiX)
    #Y
        #CREO Y SETEO NODO Y
        yMDNMULT=mc.createNode('multiplyDivide',shared=True,n=str(source)+'_Y'+'MULT'+'__MDN')
        yMDNDIV=mc.createNode('multiplyDivide',shared=True,n=str(source)+'_Y'+'DIV'+'__MDN')
        yCND=mc.createNode('condition',shared=True,n=str(source)+'_Y'+'__CND')
        mc.setAttr(yMDNMULT+'.operation', 1)
        mc.setAttr(yMDNMULT+'.input2Y', -1)
        mc.setAttr(yMDNDIV+'.operation', 2)
        mc.setAttr(yMDNDIV+'.input2Y', 1.01)
        mc.setAttr(yCND+'.operation', 1)
        #Conectando SOURCE to MDN
        mc.connectAttr(source+'.ry',yMDNMULT+'.input1Y')
        mc.connectAttr(source+'.ry',yMDNDIV+'.input1Y')
        #conectando SOURCE to CND
        mc.connectAttr(source+'.ry',yCND+'.firstTerm')
        #coenctando MDN to CND
        mc.connectAttr(yMDNMULT+'.outputY',yCND+'.colorIfFalseG')
        mc.connectAttr(yMDNDIV+'.outputY',yCND+'.colorIfTrueG')
        #conectadno CND to TARGET
        mc.connectAttr(yCND+'.outColorG',target+'.r'+axiY)
    #Z
        #CREO Y SETEO NODO Z
        zCND=mc.createNode('condition',shared=True,n=str(source)+'_Z'+'__CND')
        mc.setAttr(zCND+'.operation', 2)
        mc.setAttr(zCND+'.colorIfFalseB', 0)
        #conectando SOURCE to CND
        mc.connectAttr(source+'.rz',zCND+'.firstTerm')
        mc.connectAttr(source+'.rz',zCND+'.colorIfTrueB')
        #conectadno CND to TARGET
        mc.connectAttr(zCND+'.outColorB',target+'.r'+axiZ)

    else:
        print 'Tienes que seleccionar primero el joint y luego el transform.'

#-----------------------------------------------------------------------------------------------
#Crea seleccionando el padre y los hijos o el hijo, hace un ZTR entre ellos.
def intermedioZTR(jnts,padre):
    for jnt in jnts:
        #get the parent of the node
        zeroTransform=mc.createNode('transform',n=jnt.split('__')[0]+'__ZTR')
        mc.xform(zeroTransform,t=[0,0,0],ro=[0,0,0],s=[1,1,1],sh=[0,0,0])
        toDelete=mc.parent(zeroTransform,jnt,relative=True)
        mc.parent(zeroTransform,padre)
        mc.parent(jnt,zeroTransform)
        mc.makeIdentity(jnt,apply=True, t=1, r=1, s=1, n=0,jointOrient=1)

def intermedioZTREject(arg):
	#Uso
	padre = mc.ls(sl=1)[0]
	jnts= mc.ls(sl=1)[1:]
	intermedioZTR(jnts,padre)
#-----------------------------------------------------------------------------------------------
#Prende y apaga los atributos menos el de visibilidad
onOff=True
def switch(arg):
    sel=mc.ls(sl=1)
    global onOff
    LockHide = False
    if LockHide == False:

        if onOff==True:
            for o in sel:
                mc.setAttr(o+'.tx',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.ty',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.tz',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.rx',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.ry',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.rz',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.sx',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.sy',lock=False,channelBox=False,keyable=True )
                mc.setAttr(o+'.sz',lock=False,channelBox=False,keyable=True )

            print 'Unlock en todo.'
        else:
            for x in sel:
                mc.setAttr(x+'.tx',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.ty',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.tz',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.rx',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.ry',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.rz',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.sx',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.sy',lock=True,channelBox=False,keyable=False )
                mc.setAttr(x+'.sz',lock=True,channelBox=False,keyable=False )
            print 'Lock en todo.'

    elif LockHide == True:
        mc.setAttr(objeto+'.tx',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.ty',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.tz',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.rx',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.ry',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.rz',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.sx',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.sy',lock=LockHide,keyable=not(LockHide) )
        mc.setAttr(objeto+'.sz',lock=LockHide,keyable=not(LockHide) )
    onOff= not(onOff)
    return onOff

def delBlendshape(win=''):
	blendShapeNode = mc.textFieldGrp(win+'FieldsN', q = True, text=True)
	# to get targets
	blendTargets = cmds.listAttr (blendShapeNode + '.w', m = True)
	# to get object influenced by blendShape
	history = cmds.listHistory (blendShapeNode, f=True, lf = True)
	shape = cmds.ls (history, type = ('mesh','nurbsSurface','nurbsCurve'))
	object = cmds.listRelatives (shape, fullPath = True, parent = True, type = 'transform')[0]
	for i in range(len(blendTargets)):
		cmds.blendShape (blendShapeNode, edit=True, remove = True, t=(object, i, blendTargets[i], 1.0) )

def coneccionEspejada():
	objs = mc.ls(sl=1,type='transform')
	if len(objs)>=2:
	    NMDTRF=str(objs[0])+'_COPY_TRF__NMD'
	    NMDROT=str(objs[0])+'_COPY_ROT__NMD'
	    if not mc.objExists(NMDTRF):
	        NMDTRF=mc.createNode('multiplyDivide', n=NMDTRF)
	        mc.setAttr(NMDTRF+'.input2X',-1)
	        mc.setAttr(NMDTRF+'.input2Y',1)
	        mc.setAttr(NMDTRF+'.input2Z',1)
	        if not mc.isConnected(str(objs[0])+'.translate', NMDTRF+'.input1'):
	            mc.connectAttr(str(objs[0])+'.translate', NMDTRF+'.input1', f=1)
	            mc.connectAttr(NMDTRF+'.output',str(objs[1])+'.translate', f=1)
	    else:
	        print 'Ya existe el nodo' + NMDTRF

	    if not mc.objExists(NMDROT):
	        NMDROT=mc.createNode('multiplyDivide', n=NMDROT)
	        mc.setAttr(NMDROT+'.input2X',1)
	        mc.setAttr(NMDROT+'.input2Y',-1)
	        mc.setAttr(NMDROT+'.input2Z',-1)
	        if not mc.isConnected(str(objs[0])+'.rotate', NMDROT+'.input1'):
	            mc.connectAttr(str(objs[0])+'.rotate', NMDROT+'.input1', f=1)
	            mc.connectAttr(NMDROT+'.output',str(objs[1])+'.rotate', f=1)
	    else:
	        print 'Ya existe el nodo' + NMDROT
	else:
	    mc.warning('OJO: Selecciona dos transforms. El segundo copiara al primero\nFunciona para espejar.')



#-----------------------------------------------------------------------------------------------
# END UI functions
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# END Classes
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# UI
#-----------------------------------------------------------------------------------------------
def e_toolsUI():
    global buttomL
    global buttomC
    global buttomR
    tWin='WindowsEtools_'
    if mc.window(tWin,ex=True):
    	mc.deleteUI(tWin)
    # Make a new window
    mc.window(tWin, title="Ice Cream 2015 - v1.8", iconName='Short Name',  bgc=(0.4,0.4,0.4), toolbox=1)
    #coloco un boton abajo
    mc.columnLayout(tWin+'cl1',columnAttach=('both', 1), rowSpacing=3, columnWidth=300)
    mc.text('SI NOMBRAS DE ESTA MANERA\nFUNCIONA MEJOR LA TOOL\nPLACE_OBJNAME_DESCRIP__SUFNODO\nEJ: L_HUMANO_PIERNA__MSH\n(MSH= nodo mesh)')
    mc.button (tWin+'btn2', label='RENAME OBJETS', command=windowRename,annotation='Name and list what you want.',w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn3', label='DELETE ALL NODE', command=deletingNodeType, annotation ='Borra tipos de nodos que describas.',w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn4', label='SWITCH L<->R', command=CambiaLado, annotation ='Letter switch sides.',w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.rowLayout(tWin+'rl0',numberOfColumns=3)
    mc.button (tWin+'btn5', label='RED', command=ColorRed, annotation ='Changes color to RED.', bgc=(1.0,0.0,0.0))
    mc.button (tWin+'btn6', label='YELLOW', command=ColorYellow, annotation ='Changes color to YELLOW.', bgc=(1.0,1.0,0.0))
    mc.button (tWin+'btn7', label='GREEN', command=ColorGreen, annotation ='Changes color to GREEN.', bgc=(0.0,1.0,0.0))
    mc.columnLayout(tWin+'cl',columnAttach=('both', 1), rowSpacing=3, columnWidth=300, parent=tWin+'cl1')
    mc.rowColumnLayout(tWin+'rl',numberOfColumns=4)
    mc.radioCollection(tWin+'rb',parent=tWin+'rl')
    buttomL=mc.radioButton(tWin+'cbLeft', label='L', select=True)
    buttomR=mc.radioButton(tWin+'cbRight', label='R')
    buttomC=mc.radioButton(tWin+'cbCenter', label='C')
    mc.button (tWin+'btn8',parent=tWin+'rl', label='MirrorPiece', command=mirrorPieces, annotation= 'Renombra respecto al hueso elejido la geometria y hace un mirror de la misma.', w=90, h=50, bgc=(0.5,0.5,0.5))
    mc.rowColumnLayout(tWin+'r2',numberOfColumns=4)
    mc.columnLayout(tWin+'cl2', parent=tWin+'r2')
    mc.button (tWin+'btn9',parent=tWin+'cl2', label='CNT to TRF', command=cntToShape, annotation= 'Primero el Obj luego el CNT.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn10',parent=tWin+'cl2', label='CNT in JOINT', command=cntjoint, annotation= 'Elije el axi primario que apunta al hueso hijo para colocar un cnt.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn15',parent=tWin+'cl2', label='MIRROR TRF', command=mirrorTRF, annotation= 'Selecciona un transform y le hace el valor negativo.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn11',parent=tWin+'cl2', label='intermedio ZTR', command=intermedioZTREject, annotation= 'Hace un ZTR entre el padre y el hijo.', w=150, h=50, bgc=(0.5,0.5,0.5))
    #mc.button (tWin+'btn20', label='delTargetBlendShape', command="partial(windowGeneric,'delTargetBlendShape',delBlendshape('delTargetBlendShape'))",annotation='delete targert blendshape.',w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn21',parent=tWin+'cl2', label='COPY NAME', command=copyName, annotation= 'Selecciona un hueso y luego la geometria y te copia el nombre con el sufijo SLC para el proxy.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.columnLayout(tWin+'cl3', parent=tWin+'r2')
    mc.button (tWin+'btn12',parent=tWin+'cl3', label='create CIRCLE in TRF', command=createCIRCLEinTRF, annotation= 'Crea control CIRCULO en TRF.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn13',parent=tWin+'cl3', label='create JOINT in VERTEX', command=createJointInVertex, annotation= 'Crea un joint con la seleccion de un vertice.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn14',parent=tWin+'cl3', label='create CLUSTER in VERTEX CURVE', command=createClusterInVertex, annotation= 'Crea cluster en vertice de curve.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn16',parent=tWin+'cl3', label='ATTR-ONOFF', command=switch, annotation= 'TOGGLE CHANNEL BOX EXCEPTO VISIBILITY.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn17',parent=tWin+'cl3', label='PARENT-SLC', command=parentSLCtoJoint, annotation= 'PARENT SLC A JOINT.', w=150, h=50, bgc=(0.5,0.5,0.5))
    mc.button (tWin+'btn18',parent=tWin+'cl3', label='CONECCION-MIRROR', command=coneccionEspejada, annotation= 'CONECTA TRANSFORM ESPEJANDOLOS.', w=150, h=50, bgc=(0.5,0.5,0.5))
    #Creditos
    mc.text(label= ' By: www.pabloemmanueldeleo.com', align='right', hyperlink=1 )
    #dibujo la ventana en pantalla
    mc.showWindow(tWin)
