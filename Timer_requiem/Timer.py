import obspython as obs
from datetime import timedelta
import playmedia as pm
import os
#Other Files
import Twitch_add as twitch
import Hotkeys  


#Functions for all the buttons
class Buttons:
    pause = True
    timerActive = False
    noSong = False
    def start_pressed(props, prop):
        current_scene = obs.obs_frontend_get_current_scene()
        scene = obs.obs_scene_from_source(current_scene)
        scene_item = obs.obs_scene_find_source(scene, Timer.sourceName)        
        if (b.pause == False):
            b.timerActive = False
            obs.timer_remove(Timer.timer_start)
            #print("Stop")
            b.pause = True

            #Turn off colour filter
            obs.timer_remove(setup.alert_flash)
            Timer.colourAlertCalled = False
            setup.colourChange = True
            setup.alert_flash()

            #Stop playing music
            setup.p.stop()
            setup.played = False
                

            #Set back to orignal size and position
            obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
            obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)

        else:
            b.timerActive = True
            #Get The position of the Timer before it starts
            Timer.originalPosition = setup.get_source_position(scene_item)

            #Get the scale of the Timer before it starts
            Timer.originalScale =  setup.get_source_scale(scene_item)            

            obs.timer_add(Timer.timer_start, 1000)
            #print("Start")
            b.pause = False
        obs.obs_scene_release(scene)
        return

    def reset_pressed(props, prop):
        b.timerActive = False
        obs.timer_remove(Timer.timer_start)
        Timer.currentTime = Timer.setTime

        #Set Timer back to original value
        clock = timedelta(seconds = Timer.currentTime)
        source = obs.obs_get_source_by_name(Timer.sourceName)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", str(clock))
        obs.obs_source_update(source, settings)
        b.pause = True
        #Release
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

        #Turn off colour filter
        obs.timer_remove(setup.alert_flash)
        Timer.colourAlertCalled = False
        setup.colourChange = True
        setup.alert_flash()

        #Stop playing music
        setup.p.stop()
        setup.played = False

        #Set back to orignal size and position
        current_scene = obs.obs_frontend_get_current_scene()
        scene = obs.obs_scene_from_source(current_scene)
        scene_item = obs.obs_scene_find_source(scene, Timer.sourceName)        
        obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
        obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)
        obs.obs_scene_release(scene)

    def add_pressed(props, prop):
        Timer.currentTime = Timer.currentTime + Timer.addTime

#Copy of control buttons to be used with hotkeys (problem with "(props, prop)" in original functions as they would need to be stated and I don't know how to do so).
class Button_Hotkeys:
    def start_hotkey(pressed):
        if pressed:
            current_scene = obs.obs_frontend_get_current_scene()
            scene = obs.obs_scene_from_source(current_scene)
            scene_item = obs.obs_scene_find_source(scene, Timer.sourceName)        
            if (b.pause == False):
                b.timerActive = False
                obs.timer_remove(Timer.timer_start)
                print("Stop")
                b.pause = True

                #Turn off colour filter
                obs.timer_remove(setup.alert_flash)
                Timer.colourAlertCalled = False
                setup.colourChange = True
                setup.alert_flash()

                #Stop playing music
                setup.p.stop()
                setup.played = False

                #Set back to orignal size and position
                obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
                obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)
            else:
                b.timerActive = True
                #Get The position of the Timer before it starts
                Timer.originalPosition = setup.get_source_position(scene_item)

                #Get the scale of the Timer before it starts
                Timer.originalScale =  setup.get_source_scale(scene_item)            

                obs.timer_add(Timer.timer_start, 1000)
                print("Start")
                b.pause = False
            obs.obs_scene_release(scene)
            return

    def reset_hotkey(pressed):
        if pressed:
            b.timerActive = False
            obs.timer_remove(Timer.timer_start)
            Timer.currentTime = Timer.setTime

            #Set Timer back to original value
            clock = timedelta(seconds = Timer.currentTime)
            source = obs.obs_get_source_by_name(Timer.sourceName)
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", str(clock))
            obs.obs_source_update(source, settings)
            b.pause = True
            #Release
            obs.obs_data_release(settings)
            obs.obs_source_release(source)

            #Turn off colour filter
            obs.timer_remove(setup.alert_flash)
            Timer.colourAlertCalled = False
            setup.colourChange = True
            setup.alert_flash()

            #Stop playing music
            setup.p.stop()
            setup.played = False

            #Set back to orignal size and position
            current_scene = obs.obs_frontend_get_current_scene()
            scene = obs.obs_scene_from_source(current_scene)
            scene_item = obs.obs_scene_find_source(scene, Timer.sourceName)        
            obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
            obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)
            obs.obs_scene_release(scene)

    def add_hotkey(pressed):
        if pressed:
            Timer.currentTime = Timer.currentTime + Timer.addTime

