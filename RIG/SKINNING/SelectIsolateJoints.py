"""
    Selecciona y aisla los joints que contiene el skin junto al mesh. Activa skinning weights. 
"""
import maya.cmds as mc
import maya.mel as mel

selGeo = mc.ls (sl=True)
if selGeo:
    try:
        influenceJoints = mc.skinCluster (selGeo, query=True, influence=True)
        mc.select (influenceJoints, add=True)
        isoPnl = mc.getPanel(wf=True)
        isoCrnt = mc.isolateSelect(isoPnl, q=True, s=True)
        mel.eval('enableIsolateSelect %s %d' % (isoPnl,not isoCrnt) )
        mel.eval('ArtPaintSkinWeightsToolOptions; changeSelectMode -object; select -add %s' %selGeo[0])
    except :
        mc.warning('No se pudo. Tal vez no sea algo con skin...' )
        