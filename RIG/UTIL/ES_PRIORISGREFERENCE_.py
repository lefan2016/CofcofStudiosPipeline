import maya.cmds as cmds

def getShapeNodes(obj):
    howManyShapes = 0
    getShape = cmds.listRelatives(obj, shapes=True)
    if(getShape == None):
        print 'ERROR:: getShapeNodes : No Shape Nodes Connected to ' + obj + ' /n'
    else:
        howManyShapes = len(getShape[0])
    return (getShape, howManyShapes)

def prioritiSGreference(obj=None):
    ''' Contempla los shader de la geometria referenciada pasandolo al deformed'''
    errores=None
    if obj:
        # saco el shap de la geometria
        shapesInSel = getShapeNodes(obj)[0]
    else:
        # saco el shap de la geometria
        shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1)
    #Encuentro el Shading Group del objeto referenciado
    shadingGrps = cmds.listConnections(shapesInSel[0],type='shadingEngine')
    #Desconecto el initialShadingGroup por defecto
    try:
        cmds.disconnectAttr(str(shapesInSel[1])+'.instObjGroups','initialShadingGroup.dagSetMembers',nextAvailable=True)
    except:
        pass
    #Connecto el shader de la referencia
    try:
        cmds.connectAttr(str(shapesInSel[1])+'.instObjGroups',str(shadingGrps[0])+'.dagSetMembers',nextAvailable=True)
    except:
        errores.append(str(shapesInSel[1]))
        pass
    # get the shaders:
    shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
    print('Los shaders asignados de '+str(shapesInSel)+' son '+str(shaders))
    return errores

geos=cmds.ls(sl=True)
for geo in geos:
    errores=[]
    try:
        errores=prioritiSGreference(geo)
    except:
        pass
print ('ESTOS OBJETOS NO RESPONDIERON BIEN: \n'+str(errores))
