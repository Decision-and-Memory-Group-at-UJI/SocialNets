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
    size=[1920/2, 1080/2], fullscr=False, screen=0,
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')

fixation = visual.GratingStim(win, tex=None, mask='gauss', sf=0, size=0.02,
    name='fixation', autoLog=False)

ready = keyboard.Keyboard()

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
                if keys == 'k':
                    return lStim

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
                    if keys == 'k':
                        return lStim
                win.flip()
            routA(time,1)

    return lStim

mouse = event.Mouse()
def routOK(*stims):
    running = True
    [questStim,lines,pStim,tStim,rankStims] = stims
    while running:
        for i,p in pStim.items():
            p.draw()
        for i,t in tStim.items():
            t.draw()
        for r in rankStims:
            r.draw()
        for i,l in lines.items():
            for j,ll in l.items():
                ll.draw()
        questStim.draw()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0 :
            keys = keys[0]
            if keys == 'r':
                running = False
                ret = 'r'
                return 'r' 
            if keys == 'k':
                running = False
                ret = 'k'
                return 'k'
        win.flip()
    return ret

def routC(time,trials,*args):

    party = args[0]
    people = os.listdir("party"+str(party)+"/people/")[:5]
    with open("party"+str(party)+"/tasks.txt",'r') as f:
        tasks = f.readlines()[:5]
    pStim = {}
    tStim = {}
    pressedShape = None
    personIms = ["party"+str(party)+"/people/"+p for p in people]
    for i,p in enumerate(people):
        pStim[i] = visual.ImageStim(win,image="party"+str(party)+"/people/"+p,name="Person {0:d}".format(i),pos=Cpim_positions[i],size=(0.1,0.1))
    for i,t in enumerate(tasks):
        tStim[i] = visual.TextStim(win,text=t,height=0.05,pos=Ctim_positions[i],name=t)
    running = True
    lineKeys = {}
    linetKeys = {}
    lines = {}
    personRank = {}
    for i in range(len(tasks)):
        lineKeys[i] = []
        personRank[i] = [False,False,False] 
        lines[i] = {}
    for i in range(len(people)):
        linetKeys[i] = {}

    for i in range(len(tasks)):
        for j in range(3):
            lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1])
            linetKeys[i][j] = None

    rankStims = [visual.TextStim(win,"{0:d}".format(j),pos=[l+m for l,m in zip(tStim[len(people)-1].pos,[0.25+0.25*j,0.1])], height=0.05, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0,font='Arial', units='height') for j in range(3)]
    questStim = visual.TextStim(win=win, name='endText',
        text='If this looks correct to you, please press \'k\', otherwise press \'r\'',
        font='Arial',
        units='height', pos=[tStim[0].pos[0]+0.5, tStim[0].pos[1]-0.15], height=0.05, wrapWidth=None, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0);

    c = ['red','green','blue']
    mousePersonIndex = -1
    mouseTaskIndex = -1
    tBeg = clock.getTime()
    count = 0
    mouseIsDown = False
    mouseIsTaskDown = False
    mouseIsPersonDown = False
    while running:
        for key in pStim.keys():
            pStim[key].draw()
        for key in tStim.keys():
            tStim[key].draw()
        for r in rankStims:
            r.draw()
        if mouse.getPressed()[0] == 1 and mouseIsDown == False:
            print("Mouse Clicked",mouse.getPressed())
            mouseIsDown = True
            mousePersonIndex = -1
            for key,item in pStim.items():
                if item.contains(mouse):
                    item.size *= 1.5
                    mousePersonIndex = key
                    mouseIsPersonDown = True
                    break
        if mouse.getPressed()[0] == 0 and not mouseIsTaskDown and not mouseIsPersonDown:
            mouseIsDown = False

        if mouse.getPressed()[0] == 0 and mouseIsPersonDown:
            if mousePersonIndex == -1:
                mouseIsDown = False
                mouseIsPersonDown = False
            else:
                count = 0
                mouseIsDown = False
                mouseIsPersonDown = False
                pStim[mousePersonIndex].size /= 1.5

                print("Mouse Released",mouse.getPressed())
                key = -1
                rank = -1
                for k,item in lines.items():
                    for kk,it in item.items():
                        if it.contains(mouse):
                            key = k
                            rank = kk
                            break
                    if key != -1 and rank != -1:
                        break
                if key != -1 and rank != -1 and not personRank[mousePersonIndex][rank]:
                    if len(lineKeys[mousePersonIndex])< 3:
                        if not any([key == k for k in lineKeys[mousePersonIndex]]):
                            lineKeys[mousePersonIndex] += [key]
                            personRank[mousePersonIndex][rank] = True
                            linetKeys[key][rank] = mousePersonIndex
                            lines[key][rank] = visual.ImageStim(win, personIms[mousePersonIndex],pos=lines[key][rank].pos,size=[0.1,0.1])
                            print(key,"to",mousePersonIndex)
                        else:
                            print("This person already has this role allocated")
                    else:
                        C = 0
                        for k,it in lines.items():
                            C += sum([1 for Z in it.values() if not Z is None])
                        if C >= len(lineKeys)*3-2:
                                if not any([key == k for k in lineKeys[mousePersonIndex]]):
                                    lineKeys[mousePersonIndex] += [key]
                                    linetKeys[key][rank] = mousePersonIndex
                                    personRank[mousePersonIndex][rank] = True
                                    lines[key][rank] = visual.ImageStim(win, personIms[mousePersonIndex],pos=lines[key][rank].pos,size=[0.1,0.1])
                                    print(key,"to",mousePersonIndex)
                                else:
                                    print("This task is already has allocated to this person")
                        else:
                            print("This person already has 3 tasks",C,len(lineKeys)*3-2)
                mousePersonIndex = -1
        for _,it in lines.items():
            for _,itt in it.items(): 
                itt.draw()
        clines = 0
        for i,l in linetKeys.items():
            clines += sum([1 for Z in l.values() if not Z is None])
        if clines == 3*len(tasks):
            keys = routOK(questStim,lines,pStim,tStim,rankStims)
            if keys == 'r':
                for i in range(len(tasks)):
                    lineKeys[i] = []
                    personRank[i] = [False,False,False]
                    lines[i] = {}
                for i in range(len(people)):
                    linetKeys[i] = {}
                for i in range(len(tasks)):
                    for j in range(3):
                        lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1])
                        linetKeys[i][j] = None
            elif keys == 'k':
                running = False
               
        win.flip()
        keys = ready.getKeys(keyList=None, waitRelease=False)
        if len(keys) > 0:
            keys = keys[0]
            if keys == 'escape':
                core.quit()
            if keys == 'k':
                running = False
            if keys == 'r':
                for i in range(len(tasks)):
                    lineKeys[i] = []
                    personRank[i] = [False,False,False]
                    lines[i] = {}
                for i in range(len(people)):
                    linetKeys[i] = {}
                for i in range(len(tasks)):
                    for j in range(3):
                        lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1])
                        linetKeys[i][j] = None
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
    corruption = shuffler([0+getRandInt(0,2) for t in range(len(lStims))] + [2+getRandInt(0,2) for t in range(len(lStims))])
    otherchoice = shuffler([getRandInt(0,3) for i in range(len(corruption))])
    print(corruption)
    print(otherchoice)
    choices = []
    confidences = []
    RTs = []
    confRTs = []

    for t in range(len(lStims)*3):
        if t % len(lStims) == 0:
            lStims = shuffler(lStims)
        tind = t%len(lStims)
        leftorRight = getRandInt(0,2)*2-1
        Stims = []

        c = 0
        if corruption[tind] == 0:
            Stims += [visual.ImageStim(win,image=lStims[tind][1])]
            if otherchoice[tind] == 0:
                socfiles = shuffler(socfiles)
                choose = socfiles[c]
                while choose == lStims[tind][2]:
                    c += 1
                    choose = socfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][2])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 1:
                locfiles = shuffler(locfiles)
                choose = locfiles[c]
                while choose == lStims[tind][3]:
                    c += 1
                    choose = locfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][3])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 2:
                weather = shuffler(weather)
                choose = weather[c]
                while choose == lStims[tind][4]:
                    c += 1
                    choose = weather[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][4])]
                Stims += [visual.ImageStim(win,image=choose)]
        elif corruption[tind] == 1:
            Stims += [visual.ImageStim(win,image=lStims[tind][2])]
            if otherchoice[tind] == 0:
                sitfiles = shuffler(sitfiles)
                choose = sitfiles[c]
                while choose == lStims[tind][1]:
                    c += 1
                    choose = sitfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][1])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 1:
                locfiles = shuffler(locfiles)
                choose = locfiles[c]
                while choose == lStims[tind][3]:
                    c += 1
                    choose = locfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][3])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 2:
                weather = shuffler(weather)
                choose = weather[c]
                while choose == lStims[tind][4]:
                    c += 1
                    choose = weather[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][4])]
                Stims += [visual.ImageStim(win,image=choose)]
        elif corruption[tind] == 2:
            Stims += [visual.ImageStim(win,image=lStims[tind][3])]
            if otherchoice[tind] == 0:
                sitfiles = shuffler(sitfiles)
                choose = sitfiles[c]
                while choose == lStims[tind][1]:
                    c += 1
                    choose = sitfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][1])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 1:
                socfiles = shuffler(socfiles)
                choose = socfiles[c]
                while choose == lStims[tind][2]:
                    c += 1
                    choose = socfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][2])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 2:
                weather = shuffler(weather)
                choose = weather[c]
                while choose == lStims[tind][4]:
                    c += 1
                    choose = weather[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][4])]
                Stims += [visual.ImageStim(win,image=choose)]
        elif corruption[tind] == 3:
            Stims += [visual.ImageStim(win,image=lStims[tind][4])]
            if otherchoice[tind] == 0:
                sitfiles = shuffler(sitfiles)
                choose = sitfiles[c]
                while choose == lStims[tind][1]:
                    c += 1
                    choose = sitfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][1])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 1:
                socfiles = shuffler(socfiles)
                choose = socfiles[c]
                while choose == lStims[tind][2]:
                    c += 1
                    choose = socfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][2])]
                Stims += [visual.ImageStim(win,image=choose)]
            elif otherchoice[tind] == 2:
                locfiles = shuffler(locfiles)
                choose = locfiles[c]
                while choose == lStims[tind][3]:
                    c += 1
                    choose = locfiles[c]
                Stims += [visual.ImageStim(win,image=lStims[tind][3])]
                Stims += [visual.ImageStim(win,image=choose)]

        for this_stim in Stims:
            this_stim.size = [.33, .33]
        Stims[0].pos = Bim_positions[0]
        if leftorRight == -1:
            Stims[1].pos = Bim_positions[4]
            Stims[2].pos = Bim_positions[1]
        else:
            Stims[1].pos = Bim_positions[1]
            Stims[2].pos = Bim_positions[4]
        choice = 0
        time = clock.getTime()
        while choice == 0:
            for s in Stims:
                s.draw()
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
        
    return corruption,otherchoice,choices,confidences,RTs,confRTs

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
lStim = routB(1,1,1,1)
routText("You will now plan the birthday party")
lineKeys,planTime,planConf,plancRT = routC(1,10,1)

routText("We will now present you stimuli you saw previously. Press right arrow if the images match together. Press left arrow if they do not")
corrupt,other,choices,conf,RT,confRT = routD(1,10,1,lStim)
with open('data/{0}_Planning.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(str(planTime) + "," + str(planConf) + "," + str(plancRT) + "\n")
    for key,item in lineKeys.items():
        d = ",".join([str(it) for kk,it in item.items()])
        f.writelines(d + "\n")

with open('data/{0}_Recall.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(",".join([str(c) for c in corrupt]) + "\n")
    f.writelines(",".join([str(c) for c in other]) + "\n")
    f.writelines(",".join([str(c) for c in choices]) + "\n")
    f.writelines(",".join([str(c) for c in conf]) + "\n")
    f.writelines(",".join([str(c) for c in RT]) + "\n")
    f.writelines(",".join([str(c) for c in confRT]) + "\n")

routText("FIN")
