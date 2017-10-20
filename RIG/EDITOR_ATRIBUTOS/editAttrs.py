import maya.cmds as cmds
'''
path=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\EDITOR_ATRIBUTOS'
if not path in sys.path:
    sys.path.append(path)
try:
    import editAttrs
    reload(editAttrs)
except (RuntimeError, TypeError, NameError,IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'
'''
class attrs():
    def __init__():
        self.key=string
        self.value=None


def addAttrString(objs=None,attrName=''):
    for obj in objs:
        if not cmds.attributeQuery(attrName, node=obj, exists=1):
            cmds.addAttr(obj,shortName=attrName, dataType='string')
        else:
            print 'Ya existe el atributo '+attr+' en '+obj

def editAttrString(objs=None,typeAttr,attrName='',newText='editame'):
    for obj in objs:
        if cmds.attributeQuery(attrName, node=obj, exists=1):
            if cmds.getAttr(obj+'.'+attrName,type=True)=='string':
                cmds.setAttr(obj+'.'+attrName, newText, type='string')
                print 'Se ha editado ' + attrName + 'con el siguiente dato: ' + newText
            else:
                print 'El atributo '+attrName+' en '+obj+' no es del tipo string.'
        else:
            print 'No existe el atributo '+attrName+' en '+obj


def deleteAttributo(objs=None,attrName=''):
    for obj in objs:
        if cmds.attributeQuery(getAttrs()[0], node=obj, exists=1):
            cmds.deleteAttr( obj+'.'+getAttrs()[0] )
        else:
            print 'No existe el atributo '+attr+' en '+obj


def addAt(tf=None):
    objs=cmds.ls(sl=1)
    addAttrString(objs,getAttrs()[0])

def editAt(*args):
    objs=cmds.ls(sl=1)
    if not len(getAttrs()[0])==0:
        editAttrString(objs,getAttrs()[0],getAttrs()[1])
    else:
        cmds.warning('Necesitas agregar datos al string')

def deletAt(*args):
    objs=cmds.ls(sl=1)
    deleteAttributo(objs,getAttrs()[0])

def getAttrs(*args):
    global tfu,tftext,b2
    attr=cmds.textField(tfu, q=1,text=1)
    texto=cmds.textField(tftext, q=1,text=1)
    return attr,texto

def refreshFun(*args):
    if len(getAttrs()[0]) and len(getAttrs()[1]) != 0:
        cmds.button(b2,edit=1, enable=1)
    else:
        cmds.button(b2,edit=1, enable=0)

def UI():
    w='ES_ATTRIBUTO_PUPURRI'
    global tfu,tftext,b2
    if cmds.window(w,ex=1):
        cmds.deleteUI(w)
    w=cmds.window(w,title=w,resizeToFitChildren=True)
    c=cmds.columnLayout(adjustableColumn = True)
    rl=cmds.rowLayout(numberOfColumns=6)
    cmds.text('Nombre de Atributo: ')
    tfu=cmds.textField(w + 'At', ann='Adiere el nombre del atributo exacto.',textChangedCommand=refreshFun,receiveFocusCommand=refreshFun)
    tftext=cmds.textField(w + 'Attext', ann='Edita el atributo.',textChangedCommand=refreshFun,receiveFocusCommand=refreshFun)
    b1=cmds.button (label = "ADD", command = 'addAt()', bgc = (1.0, 0.9, 0.1),)
    b2=cmds.button (label = "EDIT", command = editAt() bgc = (0.5, 0.8, 0.1),enable=0)
    b3=cmds.button (label = "REMOVE", command = deletAt, bgc = (1.0, 0.5, 0.1),)

    cmds.showWindow(w)
UI()
