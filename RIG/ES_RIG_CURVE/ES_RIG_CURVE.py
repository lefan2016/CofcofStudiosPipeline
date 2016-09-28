from maya import cmds , OpenMaya , mel

def extraControl(objs=[],nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT'):
    #objs=cmds.ls(sl=1)
    grpYcnt=[]
    for obj in objs:
        print obj
        if '|' in obj:
            obj=obj.split('|')[-1]
        if '_' in obj:
            newName=obj.split(obj.split('_')[-1:][0])[0]
        else:
            newName=obj
        #currentParent=cmds.listRelatives(obj,parent=1)
        ztr=cmds.group(em=True,n=str(newName+nameSuf))
        pcns=cmds.parentConstraint(obj,ztr)
        scns=cmds.scaleConstraint(obj,ztr)
        cmds.delete(pcns,scns)

        trf=cmds.duplicate(ztr,n=str(newName+nameTrf))

        cmds.parent(trf,ztr)

        cnt=cmds.circle(radius=2,name=str(newName+nameCNT))[0]

        pcns=cmds.parentConstraint(trf,cnt)
        scns=cmds.scaleConstraint(trf,cnt)
        cmds.delete(pcns,scns)

        cmds.parent(cnt,trf)

        p=cmds.parent(obj,cnt)

        grpYcnt.append(ztr)
        grpYcnt.append(trf)
        grpYcnt.append(cnt)
    return grpYcnt

def creaLocWithJointsInPositionVertexOfCurve(curveActuals=None):
    #curveActuals=['L_braulio_curve_vestV2_CRV']
    dialogo=cmds.confirmDialog( title='ES_ENJONIADOR_DE_CURVAS', message='OJO! Te borrara todos los deformadores que tengas.\nRECOMENDACION: Usarlo antes de usar tu curva', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if curveActuals != None and dialogo=='Yes':
        dic={}
        locs=[]
        jnts=[]
        cnts=[]
        for curveActual in curveActuals:
            curveActualSHP=cmds.listRelatives(curveActual)[0]
            curve=cmds.rebuildCurve(curveActualSHP,keepRange=0,ch=1,rpo=1,rt=0,end=1,kcp=1,kep=1,kt=1,s=4,d=3,tol=0.01)[0]
            curveActualSHP=cmds.listRelatives(curve)[0]
            cmds.delete(curveActualSHP, ch = 1)
            if cmds.nodeType(curveActualSHP) == 'nurbsCurve':
                newName=curveActualSHP
                if '_' in curveActualSHP:
                    newName=curveActualSHP.split(curveActualSHP.split('_')[-1])[0]
                vertexs=cmds.ls( str(curveActualSHP)+'.cv[*]' )[0]
                cantVertex=range(int((vertexs.split(':')[-1])[:-1])+1)
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
                    loc=cmds.spaceLocator(n=newName+str(vtx)+'_LOC')[0]
                    cmds.connectAttr(poCi + ".position",loc+'.translate',f=1)
                    jnt=cmds.joint(n=newName+str(vtx)+'_JNT')
                    ztr=extraControl([jnt],'ZTR','TRF','CNT')
                    cmds.parentConstraint( loc,ztr[0],name=str(ztr[0])+'_HCNS', maintainOffset=False)
                    cmds.parentConstraint( ztr[2],jnt,name=str(ztr[2])+'_HCNS', maintainOffset=False)
                    locs.append(loc)
                    jnts.append(jnt)
                    cnts.append(ztr[0])
                grupoLocs=cmds.group(locs,name=newName+'LOCATORS_GRP',w=1)
                grupojnts=cmds.group(jnts,name=newName+'JOINTS_GRP',w=1)
                grupoCnts=cmds.group(cnts,name=newName+'CNTS_GRP',w=1)
                grupomaster=grupoLocs=cmds.group([grupoLocs,grupojnts,grupoCnts,curve],name=newName+'GRP',w=1)
                dic[curveActual]=locs,jnts,cnts
                return dic
            else:
                    cmds.warning(curveActualSHP+'No es una curva nurb')
    else:
        cmds.warning('No hay nada en el argumento')
seleccion=cmds.ls(sl=1)
cosas=creaLocWithJointsInPositionVertexOfCurve(seleccion)

def crearLowCrvControl(curvesActual=None):
    #curvesActual=cmds.ls(sl=1)
    for curveActual in curvesActual:
        newName=curveActual
        if '_' in curveActual:
            newName=curveActual.split(curveActual.split('_')[-1])[0]
        if curveActual:
            curve=cmds.duplicate(str(curveActual),name=newName+'CRVLOW', rr=1)[0]
            '''if not cmds.getAttr(curve+'.minMaxValue')[0] == (0.0, 1.0):'''
            curve=cmds.rebuildCurve(curve,keepRange=0,ch=1,rpo=1,rt=0,end=1,kcp=0,kep=1,kt=0,s=3,d=3,tol=0.01)[0]
            #cmds.delete(curve, ch = 1)
            newName=str(newName+'WIRE')
            mel.eval("wire -gw true -en 1.000000 -ce 0.000000 -li 0.000000 -dds 0 100 -name "+newName+" -w "+curve+" "+curveActual+";")
        else:
            cmds.warning('colocar las curvas')

crearLowCrvControl(seleccion)

sel=cmds.ls(sl=1)
for s in sel:
    cmds.select(s.replace('L_','R_'), add=1)