b = Buttons
bh = Button_Hotkeys
h1 = Hotkeys.h()
h2 = Hotkeys.h()
h3 = Hotkeys.h()

def script_description():
    return """<h1>Countdown Timer:</h1> 
    Choose the duration of the countdown and select a source to act as a timer. \n
    <h5>Click the Start box to begin the timer and Reveal more buttons</h5>"""

#Runs when the script is initiated 
def script_load(settings):
    h1.htkCopy = Hotkeys.Hotkey(bh.start_hotkey, settings, "Start/Stop")
    h2.htkCopy = Hotkeys.Hotkey(bh.reset_hotkey, settings, "Reset")
    h3.htkCopy = Hotkeys.Hotkey(bh.add_hotkey, settings, "Add")

    obs.obs_data_set_default_bool(settings, "hideBool", False)
    obs.obs_data_set_bool(settings, "hideBool", False)    


def script_save(settings):
    h1.htkCopy.save_hotkey()
    h2.htkCopy.save_hotkey()
    h3.htkCopy.save_hotkey()

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "time", "Duration (seconds)", 1, 100000, 60)

    pList = obs.obs_properties_add_list(props, "source", "Select source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    #Find the list of text Sources
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if (source_id == "text_gdiplus" or source_id == "text_ft2_source"):
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(pList, name, name)
        obs.source_list_release(sources)

    obs.obs_properties_add_path(props, "filePath", "Select mp3 file", obs.OBS_PATH_FILE, "*.mp3*", 'c:/')
    obs.obs_properties_add_bool(props, "alertBool", "Alert")

    hide = obs.obs_properties_add_bool(props, "hideBool", "Start")
    obs.obs_property_set_modified_callback(hide, setup.check_input_use)
    obs.obs_property_set_long_description(hide, "Clicking Settings Will Reset the Timer")

    obs.obs_properties_add_button(props, "startButton", "Start/Stop", Buttons.start_pressed)
    obs.obs_properties_add_button(props, "resetButton", "Reset", Buttons.reset_pressed)
    
    obs.obs_properties_add_button(props, "addButton", "Add", Buttons.add_pressed)
    obs.obs_properties_add_int_slider(props, "slider", "Add Time (minutes)", 1, 20, 2)

    # Hide all the buttons when the script is intialised so that only the setting inputs are visible
    setup.initialise_properties(props)

    return props

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "time", 300)
    obs.obs_data_set_default_int(settings, "slider", 5)
    obs.obs_data_set_default_string(settings, "filePath", setup.default_song())
    obs.obs_data_set_default_bool(settings, "hideBool", False)

def script_update(settings):
    if (b.timerActive == False):
        Timer.currentTime = obs.obs_data_get_int(settings, "time")
        Timer.setTime = Timer.currentTime
        Timer.sourceName = obs.obs_data_get_string(settings, "source")
        song = obs.obs_data_get_string(settings, "filePath")
        if song:            
            setup.p = pm.File(song)
        else:
            setup.p = pm.File(song)

    Timer.addTime = (obs.obs_data_get_int(settings, "slider") * 60)
    Timer.alertBool = obs.obs_data_get_bool(settings, "alertBool")
    if (Timer.alertBool == True):
        setup.create_filter(settings)

    setup.useFile = obs.obs_data_get_bool(settings, "hideBool")
    #Check for song
    try:
        setup.p.stop()
    except:
        Buttons.noSong = False
        #pass
    else:
        setup.p.stop()
        setup.played = False
        Buttons.noSong = True

