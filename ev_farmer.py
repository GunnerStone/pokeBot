from pokeAPI import *
import time
from threading import Thread
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
import sys
import os
import random


driver = pokeAPI().register_window(name="PokeММO")
wx, wy = driver.get_window_rect()[:2]

ROUND_COUNT = 0
print = print_formatted_text
style = Style.from_dict({
        'msg': '#71f076 bold',
        'sub-msg': '#616161 italic'
    })

def display_metrics():
        while(True):
            global ROUND_COUNT
            driver.clear_console()
            #Current dungeon run number
            str_buffer = str(ROUND_COUNT)
            print(HTML(
                u'<b>></b> <ansicyan><u>Current Dungeon Run</u></ansicyan>'+"<b> : </b>"+'<i><ansigrey>'+str_buffer+'</ansigrey></i>'
            ), style=style)

            time.sleep(1)

def navigate_to_low_level_grass():
    driver.hold_key('left',0.6)
    driver.hold_key('up',1.3)
    driver.hold_key('right',1.7)
    driver.hold_key('up',0.50)
    driver.hold_key('right',.5)
    driver.hold_key('up',2.4)
    
def navigate_to_speed_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="lacunosa")
    print("Navigating to Rapidash Grass Patches")
    driver.press_key('down')
    #get on bike
    driver.toggle_bike()
    driver.hold_key('left',random.uniform(3, 3.3))
    driver.toggle_bike()
    driver.press_key('up')
    driver.press_key('up')
    driver.press_key('up')

def navigate_to_hp_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="opelucid")
    print("Navigating to Buffoulant Grass Patches")
    #get on bike
    driver.toggle_bike()
    driver.hold_key('left',1.4)
    driver.hold_key('up',2.15)
    driver.hold_key('right',1.90)
    driver.hold_key('up',6.5)
    driver.hold_key('right',2.7)
    driver.toggle_bike()
    driver.hold_key('up',.15)
    driver.toggle_bike()
    driver.hold_key('right',1.8)
    driver.toggle_bike()
    driver.hold_key('up',.3)


def navigate_to_attack_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="opelucid")
    print("Navigating to Buffoulant Grass Patches")
    #get on bike
    driver.toggle_bike()
    driver.hold_key('left',1.4)
    driver.hold_key('up',2.15)
    driver.hold_key('right',1.90)
    driver.hold_key('up',5.5)
    driver.hold_key('right',random.uniform(.1,.2))
    driver.toggle_bike()
    driver.hold_key('up',.2)

def navigate_to_spattack_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="opelucid")
    print("Navigating to Duosion Grass Patches")
    driver.hold_key('down',.05)
    #get on bike
    driver.toggle_bike()
    driver.hold_key('left',6.8)
    time.sleep(1.5)
    driver.hold_key('left',random.uniform(.25,.4))
    driver.hold_key('down',.2)
    driver.toggle_bike()
    driver.press_key('down')

def navigate_to_spdef_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="undella")
    print("Navigating to Mantine Surf Patches")
    driver.hold_key('left',.9)
    driver.hold_key('down',1.8)
    driver.surf()

def navigate_to_def_ev():
    print("Going to pokecenter")
    driver.use_pokecenter(location="undella")
    print("Navigating to Mantine Surf Patches")
    driver.hold_key('left',.9)
    driver.hold_key('down',.8)
    driver.toggle_bike()
    driver.hold_key('right',2.5)
    driver.toggle_bike()
    driver.surf()

def navigate_to_luvdisc():
    print("Going to pokecenter")
    driver.use_pokecenter(location="undella")
    print("Navigating to luvdisc Patch")
    driver.hold_key('left',.9)
    driver.hold_key('down',.8)
    driver.toggle_bike()
    driver.hold_key('right',random.uniform(.5,1.5))
    driver.press_key('down')

def farm_heartscales(hotkey='4'):
    navigate_to_luvdisc()
    #sweet scent can be used 6 times before needing to go to pokecenter
    currentPP = 10
    print("Starting farm loop")
    while(currentPP>0):
        print("Looking for battle")
        while((not driver.is_in_battle()) and (not driver.is_in_horde())):
            driver.fish(hotkey=hotkey)
        print("Battle Found")
        in_battle = True
        #wait for battle options to pop up
        if (driver.is_in_horde()):
            print("Scanning for Horde Shinies")
            if(driver.is_shiny_horde() == False):
                print("Shiny not found")
                print("Using AOE attack")
                driver.flee_from_battle()
                print("Fleeing from horde battle")
                time.sleep(random.uniform(12,15))
                in_battle = False
            else:
                print("Shiny found!!!")
                print("Stalling until human services game")
                while True:
                    time.sleep(60)
        else:
            while(in_battle):
                print("Scanning for Single-Battle Shinies")
                if(driver.is_shiny_single()==False):
                    print("Shiny not found")
                    print("Using first attack")
                    driver.use_first_attack()
                    print("Attack animations & battle close")
                    time.sleep(random.uniform(12,15))
                    #if battle is over set loop flag to false
                    if(not driver.is_in_battle()):
                        print("Enemy pokemon was defeated")
                        in_battle = False
                else:
                    print("Shiny found!!!")
                    print("Stalling until human services game")
                    while True:
                        time.sleep(random.uniform(60, 300))
                        driver.stall_battle()
        currentPP -= 1
    

def farm_evs(ev_type = "def"):
    #Start bot underneath poke-center exit facing down
    
    
    if(ev_type=="attack"):
        navigate_to_attack_ev()
    elif(ev_type=="spattack"):
        navigate_to_spattack_ev()
    elif(ev_type=="speed"):
        navigate_to_speed_ev()
    elif(ev_type=="spdef"):
        navigate_to_spdef_ev()
    elif(ev_type=="def"):
        navigate_to_def_ev()
    elif(ev_type=="hp"):
        navigate_to_hp_ev()
    #sweet scent can be used 6 times before needing to go to pokecenter
    currentPP = 6
    print("Starting farm loop")
    while(currentPP>0):
        print("Looking for battle")
        while((not driver.is_in_battle()) and (not driver.is_in_horde())):
            driver.sweet_scent()
        print("Battle Found")
        in_battle = True
        #wait for battle options to pop up
        if (driver.is_in_horde()):
            print("Scanning for Horde Shinies")
            if(driver.is_shiny_horde() == False):
                print("Shiny not found")
                print("Using AOE attack")
                driver.use_first_attack(is_horde=True)
                print("Attack animations & battle close")
                time.sleep(12)
                in_battle = False
            else:
                print("Shiny found!!!")
                print("Stalling until human services game")
                while True:
                    time.sleep(60)
        else:
            while(in_battle):
                print("Scanning for Single-Battle Shinies")
                if(driver.is_shiny_single()==False):
                    print("Shiny not found")
                    print("Using AOE attack")
                    driver.flee_from_battle()
                    print("Attack animations & battle close")
                    time.sleep(12)
                    #if battle is over set loop flag to false
                    if(not driver.is_in_battle()):
                        print("Enemy pokemon was defeated")
                        in_battle = False
                else:
                    print("Shiny found!!!")
                    print("Stalling until human services game")
                    while True:
                        time.sleep(random.uniform(60, 300))
                        driver.stall_battle()
        
        print("Holding z through any prompts")
        driver.hold_key('z',3)
        currentPP -= 1
    



metric_thread = Thread(target=display_metrics,args=())

try:
    #metric_thread.start()
    while True:
        farm_evs("spdef")
        #farm_heartscales()
        ROUND_COUNT += 1
except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)