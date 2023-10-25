import {visual, core,event,gui,util,data,hardware} from './lib/psychojs-2023.1.3.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
var fs = require('fs');

function getRandInt(bot,top){
    bot = Math.ceil(bot);
    top = Math.floor(top);
    return Math.floor(Math.random()*(top-bot)+bot);
};

function shuffler(arr){
    newArr = [];
    for (let i = 0; i <  arr.length; i++){
        randInt = getRandInt(0,arr.length);
        newArr.push(arr[randInt]);
        Array.splice(randInt,arr);
    };
    return newArr;
};

const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));
const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

flowScheduler.add(updateInfo);
flowScheduler.add(routA(1,1));
flowScheduler.add(routB(1,10,2,1));
flowScheduler.add(routC(1,10,2));
flowScheduler.add(routD(1,10,2));
flowScheduler.add(quitPsychoJS, '', true);

dialogCancelScheduler.add(quitPsychoJS, '', false);

// Setup stimulus
const win = visual.Window(
    size=[1920/2, 1080/2], fullscr=false, screen=0,
    winType='pyglet', allowGUI=true, allowStencil=false,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=true,
    units='height');

const fixation = visual.GratingStim(win, tex=null, mask='gauss', sf=0, size=0.02,
    name='fixation', autoLog=false);

const ready = keyboard.Keyboard();

const notReady = true;
const clock = core.Clock();

const FR = 60;

const Bim_positions = {0: (0, 0.25),
                1: (0.6, -0.25),
                2: (-0.0, -0.25),
                3: (-0.6, -0.25)};


const BLim_positions = {1: (0.6, -0.45),
                2: (-0.0, -0.45),
                3: (-0.6, -0.45)};

let lArr = [...Array(5).keys()].map((k) ==> (k-2)/7.5);

var Cpim_positions = {};
for (const [i,j] of lArr){
    Cpim_positions[i] = (0.5,j);
};
const Cpim_positions = Cpim_positions;

var Ctim_positions = {}

for (const [i,j] of lArr){
    Ctim_positions[i] = (-0.5,j);
};
const Ctim_positions = Ctim_positions;

var Npim_positions = {};

for (const [i,j] of lArr){
    Npim_positions[i] = (0.65,j-0.05);
};
const Npim_positions = Npim_positions;

function routA(time, trials){
    tBegin = clock.getTime();
    while (clock.getTime() - tBegin < time){
        fixation.draw();
        win.flip();
        keys = ready.getKeys(keyList=null, waitRelease=false);
        if (keys.length > 0){
            keys = keys[0];
            if (keys == 'escape'){
                core.quit();
            };
        };
    };
    return; 
};

