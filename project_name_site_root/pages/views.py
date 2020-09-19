from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Page_Geneal
from . models import Page_Project
from . models import Server
from . models import Sensors_Set
from . models import Home
from . models import Helicopter

# global variables
PRODUCTION = False

# Create your views here.

def index(request, pagename):

    if pagename != '':
        projects(request, pagename)

    pagename = '/' + pagename
    pg = get_object_or_404(Page_Geneal, permalink=pagename)
    context_pages = {
        'title': pg.title,
        'content': pg.bodytext,
        'last_updated': pg.update_date,
        'page_list': Page_Geneal.objects.all(),
        'project_list': Page_Project.objects.all(),          # project also a page, so should be part of the TOC
    }

    # assert False
    # return render(request, 'pages/general/page_toc.html', {'pages': context_pages})
    return render(request, 'pages/np/index.html', {'pages': context_pages})


def projects(request, project_permalink):

    project_permalink = '/' + project_permalink
    project = get_object_or_404(Page_Project, permalink=project_permalink)          

    context_project = {
        'project_name': project.project_name,
        'description': project.description,
        'last_updated': project.update_date,
        'functionality': project.functionality, 
        'limitation': project.limitation,
    }

    server = get_object_or_404(Server, permalink="/my_server")
    sensors = get_object_or_404(Sensors_Set, permalink="/my_sensors")
    home = get_object_or_404(Home, permalink="/my_house")
    helicopter = get_object_or_404(Helicopter, permalink="/my_helicopter")

    sensors.print_status(request)
    home.print_status(request)

    # if PRODUCTION is true, i just want to show the project's htmls, no functionality
    if PRODUCTION is True:
        if project_permalink == '/page_server':
            server.msg_from_server = "The server can be reached only from the local network. It looks like you trying to reach it outside from the local network"
            return render(request, 'pages/projects/server.html', {"project": context_project, "server" : server, "sensors" : sensors})
        elif project_permalink == '/page_house':
            if (request.POST.get('ac_toggle', '') == 'on'):
                home.ac = "on"
            if (request.POST.get('ac_toggle', '') == ''):
                home.ac = ''
            return render(request, 'pages/projects/house.html', {"project": context_project, "home" : home})
        elif project_permalink == '/page_helicopter':
            return render(request, 'pages/projects/helicopter.html', {"project": context_project, "helicopter" : helicopter})


    if project_permalink == '/page_server':                     
        if (request.POST.get('msg_to_server', '') != ''):
            server.msg_to_server = request.POST.get('msg_to_server', '')
            server.send()
        if (request.POST.get('led_1_toggle', '') == 'on'):          # if checked, will return 'on'
            # if sensors.led_1 == False:
            sensors.led_1_on(server)
        elif (request.POST.get('led_1_toggle', '') == ''):          # if unchecked, will return ''
            # if sensors.led_1 == True:
            sensors.led_1_off(server)
        if (request.POST.get('led_2_toggle', '') == 'on'):
            sensors.led_2_on()
        elif (request.POST.get('led_2_toggle', '') == 'off'):
            sensors.led_2_off()
        if (request.POST.get('msg_lcd', '') != ''):
            sensors.send_lcd_msg(request, server)
        if (request.POST.get('msg_ir', '') != ''):
            sensors.send_ir_msg(request)
        if (request.POST.get('get_sonar_reading', '') == 'on'):
            sensors.get_sonar_reading(request, server)
        if (request.POST.get('get_gps_reading', '') == 'on'):
            sensors.get_gps_reading(request)
        if (request.POST.get('get_ir_reading', '') == 'on'):
            sensors.get_ir_reading(request)
        if (request.POST.get('get_gyro_reading', '') == 'on'):
            sensors.get_gyro_reading(request)
        
        return render(request, 'pages/projects/server.html', {"project": context_project, "server" : server, "sensors" : sensors})
        # return render(request, 'pages/np/server.html', {"project": context_project, "server" : server, "sensors" : sensors})

    if project_permalink == '/page_house':
        if (request.POST.get('ac_toggle', '') == 'on'):         # if checked, will return 'on'
            home.ac_on(server)
        if (request.POST.get('ac_toggle', '') == ''):           # if unchecked, will return ''
            home.ac_off(server)
        if (request.POST.get('irobot_toggle', '') == 'on'):
            home.irobot_on()
        elif (request.POST.get('irobot_toggle', '') == ''):
            home.irobot_on()

        return render(request, 'pages/projects/house.html', {"project": context_project, "home" : home})
        # return HttpResponse("<h1>Sorry, this page is not complete yet</h1>")

    
    if project_permalink == '/page_helicopter':
        print(request.POST.get('up', ''))
        print(request.POST.get('down', ''))
        print(request.POST.get('land', ''))
        print(request.POST.get('right', ''))
        print(request.POST.get('left', ''))
        if (request.POST.get('up', '') == 'up'):
            helicopter.up()
        elif (request.POST.get('down', '') == 'down'):
            helicopter.down()
        elif (request.POST.get('land', '') == 'land'):
            helicopter.land()
        elif (request.POST.get('right', '') == 'right'):
            helicopter.right()
        elif (request.POST.get('left', '') == 'left'):
            helicopter.left()

        return render(request, 'pages/projects/helicopter.html', {"project": context_project, "helicopter" : helicopter})
        # return HttpResponse("<h1>Sorry, this page is not complete yet</h1>")
