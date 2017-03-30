# -*- coding: utf-8 -*-
import pymel.core as pm
import re
import sets
from maya import cmds, OpenMaya, mel

def edgeLoopCrv(meshEdgeList, rebuild=False, rebuildSpans=0, form=2, keepHistory=True, prefix=''):
	'''
	INPUT:
	meshEdgeList (TIPO: list, DESCROPCION: edges seleccionados)
	rebuild (TIPO: bool, DESCROPCION: rebuild de la curva)
	rebuildSpans (TIPO: int, DESCROPCION: rebuild cantidad de spans)
	form (TIPO: int, DESCROPCION: cantidad de suavisado)
	keepHistory (TIPO: bool, DESCROPCION: keepHistory colapce)
	prefix (TIPO: string, DESCROPCION: nombre de la curva )
	OUPUT:
	curve (TIPO: string, DESCROPCION: nombre de la curva )
	EJEMPLO:
	Crear curva segun edge con joints
	tambien podras aderir algun modificador.

	seleccion=cmds.ls(sl=1,o=True)
	seleccionEdge=cmds.ls(sl=1)
	cosas={}
	crv=ere.edgeLoopCrv(seleccionEdge)
	cosas[0]=ere.creaLocWithJointsInPositionVertexOfCurve([crv],step=2)
	ere.aimConsecutiveList(cosas[0][0],'coco')
	lowCRV=ere.crearLowCrvControl([crv])

	ere.nonlinearDeformer([lowCRV[0]],'twist',rotate=(0,0,90))
	ere.nonlinearDeformer([lowCRV[0]],'sine',rotate=(0,0,90))
	'''
	# Nombro igual al objeto
	if prefix=='': prefix =  str(meshEdgeList[0]).split('.')[0]
	#obtengo los edge seleccionados
	meshEdgeList = cmds.ls(meshEdgeList, fl=True)
	rebuldSpans = len(meshEdgeList)
	# Convert edge selection to nurbs curve
	crvDegree = 1
	if rebuild:
		crvDegree = 3
	curve = cmds.polyToCurve(ch=keepHistory, form=form, degree=crvDegree)[0]
	# Rebuild as degree 3
	if rebuild and rebuildSpans:
		curve = cmds.rebuildCurve(curve, ch=keepHistory, rpo=1, rt=0, end=1,
								  kr=0, kcp=1, kep=1, kt=1, s=rebuildSpans, d=3, tol=0.01)[0]
	# Rename curve
	curve = cmds.rename(curve, prefix + '_CRV')
	# Return result
	return curve

# GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
def nonlinearDeformer(objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None, name='nonLinear'):
	# If something went wrong or the type is not valid, raise exception
	if not objects or defType not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
		raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"
	# Create and rename the deformer
	nonLinDef = cmds.nonLinear(
		objects[0], type=defType, lowBound=lowBound, highBound=highBound)
	nonLinDef[0] = cmds.rename(nonLinDef[0], (name + '_' + defType + '_def'))
	nonLinDef[1] = cmds.rename(nonLinDef[1], (name + '_' + defType + 'Handle'))
	# If translate was specified, set the translate
	if translate:
		cmds.setAttr((nonLinDef[1] + '.translate'),
					 translate[0], translate[1], translate[2])
	# If rotate was specified, set the rotate
	if rotate:
		cmds.setAttr((nonLinDef[1] + '.rotate'),
					 rotate[0], rotate[1], rotate[2])
	# Return the deformer
	return nonLinDef

def Aliniar(object=None,offsetGrp=None):
    # match object transform
    if cmds.nodeType(object)=='transform':
        if cmds.nodeType(offsetGrp)=='transform':
            cmds.delete( cmds.parentConstraint( object, offsetGrp ) )
            cmds.delete( cmds.scaleConstraint( object, offsetGrp ) )
        else:
            cmds.warning('Falta el target.')
    else:
        cmds.warning('No hay que alinear.')

def controlSphera(name='_CNT',scale=1,toObj=None):
    ctrlObject = cmds.circle( n = name, ch = False, normal = [1, 0, 0], radius = scale )
    addShape = cmds.circle( n =name, ch = False, normal = [0, 0, 1], radius = scale )[0]
    addShape2 = cmds.circle( n =name, ch = False, normal = [0, 1, 0], radius = scale )[0]
    cmds.parent( cmds.listRelatives( addShape, s = 1 ), ctrlObject[0], r = 1, s = 1 )
    cmds.parent( cmds.listRelatives( addShape2, s = 1 ), ctrlObject[0], r = 1, s = 1 )
    cmds.delete( addShape,addShape2 )
    if toObj:
        Aliniar(ctrlObject,toObj)
    return ctrlObject

