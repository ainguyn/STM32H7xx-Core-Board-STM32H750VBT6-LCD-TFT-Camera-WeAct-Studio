# Untitled - By: Weact - 7 8 2020
red_threshold = (53, 31, 44, 82, 18, 78)
green_threshold = (54, 90, -64, -30, -19, 108)
blue_threshold = (34, 65, 22, 60, -100, -29)
area = (0, 0, 320, 240)
import sensor, image, time, lcd

clock = time.clock()

sensor.reset()
if sensor.get_id() == sensor.OV7725:
    sensor.set_hmirror(True)
    sensor.set_vflip(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
# Close the white balance.White Balance is turned on by default. In color recognition, white balance needs to be turned off
clock = time.clock()

# search max blob
def search_max(blobs):
    max_blob = 0
    max_size = 0
    for blob in blobs:
        blob_area = blob[2] * blob[3]
        if blob_area > max_size:
            max_blob = blob
            max_size = blob_area
    return max_blob


# Find the largest circle position in the frame
def search_max_circle(ball_threshold, area):
    clock.tick()  # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()  # Take a picture and return the image.
    blobs = img.find_blobs([ball_threshold], roi=area)
    print(blobs)
    if blobs:
        max_blob = search_max(blobs)
        x = max_blob[0] - 3
        y = max_blob[1] - 3
        w = max_blob[2] + 6
        h = max_blob[3] + 6
        outside_rect = (x, y, w, h)
        print(max_blob)
        print("fps:", clock.fps())
        img.draw_rectangle(max_blob[0:4])  # rect
        img.draw_rectangle(outside_rect[0:4])  # rect
        img.draw_cross(max_blob[5], max_blob[6]) # cx,cy
        return max_blob


# Follow the largest circle
def track_max_circle(red_threshold, green_threshold, blue_threshold, area1):
    global area
    track = search_max_circle(red_threshold, area1)
    if track:
        x = track[0] - 5 if track[0] - 5 > 0 else 0
        y = track[1] - 5 if track[1] - 5 > 0 else 0
        w = track[2] + 10
        h = track[3] + 10
        area = (x, y, w, h)
        print('area=', area)
    else:
        track1 = search_max_circle(green_threshold, area1)
        if track1:
            x = track1[0] - 5 if track1[0] - 5 > 0 else 0
            y = track1[1] - 5 if track1[1] - 5 > 0 else 0
            w = track1[2] + 10
            h = track1[3] + 10
            area = (x, y, w, h)
            print('area=', area)
        else:
            print('out of range')
            area = (0, 0, 320, 240)


while(True):
    track_max_circle(red_threshold, green_threshold, blue_threshold, area)



'''def track_max_circle(red_threshold, green_threshold, blue_threshold, area1):
    global area
    track = search_max_circle(green_threshold, area1)
    if track:
        x = track[0] - 5 if track[0] - 5 > 0 else 0
        y = track[1] - 5 if track[1] - 5 > 0 else 0
        w = track[2] + 10
        h = track[3] + 10
        area = (x, y, w, h)
        print('area=', area)
    else:
        print('out of range')
        area = (0, 0, 320, 240)

while(True):
    track_max_circle(red_threshold, green_threshold, blue_threshold, area)

# Follow the largest circle
def track_max_circle(red_threshold, area1):
    global area
    track = search_max_circle(red_threshold, area1)
    if track:
        x = track[0] - 5 if track[0] - 5 > 0 else 0
        y = track[1] - 5 if track[1] - 5 > 0 else 0
        w = track[2] + 10
        h = track[3] + 10
        area = (x, y, w, h)
        print('area=', area)
        if track[2] * track[3] > 2500:      # restricted area
            return True
        else:
            return False
    else:
        print('out of range')
        area = (0, 0, 320, 240)
        return Falsewhile(True)

threshold_count = 1
def circle_rec(flag):
    global threshold_count
    global area
    while flag[0]:
        count = 0
        # choose threshold
        if threshold_count == 1:    # red
            threshold_temp = red_threshold
        elif threshold_count == 2:   # green
            threshold_temp = green_threshold
        elif threshold_count == 3:   # blue
            threshold_temp = blue_threshold
        #rec circle
        for i in range(40):
            if track_max_circle(threshold_temp, area):
                count += 1
            if count >= 20:
                flag[0] = False
                area = (0, 0, 320, 240)
                break
        if flag[0]:         # flag is true
            if threshold_count == 3:    # three threshold had rec
                threshold_count = 1
                flag[0] = False
                return False
            else:
                threshold_count += 1
        else:
            temp = threshold_count
            threshold_count = 1
            return temp
circle_flag[0] = True
'''