class Timer:
    currentTime = 0
    setTime = 0
    addTime = 300
    sourceName = ""
    finish = f"{0:01d}:{0:02d}:{0:02d}"
    colourAlertCalled = False
    vec = obs.vec2()
    originalPosition = vec
    originalScale = vec
    originalScale.x = 1
    originalScale.y = 1
    alertBool = False
    restart = False


    def timer_start():
        #Calculates the time left in the format hh:mm:ss from seconds (currentTime)
        clock = timedelta(seconds = Timer.currentTime)
        print(clock)

        #Main Timer statements 
        source = obs.obs_get_source_by_name(Timer.sourceName)
        settings = obs.obs_data_create()
        if (Timer.currentTime > 0):
            obs.obs_data_set_string(settings, "text", str(clock))            
            Timer.currentTime = Timer.currentTime - 1            
        else:
            #Restart the Timer once finished
            #Set default text for when the timer is finish
            obs.obs_data_set_string(settings, "text", Timer.finish)
            obs.timer_remove(Timer.timer_start)
            b.pause = True
            Timer.restart = True
        obs.obs_source_update(source, settings)
        #Release
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

        Timer.currentTime = twitch.twitch_add(Timer.currentTime, Timer.addTime)
        if (Timer.alertBool == True):
            Timer.play_song()
            Timer.colour_alert()
            Timer.alert_move()

        if (Timer.restart == True):
            Timer.currentTime = Timer.setTime
            Timer.restart = False
            

    
    #Check if the timer is below 60s then play or stop the song depending on the duration
    def play_song():
        if (Timer.currentTime < 60 and setup.played == False and Timer.currentTime > 0):
            setup.play_media()
            setup.played = True
        elif (Timer.currentTime > 60 and setup.played == True):
            setup.play_media()
            setup.played = False
        elif (Timer.currentTime == 0):
            setup.p.stop()
            setup.played = False

    def colour_alert():
        # When the timer is below 60 seconds set the function "alert_flash" on a timer 
        # half the speed of the timer.
        if (60 > Timer.currentTime > 0):
            if (Timer.colourAlertCalled == False):
                obs.timer_add(setup.alert_flash, 500)
                Timer.colourAlertCalled = True
        # Stop alert and turn the filter off.
        elif (Timer.colourAlertCalled == True):
            obs.timer_remove(setup.alert_flash)
            Timer.colourAlertCalled = False
            setup.colourChange = True
            setup.alert_flash()

    def alert_move():
        #Set up to change the postion and scale of source
        pos = obs.vec2()
        new_location = pos
        scale = obs.vec2()
        new_scale = scale

        #Get the Timer text source in the active scene
        current_scene = obs.obs_frontend_get_current_scene()
        scene = obs.obs_scene_from_source(current_scene)
        scene_item = obs.obs_scene_find_source(scene, Timer.sourceName)

        if (Timer.currentTime < 60):
            dx, dy = 384, 342      #Middle of screen
            #change positional values of scene item
            new_location.x = dx
            new_location.y = dy            
            
            #change scale values of scene item (multiplier of default value)
            new_scale.x = 1.5
            new_scale.y = 1.5

            #Set the Timer to the new postion and scale
            if (54 < Timer.currentTime < 59):                
                obs.obs_sceneitem_set_scale(scene_item, new_scale)
                obs.obs_sceneitem_set_pos(scene_item, new_location)   
            #Set the Timer back to its orginal postion and scale
            elif (Timer.currentTime < 54):                
                obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
                obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)   
        #Set the Timer back to its orginal postion and scale
        elif (Timer.currentTime > 60):            
            obs.obs_sceneitem_set_scale(scene_item, Timer.originalScale)
            obs.obs_sceneitem_set_pos(scene_item, Timer.originalPosition)
        obs.obs_scene_release(scene)         