function routB(time,trialtime,nParty,iters){
    let party = "party" + str(nParty);
    let iterations = iters;
    let people = fs.readdirSync(party+"/people/")[:5];
    let seen = [...Array(people.length).keys()].map((k) ==> 0);

    let socsitDirs = shuffler(fs.readdirSync(party+"/socialSit/");
    let situation = [...Array(socsitDirs.length).keys()].map((s)=>party+"/socialSit/"+s);
    situation = shuffler(situation);
    let sitimages = [...Array(situation.length).keys()].map((s) => fs.readdirSync(s));

    let locDirs = shuffler(fs.readdirSync(party+"/locations/");
    let localation = [...Array(socsitDirs.length).keys()].map((s)=>party+"/locations/"+s);
    localation = ["{0}/locations/{1}".format(party,s) for s in shuffler(os.listdir(party+"/locations/"))];
    localation = shuffler(localation);
    let locimages = [...Array(localation.length).keys()].map((s) => fs.readdirSync(s));

    let sgroupDirs = shuffler(fs.readdirSync(party+"/socgroups/");
    let socgroups = [...Array(socsitDirs.length).keys()].map((s)=>party+"/socgroups/"+s);
    socgroups = ["{0}/socgroups/{1}".format(party,s) for s in shuffler(os.listdir(party+"/socgroups/"))];
    socgroups = shuffler(socgroups);
    let socimages = [...Array(socgroups.length).keys()].map((s) => fs.readdirSync(s));

    let labels = ["Situation","Location","Group"];
    let TextStims = [];
    for (let i = 0; i < labels.length; i++){
        t = labels[i];
        TextStims.push(visual.TextStim(win,text=t,height=0.05,pos=BLim_positions[i+1],name=t));
    };

    let lStim = [];
    let trials = people.length;
    let locs = [...Array(socgroups.length).keys()].map((k)=>true);
    let socs = [...Array(socgroups.length).keys()].map((k)=>true);
    let sits = [...Array(socgroups.length).keys()].map((k)=>true);

    let persons =  [...Array(5).keys()].map((s)=>party+"/people/"+people[s]);
    let locs = [...Array(5).keys()].map((k)=>[]);
    let sits = [...Array(5).keys()].map((k)=>[]);
    let groups = [...Array(5).keys()].map((k)=>[]);
    let indices = [...Array(4).keys()].map((k)=>k+1);

    for (let i = 0; i < 5; i++){
        for (let j = 0; j < 2; j++){
            locs[i].push(localation[i]+"/"+locimages[i][j]);
            sits[i].push(situation[i]+"/"+sitimages[i][j]);
            groups[i].push(socgroups[i]+"/"+socimages[i][j]);
        };
    };
    stimlist = [persons,sits,groups,locs];
    // What a wild line. I had this in python to do a deep copy, wonder if it's
    // necessary here too?
    Stims = [...Array(stimlist.length).keys()].map((i)=>[...Array(stimlist[i].length).keys()].map((j)=>stimlist[i][j]));
    psychoJS.experiment.addData("Stimuli",Stims);
    for (let t = 0; t < trials*2; t++){ 
        while (seen[selectperson = getRandInt(0,people.length-1)] >= 2){
            Array.splice(selectperson,people);
            Array.splice(selectperson,seen);
            Array.splice(selectperson,situation);
            Array.splice(selectperson,sitimages);
            Array.splice(selectperson,localation);
            Array.splice(selectperson,locimages);
            Array.splice(selectperson,socgroups);
            Array.splice(selectperson,socimages);
        };

        seen[selectperson] += 1;
        let person = party+"/people/"+people[selectperson];
        let Person = visual.ImageStim(win, image=person);
        if (sits[selectperson]){
            let indsit = getRandInt(0,2);
            sits[selectperson]=false;
        }
        else{let indsit = indsit ^ 1};

        if (locs[selectperson]){
            let indloc = getRandInt(0,2);
            locs[selectperson]=false;
        }
        else{let indloc = indloc ^ 1};

        if (socs[selectperson]){
            let indsoc = getRandInt(0,2);
            socs[selectperson]= false;
        }
        else{let indsoc = indsoc ^ 1;}

        let socim = situation[selectperson]+"/"+sitimages[selectperson][indsit];
        let SocialSit = visual.ImageStim(win,image=socim);
        let locim = localation[selectperson]+"/"+locimages[selectperson][indloc];
        let sgroupim = socgroups[selectperson]+"/"+socimages[selectperson][indsoc];
        let SocialGroup = visual.ImageStim(win,image=sgroupim);
        let Location = visual.ImageStim(win,image=locim);
        lStim.push([person, socim,sgroupim,locim]);
        Person.size = [.25, .25];
        SocialSit.size = [.33, .33];
        Location.size = [.33, .33];
        SocialGroup.size = [.33, .33];

        Person.pos = Bim_positions[0];
        if (t > 5){indices = shuffler(indices)};
        SocialSit.pos = Bim_positions[indices[0]];
        Location.pos = Bim_positions[indices[1]];
        SocialGroup.pos = Bim_positions[indices[2]];

        let tBegin = clock.getTime();
        while (clock.getTime() - tBegin < trialtime){
            Person.draw();
            Person.opacity /= 1.01;
            SocialSit.draw();
            SocialGroup.draw();
            Location.draw();
            if (t < 5){
                for (let j = 0; j < TextStims.length; j++){TextStims[j].draw()};

            let keys = ready.getKeys(keyList=null, waitRelease=false);
            if (keys.length > 0){
                let keys = keys[0];
                if (keys == 'escape'){core.quit()};
                if (keys == 'k'){return};
            };

            win.flip();
        };
        routA(time,1);
    };
    for (let i=0; i < iterations; i++)
        lStim = shuffler(lStim);
        for (let lind = 0; lind < lStim.length; lind++)
            [person,socim,sgroupim,locim] = lStim[lind];
            let Person = visual.ImageStim(win,image=person);
            let SocialSit = visual.ImageStim(win,image=socim);
            let SocialGroup = visual.ImageStim(win,image=sgroupim);
            let Location = visual.ImageStim(win,image=locim);
            Person.size = [.25, .25];
            SocialSit.size = [.33, .33];
            SocialGroup.size = [.33, .33];
            Location.size = [.33, .33];

            indices = shuffler(indices);

            Person.pos = Bim_positions[0];
            SocialSit.pos = Bim_positions[indices[0]];
            Location.pos = Bim_positions[indices[1]];
            SocialGroup.pos = Bim_positions[indices[2]];

            let tBegin = clock.getTime();
            while (clock.getTime() - tBegin < trialtime){
                Person.draw();
                Person.opacity /= 1.01;
                SocialSit.draw();
                SocialGroup.draw();
                Location.draw();
                let keys = ready.getKeys(keyList=null, waitRelease=false);
                if (keys.length > 0 ){
                    let keys = keys[0];
                    if (keys == 'escape'){core.quit()};
                    if (keys == 'k'){return};
                };
                win.flip();
            };
            routA(time,1);
    return;
};

var mouse = event.Mouse();

function routOK(*stims){
    let running = true;
    let [questStim,lines,pStim,tStim,rankStims] = stims;
    while (running){
        for (let i = 0; i < pStim.length; i++) {pStim[i].draw()};
        for (let i = 0; i < tStim.length; i++) {tStim[i].draw()};
        for (let i = 0; i < rankStims.length; i++) {rankStims[i].draw()};
        for (let i = 0; i < pStim.length; i++) {for (let j =0; j < lines[i].length; j++) {lines[i][j].draw()}};
        questStim.draw();
        let keys = ready.getKeys(keyList=null, waitRelease=false);
        if (len(keys) > 0){
            let keys = keys[0];
            if (keys == 'r'){
                running = false;
                let ret = 'r';
                return 'r';
            };
            if (keys == 'k'){
                running = false;
                let ret = 'k';
                return 'k';
            };
        };
        win.flip();
    };
    return ret;
};

function checkTs(ind,db){
    let ret = -1;
    for (let key = 0; key < db.length; key++){ if (db[key] == ind){ return key} };
    return ret;
}

function routC(time,trials,nParty){

    let party = nParty; 
    let people = fs.readdirSync("party"+party+"/people/")[:5];
    let tasks = fs.readFileSync("party"+party+"/tasks.txt")[:5];
    let pStim = {};
    let tStim = {};
    let pressedShape = null;
    personIms = [...Array(people.length).keys()].map((i)=>"party"+party+"/people/"+people[i]);
    for (let i = 0; i < people.length; i++){
        p = people[p];
        pStim[i] = visual.ImageStim(win,image="party"+str(party)+"/people/"+p,name="Person " + i,pos=Cpim_positions[i],size=(0.1,0.1),color='white');
    };
    for (let i = 0; i < tasks.length; i++){
        t = tasks[i];
        tStim[i] = visual.TextStim(win,text=t,height=0.05,pos=Ctim_positions[i],name=t,color='white');
    };
    running = true;
    lineKeys = {};
    linetKeys = {};
    lines = {};
    personRank = {};
    for (let i = 0; i < tasks.length; i++){
        lineKeys[i] = {};
        personRank[i] = [false,false,false];
        lines[i] = {};
    };
    for (let i = 0; i < people.length; i++){linetKeys[i] = {}};

    for (let i =0; i < tasks.length; i++){
        for (let j = 0; j < 3; j++){
            lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1]);
            linetKeys[i][j] = null;
        };
    };
    let rankStims = [];
    for (let j = 0; j < 3; j++){
        let pos = tStim[people.length-1].pos + [0.25+0.25*j,0.1];
        rankStims.push(visual.TextStim(win,j,pos=pos, height=0.05, wrapWidth=null, ori=0, color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', depth=0.0,font='Arial', units='height'));
    };
    let questStim = visual.TextStim(win=win, name='endText',
        text='If this looks correct to you, please press \'k\', otherwise press \'r\'',
        font='Arial',
        units='height', pos=[tStim[0].pos[0]+0.5, tStim[0].pos[1]-0.15], height=0.05, wrapWidth=null, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0);

    let c = ['red','green','blue'];
    let mousePersonIndex = -1;
    let mouseTaskIndex = -1;
    let tBeg = clock.getTime();
    let count = 0;
    let mouseIsDown = false;
    let mouseIsTaskDown = false;
    let mouseIsPersonDown = false;
    while (running){
        for (let i = 0; i < rankStims.length; i++){ rankStims[i].draw()};
        if (mouse.getPressed()[0] == 1 && mouseIsDown == false){
            mouseIsDown = true;
            mousePersonIndex = -1;
            for (let key = 0; key < pStim.length; key++){
                item = pStim[key];
                if item.contains(mouse){
                    item.size *= 1.5;
                    mousePersonIndex = key;
                    mouseIsPersonDown = true;
                    break;
                };
            };
        };
        if (mouse.getPressed()[0] == 0 && ! mouseIsTaskDown && ! mouseIsPersonDown){mouseIsDown = false};

        if (mouse.getPressed()[0] == 0 && mouseIsPersonDown){
            if (mousePersonIndex == -1){ mouseIsDown = false; mouseIsPersonDown = false};
            else{
                count = 0;
                mouseIsDown = false;
                mouseIsPersonDown = false;
                pStim[mousePersonIndex].size /= 1.5;

                console.log("Mouse Released",mouse.getPressed());
                key = -1;
                rank = -1;
                for (let k = 0; k < lines.length; k++){
                    let item = lines[k];
                    for (let kk = 0; kk < item.length; kk++){
                        let it = item[kk];
                        if (it.contains(mouse)){
                            key = k;
                            rank = kk;
                            break;
                        };
                    };
                    if (key != -1 && rank != -1)
                        break;
                };
                if (key != -1 && rank != -1){
                    // If this person already has this rank occupied
                    if (rank in lineKeys[mousePersonIndex]){
                        pastkey = lineKeys[mousePersonIndex][rank];
                        Array.splice(rank,lineKeys[mousePersonIndex]);
                        if rank in linetKeys[pastkey]{linetKeys[pastkey][rank] = null};
                        pos = tStim[pastkey].pos + [0.25+0.25*rank,0];
                        lines[pastkey][rank] = visual.Rect(win, fillColor='white',pos=pos,size=[0.1,0.1]);
                    };
                    // If this person was already assigned this task before
                    else if ((pastrank = checkTs(mousePersonIndex, linetKeys[key])) != -1){
                        if pastrank in linetKeys[key]{linetKeys[key][pastrank] = null};
                        if pastrank in lineKeys[mousePersonIndex]{Array.splice(pastrank,lineKeys[mousePersonIndex][pastrank])};
                        pos = tStim[key].pos + [0.25+0.25*pastrank,0];
                        lines[key][pastrank] = visual.Rect(win, fillColor='white',pos=pos,size=[0.1,0.1]);
                    };
                    // If someone is already occupying this task rank, properly
                    // overwrite their occupation wit the new person
                    if (rank in linetKeys[key] && ! linetKeys[key][rank] === null){Array.split(rank, lineKeys[linetKeys[key][rank]])};
                    lineKeys[mousePersonIndex][rank] = key;
                    linetKeys[key][rank] = mousePersonIndex;
                    lines[key][rank] = visual.ImageStim(win, personIms[mousePersonIndex],pos=lines[key][rank].pos,size=[0.1,0.1]);
                    console.log(key,"to",mousePersonIndex);
                };
                mousePersonIndex = -1;
            };
        };

        for (let i = 0; i < lines.length; i++){it = lines[i]; for (let j = 0; j < it.length; j++){it[j].draw()}};

        for (let i = 0; i < lineKeys.length; i++){
            let l = lineKeys[i];
            let temp = 0;
            l.filter((ll) => ll != null).forEach(s => temp += s);
            for (t of temp) { tsum += t };
            if (temp == 3 && pStim[i].color != 'red'){pStim[i].color = 'red'};
            else if (temp != 3 && pStim[i].color != 'white'){pStim[i].color = 'white'};
            pStim[i].draw();
        };

        let clines = 0;
        for (let i = 0; i < linetKeys.length; i++){
            let l = linetKeys[i];
            let temp = 0;
            l.filter((ll) => ll != null).forEach(s => temp += s);
            clines += temp;
            if (temp == 3 && tStim[i].color != [1,-1,-1] != 'red'){tStim[i].color='red'};
            else if (tStim[i].color != 'white'){tStim[i].color='white'};
            tStim[i].draw();
        };
        if (clines == 3*len(tasks)){
            keys = routOK(questStim,lines,pStim,tStim,rankStims);
            if (keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    lines[i] = {};
                };
                for (let i = 0; i < people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 3; j++){
                        lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1]);
                        linetKeys[i][j] = null;
                    };
                };
            };
            else if (keys == 'k'){running = false};
        };
               
        win.flip();
        let keys = ready.getKeys(keyList=null, waitRelease=false);
        if (keys.length > 0){
            let keys = keys[0];
            if (keys == 'escape'){core.quit()};
            if (keys == 'k'){running = false};
            if (keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    lines[i] = {};
                };
                for (let i = 0; i< people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 3; j++){
                        lines[i][j] = visual.Rect(win, fillColor='white',pos=[l+m for l,m in zip(tStim[i].pos,[0.25+0.25*j,0])],size=[0.1,0.1]);
                        linetKeys[i][j] = null;
                    };
                };
            };
        };
    };
    let RT = clock.getTime() - tBeg;
    confidence,cRT = routDc();
    for (let key = 0; key < lineKeys.length; key++){
        let item = lineKeys[key];
        allKeys = item.keys();
        sortedKeys = allKeys.sort();
        newdict = {};
        for (let i = 0; i < sortedKeys; i++){newdict[i] = item[sortedKeys[i]]};
        lineKeys[key] = newdict;
    };
    psychoJS.addData("rankDec",lineKeys);
    psychoJS.addData("rankRT",RT);
    psychoJS.addData("rankconf",confidence);
    psychoJS.addData("rankconfRT",cRT);
    return;
};

