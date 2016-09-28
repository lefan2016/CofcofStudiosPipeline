import maya.cmds as mc

def addAttrString(objs=None,attrName='', date=''):
    for obj in objs:
        if not mc.attributeQuery(attrName, node=obj, exists=1):
            mc.addAttr(obj,shortName=attrName, dataType='string')
        else:
            print 'Ya existe el atributo '+attrName+' en '+obj
            return 1

def editAttrString(objs=None,attrName='',newText='editame'):
    for obj in objs:
        if mc.attributeQuery(attrName, node=obj, exists=1):
            if mc.getAttr(obj+'.'+attrName,type=True)=='string':
                mc.setAttr(obj+'.'+attrName, newText, type='string')
                print 'Se ha editado el atributo ' + attrName + ' con el siguiente dato:/n ' + newText
            else:
                print 'El atributo '+attrName+' en '+obj+' no es del tipo string.'
        else:
            print 'No existe el atributo '+attrName+' en '+obj


def deleteAttributo(objs=None,attrName=''):
    for obj in objs:
        if mc.attributeQuery(getAttrs()[0], node=obj, exists=1):
            mc.deleteAttr( obj+'.'+getAttrs()[0] )
        else:
            print 'No existe el atributo '+attr+' en '+obj


def addAt(tf=None):
    objs=mc.ls(sl=1)
    addAttrString(objs,getAttrs()[0])
    editAt()

def editAt():
    objs=mc.ls(sl=1)
    if not len(getAttrs()[0])==0:
        editAttrString(objs,getAttrs()[0],getAttrs()[1])
    else:
        mc.warning('Necesitas agregar datos al string')

def deletAt():
    objs=mc.ls(sl=1)
    deleteAttributo(objs,getAttrs()[0])

global def getAttrs():
    global tfu,tftext,b2
    attr=mc.textField(tfu, q=1,text=1)
    texto=mc.textField(tftext, q=1,text=1)
    return attr,texto

def refreshFun():
    if len(getAttrs()[0]) and len(getAttrs()[1]) != 0:
        mc.button(b2,edit=1, enable=1)
    else:
        mc.button(b2,edit=1, enable=0)
        
def UI():
    w='ES_ATTRIBUTO_PUPURRI_'
    global tfu,tftext,b2
    if mc.window(w,ex=1):
        mc.deleteUI(w)
    w=mc.window(w,title=w,resizeToFitChildren=True)
    c=mc.columnLayout(adjustableColumn = True)
    rl=mc.rowLayout(numberOfColumns=6)
    mc.text('Nombre de Atributo: ')
    tfu=mc.textField(w + 'At', ann='Adiere el nombre del atributo exacto.',width=50,textChangedCommand="refreshFun()",receiveFocusCommand='refreshFun()')
    tftext=mc.textField(w + 'Attext', ann='Edita el atributo.',width=300,textChangedCommand="refreshFun()",receiveFocusCommand='refreshFun()')
    b1=mc.button (label = "ADD", command = 'addAt()', bgc = (1.0, 0.9, 0.1),)
    b2=mc.button (label = "EDIT", command = 'editAt()', bgc = (0.5, 0.8, 0.1),enable=0)
    b3=mc.button (label = "REMOVE", command = 'deletAt()', bgc = (1.0, 0.5, 0.1),)
    
    mc.showWindow(w)
UI()