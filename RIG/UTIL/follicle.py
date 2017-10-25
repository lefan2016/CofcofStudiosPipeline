# @Date:   2017-10-25T16:34:32-03:00
# @Last modified time: 2017-10-25T16:34:35-03:00
import pymel.core as pm

def create_follicle(oNurbs, uPos=0.0, vPos=0.0):
    # manually place and connect a follicle onto a nurbs surface.
    if oNurbs.type() == 'transform':
        oNurbs = oNurbs.getShape()
    elif oNurbs.type() == 'nurbsSurface':
        pass
    else:
        'Warning: Input must be a nurbs surface.'
        return False

    # create a name with frame padding
    pName = '_'.join((oNurbs.name(),'follicle','#'.zfill(2)))

    oFoll = pm.createNode('follicle', name=pName)
    oNurbs.local.connect(oFoll.inputSurface)
    # if using a polygon mesh, use this line instead.
    # (Warning! The polygons will need to have UVs in order to work!)
    #oMesh.outMesh.connect(oFoll.inMesh)

    oNurbs.worldMatrix[0].connect(oFoll.inputWorldMatrix)
    oFoll.outRotate.connect(oFoll.getParent().rotate)
    oFoll.outTranslate.connect(oFoll.getParent().translate)
    oFoll.parameterU.set(uPos)
    oFoll.parameterV.set(vPos)
    oFoll.getParent().t.lock()
    oFoll.getParent().r.lock()

    return oFoll

oFoll = create_follicle(pm.selected()[0], 0.5, 0.5)
