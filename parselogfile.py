import re, os.path, argparse, sys
parser = argparse.ArgumentParser(description="This utility parses a log file and makes a batch file that changes permissions for copying files from a directory that was extracted from install.wim, and then copies the files over the corrupted ones.")
parser.add_argument("logfilepath", type=argparse.FileType("r"), help="The full path to the sfcdetails file")
parser.add_argument("goodfilepath", type=str, help="The full path to the copy of files that are from the install.wim image.  Lets say I extracted the 2 folder (Windows Home Premium) from the install.wim file, and it was located at \"C:\\2\\\". Then this argument would be \"C:\\2\\\".  Make sure that backslash is there at the end too.  There will be a Windows folder inside if you look in there.")
parser.add_argument("windowsdriveletter", type=str, help="The drive letter that your running copy of Windows is on.  For most users, it would be \"C\".")
if len(sys.argv) == 1 :
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
goodfilepath = args.goodfilepath
windowsdriveletter = args.windowsdriveletter
x = args.logfilepath
#x = open("C:\\Users\\westly\\Desktop\\sfcdetails.txt", "r")
y = x.read()
x.close()
a = open("fixfiles.bat", "w")
stringscan = re.compile(r'\[SR\] Could not reproject corrupted file \[.+?\:.+?\{.+?\}\,.+?\:.+?\{.+?\}\]\"\\\?\?\\C\:\\(.+?)\"\\\[.+?\:.+?\{.+?\}\]\"(.+?)\"\; source file in store is also corrupted')
z = stringscan.findall(y)
results = []
for result in z :
    if result not in results :
        results.append(result)
for result in results :
    filepath = os.path.join(result[0], result[1])
    #filepath = "G:\\installwim\\2\\" + os.path.join(result[0], result[1])
#    if os.path.exists(filepath) :
#        print "OK", filepath
#    else :
#        print "NOT OK", filepath
    a.write("echo Copying " + result[1] + "\r\n")
    a.write("takeown /f %(driveletter)s:\\%(filepath)s\r\n" % {"driveletter":windowsdriveletter, "filepath":filepath})
    a.write("icacls %(driveletter)s:\\%(filepath)s /grant administrators:F\r\n" % {"driveletter":windowsdriveletter, "filepath":filepath})
    a.write('Copy /Y "%s:%s" "%s\\%s"\r\n' % (windowsdriveletter, filepath, goodfilepath, filepath))
a.write("pause\r\n")
a.close()
print "Success"
