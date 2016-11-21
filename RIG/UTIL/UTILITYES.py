import maya.cmds as cmds
#Crea un offset en seleccion.
def offSetGrp(obj=None,suf=''):
    newName=''
    newNode=None
    if cmds.nodeType(obj)=='transform':
        newName=obj
        if '|' in newName:
            newName=str(obj.split('|')[-1])
        if '_' in str(newName) and (not suf in str(newName)):
            newName=str( newName[:newName.rfind("_")])+suf
        else:
            newName=str(newName)+suf

        newNode=cmds.duplicate(obj,n=newName,parentOnly=True)
        cmds.parent(obj,newNode[0])
        return newNode[0]
    else:
        print str(obj) + ' necesitas que sea un nodo de transformacion.'

def extraControl(objs=[],nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT',rad=14):
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
        pcns=cmds.parentConstraint(obj,ztr)[0]
        scns=cmds.scaleConstraint(obj,ztr)[0]
        cmds.delete(pcns,scns)
        trf=cmds.duplicate(ztr,n=str(newName+nameTrf))[0]
        cmds.parent(trf,ztr)
        cnt=cmds.circle(radius=rad,nrx=1,normalZ=0,name=str(newName+nameCNT))[0]
        pcns=cmds.parentConstraint(trf,cnt)
        scns=cmds.scaleConstraint(trf,cnt)
        cmds.delete(pcns,scns)
        cmds.parent(cnt,trf)
        #p=cmds.parent(obj,cnt)
        grpYcnt.append(ztr)
        grpYcnt.append(trf)
        grpYcnt.append(cnt)
    return grpYcnt


###Colocar control con offset en el lugar deseado.
###sn=extraControl(cmds.ls(sl=1,long=True))
