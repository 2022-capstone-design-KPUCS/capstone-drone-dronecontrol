import math
import numpy
from api_call import get_api
from haversine import haversine

# gps=[(37.3408847,126.7328347), (37.3411523,126.7324290),(37.3416870,126.7329567),(37.3423832,126.7319496)]
gps = get_api()
distance=[]
angle=[]
diff_angle=[]

def cal_distance(s_lat,s_long,g_lat,g_long):
    start=(float(s_lat),float(s_long))
    goal=(float(g_lat),float(g_long))
    return int(haversine(start,goal,unit='m')*100)

def cal_angle(s_lat, s_long, g_lat, g_long):
    Lat1 = math.radians(s_lat)
    Lat2 = math.radians(g_lat)
    Lng1 = math.radians(s_long)
    Lng2 = math.radians(g_long)

    y = math.sin(Lng2-Lng1)*math.cos(Lat2)

    x = math.cos(Lat1)*math.sin(Lat2)-math.sin(Lat1)*math.cos(Lat2)*math.cos(Lng2-Lng1)

    z = math.atan2(y, x)

    a = numpy.rad2deg(z)
    if(a < 0):
        a = 180+(180+a)
    return int(a)

def max_distance(args):
    return(max(args))

def cal_demo_size(demo_size,max_dist,distance):
    data=[]
    ratio=demo_size/max_dist
    for i in distance:
        data.append(int(i*ratio))
    return data



def cal_f_angle():
    diff_angle.append(angle[0])
    for i in range(len(angle)-1):
        diff_angle.append(angle[i+1]-angle[i])
        print(diff_angle)

def command(speed):
    f=open("./command.txt",'w')
    angle_command=[]
    distance_command=[]

    for i in range(0,len(diff_angle)):
        if diff_angle[i] >=0 and diff_angle[i] < 180:
            angle_command.append("cw {}\n".format(diff_angle[i]))
        elif(diff_angle[i]>=180):
            angle_command.append("ccw {}\n".format(360-diff_angle[i]))
        elif (diff_angle[i] < 0 and diff_angle[i] > -180):
            angle_command.append("ccw {}\n".format(-diff_angle[i]))
        elif(diff_angle[i]<= -180):
            angle_command.append("cw {}\n".format(360+diff_angle[i]))

    for i in range(0, len(distance)):
        j=distance[i]//500
        k=distance[i]%500
        section_distance=[]
        for l in range(j):
            section_distance.append("forward 500\n")
        section_distance.append("forward {}\n".format(k))
        distance_command.append(section_distance)

    f.write("command\n")
    f.write("takeoff\n")
    f.write("speed {}\n".format(speed))

    for i in range(len(angle_command)):
        f.write(angle_command[i])

        for j in range(len(distance_command[i])):
            f.write(distance_command[i][j])

    f.write("land\n")

    f.close()

def drone_control():
    f= open('./command.txt', 'r')
    command=f.readlines()
    for i in command:
        if i == "takeoff\n":
            tello.takeoff()

        elif i[:5] =="speed":
            speed=int(i[6:])
            tello.set_speed(speed)
        elif i[:3] =="ccw":
            angle=int(i[4:])
            tello.rotate_counter_clockwise(angle)

        elif i[:2] =="cw":
            angle=int(i[3:])
            tello.rotate_clockwise(angle)

        elif i[:7] == "forward":
            distance=int(i[8:])
            tello.move_forward(distance)

        elif i == "land\n":
            tello.land()





if __name__=="__main__":
    for i in range(len(gps)-1):
        distance.append(cal_distance(gps[i][0], gps[i][1], gps[i+1][0], gps[i+1][1]))
        angle.append(cal_angle(gps[i][0], gps[i][1], gps[i+1][0], gps[i+1][1]))

    print(distance)
    maxDistance=max_distance(distance)
    distance=cal_demo_size(300,maxDistance,distance)
    cal_f_angle()
    command(20)



