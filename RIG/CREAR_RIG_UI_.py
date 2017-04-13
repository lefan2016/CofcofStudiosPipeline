# -*- coding: utf-8 -*-
import maya.cmds as cmds
def createUI(name='NAMEINGERFACE',size=10.0,texto='no name'):

    grp='FACE_UI_GRP'
    if not cmds.objExists(grp):
        grp=cmds.group(n=grp,em=True)

    if not cmds.objExists(name+'_UI_ZTR'):

        ztr=cmds.group(n=name+'_UI_ZTR',em=True)

        shape=cmds.curve(n=name+'_UI_TRF',d=1, p=[(1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, -1, 0),(1, -1, 0)] )
        cnt=cmds.circle(n=name+'_UI_CNT', nr=[0,0,1],radius=0.3)[0]
        cmds.transformLimits(cnt, tx=(-1 , 1),ty=(-1 , 1),etx=(True, True) ,ety=(True, True))

        changeColor([shape],2)
        changeColor([cnt],22)

        try:
            text=cmds.textCurves( n= name+'_UI_TCV', f='Arial', t=texto )
            cmds.move(0, size/2.0, 0, text, absolute=True)
        except:
            pass

        cmds.parent(ztr,grp)
        cmds.parent(shape,ztr)
        cmds.parent(cnt,shape)

        cmds.setAttr(str(shape)+'.scaleX',size)
        cmds.setAttr(str(shape)+'.scaleY',size)
        cmds.setAttr(str(shape)+'.scaleZ',size)

        transfomrs=['tz','rx','ry','rz','sx','sy','sz','v','tx','ty']
        for a in transfomrs[0:7]:
            cmds.setAttr(str(cnt)+'.'+a, lock=True,keyable=False,channelBox=False)
        for a in transfomrs:
            cmds.setAttr(str(shape)+'.'+a, lock=True,keyable=False,channelBox=False)

        cmds.select(ztr)

    else:
        cmds.warning('Eliga otro nombre para la interface porfavor, '+name+' ya existe.')

def changeColor(objs=[],color=22):
    for o in objs:
        cmds.setAttr (o+'.overrideEnabled', True)
        cmds.setAttr (o+'.overrideColor', color)

def accionCreateUI(*args):
    controlName = cmds.textField( 'nameOfTheTextField' ,query=True, text=True)
    controlSize = cmds.floatField( 'tamanio' ,query=True, value=True)
    createUI(controlName.upper(),controlSize,controlName.upper())

def winUI():
    nameW='CREAR RIG UI FACE'
    v=' v0.1'
    if cmds.window(nameW,ex=1):
        cmds.deleteUI(nameW)

    nameW=cmds.window(nameW,title=nameW+v)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,adjustableColumn=2)
    cmds.text(label='NOMBRE UI ')
    nameUI=cmds.textField('nameOfTheTextField',enterCommand=accionCreateUI,text='C_MOUTH')
    cmds.textField(nameUI,edit=True,)
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=3,adjustableColumn=2)
    cmds.text(label='SIZE UI ')
    sizeUI=cmds.floatField('tamanio',value=10.0,minValue=1,precision=3)
    btn=cmds.button('btn',label='CREAR UI',command=accionCreateUI,bgc=(0.65,0.82,0.24))
    cmds.showWindow(nameW)
