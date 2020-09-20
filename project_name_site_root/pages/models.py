from django.db import models
import socket
import time

PASSWORD_ESP = 'abc'
PWD_ESP = 'abc'

# Create your models here.

class Page_Geneal(models.Model):
    title = models.CharField(max_length=60)
    permalink = models.CharField(max_length=12, unique=True)    # permalink for an individual page
    update_date = models.DateTimeField('Last Updated')
    bodytext = models.TextField('Page Content', blank=True)

    def __str__(self):
        return self.title


class Page_Project(models.Model):
    project_name = models.CharField(max_length=64, unique=True)
    permalink = models.CharField(max_length=32, unique=True)        # permalink for an individual page
    description = models.TextField(blank=True)                      # ? - change it to models.TextField('project description', blank=True)
    update_date = models.DateTimeField('Last Updated')
    functionality = models.TextField(blank=True)               # todo: consider change it to a list field
    limitation = models.TextField(blank=True)
    # functionality = models.CharField(max_length=1023)               # todo: consider change it to a list field
    # functionality = models.ManyToManyField(Function)               # todo: consider change it to a list field
    # components = models.CharField(max_length=1023)


class Server(models.Model):
    server_name = models.CharField(max_length=64, unique=True)
    permalink = models.CharField(max_length=32, unique=True)        # permalink for an individual page
    update_date = models.DateTimeField('Last Updated')

    msg_to_server = models.CharField(max_length=9600, null=True, blank=True)
    # msg_from_server = models.CharField(max_length=9600, null=True, blank=True)
    # msg_from_server = models.CharField(max_length=9600, blank=True)
    msg_from_server = models.CharField(max_length=9600, blank=True)

    
    # todo: configure after the check
    def send(self):
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ////////////////// connections
        # coursera
        # mysock.connect( ("data.pr4e.org", 80) )

        # if local - so i want to connect directly to the ip and port of esp
        # mysock.connect( ("192.168.43.240", 1025) )

        # if not local (dynamic) - so i want to connect to the dynamic ip which i discovered "using what is my ip", and i will defin that it will be port 1025 in my hot spot. but it does not must be also 1025 
        # mysock.connect( ("188.64.207.172", 1025) )

        # if i am using ngrok service (even if we configured port 301 in the esp, we will connect to the port we got from ngrok, where 80 is the default):
        # mysock.connect( ("bea8dae8846a.ngrok.io", 80))

        # if i am using trmote.it service and got from them the address to esp, which will be accessible from the internet
        remoteit_addr = 'proxy72.rt3.io'
        # remoteit_addr.lstrip('http://')
        remoteit_port = 31217
        mysock.connect( (remoteit_addr, remoteit_port) )   


        # ////////////////// commands
        # coursera
        # cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()

        # local network - the ip is the local esp ip
        # cmd = ('POST 192.168.43.240 HTTP/1.1 \r\n' +  'password: ' + PASSWORD_ESP + '\n' + self.msg_to_server + '\n' + 'end' + '\r\n\r\n').encode()
        
        # if not local network - the address we got from ngrok service
        # cmd = ('POST bea8dae8846a.ngrok.io HTTP/1.1 \r\n' +  'password: ' + PASSWORD_ESP + '\n' + self.msg_to_server + '\n' + 'end' + '\r\n\r\n').encode()

        # if not local network - the address we got from remote.it service
        # cmd = ('POST proxy71.rt3.io HTTP/1.1 \r\n' +  'password: ' + PASSWORD_ESP + '\n' + self.msg_to_server + '\n' + 'end' + '\r\n\r\n').encode()

        # if not local network - the address we got from remote.it service (no password)
        cmd = ('POST ' +  remoteit_addr + ' HTTP/1.1 \r\n' +  'p: ' + PWD_ESP + '\n' + self.msg_to_server + '\n' + 'end' + '\r\n\r\n').encode()
        
    # ////////////////// sending commands

        mysock.send(cmd)
        # mysock.send('Hello'.encode())

    # ////////////////// getting data


        # ack to the sent message
        self.msg_from_server = ""       # init
        
        """
        while True:
            frame = mysock.recv(9600)
            if len(frame) < 1:
                break
            # print("msg from the server: " + ' ' + str(frame.decode()), end='')
            # print("msg from the server: " + ' ' + str(frame.decode()), end='')
            self.msg_from_server = str(self.msg_from_server) + '\n' + str(frame.decode())
            # self.msg_from_server = str(self.msg_from_server)            
        print("msg from the server: " + self.msg_from_server)
        """


        try:
            while True:
                frame = mysock.recv(9600)
                if len(frame) < 1:
                    break
                # print("msg from the server: " + ' ' + str(frame.decode()), end='')
                # print("msg from the server: " + ' ' + str(frame.decode()), end='')
                self.msg_from_server = str(self.msg_from_server) + '\n' + str(frame.decode())
                # self.msg_from_server = str(self.msg_from_server)            
            print("msg from the server: " + self.msg_from_server)
        except:
            self.msg_from_server = "The server's public ip is timed out. Ask the owner to allocate a new public ip"
            print("msg from the server: " + self.msg_from_server)