def extraControl(objs=[], nameSuf='ZTR', nameTrf='TRF', nameCNT='CNT', **kwargs):
	# objs=cmds.ls(sl=1)
	grpYcnt = []
	for obj in objs:
		if '|' in obj:
			obj = obj.split('|')[-1]
		if '_' in obj:
			newName = obj.split(obj.split('_')[-1:][0])[0]
		else:
			newName = obj
		# currentParent=cmds.listRelatives(obj,parent=1)
		ztr = cmds.group(em=True, n=str(newName + nameSuf))
		pcns = cmds.parentConstraint(obj, ztr)
		scns = cmds.scaleConstraint(obj, ztr)
		cmds.delete(pcns, scns)

		trf = cmds.duplicate(ztr, n=str(newName + nameTrf))

		cmds.parent(trf, ztr)

		cnt = cmds.circle(name=str(newName + nameCNT), **kwargs)[0]

		pcns = cmds.parentConstraint(trf, cnt)
		scns = cmds.scaleConstraint(trf, cnt)
		cmds.delete(pcns, scns)

		cmds.parent(cnt, trf)

		p = cmds.parent(obj, cnt)

		grpYcnt.append(ztr)
		grpYcnt.append(trf)
		grpYcnt.append(cnt)
	return grpYcnt


def creaLocWithJointsInPositionVertexOfCurve(curveActuals=None, step=1, rebuild=False):
	#step=2
	#curveActuals=['curva_loca_CRV']
	if curveActuals != None:
		dic={}
		locs=[]
		jnts=[]
		cnts=[]
		for curveActual in curveActuals:
			curveActualSHP=cmds.listRelatives(curveActual)[0]
			if cmds.nodeType(curveActualSHP) == 'nurbsCurve':
				curve=curveActualSHP
			else:
				curveActualSHP=cmds.listRelatives(curve)[0]
			cmds.delete(curveActualSHP, ch = 1)
			if cmds.nodeType(curveActualSHP) == 'nurbsCurve':
				newName=curveActualSHP
				if '_' in curveActualSHP:
					newName=curveActualSHP.split(curveActualSHP.split('_')[-1])[0]
				vertexs=cmds.ls( str(curveActualSHP)+'.cv[*]' )[0]
				cantVertex=range(int((vertexs.split(':')[-1])[:-1])+1)
				if step!=1:
					end=cantVertex[-1]
					cantVertex=range(0,end,step)
					if not end in cantVertex:
						cantVertex.insert(-1,end)
				for vtx in cantVertex:
					npC = cmds.createNode("nearestPointOnCurve",n=newName+str(vtx)+'_POC')
					poCi = cmds.createNode("pointOnCurveInfo",n=newName+str(vtx)+'_POCI')
					cmds.connectAttr(curveActualSHP+".worldSpace", npC + ".inputCurve", f=1)
					cmds.connectAttr(curveActualSHP+".worldSpace", poCi + ".inputCurve", f=1)
					cmds.connectAttr(npC+".parameter", poCi + ".parameter", f=1)
					wsPos=cmds.getAttr(curveActualSHP+'.controlPoints['+str(vtx)+']')[0]
					cmds.setAttr(npC + ".inPosition", wsPos[0], wsPos[1], wsPos[2], type="double3")
					uParam = cmds.getAttr(npC + ".parameter")
					cmds.delete(npC)
					loc=cmds.spaceLocator(n=newName+str(vtx)+'_LOC',)[0]
					locs.append(loc)
					[cmds.setAttr(loc+'.localScale'+axi,0.2) for axi in ['X','Y','Z']]
					cmds.connectAttr(poCi + ".position",loc+'.translate',f=1)
					jnt=cmds.joint(n=newName+str(vtx)+'_JNT',rad=0.3)

					ztr=extraControl([jnt],'ZTR','TRF','CNT',radius=0.4)
					cmds.parentConstraint( loc,ztr[0],name=str(ztr[0])+'_HCNS', maintainOffset=False)
					cmds.parentConstraint( ztr[2],jnt,name=str(ztr[2])+'_HCNS', maintainOffset=False)

					jnts.append(jnt)
					cnts.append(ztr[0])

				gLocs=cmds.group(locs,name=newName+'LOCATORS_GRP')
				gjnts=cmds.group(jnts,name=newName+'JOINTS_GRP',w=1)
				gCnts=cmds.group(cnts,name=newName+'CNTS_GRP',w=1)

				gNoXform=cmds.group(em=True, name=newName+'NOXFORM_GRP')
				cmds.setAttr(gNoXform+'.inheritsTransform',0)

				cmds.parent(curveActual,gNoXform)
				gMaster=cmds.group(em=True,n=newName+'GRP')

				cmds.parent([gLocs,gjnts,gCnts,gNoXform],gMaster)

				return [locs, jnts, cnts]
			else:
				cmds.warning(curveActualSHP + 'No es una curva nurb')
	else:
		cmds.warning('No hay nada en el argumento')

