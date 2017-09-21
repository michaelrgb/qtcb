import os, sys, pudb

def refresh_qtcreator_session():
    import subprocess, time
    try: stdout = subprocess.check_output('xdotool search --name "Qt Creator"', shell=True)
    except: return
    stdout = stdout.decode().splitlines()
    if not stdout:
        return
    id_qtc = stdout[0]
    stdout = subprocess.check_output('xdotool getactivewindow', shell=True)
    id_focus = stdout.decode().splitlines()[0]
    MODE_SELECT_SHORTCUT = 'Ctrl+4 key Ctrl+1'
    # Select the Projects Mode to recreate the session xml.
    subprocess.check_output('xdotool windowfocus ' + id_qtc + ' key ' + MODE_SELECT_SHORTCUT + ' windowfocus ' + id_focus,
                            shell=True)
    time.sleep(0.5)

    return True

HOME = os.path.expanduser('~') + '/'
QT_CREATOR_SESSION_XML = HOME + '.config/QtProject/qtcreator/default.qws'

def make_pudb_breakpoint_file():
    import xml.etree.ElementTree
    root = xml.etree.ElementTree.parse(QT_CREATOR_SESSION_XML).getroot()

    with open(pudb.settings.get_breakpoints_file_name(), 'w') as f:
        for data in root.findall('data'):
            children = data.getchildren()
            if children[0].text != 'value-Breakpoints':
                continue
            for valuemap in children[1].getchildren():
                file_line = valuemap.getchildren()
                filename = file_line[0].text
                if not filename.endswith('.py'):
                    continue
                f.write('b ' + filename + ':' + file_line[1].text + '\n')

def main():
    argv = sys.argv[1:]
    if len(argv) < 1:
        print('Usage: python -m qtcb myscript.py <args>')
        return

    if not refresh_qtcreator_session():
        print('Could not find QtCreator instance.')
        return

    make_pudb_breakpoint_file()
    pudb.runscript(argv[0], argv[1:])

if __name__ == "__main__":
    main()
