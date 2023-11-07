#!/usr/bin/env python3

import rospy
import json
import actionlib
import os
import math
from functools import partial
import time
from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
from colorama import Fore, Back
from std_msgs.msg import Bool

marker_pos = 0
menu_handler = MenuHandler()


#---------Coordinates of house divisions in json file---------------
cord = []

f = open(os.path.join(os.path.dirname(__file__), 'house_coordenates.json'))
data = json.load(f)
for i in range(len(data)):   #Put the information in an internal array cord[]
    cord.append(data[i])
    i=i+1
f.close()

#-------------Atual Pose-------------
def atual_pos(odom_msg):
    global atual_x, atual_y
    atual_x = round(odom_msg.pose.pose.position.x,1)
    atual_y = round(odom_msg.pose.pose.position.y,1)

#------------Goal pose------------
def goal_pose(x,y, orientZ, orientW):
    navclient = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    navclient.wait_for_server()
    
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = orientZ
    goal.target_pose.pose.orientation.w = orientW
    
    navclient.send_goal(goal)
    finished = navclient.wait_for_result()   

#-------------Go House Division-------------
def deepCb(feedback , dest):
    print("Going to " + cord[dest]['Division'] + "...")
    x = float(cord[dest]['x'])
    y = float(cord[dest]['y'])
    orientY = float(cord[dest]['Orient_z'])
    orientW = float(cord[dest]['Orient_w'])
    goal_pose(x,y, orientY, orientW) 
    print(Fore.GREEN + 'Arrived at '+ str(cord[dest]['Division']) + Fore.RESET + '\n')

#-------------XY Position-------------
def inst_coord(feedback):

    print("\n############# XY Pose #############")
    while True:
        x = float(input("x: "))
        if -7.5 <= x <= 2:
            break 
        else:
            print(Fore.RED + "Invalid x coordinate, x=[-7.5, 2]" + Fore.RESET)

    while True:
        y = float(input("y: "))
        if -5 <= y <= 5:
            break 
        else:
            print(Fore.RED + "Invalid y coordinates, y=[-5, 5]" + Fore.RESET)
    goal_pose(x,y, 0, 1)
    print(Fore.GREEN + 'Arrived at destination x =' + str(float(x)) + " y =" + str(float(y)) + Fore.RESET)
    print("###################################\n")
   
#-------------Search mission-------------

#Feedback perception_sphere
def perception_sphere(msg):
    global foundSphere
    foundSphere = msg.data

#Feedback perception_sphere
def perception_person(msg):
    global foundPerson
    foundPerson = msg.data

#Euclidean distance calculation
def distance(coord_div, current_pos):
   return math.sqrt((coord_div["x"]-current_pos[0])**2 + (coord_div["y"]-current_pos[1])**2)

#Sort the array by Euclidean distance
def sort_by_distance(array, AtualPos):
    return sorted(array, key=lambda x: distance(x, AtualPos))

def find(feedback):
    print("###############################")
    print("Search for Sphere...")

    sort_list = cord
    atualPos = start_find_pos = [atual_x, atual_y] #posição de inicio de procura
    while len(sort_list) != 0: 
    
        #É feito sort ao array (da divisão mais perto para a mais longe)
        sort_list = sort_by_distance(sort_list, atualPos)
        dest = sort_list[0]['Division']

        #Vai para a primeira posição do Array (divisão mais perto)
        goal_pose(sort_list[0]['x'],sort_list[0]['y'], sort_list[0]['Orient_z'], sort_list[0]['Orient_w'])
        time.sleep(1)
        if foundSphere == True:
            break
        
        #Atulização do ponto atual
        atualPos = [atual_x, atual_y]
        #Chegada a posição é retirada a divisão ja procurada
        sort_list.pop(0)
    if foundSphere == True:
        print(Fore.GREEN + 'Object found in ' + str(dest) + Fore.RESET)
    else:
        goal_pose(start_find_pos[0],start_find_pos[1], 0, 1)
        print(Fore.RED + 'Object not found!' + Fore.RESET)
    print("###############################\n")


def person_doubleRoom(feedback):
    print("###############################")
    print("Search for people in Double Room...")
    goal_pose(cord[0]['x'],cord[0]['y'], cord[0]['Orient_z'], cord[0]['Orient_w'])
    time.sleep(1)
    if foundPerson == True:
        print(Fore.GREEN + 'Person in Double Room '+ Fore.RESET)
    else:
        print(Fore.RED + 'Person not found!' + Fore.RESET)
    print("###############################\n")

################# MENU #################
#------------Creates a volume for click------------
def makeMarker(msg):
    marker = Marker()
    marker.type = Marker.CUBE
    marker.scale.x = msg.scale * 0.4
    marker.scale.y = msg.scale * 0.4
    marker.scale.z = msg.scale * 0.4
    marker.color.r = 0.5
    marker.color.g = 0.5
    marker.color.b = 0.5
    marker.color.a = 0.1 #Transparency to 0
    return marker

def makeEmptyMarker( dummyBox=True ):
    global marker_pos
    int_marker = InteractiveMarker()
    int_marker.header.frame_id = "base_link"
    int_marker.pose.position.y = -3.0 * marker_pos
    marker_pos += 1
    int_marker.scale = 1
    return int_marker

#------------Interaction with the marker------------
def makeMenuMarker( name ):
    int_marker = makeEmptyMarker()
    int_marker.name = name
    control = InteractiveMarkerControl()
    control.interaction_mode = InteractiveMarkerControl.BUTTON
    control.always_visible = True
    control.markers.append(makeMarker(int_marker))
    int_marker.controls.append(control)
    server.insert( int_marker )

#------------Output Menu------------
def initMenu():
    move_menu = menu_handler.insert("Go to")                                
    for i in range(len(cord)):
        menu_handler.insert(cord[i]['Division'], parent=move_menu, callback=partial(deepCb,dest = i)) 

    menu_handler.insert("XY Pose", callback=inst_coord)

    mission_menu = menu_handler.insert("Mission")                           
    menu_handler.insert("Find ball", parent=mission_menu, callback=find) 
    menu_handler.insert("Check for people in Double room", parent=mission_menu, callback=person_doubleRoom)

########################################

if __name__=="__main__":
    rospy.init_node("menu")
    server = InteractiveMarkerServer("menu")
    initMenu()
    makeMenuMarker( "marker1" )
    menu_handler.apply( server, "marker1" )
    server.applyChanges()

    #Subs the atual position 
    odom_sub = rospy.Subscriber("/odom", Odometry, atual_pos)

    #Subs the perception sphere
    sphere_subscriber = rospy.Subscriber('sphere_info', Bool, perception_sphere)

    #Subs the perception person
    people_subscriber=rospy.Subscriber('people_info', Bool, perception_person)

    print("##########################")
    print("Waiting for user commands")
    print("##########################\n")

    rospy.spin()
    
