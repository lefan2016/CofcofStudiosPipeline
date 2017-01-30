import maya.cmds as cmds

def getShapeNodes(obj):
    howManyShapes = 0
    getShape = cmds.listRelatives(obj,fullPath=True, shapes=True)
    if(getShape == None):
        print 'ERROR:: getShapeNodes : No Shape Nodes Connected to ' + obj + ' /n'
    else:
        howManyShapes = len(getShape[0])
    return (getShape, howManyShapes)

grpOrigen = 'R345_GEO_GRP'
grpDestino = 'R345_GEO_GRP1'
getShapeNodes(obj)
shapesOrigen = cmds.listRelatives(grpOrigen,type='mesh',allDescendents=True,fullPath=True)
shapesDestino = cmds.listRelatives(grpDestino,type='mesh',allDescendents=True,fullPath=True)

for shapesO in shapesOrigen:
    for shapesD in shapesDestino:
        if shapesO.split('|')[-1] == shapesD.split('|')[-1]:
            cmds.transferShadingSets(shapesO,)