function routD(fixtime,trials,Nparty){
    let party = "party" + Nparty;
    let [people,situation,sgroup,localation,weather] = psychoJS._currentTrialData['Stimuli'];

    // Person Select
    let pind = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,5));
    // Episode Select
    let eind = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2));
    // Reference cue
    let corruption = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,3));
    // Query cues
    let otherchoice = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2));
    // Between or within person corruption
    let bwgroup = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2));
    let choices = [];
    let confidences = [];
    let RTs = [];
    let confRTs = [];
    let correct = [];
    for (let t = 0; t < eind.length; t++){
        let p = pind[t];
        let e = eind[t];
        let corr = corruption[t];
        let oc = otherchoice[t];
        let bw = bwgroup[t];
        let leftorRight = getRandInt(0,2)*2-1;
        correct.push(leftorRight);
        let Stims = [];
        let c = 0;
        choices = []
        if (corr == 0){
            Stims.push([visual.ImageStim(win,image=situation[p][e])];
            if (oc == 0){
                if (bw == 1){
					for (let i=0; i < sgroup.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(sgroup[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = sgroup[p][e^1]};
                Stims.push(visual.ImageStim(win,image=sgroup[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
            else if (oc == 1){
                if (bw == 1){
   					for (let i=0; i < localation.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(localation[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = localation[p][e^1]};
                Stims.push([visual.ImageStim(win,image=localation[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
        };
        else if (corr == 1){
            Stims.push(visual.ImageStim(win,image=sgroup[p][e]));
            if (oc == 0){
                if (bw == 1){
   					for (let i=0; i < situation.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(situation[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = situation[p][e^1]};
                Stim.push(svisual.ImageStim(win,image=situation[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
            else if (oc == 1){
                if (bw == 1){
   					for (let i=0; i < localation.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(localation[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = localation[p][e^1]};
                Stims.push(visual.ImageStim(win,image=localation[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
        };
        else if (corr == 2){
            Stims.push(visual.ImageStim(win,image=localation[p][e]));
            if (oc == 0){
                if (bw == 1){
   					for (let i=0; i < situation.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(situation[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = situation[p][e^1]};
                Stims.push(visual.ImageStim(win,image=weather[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
            else if (oc == 1){
                if (bw == 1){
   					for (let i=0; i < sgroup.length; i++){for (let j = 0; j < 2; j++){if (i != p){choices.push(sgroup[i][j])}}}
                    choose = choices[getRandInt(0,len(choices))];
                };
                else{choose = sgroup[p][e^1]};
                Stims.push(visual.ImageStim(win,image=weather[p][e]));
                Stims.push(visual.ImageStim(win,image=choose));
            };
        };
        for (k = 0; k < Stims.length; k++){Stims[k].size = [.33, .33]};
        Stims[0].pos = Bim_positions[0];
        if (leftorRight == -1){
            Stims[1].pos = Bim_positions[3];
            Stims[2].pos = Bim_positions[1];
        };
        else{
            Stims[1].pos = Bim_positions[1];
            Stims[2].pos = Bim_positions[3];
        };
        let choice = 0;
        time = clock.getTime();
        while (choice == 0){
            for (let s = 0; s < Stims.length; s++){Stims[s].draw()};
            let keys = ready.getKeys(keyList=null, waitRelease=false);
            if (keys.length > 0){
                let keys = keys[0];
                if (keys == 'escape'){core.quit()};
                if (keys == 'left'){
                    choice = -1;
                    RT = clock.getTime() - time;
                    confidence,cRT = routDc();
                };
                else if (keys == 'right'){
                    choice = 1;
                    RT = clock.getTime() - time;
                    confidence,cRT = routDc();
                };
            };
            win.flip();
        };
        choices.push(choice);
        confidences.push(confidence);
        RTs.push(RT);
        confRTs.push(cRT);
        routA(fixtime,1);
    psychoJS.addData("Reference",corruption);
    psychoJS.addData("Query", otherchoice);
    psychoJS.addData("Choice",choices);
    psychoJS.addData("correctChoice",correct);
    psychoJS.addData("BWgroup", bwgroup);
    psychoJS.addData("retrievalConf",confidences);
    psychoJS.addData("retrievalRT",RTs);
    psychoJS.addData("retrievalConfRT",confRTs);
    return;
};

function routDc(){
    notReady = true;
    time = clock.getTime();
    text = visual.TextStim(win=win, name='endText',
                text='How confident are you? Adjust the slider, and press spacebar to continue',
                font='Arial',
                units='height', pos=[0, 0.35], height=0.05, wrapWidth=null, ori=0,
                color='white', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
    slider = visual.Slider(win,(1,2,3,4,5,6,7),granularity=0,pos=(0,0));
    while (notReady){
        text.draw();
        slider.draw();
        let keys = ready.getKeys(keyList=null, waitRelease=false);
        if (len(keys) > 0){
            keys = keys[0];
            if (keys == 'space'){
                RT = clock.getTime() - time;
                notReady = false;
            };
        };
        win.flip();
    };
    return slider.getRating(),RT;

function routText(fill){
    let Text = visual.TextStim(win=win, name='Text',
        text=fill,
        font='Arial',
        units='height', pos=[0, 0], height=0.05, wrapWidth=null, ori=0,
        color='white', colorSpace='rgb', opacity=1,
        languageStyle='LTR',
        depth=0.0);
    
    let notReady = true;
    while (notReady){
        let t = clock.getTime();
        let keys = ready.getKeys(keyList=null, waitRelease=false);
        if (keys.length > 0){
            let keys = keys[0];
            if keys == 'escape'{core.quit()};
            else{notReady = false};
        };
        Text.draw();
        win.flip();
    };
    return;
};

async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});

  return Scheduler.Event.QUIT;
}

/*
routText("We will show you groups of images regarding a group of friends. Please pay attention to these sets of images as you will need to assign roles to these friends later for a _birthday party_")
routA(1,1)
lStim = routB(1,10,2,1)

routText("You will now plan the birthday party")
lineKeys,planTime,planConf,plancRT = routC(1,10,2)

routText("We will now present you stimuli you saw previously. Press right arrow if the images match together. Press left arrow if they do not")
corrupt,other,choices,bw,conf,RT,confRT = routD(1,10,2,lStim)
with open('data/{0}_Planning.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(str(planTime) + "," + str(planConf) + "," + str(plancRT) + "\n")
    for key,item in lineKeys.items():
        d = ",".join([str(it) for kk,it in item.items()])
        f.writelines(d + "\n")

with open('data/{0}_Recall.txt'.format(expInfo['participant']),'w') as f:
    f.writelines(",".join([str(c) for c in corrupt]) + "\n")
    f.writelines(",".join([str(c) for c in other]) + "\n")
    f.writelines(",".join([str(c) for c in choices]) + "\n")
    f.writelines(",".join([str(c) for c in bw]) + "\n")
    f.writelines(",".join([str(c) for c in conf]) + "\n")
    f.writelines(",".join([str(c) for c in RT]) + "\n")
    f.writelines(",".join([str(c) for c in confRT]) + "\n")

routText("FIN")
*/
