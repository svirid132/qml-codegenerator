import shutil
import os
import re
import header

# удаляет специальные символы (\n \t \r) и удаляет пустые строки
# аргументы - список _list
# возращает новый список
def deleteSpecialSymbol(_list):
    new_list = list( filter(lambda line: line != "", _list) )
    new_list = list( map(lambda line: line.strip(), new_list) )
    return new_list

titleHeader = '''#ifndef NAME_OBJECT_H
#define NAME_OBJECT_H
#include <QObject>

class NameObject : public QObject {
\tQ_OBJECT'''

varHeader = '''\tType m_prop;'''
endHeader = '''};

#endif'''

class DataProps:
    prop = ''
    init = ''

f = open('pragma.qg')
projectDir = ''
while f.readable():
    line = f.readline()

    if line == '': 
        break

    if '#project' in line:
        args = deleteSpecialSymbol( re.split(' +', line) )
        projectDir = args[1]
        if os.path.exists( projectDir ):
            shutil.rmtree( projectDir )
        os.mkdir( projectDir )
    
    if 'object' in line:
        args = deleteSpecialSymbol( re.split(' +', line) )
        objectName = args[1]
        objectF = open( projectDir + "/" + objectName.lower() + '.h', "w" )
        resultHeader = titleHeader.replace('NameObject', objectName).replace('NAME_OBJECT', objectName.upper()) + '\n'
        inits = []
        qpropertyHeaders = []
        writeHeaders = []
        readHeaders = []
        notifyHeaders = []
        m_datas = []
        while True:
            line = f.readline()
            if 'end' in line:
                break

            props = re.search(r'\(.+\)', line).group()[1:-1]
            props = re.split(';', props)
            print(props)
            dataProps = DataProps()
            for prop in props:
                args = re.split('=', prop)
                args = deleteSpecialSymbol(args)
                propName = args[0]
                propValue = args[1]
                if 'prop' in propName:
                    dataProps.prop = propValue
                if 'init' in propName:
                    dataProps.init = propValue

            is_m_val = 'm' in dataProps.prop
            args = deleteSpecialSymbol( re.split(' +', line) )
            name = args[0].replace(':', '')
            dataType = re.sub(r'\(.*', '', args[1])
            m_data = '\t' + dataType + ' ' + 'm_' + name + ';'
            if is_m_val:
                m_datas.append( m_data ) # QString m_data;

            _qproperty = header.qproperty( dataProps.prop, name, dataType )
            qpropertyHeaders.append( _qproperty )

            if 'r' in dataProps.prop:
                _read = header.read(name, dataType, is_m_val)
                readHeaders.append( _read )
            if 'w' in dataProps.prop:
                _write = header.write(name, dataType, is_m_val)
                writeHeaders.append(_write)
            if 'n' in dataProps.prop:
                _notify = header.notify(name)
                notifyHeaders.append(_notify)

            if dataProps.init != '':
                init = header.Init()    
                init.dataType = dataType
                init.name = name
                init.value = dataProps.init
                inits.append(init)

        for line in qpropertyHeaders:
            resultHeader += line + '\n'
        resultHeader += '\n'
        resultHeader += 'public:\n'

        _constructor = header.constructor(objectName, inits)
        resultHeader += _constructor
        resultHeader += '\n\n'

        for _read in readHeaders:
            resultHeader += _read + '\n'
        if len(readHeaders) > 0:
            resultHeader += '\n'

        for _write in writeHeaders:
            resultHeader += _write + '\n'
        if len(writeHeaders) > 0:
            resultHeader += '\n'

        resultHeader += 'signals:\n'
        for _notify in notifyHeaders:
            resultHeader += _notify + '\n'
        resultHeader += '\n'
        resultHeader += 'private:\n'
        for _data in m_datas:
            resultHeader += _data + '\n'
        resultHeader += endHeader

        objectF.write(resultHeader)
        objectF.close()
    
print( 'успешно' )
f.close()