class Timer_Setup:
    played = False
    p = ''
    colourChange = False
    useFile = True

    #When called turns the alert song on or off depending on the bool "played".
    def play_media():
        if (setup.played == False):
            setup.p.start()
        elif (setup.played == True):
            setup.p.stop()
    
    # When called turns the filter on or off depending on the bool "colourChange".
    def alert_flash():
        source = obs.obs_get_source_by_name(Timer.sourceName)
        source_filter = obs.obs_source_get_filter_by_name(source, "Red")
        
        if (setup.colourChange == False):
            obs.obs_source_set_enabled(source_filter, True)
            setup.colourChange = True
        else:
            obs.obs_source_set_enabled(source_filter, False)
            setup.colourChange = False

        obs.obs_source_release(source)
    
    # Creates a variable of type 'struct vec2 const *' for the position and scale 
    # respectively so that a sources current state is saved before being changed by 
    # the alert functions.
    def get_source_position(scene_item):
        pos = obs.vec2()
        obs.obs_sceneitem_get_pos(scene_item, pos)
        return pos
    def get_source_scale(scene_item):
        scale = obs.vec2()
        obs.obs_sceneitem_get_scale(scene_item, scale)
        return scale

    def create_filter(settings):
        # Find Filter
        source = obs.obs_get_source_by_name(Timer.sourceName)
        source_filter = obs.obs_source_get_filter_by_name(source, "Red")
        check = obs.obs_source_get_type(source_filter)

        # Checks if the source "Timer2" has a filter called "Red" and if not creates it
        if (check != obs.OBS_SOURCE_TYPE_FILTER):
            # Create Filter
            obs.obs_data_set_int(settings, "color", 255)
            source_colour = obs.obs_source_create_private("color_filter", "Red", settings)            
            obs.obs_source_filter_add(source, source_colour)

            # Turn the filter off
            source_filter = obs.obs_source_get_filter_by_name(source, "Red")
            obs.obs_source_set_enabled(source_filter, False)

            print("Filter 'Red' Created or No Source Selected")
        obs.obs_source_release(source)

    # Makes sure relevant inputs are selected before displaying the control buttons
    def check_input_use(props, prop, settings):
        if (Buttons.noSong == False or Timer.alertBool == False or (Buttons.noSong == True and Timer.alertBool == True)):
            setup.all_properties(props)           

            # Stop the timer when going back to settings
            b.start_pressed(props,prop)
            if (b.timerActive == True):
                b.start_pressed(props, prop)

            # Change the text with the bool depending on the buttons and inputs displayed
            pGet = obs.obs_properties_get(props, "hideBool")
            if (setup.useFile == False):                
                obs.obs_property_set_description(pGet, f"Go to Start")
            else:
                obs.obs_property_set_description(pGet, f"Back to Settings")
        else:
            print("Please set a song, or uncheck both boxes")
        return True

    # Called to switch between the settings inputs and the control buttons
    def all_properties(props):
        visible = setup.useFile
        setup.visible_properties(props, visible)

        # Change the text with the bool depending on the buttons and inputs displayed
        pGet = obs.obs_properties_get(props, "hideBool")
        if (setup.useFile == False):
            obs.obs_property_set_description(pGet, f"Go to Start")
        else:
            obs.obs_property_set_description(pGet, f"Back to Settings")
    
    # Called when the script is initialised to only show the settings inputs
    def initialise_properties(props):
        visible = False
        setup.visible_properties(props, visible)

    def visible_properties(props, visible):
        # Get all GUI input properties
        t = obs.obs_properties_get(props, "time")
        s = obs.obs_properties_get(props, "source")
        fp = obs.obs_properties_get(props, "filePath")
        sb = obs.obs_properties_get(props, "startButton")
        rb = obs.obs_properties_get(props, "resetButton")
        ab = obs.obs_properties_get(props, "addButton")
        sl = obs.obs_properties_get(props, "slider")
        alb = obs.obs_properties_get(props, "alertBool")
        #These input properties' visiblity are alternated since they should not be used at the same time.
        obs.obs_property_set_visible(t, not visible)
        obs.obs_property_set_visible(s, not visible)
        obs.obs_property_set_visible(fp, not visible)
        obs.obs_property_set_visible(alb, not visible)
        obs.obs_property_set_visible(sb, visible)
        obs.obs_property_set_visible(rb, visible)
        obs.obs_property_set_visible(ab, visible)
        obs.obs_property_set_visible(sl, visible)

    def default_song():
        # Get the current directory (where the script is located)
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Name of the file you're searching for
        target_file_name = "Low Hp.mp3"

        # Construct the full path to the target file
        target_file_path = os.path.join(script_directory, target_file_name)

        # Check if the file exists
        if os.path.exists(target_file_path):
            print("File found at:", target_file_path)
        else:
            print("File not found in the script directory.")

        return target_file_path

setup = Timer_Setup