def crearLowCrvControl(curvesActual=None, cnt=True,rad=1):
	# curvesActual=cmds.ls(sl=1)
	for curveActual in curvesActual:
		newName = curveActual
		if '_' in curveActual:
			newName = curveActual.split(curveActual.split('_')[-1])[0]
		if curveActual:
			curve = cmds.duplicate(
				str(curveActual), name=newName + 'CRVLOW', rr=1)[0]
			'''if not cmds.getAttr(curve+'.minMaxValue')[0] == (0.0, 1.0):'''
			curve = cmds.rebuildCurve(
				curve, keepRange=0, ch=1, rpo=1, rt=0, end=0, kcp=0, kep=1, kt=0, s=3, d=3, tol=0.01)[0]
			#cmds.delete(curve, ch = 1)
			mel.eval("wire -gw true -en 1.000000 -ce 0.000000 -li 0.000000 -dds 0 100 -name " +
					 newName + 'WIRE' + " -w " + curve + " " + curveActual + ";")
		else:
			cmds.warning('colocar las curvas')
		if cnt:
			#creo cluster and rename that
			topCLR=cmds.cluster( str(curve)+'.cv[0:2]')[1]
			topCLR=cmds.rename(topCLR,newName+'TOP_CLR')

			midCLR=cmds.cluster( str(curve)+'.cv[2:3]' )[1]
			midCLR=cmds.rename(midCLR,newName+'MID_CLR')

			endCLR=cmds.cluster( str(curve)+'.cv[3:5]' )[1]
			endCLR=cmds.rename(endCLR,newName+'BOT_CLR')
			#change pivot to start vertex
			p1=cmds.xform(str(curve)+'.cv[0]',q=1,t=1,ws=1)
			cmds.xform(str(topCLR),piv=p1,ws=1)

			p2=cmds.xform(str(curve)+'.cv[5]',q=1,t=1,ws=1)
			cmds.xform(str(endCLR),piv=p2,ws=1)

			CNTS=extraControl([topCLR,midCLR,endCLR],'ZTR','TRF','CNT',radius=rad)
	return curve,topCLR,midCLR,endCLR


def aimConsecutiveList(listObjects=[],fixList=False,name=''):
	if fixList:
		#fixlista remove and insert the last value
		listObjects.insert(len(listObjects)-2, listObjects.pop(len(listObjects)-1))
		#####
	current = 0
	prox = 1
	last = len(listObjects)-1
	if name != '':
		name=cmds.ls(sl=1,o=True)
	if '_' in name:
		name = name.split(name.split('_')[-1])[0]
	'''#constraint el primer objeto
	cmds.aimConstraint(listObjects[prox], listObjects[current],
						offset=[0,0,0], aimVector=[ 0, 1, 0], upVector=[0, 1, 0],
						n=str(listObjects[prox]) + '_ACNS')'''
	#constraint en todos los siguientes objetos
	for o in listObjects:
		if listObjects[current] != last:
			aim=cmds.aimConstraint(listObjects[current], listObjects[prox],
									offset=[0,0,0], aimVector=[	0, 1, 0], upVector=[0, 1, 0],
									worldUpType='object',worldUpObject=str(listObjects[prox-1]),
									n=str(o) + '_ACNS')
			current += 1
			prox += 1

def midPointV3(p1=(),p2=()):
	return (( p1[0] + p2[0] ) / 2) , (( p1[1] + p2[1] ) / 2),(( p1[2] + p2[2] ) / 2)