class Sensors_Set(models.Model):
    sensors_name = models.CharField(max_length=64, unique=True)
    permalink = models.CharField(max_length=32, unique=True)        # permalink for an individual page
    update_date = models.DateTimeField('Last Updated')

    led_1 = models.BooleanField(default=False)
    led_2 = models.BooleanField(default=False)
    lcd_msg = models.CharField(max_length=64, null=True, blank=True)
    sonar_reading = models.FloatField(max_length=64, null=True, blank=True)
    gps_reading = models.FloatField(max_length=64, null=True, blank=True)
    ir_reading = models.FloatField(max_length=64, null=True, blank=True)
    gyro_reading = models.FloatField(max_length=64, null=True, blank=True)

    def print_status(self, request):
        print(request.POST.get('led_1_toggle', ''))
        print(request.POST.get('led_2_toggle', ''))
        print(request.POST.get('sonar_reading', ''))
        print(request.POST.get('gps_reading', ''))
        print(request.POST.get('ir_reading', ''))
        print(request.POST.get('gyro_reading', ''))
        print(request.POST.get('msg_lcd', ''))
        print(request.POST.get('msg_ir', ''))

    def led_1_toggle(self):
        self.led_1 = not self.led_1
        

    def led_1_on(self, server):
        #  this code should be simpified 
        tmp = server.msg_from_server
        self.led_1 = True
        server.msg_to_server = "led -cmd on"
        server.send()
        server.msg_from_server = tmp                   # init the server's text box back to what it was

    def led_1_off(self, server):
        #  this code should be simpified 
        tmp = server.msg_from_server
        self.led_1 = False
        server.msg_to_server = "led -cmd off"
        server.send()
        server.msg_from_server = tmp                   # init the server's text box back to what it was

    def led_2_toggle(self):
        self.led_2 = not self.led_2

    def led_2_on(self):
        self.led_2 = True

    def led_2_off(self):
        self.led_2 = False
    
    def send_lcd_msg(self, request, server):
        # print("TODO: send new message to LCD: " + request.POST.get('msg_lcd', ''))
        server.msg_to_server = "lcd -display " + request.POST.get('msg_lcd', '')
        server.send()

    def send_ir_msg(self, request):
        print("TODO: send new message to IR: " + request.POST.get('msg_ir', ''))

    def get_sonar_reading(self, request, server):
        print("TODO: get new message from sonar: " + request.POST.get('get_sonar_reading', ''))
        if (request.POST.get('get_sonar_reading', '') == 'on'):
            server.msg_to_server = "sonar"
            server.send()
            self.sonar_reading = server.msg_from_server
        # self.sonar_reading = request.POST.get('get_sonar_reading', '')

    def get_gps_reading(self, request):
        print("TODO: send new message from GPS: " + request.POST.get('get_gps_reading', ''))

    def get_ir_reading(self, request):
        print("TODO: send new message from IR: " + request.POST.get('get_ir_reading', ''))

    def get_gyro_reading(self, request):
        print("TODO: send new message from gyro: " + request.POST.get('get_gyro_reading', ''))


class Home(models.Model):
    home_name = models.CharField(max_length=64, unique=True)
    permalink = models.CharField(max_length=32, unique=True)        
    update_date = models.DateTimeField('Last Updated')

    ac = models.BooleanField(default=False)
    irobot = models.BooleanField(default=False)

    def print_status(self, request):
        print(request.POST.get('ac_toggle', ''))
        print(request.POST.get('irobot_toggle', ''))

    def ac_on(self, server):
        self.ac = True
        server.msg_to_server = "ac -cmd on"
        server.send()

    def ac_off(self, server):
        self.ac = False
        server.msg_to_server = "ac -cmd off"
        server.send()

    def ac_toggle(self):
        self.ac = not self.ac

    def irobot_on(self):
        self.irobot = True

    def irobot_off(self):
        self.irobot = False
    
    def irobot_toggle(self):
        self.irobot = not self.irobot
    

class Helicopter(models.Model):
    helicopter_name = models.CharField(max_length=64, unique=True)
    permalink = models.CharField(max_length=32, unique=True)        
    update_date = models.DateTimeField('Last Updated')

    # throttle = models.PositiveIntegerField(default=0)
    # direction = models.IntegerField(default=0)

    # def print_status(self, request):
    #     print(request.POST.get('ac_toggle', ''))
    #     print(request.POST.get('irobot_toggle', ''))


    def up(self):
        # self.throttle = self.throttle + 10
        print("sending up command")

    def down(self):
        # self.throttle = self.throttle - 10
        print("sending down command")

    def land(self):
        # while (self.throttle):
            # self.throttle = self.throttle - 1
            # time.sleep(0.1)
        print("sending land command")

    def right(self):
        # self.direction = self.direction + 10
        print("sending right command")

    def left(self):
        # self.direction = self.direction - 10
        print("sending left command")
