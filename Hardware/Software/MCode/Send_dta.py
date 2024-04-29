import serial
import pyrebase
import struct

# vis b0,0 // hide component with .objname b0
# vis b0,1 // show component with .objname b0, refresh on front layer
# vis 1,0 // hide component with .id 1

# tsw b0,0 // disable Touch Press/Release events for component b0
# tsw b0,1 // enable Touch Press/Release events for component b0

# baud=9600, bauds=9600, thsp=30 Sets internal No-touch-then-sleep timer to specified value in seconds
# thup=0 (do not wake), thup=1 (wake on touch) Sets if Nextion should auto-wake from sleep when touch press occurs.


class nextScrn():
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

        self.k = struct.pack('B', 0xff)

        data2 = str(120)
        self.ser.write("thsp=".encode())
        self.ser.write(data2.encode())
        self.wbyte()

        data2 = str(1)
        self.ser.write("thup=".encode())
        self.ser.write(data2.encode())
        self.wbyte()

        data2 = str(85)
        self.ser.write("dim=".encode())
        self.ser.write(data2.encode())
        self.wbyte()

    def wbyte(self):
        self.k = struct.pack('B', 0xff)
        self.ser.write(self.k)
        self.ser.write(self.k)
        self.ser.write(self.k)

    def prg_bar(self, data1):
        data1 = int(data1)
        data1 = str(data1)
        self.ser.write("j0.val=".encode())
        self.ser.write(data1.encode())
        self.wbyte()

    def page_home(self):
        self.ser.write("page 1".encode())
        self.wbyte()

    def page_load(self):
        self.ser.write("page 0".encode())
        self.wbyte()

    def set_text(self, data1):
        data2 = '"' + data1 + '"'
        self.ser.write("t1.txt=".encode())
        self.ser.write(data2.encode())
        self.wbyte()

    def reset_txt(self):
        data1 = str('" "')
        self.ser.write("t1.txt=".encode())
        self.ser.write(data1.encode())
        self.wbyte()

    def invis_btn(self):
        self.ser.write("vis b0,0".encode())
        self.wbyte()

    def invis_btn1(self):
        self.ser.write("vis b1,0".encode())
        self.wbyte()

    def vis_btn(self):
        self.ser.write("vis b0,1".encode())
        self.wbyte()

    def vis_btn1(self):
        self.ser.write("vis b1,1".encode())
        self.wbyte()

    def Read(self):
        resp = self.ser.read()
        resp = str(resp)
        input = resp[-3:-1]
        return input

    def reset(self):
        self.ser.write("rest".encode())
        self.wbyte()

    def ref(self):
        self.ser.write("ref b0".encode())
        self.wbyte()
        self.ser.write("ref b1".encode())
        self.wbyte()

    def send_HSp(self, data1, data2):
        data1 = int(data1)
        data2 = int(data2)
        data1 = str(data1)
        data2 = str(data2)
        self.ser.write("heartvaln.val=".encode())
        self.ser.write(data1.encode())
        self.wbyte()
        self.ser.write("spo2valn.val=".encode())
        self.ser.write(data2.encode())
        self.wbyte()
        # pass

    def send_temp(self, data1):
        data1 = int(data1)
        data1 = str(data1)
        self.ser.write("tempvaln.val=".encode())
        self.ser.write(data1.encode())
        self.wbyte()


class FireDB():
    def __init__(self):
        self.config = {
            "apiKey": "6iTC0rIMa8QG4CO6CR0D78fRGxrOKeYGTucgHZJB",
            "authDomain": "api-ear.firebaseapp.com",
            "databaseURL": "https://api-ear-default-rtdb.firebaseio.com/",
            "storageBucket": "api-ear.appspot.com"
        }

        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

    def fire_temp(self, data1, data2):
        ambientString = "{:.2f}".format(data1)
        objectString = "{:.2f}".format(data2)

        ambientCelsius = float(ambientString)
        objectCelsius = float(objectString)

        data = {
            "ambient": ambientCelsius,
            "object": objectCelsius,
        }

        self.db.child("mlx90614").child("1-set").set(data)
        self.db.child("mlx90614").child("2-push").push(data)

    def fire_hrt(self, data1, data2):
        hrtString = "{:.2f}".format(data1)
        spo2String = "{:.2f}".format(data2)

        hrtString = float(hrtString)
        spo2String = float(spo2String)

        data = {
            "Heart rate": hrtString,
            "SPO2": spo2String,
        }

        self.db.child("max30105").child("1-set").set(data)
        self.db.child("max30105").child("2-push").push(data)

    def fire_img(self, iname, imgtyp):
        self.storage.child("Image").child(imgtyp).child(iname).put(iname)
        print("Image sent")

    def fire_vid(self, iname):
        self.storage.child("Video").child(iname).put(iname)
        print("Video sent")

    def fire_snd(self, iname):
        self.storage.child("Sounds").child(iname).put(iname)
        print("Sound MP3 sent")
