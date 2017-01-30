import maya.cmds as cmds

def getShapeNodes(obj):
    howManyShapes = 0
    getShape = cmds.listRelatives(obj,fullPath=True, shapes=True)
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
        shapesInSel = cmds.ls(dag=1,o=1,s=1,sl=1,absoluteName=True)
    #Encuentro el Shading Group del objeto referenciado
    shadingGrps = cmds.listConnections(shapesInSel[0],type='shadingEngine')
    for shdrs in shadingGrps:
        if str(shdrs[-1]) == str(1):
            cmds. error ('Existe el '+str(shdrs)+ ' shadingGroup no contiene nombre UNICO porfavor corregir.')
    #Si existe initialShadingGroup lo desconecto
    if 'initialShadingGroup' in shadingGrps:
        try:
            cmds.disconnectAttr(str(shapesInSel[0])+'.instObjGroups','initialShadingGroup.dagSetMembers',nextAvailable=True)
        except:
            pass
        try:
            cmds.disconnectAttr(str(shapesInSel[0])+'.compInstObjGroups[0].compObjectGroups[0]','initialShadingGroup.dagSetMembers',nextAvailable=True)
        except:
            pass
        shadingGrps.pop(shadingGrps.index('initialShadingGroup'))
    #Connecto el shader de la referencia
    try:
        for shders in shadingGrps:
            cmds.connectAttr(str(shders)+'.instObjGroups',str(shders)+'.dagSetMembers',nextAvailable=True)
    except:
        errores.append(str(shapesInSel[1]))
        pass
    # get the shaders:
    shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)
    print('Los shaders asignados de '+str(shapesInSel)+' son '+str(shaders))
    return errores

geos=cmds.ls(sl=True)
for geo in geos:
    try:
        prioritiSGreference(geo)
    except:
        pass
