# -*- coding: utf-8 -*-
import pymel.core as pm
import re
import sets
from maya import cmds , OpenMaya

# GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
def nonlinearDeformer(objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None, name='nonLinear'):
    #If something went wrong or the type is not valid, raise exception
    if not objects or defType not in ['bend','flare','sine','squash','twist','wave']:
        raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"
    #Create and rename the deformer
    nonLinDef = mc.nonLinear(objects[0], type=defType, lowBound=lowBound, highBound=highBound)
    nonLinDef[0] = mc.rename(nonLinDef[0], (name + '_' + defType + '_def'))
    nonLinDef[1] = mc.rename(nonLinDef[1], (name + '_' + defType + 'Handle'))
    #If translate was specified, set the translate
    if translate:
        mc.setAttr((nonLinDef[1] + '.translate'), translate[0], translate[1], translate[2])
    #If rotate was specified, set the rotate
    if rotate:
        mc.setAttr((nonLinDef[1] + '.rotate'), rotate[0], rotate[1], rotate[2])
    #Return the deformer
    return nonLinDef

def getUParam( pnt = [], crv = None):

    point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill=OpenMaya.MScriptUtil()
    paramPtr=paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:

        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    else :
        point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )

    param = paramUtill.getDouble(paramPtr)
    return param

def createCurveFromEdge(name='spline_loca',step=1):

    sel=pm.selectedNodes()
    if len(sel) != 1:
        cmds.error('Trabaje en un objeto y sus edge')
    edges=pm.filterExpand(sm=32)
    if len(edges) == 1:
        cmds.error('Seleccione edges continuos')
    #Guardo el nombre del objeto
    nameObj=sel[0].split('|')[1]
    #Cantidad de edges
    cant=len(edges)

    infoVerts = []
    fVerts = []
    lVerts = []
    #Recorro los edge y spliteo para conseguir el principio y final de cada edge
    for i in range(0,cant,step):
    	infoVerts=pm.polyInfo(edges[i], ev=1)
    	infoVerts=infoVerts[0].split(" ")
        fVerts.append(infoVerts[8])
    	lVerts.append(infoVerts[12])

    #ordeno y compongo la seleccion de vertices
    vertexNum=[]
    [vertexNum.append(x) for x in fVerts+lVerts if x not in vertexNum]

    #si tiene step diferente a 1, agrego el primero y el ultimo
    if step!=1:
        if not fVerts in vertexNum:
            vertexNum.insert(-1,lVerts)
        if not lVerts in vertexNum:
            vertexNum.insert(0,fVerts)

    vertexSel=[]
    [vertexSel.append(nameObj+'.vtx['+str(x)+']') for x in vertexNum]
    #saco la posicion de cada vertice
    xOrig = mc.xform( vertexSel, q=True, ws=True, t=True )
    #Formateo las posicions de vertices
    origPts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])
    #Cuento la cantidad de puntos para la curva
    vertCount = len(vertexSel)
    #Creo la curva
    crv = mc.curve( n=name,p=origPts, degree=2 )
    #Limpio la curva
    try:
        mc.rebuildCurve(crv, ch=False, rpo=True, rt=False, end=True, kr=False, kcp=False, kep=True, kt=True, s=vertCount, d=3, tol=0.01)
        mc.rebuildCurve(crv, ch=True, rpo=True, rt=False, end=True, kr=False, kcp=False, kep=True, kt=False, s=0, d=3, tol=0.01)
    except:
        pass
    return crv

def createInCurveJoint(spline=None):
    jnts=[]
    locs=[]
    vertexs=mc.polyListComponentConversion(spline,toVertex=True,fromEdge=True)
    #vertexs=mc.ls(spline, orderedSelection=True )
    for i in range(len(vertexs)):
        pointCrv=crv+".ep["+str(i)+"]"
        point=mc.pointPosition( pointCrv )

        loc=str(mc.spaceLocator(n=crv+"_"+str(i)+'_LOC')[0])
        #mc.xform(loc, t=point)

        #update in curve point
        poc=str(mc.createNode( 'pointOnCurveInfo',n= crv + '_POC' ))
        mc.connectAttr (  str(mc.listRelatives( crv,shapes=True )[0]) +'.worldSpace', poc+'.inputCurve',f=True )
        mc.connectAttr ( poc+'.position', loc+'.translate' ,f=True)
        parameter = getUParam(point,crv)
        mc.setAttr(poc+'.parameter',parameter)

        #create joint in locs
        mc.select(clear=True)
        jnt=mc.joint(p=point, name=crv+"_"+str(i)+'_JSK',rad=0.4)
        #Connectar loc con jnt
        mc.parent(jnt, loc)

        jnts.append(jnt)
        locs.append(loc)
        return jnts,locs

print 'DONE'