import os
import sys
import MCode

sys.stdout.flush()
os.execv(sys.argv[0], sys.argv)

sys.stdout.flush()
os.execl(sys.executable, 'python', __file__, *sys.argv[1:])

while(True):
    MCode.main()
