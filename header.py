import re

qpropertyHeader = '''\tQ_PROPERTY(Type prop READ prop WRITE setProp NOTIFY propChanged)'''

constructorHeader = '''\tConstructor() {
Inits
\t}'''

m_readHeader = '''\tType prop() {
\t\treturn m_prop;
\t}'''
readHeader = '''\tType prop() {
\t\t// TODO
\t}'''

m_writeHeader = '''\tvoid setProp(const Type &prop)
\t{
\t\tif (prop == m_prop) {
\t\t\treturn;
\t\t}
\t\tm_prop = prop;
\t\temit propChanged();
\t}'''
writeHeader = '''\tvoid setProp(const Type &prop)
\t\t// TODO
\t\temit propChanged();
\t}'''

notifyHeader = '''\tvoid propChanged();'''

class Init:
    dataType = ''
    name = ''
    value = ''

def constructor(name, initList):
    _constructorHeader = constructorHeader.replace('Constructor', name)
    if len(initList) > 0:
        initValues = ''
        for init in initList:
            value = '\t\t' + init.name + ' = '
            if 'new' in init.value:
                _name = init.name.replace('*', '')
                _value = re.search(r'\(.*\)', init.value ).group()
                _type = init.dataType.replace('*', '')
                value += 'new ' + _type + _value + ';\n'
            else:
                value += init.value + ';\n'
            initValues += value
        initValues = initValues[:-1]
        _constructorHeader = _constructorHeader.replace('Inits', initValues)
    else:
        _constructorHeader = _constructorHeader.replace('Inits', '')
    return _constructorHeader

def qproperty(prop, name, dataType):
    _qpropertyHeader = qpropertyHeader
    if 'r' not in prop:
        _qpropertyHeader = _qpropertyHeader.replace(' READ prop', '')
    if 'w' not in prop:
        _qpropertyHeader = _qpropertyHeader.replace(' WRITE setProp', '')
    if 'n' not in prop:
        _qpropertyHeader = _qpropertyHeader.replace(' NOTIFY propChanged', '')
    _qpropertyHeader = _qpropertyHeader.replace('prop', name).replace('Type', dataType).replace('Prop', name.title())
    return _qpropertyHeader

def read(name, dataType, is_m_val):
    _read = ''
    if is_m_val:
        _read = m_readHeader.replace('prop', name).replace('Type', dataType)
    else:
        _read = readHeader.replace('prop', name).replace('Type', dataType)
    return _read

def write(name, dataType, is_m_val):
    _write = m_writeHeader if is_m_val else writeHeader
    _write = _write.replace('Prop', name.title())
    if '*' in dataType:
        _write = _write.replace('const Type &prop', dataType + ' ' + name).replace('prop', name).replace('Type', dataType)
    else:
        _write = _write.replace('prop', name).replace('Type', dataType)
    return _write

def notify(name):
    _notify = notifyHeader.replace('prop', name)
    return _notify
