from psychopy import visual, core,event,gui
import random
import os
from psychopy.hardware import keyboard
from psychopy.constants import NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER
import math

def getRandInt(bot,top):
    bot = math.ceil(bot)
    top = math.floor(top)
    return math.floor(random.random()*(top-bot)+bot)

def shuffler(arr):
    newArr = []
    for i in range(len(arr)):
        randInt = getRandInt(0,len(arr))
        newArr += [arr[randInt]]
        del arr[randInt]
    return newArr
expInfo = {'session': '01', 'participant': ''}
expName = 'socialNets'
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
print(expInfo)
# Setup stimulus
win = visual.Window(
    size=[1920/2, 1080/2], fullscr=True, screen=0,
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')

fixation = visual.GratingStim(win, tex=None, mask='gauss', sf=0, size=0.02,
    name='fixation', autoLog=False)

ready = keyboard.Keyboard()
# Let's draw a stimulus for 200 frames, drifting for frames 50:100
notReady = True
clock = core.Clock()

FR = 60

Bim_positions = {0: (0, 0.25),
                1: (0.2, -0.25),
                2: (-0.6, -0.25),
                3: (0.6, -0.25),
                4: (-0.2, -0.25)}

Cpim_positions = {}
for i,j in enumerate([(k-2)/7.5 for k in range(5)]):
    Cpim_positions[i] = (0.5,j)

Ctim_positions = {}
for i,j in enumerate([(k-2)/7.5 for k in range(5)]):
    Ctim_positions[i] = (-0.5,j)

Npim_positions = {}

for i,j in enumerate([(k-2)/7.5 for k in range(5)]):
    Npim_positions[i] = (0.65,j-0.05)

def routA(time, trials):
    tBegin = clock.getTime()
#    for i in range(time*FR):
    while clock.getTime() - tBegin < time:
        fixation.draw()
        win.flip()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0 :
            keys = keys[0]
            if keys == 'escape':
                core.quit()
    return 

def routB(time,trialtime,*args):
    party = args[0]
    iterations = args[1]
    people = os.listdir("party"+str(party)+"/people/")[:5]
    seen = [0 for i in range(len(people))]

    other = os.listdir("party"+str(party)+"/other/")
    situation = ["party"+str(party)+"/socialSit/"+s for s in shuffler(os.listdir("party"+str(party)+"/socialSit/"))]
    situation = shuffler(situation)
    sitimages = [os.listdir(s) for s in situation]

    location = ["locations/"+s for s in shuffler(os.listdir("locations/"))]
    location = shuffler(location)
    locimages = [os.listdir(s) for s in location]

    socgroups = ["socgroups/"+s for s in shuffler(os.listdir("socgroups/"))]
    socgroups = shuffler(socgroups)

    print(situation)
    print(socgroups)
    socimages = [os.listdir(s) for s in socgroups]

    weather = ["weather/"+s for s in shuffler(os.listdir("weather/"))]
    weather = shuffler(weather)

    lStim = []
    trials = len(people)
    perm = [i for i in range(len(weather))]
    locs = [True for i in range(len(socgroups))]
    socs = [True for i in range(len(socgroups))]
    sits = [True for i in range(len(socgroups))]
    for t in range(trials*2):
        selectperson = getRandInt(0,len(people)-1)
        while seen[selectperson] >= 2:
            del people[selectperson]
            del seen[selectperson]
            del situation[selectperson]
            del sitimages[selectperson]
            del location[selectperson]
            del locimages[selectperson]
            del socgroups[selectperson]
            del socimages[selectperson]

            selectperson = getRandInt(0,len(people)-1)
        seen[selectperson] += 1
        person = "party"+str(party)+"/people/"+people[selectperson]
        Person = visual.ImageStim(win, image=person)
        if sits[selectperson]:
            indsit = getRandInt(0,2)
            sits[selectperson]=False
        else:
            indsit = indsit ^ 1

        if locs[selectperson]:
            indloc = getRandInt(0,2)
            locs[selectperson]=False
        else:
            indloc = indloc ^ 1 

        if socs[selectperson]:
            indsoc = getRandInt(0,2)
            socs[selectperson]= False
        else:
            indsoc = indsoc ^ 1

        socim = situation[selectperson]+"/"+sitimages[selectperson][indsit]
        SocialSit = visual.ImageStim(win,image=socim)
        perm = shuffler(perm)
        locim = location[selectperson]+"/"+locimages[selectperson][indloc]
        sgroupim = socgroups[selectperson]+"/"+socimages[selectperson][indsoc]
        SocialGroup = visual.ImageStim(win,image=sgroupim)
        Location = visual.ImageStim(win,image=locim)
        Weather = visual.ImageStim(win,image=weather[perm[0]])
        lStim += [[person, socim,sgroupim,locim,weather[perm[0]]]]
        for this_stim in [Person, SocialSit,SocialGroup, Location,Weather]:
            this_stim.size = [.25, .25]
        for this_stim in [SocialSit, SocialGroup,Location,Weather]:
            this_stim.size = [.33, .33]
        Person.pos = Bim_positions[0]
        SocialSit.pos = Bim_positions[1]
        Location.pos = Bim_positions[2]
        Weather.pos = Bim_positions[3]
        SocialGroup.pos = Bim_positions[4]
        tBegin = clock.getTime()
        #for i in range(trialtime*FR):
        while clock.getTime() - tBegin < trialtime:
            Person.draw()
            Person.opacity /= 1.01
            SocialSit.draw()
            SocialGroup.draw()
            Location.draw()
            Weather.draw()           
            keys = ready.getKeys(keyList=None, waitRelease=False)
            if len(keys) > 0 :
                keys = keys[0]
                if keys == 'escape':
                    core.quit()
            win.flip()
        routA(time,1)
    for i in range(iterations):
        lStim = shuffler(lStim)
        for l in lStim:
            [person,socim,sgroupim,locim,weather] = l
            Person = visual.ImageStim(win,image=person)
            SocialSit = visual.ImageStim(win,image=socim)
            SocialGroup = visual.ImageStim(win,image=sgroupim)
            Location = visual.ImageStim(win,image=locim)
            Weather = visual.ImageStim(win,image=weather)
            for this_stim in [Person, SocialSit,SocialGroup, Location,Weather]:
                this_stim.size = [.25, .25]
            for this_stim in [SocialSit, SocialGroup,Location,Weather]:
                this_stim.size = [.33, .33]
            Person.pos = Bim_positions[0]
            SocialSit.pos = Bim_positions[1]
            Location.pos = Bim_positions[2]
            Weather.pos = Bim_positions[3]
            SocialGroup.pos = Bim_positions[4]
            tBegin = clock.getTime()
#            for i in range(trialtime*FR):
            while clock.getTime() - tBegin < trialtime:
                Person.draw()
                Person.opacity /= 1.01
                SocialSit.draw()
                SocialGroup.draw()
                Location.draw()
                Weather.draw()           
                keys = ready.getKeys(keyList=None, waitRelease=False)
                if len(keys) > 0 :
                    keys = keys[0]
                    if keys == 'escape':
                        core.quit()
                win.flip()
            routA(time,1)

    return lStim

mouse = event.Mouse()
def routC(time,trials,*args):
    questStim = visual.TextStim(win=win, name='endText',
        text='If this looks correct to you, please press \'k\', otherwise press \'r\'',
        font='Arial',
        units='height', pos=[0, 0], height=0.05, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0);

    party = args[0]
    people = os.listdir("party"+str(party)+"/people/")[:5]
    with open("party"+str(party)+"/tasks.txt",'r') as f:
        tasks = f.readlines()[:5]
    pStim = {}
    tStim = {}
    pressedShape = None
    for i,p in enumerate(people):
        pStim[i] = visual.ImageStim(win,image="party"+str(party)+"/people/"+p,name="Person {0:d}".format(i),pos=Cpim_positions[i],size=(0.1,0.1))
    for i,t in enumerate(tasks):
        tStim[i] = visual.TextStim(win,text=t,height=0.05,pos=Ctim_positions[i],name=t)
    running = True
    mouseIsDown = False
    lineKeys = {}
    linepKeys = {}
    lines = {}
    for i in range(len(tasks)):
        lineKeys[i] = []
        lines[i] = []
    for i in range(len(people)):
        linepKeys[i] = []
    c = ['red','green','blue']
    lastPress = -1
    mouseTaskIndex = -1
    tBeg = clock.getTime()
    count = 0
    while running:
        for key in pStim.keys():
            pStim[key].draw()
        for key in tStim.keys():
            tStim[key].draw()

        if mouse.getPressed()[0] == 1 and mouseIsDown == False:
            print("Mouse Clicked",mouse.getPressed())
            mouseIsDown = True
            mouseTaskIndex = -1
            lastPressed = -1
            for key,item in tStim.items():
                if item.contains(mouse):
                    item.size *= 1.5
                    item.color='red'
                    mouseTaskIndex = key
                    lastPress = key
                    break

        if mouse.getPressed()[0] == 0 and mouseIsDown:
            if mouseTaskIndex == -1:
                mouseIsDown = False
            else:
                count = 0
                mouseIsDown = False
                tStim[mouseTaskIndex].size /= 1.5
                tStim[mouseTaskIndex].color = 'white'

                print("Mouse Released",mouse.getPressed())
                for key,item in pStim.items():
                    if item.contains(mouse):
                        if len(linepKeys[key]) < 3:
                            if len(lineKeys[mouseTaskIndex]) < 3:
                                if not any([key == k for k in lineKeys[mouseTaskIndex]]):
                                    lineKeys[mouseTaskIndex] += [key]
                                    linepKeys[key] += [mouseTaskIndex]
                                    lines[mouseTaskIndex] += [visual.Line(win, tStim[mouseTaskIndex].pos,pStim[key].pos,lineColor=c[len(lines[mouseTaskIndex])])]
                                    print(key,"to",mouseTaskIndex)
                                    break
                                else:
                                    print("This person already has this role allocated")
                            else:
                                print("This task already has 3 people",C)
                        else:
                            C = 0
                            for k,it in linepKeys.items():
                                C += len(it)
                            if C >= len(linepKeys)*3-2:
                                if len(lineKeys[mouseTaskIndex]) < 3:
                                    if not any([key == k for k in lineKeys[mouseTaskIndex]]):
                                        lineKeys[mouseTaskIndex] += [key]
                                        linepKeys[key] += [mouseTaskIndex]
                                        lines[mouseTaskIndex] += [visual.Line(win, tStim[mouseTaskIndex].pos,pStim[key].pos,lineColor=c[len(lines[mouseTaskIndex])])]
                                        print(key,"to",mouseTaskIndex)
                                        break
                                    else:
                                        print("This person already has this role allocated")
                                else:
                                    print("This task already has 3 people",C)
                            else:
                                print("This person already has 3 tasks")
                mouseTaskIndex = -1
        if mouseTaskIndex == -1 and count <= 10:
            count += 1
            if count >= 10:
                lastPress = -1
        if lastPress != -1:
            for it in lines[lastPress]:
                it.draw()
        clines = 0
        for i,l in linepKeys.items():
            clines += len(l)
        if clines == 3*len(tasks):
            questStim.draw()
        win.flip()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0:
            keys = keys[0]
            if keys == 'escape':
                core.quit()
            if keys == 'k':
                running = False
            if keys == 'r':
                lastPress = -1
                lineKeys = {}
                linepKeys = {}
                lines = {}
                for i in range(len(tasks)):
                    lineKeys[i] = []
                    lines[i] = []
                for i in range(len(people)):
                    linepKeys[i] = []
    RT = clock.getTime() - tBeg
    confidence,cRT = routDc()

    return lineKeys,RT,confidence,cRT

def routD(fixtime,trials,*args):
    party = args[0]
    lStims = args[1]
    people = os.listdir("party"+str(party)+"/people/")[:5]
    seen = [0 for i in range(len(people))]

    other = os.listdir("party"+str(party)+"/other/")

    situation = ["party"+str(party)+"/socialSit/"+s for s in shuffler(os.listdir("party"+str(party)+"/socialSit/"))]
    sitimages = [os.listdir(s) for s in situation]
    sitfiles = []
    for i,j in zip(sitimages,situation):
            for k in i:
                sitfiles += [j + "/" + k]

    location = ["locations/"+s for s in shuffler(os.listdir("locations/"))]
    locimages = [os.listdir(s) for s in location]
    locfiles = []
    for i,j in zip(locimages,location):
        for k in i:
            locfiles += [j + "/" + k]

    socgroup = ["socgroups/"+s for s in shuffler(os.listdir("socgroups/"))]
    sgrupimages = [os.listdir(s) for s in socgroup]
    socfiles = []
    for i,j in zip(sgrupimages,socgroup):
        for k in i:
            socfiles += [j + "/" + k]

    weather = ["weather/"+s for s in shuffler(os.listdir("weather/"))]
    # 0 is no corruption, 1 is social corruption, 2 is nonsocial corruption
    corruption = shuffler([0 for t in range(len(lStims))] + [1+getRandInt(0,2) for t in range(len(lStims))] + [3+getRandInt(0,2) for t in range(len(lStims))])
    otherchoice = shuffler([getRandInt(0,3) for i in range(len(corruption))])
    print(corruption)
    choices = []
    confidences = []
    RTs = []
    confRTs = []

    for t in range(len(lStims)*3):
        if t % len(lStims) == 0:
            lStims = shuffler(lStims)
        tind = t%len(lStims)
        Person = visual.ImageStim(win, image=lStims[tind][0])

        if corruption[tind] == 0:
            SocialSit = visual.ImageStim(win,image=lStims[tind][1])
            SocialGroup = visual.ImageStim(win,image=lStims[tind][2])
            Location = visual.ImageStim(win,lStims[tind][3])
            Weather = visual.ImageStim(win,image=lStims[tind][4])
        elif corruption[tind] == 1 or corruption[tind] == 2:
            c = 0
            if corruption[tind] == 1:
                sitfiles = shuffler(sitfiles)
                choose = sitfiles[c]
                while choose == lStims[tind][1]:
                    c += 1
                    choose = sitfiles[c]
                SocialSit = visual.ImageStim(win,image=choose)
                SocialGroup = visual.ImageStim(win,image=lStims[tind][2])
            else:
                socfiles = shuffler(socfiles)
                choose = socfiles[c]
                while choose == lStims[tind][2]:
                    c += 1
                    choose = socfiles[c]
                SocialSit = visual.ImageStim(win,image=lStims[tind][1])
                SocialGroup = visual.ImageStim(win,image=choose)

            Location = visual.ImageStim(win,lStims[tind][3])
            Weather = visual.ImageStim(win,image=lStims[tind][4])
        elif corruption[tind] == 3 or corruption[tind] == 4:
            c = 0
            if corruption[tind] == 3:
                locfiles = shuffler(locfiles)
                choose = locfiles[c]
                while choose == lStims[tind][3]:
                    c += 1
                    choose = locfiles[c]
                Location = visual.ImageStim(win,choose)
                Weather = visual.ImageStim(win,image=lStims[tind][4])
            else:
                weather = shuffler(weather)
                choose = socfiles[c]
                while choose == lStims[tind][4]:
                    c += 1
                    choose = weather[c]
                Location = visual.ImageStim(win,lStims[tind][3])
                Weather = visual.ImageStim(win,image=choose)

            SocialSit = visual.ImageStim(win,image=lStims[tind][1])
            SocialGroup = visual.ImageStim(win,image=lStims[tind][2])

        for this_stim in [Person, SocialSit, SocialGroup, Location,Weather]:
            this_stim.size = [.33, .33]
        Person.pos = Bim_positions[0]
        SocialSit.pos = Bim_positions[1]
        SocialGroup.pos = Bim_positions[4]
        Location.pos = Bim_positions[2]
        Weather.pos = Bim_positions[3]
        StimsAll =  [SocialSit, SocialGroup, Location,Weather]
        S1 = getRandInt(0,4)
        Stim1 = StimsAll[S1]
        del StimsAll[S1]
        S2 = getRandInt(0,3)
        Stim2 = StimsAll[S2]
        choice = 0
        time = clock.getTime()
        while choice == 0:
            Person.draw()
            if corruption[tind] == 0:
                Stim1.draw()
                Stim2.draw()
#                SocialSit.draw()
#                SocialGroup.draw()
#                Location.draw()
#                Weather.draw()           
            elif corruption[tind] == 1:
                SocialSit.draw()
                if otherchoice[tind] == 0:
                    SocialGroup.draw()
                elif otherchoice[tind] == 1:
                    Location.draw()
                elif otherchoice[tind] == 2:
                    Weather.draw()
            elif corruption[tind] == 2:
                SocialGroup.draw()
                if otherchoice[tind] == 0:
                    SocialSit.draw()
                elif otherchoice[tind] == 1:
                    Location.draw()
                elif otherchoice[tind] == 2:
                    Weather.draw()
            elif corruption[tind] == 3:
                Location.draw()
                if otherchoice[tind] == 0:
                    SocialSit.draw()
                elif otherchoice[tind] == 1:
                    SocialGroup.draw()
                elif otherchoice[tind] == 2:
                    Weather.draw()
            elif corruption[tind] == 4:
                if otherchoice[tind] == 0:
                    SocialSit.draw()
                elif otherchoice[tind] == 1:
                    SocialGroup.draw()
                elif otherchoice[tind] == 2:
                    Location.draw()
                Weather.draw()
            keys = ready.getKeys(keyList=None, waitRelease=False)
            if len(keys) > 0 :
                keys = keys[0]
                if keys == 'escape':
                    core.quit()
                if keys == 'left':
                    choice = -1
                    RT = clock.getTime() - time
                    confidence,cRT = routDc()
                elif keys == 'right':
                    choice = 1
                    RT = clock.getTime() - time
                    confidence,cRT = routDc()
            win.flip()
        choices += [choice]
        confidences += [confidence]
        RTs += [RT]
        confRTs += [cRT]
        routA(fixtime,1)
        
    return corruption,choices,confidences,RTs,confRTs

def routDc():
    notReady = True
    time = clock.getTime()
    text = visual.TextStim(win=win, name='endText',
                text='How confident are you? Adjust the slider, and press spacebar to continue',
                font='Arial',
                units='height', pos=[0, 0.35], height=0.05, wrapWidth=None, ori=0,
                color='white', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
    slider = visual.Slider(win,(1,2,3,4,5,6,7),granularity=0,pos=(0,0))
    while notReady:
        text.draw()
        slider.draw()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0:
            keys = keys[0]
            if keys == 'space':
                RT = clock.getTime() - time
                notReady = False
        win.flip()
    return slider.getRating(),RT

def routText(fill):
    Text = visual.TextStim(win=win, name='Text',
        text=fill,
        font='Arial',
        units='height', pos=[0, 0], height=0.05, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0);
    
    notReady = True
    while notReady:
        t = clock.getTime()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0:
            keys = keys[0]
            if keys == 'escape':
                core.quit()
            else:
                notReady = False 
        Text.draw()
        win.flip()
    return

routText("We will show you groups of images regarding a group of friends. Please pay attention to these sets of images as you will need to assign roles to these friends later for a _birthday party_")
routA(1,1)
lStim = routB(1,10,1,1)
routText("You will now plan the birthday party")
lineKeys,planTime,planConf,plancRT = routC(1,10,1)

routText("We will now present you stimuli you saw previously. Press right arrow if the images match together. Press left arrow if they do not")
corrupt,choices,conf,RT,confRT = routD(1,10,1,lStim)
with open('data/{0}_Planning.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(str(planTime) + "," + str(planConf) + "," + str(plancRT) + "\n")
    for key,item in lineKeys.items():
        d = ",".join([str(it) for it in item])
        f.writelines(d + "\n")

with open('data/{0}_Recall.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(",".join([str(c) for c in corrupt]) + "\n")
    f.writelines(",".join([str(c) for c in choices]) + "\n")
    f.writelines(",".join([str(c) for c in conf]) + "\n")
    f.writelines(",".join([str(c) for c in RT]) + "\n")
    f.writelines(",".join([str(c) for c in confRT]) + "\n")

routText("FIN")
