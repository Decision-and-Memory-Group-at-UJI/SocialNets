import {visual, core,util,data,hardware} from 'https://pavlovia.org/lib/psychojs-2023.1.3.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;

function getRandInt(bot,topp){
    bot = Math.ceil(bot);
    topp = Math.floor(topp);
    return Math.floor(Math.random()*(topp-bot)+bot);
};

function shuffler(arr){
    let newArr = [];
    let arrlength = arr.length
    for (let i = 0; i <  arrlength; i++){
        let randInt = getRandInt(0,arr.length);
        newArr.push(arr[randInt]);
        arr.splice(randInt,1);
    };
    return newArr;
};

const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: false,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true
});
let expName = 'SocialNets';  // from the Builder filename that created this script
let expInfo = {
    'participant': '',
    'session': '001',
};
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'party2/people/1.png', 'path': 'party2/people/1.png'},
    {'name': 'party2/people/2.png', 'path': 'party2/people/2.png'},
    {'name': 'party2/people/3.png', 'path': 'party2/people/3.png'},
    {'name': 'party2/people/4.png', 'path': 'party2/people/4.png'},
    {'name': 'party2/people/5.png', 'path': 'party2/people/5.png'},
    {'name': 'party2/socialSit/1/1.jpg', 'path': 'party2/socialSit/1/1.jpg'},
    {'name': 'party2/socialSit/2/1.jpg', 'path': 'party2/socialSit/2/1.jpg'},
    {'name': 'party2/socialSit/3/1.jpg', 'path': 'party2/socialSit/3/1.jpg'},
    {'name': 'party2/socialSit/4/1.jpg', 'path': 'party2/socialSit/4/1.jpg'},
    {'name': 'party2/socialSit/5/1.jpg', 'path': 'party2/socialSit/5/1.jpg'},
    {'name': 'party2/socialSit/1/2.jpg', 'path': 'party2/socialSit/1/2.jpg'},
    {'name': 'party2/socialSit/2/2.jpg', 'path': 'party2/socialSit/2/2.jpg'},
    {'name': 'party2/socialSit/3/2.jpg', 'path': 'party2/socialSit/3/2.jpg'},
    {'name': 'party2/socialSit/4/2.jpg', 'path': 'party2/socialSit/4/2.jpg'},
    {'name': 'party2/socialSit/5/2.jpg', 'path': 'party2/socialSit/5/2.jpg'},
    {'name': 'party2/socgroups/1/1.jpg', 'path': 'party2/socgroups/1/1.jpg'},
    {'name': 'party2/socgroups/2/1.jpg', 'path': 'party2/socgroups/2/1.jpg'},
    {'name': 'party2/socgroups/3/1.jpg', 'path': 'party2/socgroups/3/1.jpg'},
    {'name': 'party2/socgroups/4/1.jpg', 'path': 'party2/socgroups/4/1.jpg'},
    {'name': 'party2/socgroups/5/1.jpg', 'path': 'party2/socgroups/5/1.jpg'},
    {'name': 'party2/socgroups/1/2.jpg', 'path': 'party2/socgroups/1/2.jpg'},
    {'name': 'party2/socgroups/2/2.jpg', 'path': 'party2/socgroups/2/2.jpg'},
    {'name': 'party2/socgroups/3/2.jpg', 'path': 'party2/socgroups/3/2.jpg'},
    {'name': 'party2/socgroups/4/2.jpg', 'path': 'party2/socgroups/4/2.jpg'},
    {'name': 'party2/socgroups/5/2.jpg', 'path': 'party2/socgroups/5/2.jpg'},
    {'name': 'party2/locations/1/1.jpg', 'path': 'party2/locations/1/1.jpg'},
    {'name': 'party2/locations/2/1.jpg', 'path': 'party2/locations/2/1.jpg'},
    {'name': 'party2/locations/3/1.jpg', 'path': 'party2/locations/3/1.jpg'},
    {'name': 'party2/locations/4/1.jpg', 'path': 'party2/locations/4/1.jpg'},
    {'name': 'party2/locations/5/1.jpg', 'path': 'party2/locations/5/1.jpg'},
    {'name': 'party2/locations/1/2.jpg', 'path': 'party2/locations/1/2.jpg'},
    {'name': 'party2/locations/2/2.jpg', 'path': 'party2/locations/2/2.jpg'},
    {'name': 'party2/locations/3/2.jpg', 'path': 'party2/locations/3/2.jpg'},
    {'name': 'party2/locations/4/2.jpg', 'path': 'party2/locations/4/2.jpg'},
    {'name': 'party2/locations/5/2.jpg', 'path': 'party2/locations/5/2.jpg'},
//    {'name': 'party1/people/1.png', 'path': 'party1/people/1.png'},
//    {'name': 'party1/people/2.png', 'path': 'party1/people/2.png'},
//    {'name': 'party1/people/3.png', 'path': 'party1/people/3.png'},
//    {'name': 'party1/people/4.png', 'path': 'party1/people/4.png'},
//    {'name': 'party1/people/5.png', 'path': 'party1/people/5.png'},
//    {'name': 'party1/socialSit/1/1.jpg', 'path': 'party1/socialSit/1/1.jpg'},
//    {'name': 'party1/socialSit/2/1.jpg', 'path': 'party1/socialSit/2/1.jpg'},
//    {'name': 'party1/socialSit/3/1.jpg', 'path': 'party1/socialSit/3/1.jpg'},
//    {'name': 'party1/socialSit/4/1.jpg', 'path': 'party1/socialSit/4/1.jpg'},
//    {'name': 'party1/socialSit/5/1.jpg', 'path': 'party1/socialSit/5/1.jpg'},
//    {'name': 'party1/socialSit/1/2.jpg', 'path': 'party1/socialSit/1/2.jpg'},
//    {'name': 'party1/socialSit/2/2.jpg', 'path': 'party1/socialSit/2/2.jpg'},
//    {'name': 'party1/socialSit/3/2.jpg', 'path': 'party1/socialSit/3/2.jpg'},
//    {'name': 'party1/socialSit/4/2.jpg', 'path': 'party1/socialSit/4/2.jpg'},
//    {'name': 'party1/socialSit/5/2.jpg', 'path': 'party1/socialSit/5/2.jpg'},
//    {'name': 'party1/socgroups/1/1.jpg', 'path': 'party1/socgroups/1/1.jpg'},
//    {'name': 'party1/socgroups/2/1.jpg', 'path': 'party1/socgroups/2/1.jpg'},
//    {'name': 'party1/socgroups/3/1.jpg', 'path': 'party1/socgroups/3/1.jpg'},
//    {'name': 'party1/socgroups/4/1.jpg', 'path': 'party1/socgroups/4/1.jpg'},
//    {'name': 'party1/socgroups/5/1.jpg', 'path': 'party1/socgroups/5/1.jpg'},
//    {'name': 'party1/socgroups/1/2.jpg', 'path': 'party1/socgroups/1/2.jpg'},
//    {'name': 'party1/socgroups/2/2.jpg', 'path': 'party1/socgroups/2/2.jpg'},
//    {'name': 'party1/socgroups/3/2.jpg', 'path': 'party1/socgroups/3/2.jpg'},
//    {'name': 'party1/socgroups/4/2.jpg', 'path': 'party1/socgroups/4/2.jpg'},
//    {'name': 'party1/socgroups/5/2.jpg', 'path': 'party1/socgroups/5/2.jpg'},
//    {'name': 'party1/locations/1/1.jpg', 'path': 'party1/locations/1/1.jpg'},
//    {'name': 'party1/locations/2/1.jpg', 'path': 'party1/locations/2/1.jpg'},
//    {'name': 'party1/locations/3/1.jpg', 'path': 'party1/locations/3/1.jpg'},
//    {'name': 'party1/locations/4/1.jpg', 'path': 'party1/locations/4/1.jpg'},
//    {'name': 'party1/locations/5/1.jpg', 'path': 'party1/locations/5/1.jpg'},
//    {'name': 'party1/locations/1/2.jpg', 'path': 'party1/locations/1/2.jpg'},
//    {'name': 'party1/locations/2/2.jpg', 'path': 'party1/locations/2/2.jpg'},
//    {'name': 'party1/locations/3/2.jpg', 'path': 'party1/locations/3/2.jpg'},
//    {'name': 'party1/locations/4/2.jpg', 'path': 'party1/locations/4/2.jpg'},
//    {'name': 'party1/locations/5/2.jpg', 'path': 'party1/locations/5/2.jpg'},
  ]
});



const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

flowScheduler.add(setText,"You'll view sets of 3 images comprising locations, groups and activities corresponding to an individual. When viewing the 3 images, please imagine the listed person performing the given activity in the displayed location with the presented group of people. Please try to remember these events that you imagine since they'll be needed to accurately assign the presented individual to specific roles in a TASKNAME.");
flowScheduler.add(routText);
flowScheduler.add(routAbeg)
flowScheduler.add(routA,1,1);
flowScheduler.add(routAEnd)
/flowScheduler.add(routBbeg,1,1,2);
flowScheduler.add(routB,1,2);
flowScheduler.add(routBIters,2,2);
flowScheduler.add(setText,"Based on the set of images you have just seen for each individual, please rank which individual would be the first, second, and third best for each role in TASKNAME. To rank the individual for a role, you'll need to click the photo of an individual and drop them to the rank placeholder for the role. Please rank them as quickly and accurately as possible. Also, note that no individual can be ranked first, second, or third in multiple roles")
flowScheduler.add(routText);
flowScheduler.add(routCbeg,2);
flowScheduler.add(routC);
flowScheduler.add(routCConfbeg);
flowScheduler.add(routCConf);
flowScheduler.add(setText,"You'll now view a series of reference images. You will need to choose which of the two images at the bottom left and right of the screen was previously paired with a reference image as quickly and accurately as possible by either pressing the left or right button on the keyboard.")
flowScheduler.add(routText);
flowScheduler.add(routDbeg,10);
flowScheduler.add(routD,10);
flowScheduler.add(quitPsychoJS, '', true);

dialogCancelScheduler.add(quitPsychoJS, '', false);
var _ready_allKeys;
const clock = new util.Clock();

var Bim_positions;

var BLim_positions;
let lArr = [...Array(5).keys()].map((k) => (k-2)/7.5);

var Cpim_positions = {};

var Ctim_positions = {}

var Npim_positions = {};

// tFixation is for controlling the fixation stimuli
// tBegin is for controlling the triplet timing
// timeCF is for controlling the response time for confidence ratings
// timeRank is for controlling the ranking response time
// timeDec is for controlling the memory retrieval response time
var tFixation;
var tBegin;
var timeCF;
var timeRank;
var timeDec;

//const fixation = new visual.GratingStim({win: psychoJS.window,opacity:1,tex:null,pos:[0,0], mask:'gauss', sf:0, size:0.02, name:'fixation', autoLog:false});
const fixation = new visual.TextStim({win: psychoJS.window,name:'Text',
        text:"+",
        font:'Arial',
        units:'height', pos:[0, 0], height:0.05, wrapWidth:null, ori:0,
        color:'white', colorSpace:'rgb', opacity:1,
        languageStyle:'LTR',
        depth:0.0});

var instrText = new visual.TextStim({win:psychoJS.window, name:'Text',
        font:'Arial',
        units:'height', pos:[0, 0], height:0.05, wrapWidth:null, ori:0,
        color:'white', colorSpace:'rgb', opacity:1,
        languageStyle:'LTR',
        depth:0.0});
var confText = new visual.TextStim({win:psychoJS.window, name:'Text',
        font:'Arial',
        units:'height', pos:[0, 0], height:0.05, wrapWidth:null, ori:0,
        color:'white', colorSpace:'rgb', opacity:1,
        languageStyle:'LTR',
        depth:0.0});
var notReady;


var frames;
var mouse = new core.Mouse({win:psychoJS.window});

const ready = new core.Keyboard({psychoJS: psychoJS});

async function saveRes(){
    if (frames % 600 == 0){
        psychoJS.experiment.save();
    }
}
async function routAbeg(){
    frames = 0;
     tFixation = clock.getTime() 
    // Setup stimulus
    notReady = true;
    
    const FR = 60;
    

    _ready_allKeys = [];
    fixation.autoDraw = true;
    return Scheduler.Event.NEXT;
}

async function routAEnd(){
    tFixation = clock.getTime();
    _ready_allKeys = [];
    fixation.autoDraw = false;
    return Scheduler.Event.NEXT;
}

function routA(time, trials){
    if (clock.getTime() - tFixation< time){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == "escape"){return quitPsychoJS()}
        }
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }
    return Scheduler.Event.NEXT;
};

var people,seen,situation,sitimages,localation,locimages,socgroups,socimages;
var tpeople,seen,tsituation,tsitimages,tlocalation,tlocimages,tsocgroups,tsocimages;
var party;
var lStim;
let labels = ["Situation","Group","Location"];
var TextStims = [];

var locs,socs,sits,trials;
var trialT;
var selected,postselect,iters,indices;
var groupays,locays,sitays;

async function routBbeg(time,trialtime,nParty){
    let party = "party" + nParty;
    Bim_positions = {0: [0, 0.25],
                1: [0.6, -0.25],
                2: [-0.0, -0.25],
                3: [-0.6, -0.25]};


    BLim_positions = {1: [0.6, -0.45],
                2: [-0.0, -0.45],
                3: [-0.6, -0.45]};

    for (let i = 0; i < labels.length; i++){
        let t = labels[i];
        TextStims.push(new visual.TextStim({win: psychoJS.window,text:t,height:0.05,pos:BLim_positions[i+1],name:t,wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0}));
//        TextStims[i].autoDraw = true
    };

    people = [...Array(5).keys()].map((k)=>party+"/people/"+(k+1)+".png");
    seen = [...Array(people.length).keys()].map((k) => 0);
    situation = [...Array(5).keys()].map((s)=>party+"/socialSit/"+(s+1));
    situation = shuffler(situation);
    sitimages = situation.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    localation = [...Array(5).keys()].map((s)=>party+"/locations/"+(s+1));
    localation = shuffler(localation);
    locimages = localation.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    socgroups = [...Array(5).keys()].map((s)=>party+"/socgroups/"+(s+1));
    socgroups = shuffler(socgroups);
    socimages = socgroups.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    tpeople = [...Array(5).keys()].map((k)=>party+"/people/"+(k+1)+".png");
    tsituation = [...Array(5).keys()].map((s)=>party+"/socialSit/"+(s+1));
    tsituation = shuffler(tsituation);
    tsitimages = tsituation.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    tlocalation = [...Array(5).keys()].map((s)=>party+"/locations/"+(s+1));
    tlocalation = shuffler(tlocalation);
    tlocimages = tlocalation.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    tsocgroups = [...Array(5).keys()].map((s)=>party+"/socgroups/"+(s+1));
    tsocgroups = shuffler(tsocgroups);
    tsocimages = tsocgroups.map((s)=>[...Array(2).keys()].map((ss)=> (ss+1)+".jpg"));

    lStim = [];
    trials = people.length;
    locs = [...Array(socgroups.length).keys()].map((k)=>true);
    socs = [...Array(socgroups.length).keys()].map((k)=>true);
    sits = [...Array(socgroups.length).keys()].map((k)=>true);

    let persons =  [...Array(5).keys()].map((s)=>people[s]);
    locays = [...Array(5).keys()].map((k)=>[]);
    sitays = [...Array(5).keys()].map((k)=>[]);
    groupays = [...Array(5).keys()].map((k)=>[]);
    indices = [...Array(3).keys()].map((k)=>k+1);

    for (let i = 0; i < 5; i++){
        for (let j = 0; j < 2; j++){
            locays[i].push(localation[i]+"/"+locimages[i][j]);
            sitays[i].push(situation[i]+"/"+sitimages[i][j]);
            groupays[i].push(socgroups[i]+"/"+socimages[i][j]);
        };
    };
    let stimlist = [persons,sitays,groupays,locays];
    // What a wild line. I had this in python to do a deep copy, wonder if it's
    // necessary here too?
    let Stims = [...Array(stimlist.length).keys()].map((i)=>[...Array(stimlist[i].length).keys()].map((j)=>stimlist[i][j]));
    psychoJS.experiment.addData("Stimuli",Stims);
    trialT = 0
    tFixation = clock.getTime();
    selected = false;
    postselect = true;
    return Scheduler.Event.NEXT;
}
var person,Person,indsit,indloc,indsoc,socim,locim,sgroupim,SocialSit,SocialGroup,Location;
function routB(time,trialtime){

    let t = trialT
    if(postselect){
        fixation.autoDraw = true;
        let ret = routA(time,1);
        if (ret === Scheduler.Event.FLIP_REPEAT){
            return ret;
        }else{
            fixation.autoDraw = false;
            postselect = false;
            selected = false;
            if (t <= 5){for (let j = 0; j < TextStims.length;j++){TextStims[j].autoDraw = true}}
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        }
    }

    if (!selected){
        selected = true;
        let selectperson = getRandInt(0,tpeople.length-1)

        while (seen[selectperson] >= 2){
            tpeople.splice(selectperson,1);
            seen.splice(selectperson,1);
            tsituation.splice(selectperson,1);
            tsitimages.splice(selectperson,1);
            tlocalation.splice(selectperson,1);
            tlocimages.splice(selectperson,1);
            tsocgroups.splice(selectperson,1);
            tsocimages.splice(selectperson,1);
            selectperson = getRandInt(0,tpeople.length-1)
        };
   
        seen[selectperson] += 1;
        person = tpeople[selectperson];
        indsit, indloc, indsoc;
        if (sits[selectperson]){
            indsit = getRandInt(0,2);
            sits[selectperson]=false;
        }
        else{indsit = indsit ^ 1};
    
        if (locs[selectperson]){
            indloc = getRandInt(0,2);
            locs[selectperson]=false;
        }
        else{indloc = indloc ^ 1};
    
        if (socs[selectperson]){
            indsoc = getRandInt(0,2);
            socs[selectperson]= false;
        }
        else{indsoc = indsoc ^ 1;}
    
        socim = tsituation[selectperson]+"/"+tsitimages[selectperson][indsit];
        locim = tlocalation[selectperson]+"/"+tlocimages[selectperson][indloc];
        sgroupim = tsocgroups[selectperson]+"/"+tsocimages[selectperson][indsoc];
 
        if (t >= 5){indices = shuffler(indices)};
        Person = new visual.ImageStim({win:psychoJS.window,image:person,size:[.25,.25], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[0],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit = new visual.ImageStim({win:psychoJS.window,image:socim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[0]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialGroup = new visual.ImageStim({win:psychoJS.window,image:sgroupim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[1]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        Location = new visual.ImageStim({win:psychoJS.window,image:locim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[2]], color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit.autoDraw = true
        Person.autoDraw = true
        SocialGroup.autoDraw = true
        Location.autoDraw = true

        lStim.push([person, socim,sgroupim,locim]);
        tBegin = clock.getTime();
        if (t == 5){for (let j = 0; j < TextStims.length; j++){TextStims[j].autoDraw = false}};
    }

    if(clock.getTime() - tBegin < trialtime){
        Person.opacity /= 1.01;

        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == "escape"){return quitPsychoJS()}
            if(ready.keys == "k"){
                selected = false;
                SocialSit.autoDraw = false
                Person.autoDraw = false
                SocialGroup.autoDraw = false
                Location.autoDraw = false
                postselect = true;
                for (let j = 0; j < TextStims.length; j++){TextStims[j].autoDraw = false};

                return Scheduler.Event.NEXT}
        }
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }else{
        trialT += 1
        tFixation = clock.getTime();
        selected = false;
        SocialSit.autoDraw = false
        Person.autoDraw = false
        SocialGroup.autoDraw = false
        Location.autoDraw = false
        postselect = true;
        for (let j = 0; j < TextStims.length;j++){TextStims[j].autoDraw = false}
        if (trialT >= trials*2){
            trialT = 0;
            return Scheduler.Event.NEXT;
        }else{
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT
        };
    };
}

function routBIters(iterations,trialtime){
    let lind = trialT
    if (lind % lStim.length == 0){
        lStim = shuffler(lStim);
    }
    if(postselect){
        fixation.autoDraw = true;
        let ret = routA(1,1);
        if (ret === Scheduler.Event.FLIP_REPEAT){
            return ret;
        }else{
            fixation.autoDraw = false;
            postselect = false;
            tBegin = clock.getTime();
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        }
    }
    if (!selected){
        selected = true;
        tBegin = clock.getTime();
        let t = lind % lStim.length;
        [person,socim,sgroupim,locim] = lStim[t];
        indices = shuffler(indices);
        Person = new visual.ImageStim({win:psychoJS.window,image:person,size:[.25,.25], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[0],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit = new visual.ImageStim({win:psychoJS.window,image:socim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[0]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialGroup = new visual.ImageStim({win:psychoJS.window,image:sgroupim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[1]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        Location = new visual.ImageStim({win:psychoJS.window,image:locim,size:[.33, .33], mask : undefined, anchor : 'center', ori : 0, pos: Bim_positions[indices[2]], color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit.autoDraw = true;
        Person.autoDraw = true;
        SocialGroup.autoDraw = true;
        Location.autoDraw = true;
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }

    if (clock.getTime() - tBegin < trialtime){
        Person.opacity /= 1.01;
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == "escape"){return quitPsychoJS()}
            if(ready.keys == "k"){
                selected = false;
                SocialSit.autoDraw = false
                Person.autoDraw = false
                SocialGroup.autoDraw = false
                Location.autoDraw = false
                return Scheduler.Event.NEXT}
        }
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }else{
        trialT += 1
        tFixation = clock.getTime();
        selected = false;
        SocialSit.autoDraw = false
        Person.autoDraw = false
        SocialGroup.autoDraw = false
        Location.autoDraw = false
        postselect = true;
        if (trialT > trials*iterations){
            trialT = 0;
            return Scheduler.Event.NEXT;
        }else{
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT
        };
    };
};


function routOK(){
    let keys = ready.getKeys({keyList:[], waitRelease:false});
    _ready_allKeys = [].concat(keys);
    let ret = null;
    if (_ready_allKeys.length > 0) {
        ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
        ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
        ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
        if (ready.keys == 'r'){
            okroutRun = false;
            let ret = 'r';
            return 'r';
        };
        if (ready.keys == 'k'){
            okroutRun = false;
            let ret = 'k';
            return 'k';
        };
    };
    return ret;
};

function checkTs(ind,db){
    let ret = -1;
    for (let key = 0; key < Object.keys(db).length; key++){ if (db[key] == ind){ return key} };
    return ret;
}
var tasksAll = [["DJ","Desserts","Barbecue","Decorations","Clean Up"],
            ["Fisher","Deckhand","Steering","Captain","Radio Operator"]];
var pStim,tStim,tasks,rankStims,questStim,running;
var c,mousePersonIndex, mouseTaskIndex, count,mouseIsDown,mouseIsTaskDown,mouseIsPersonDown,okroutRun;
var lineKeys, linetKeys,lines,personRank;
var mouseIdleTime,mousePrevPos;
async function routCbeg(nParty){
    tasks = tasksAll[nParty-1]
    pStim = {};
    tStim = {};

    for (let i = 0; i < lArr.length; i++){
        Cpim_positions[i] = [0.5,lArr[i]];
    };

    for (let i = 0; i < lArr.length; i++){
        Ctim_positions[i] = [-0.5,lArr[i]];
    };

    for (let i = 0; i < lArr.length; i++){
        Npim_positions[i] = [0.65,lArr[i]-0.05];
    };

    for (let i = 0; i < people.length; i++){
        let p = people[i];
        pStim[i] = new visual.ImageStim({win:psychoJS.window,image:p,name:"Person " + i,pos:Cpim_positions[i],size:[0.1,0.1],color:'white'});
        pStim[i].autoDraw=true;
    };
    for (let i = 0; i < tasks.length; i++){
        let t = tasks[i];
        tStim[i] = new visual.TextStim({win:psychoJS.window,text:t,height:0.05,pos:Ctim_positions[i],name:t,color:'white'});
        tStim[i].autoDraw=true;
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
            lines[i][j] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:[tStim[i].pos[0]+0.25+0.25*j,tStim[i].pos[1]],size:[0.1,0.1]});
            lines[i][j].autoDraw = true
            linetKeys[i][j] = null;
        };
    };
    rankStims = [];
    for (let j = 0; j < 3; j++){
        let pos = [tStim[people.length-1].pos[0] + 0.25+0.25*j,0.4];
        rankStims.push(new visual.TextStim({win:psychoJS.window,text:j,pos:pos,
                    height:0.05, wrapWidth:null, ori:0, color:'white',
                    colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0,font:'Arial', units:'height'}));
        rankStims[j].autoDraw = true;
    };
    questStim = new visual.TextStim({win:psychoJS.window, name:'endText', text:'If this looks correct to you, please press \'k\', otherwise press \'r\'', font:'Arial', units:'height', pos:[tStim[0].pos[0]+0.5, tStim[0].pos[1]-0.15], height:0.05, wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0});

    c = ['red','green','blue'];
    mousePersonIndex = -1;
    mouseTaskIndex = -1;
    timeRank = clock.getTime();
    count = 0;
    mouseIsDown = false;
    mouseIsTaskDown = false;
    mouseIsPersonDown = false;
    okroutRun = false;
    mouseIdleTime = clock.getTime();
    mousePrevPos = mouse.getPos();
    return Scheduler.Event.NEXT;
}

function routC(){

    if (running){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == 'escape'){return quitPsychoJS()};
            if (ready.keys == 'k'){running = false};
            if (ready.keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    for (let j = 0; j < 3; j++){lines[i][j].autoDraw=false}
                    lines[i] = {};
                };
                for (let i = 0; i< people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 3; j++){
                        lines[i][j] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:[tStim[i].pos[0]+0.25+0.25*j,tStim[i].pos[1]],size:[0.1,0.1]});
                        lines[i][j].autoDraw=true
                        linetKeys[i][j] = null;
                    };
                };
                questStim.autoDraw = false;
            };
        };

        // Kick out the user if their mouse has been idle for to long
        if (mousePrevPos[0] != mouse.getPos()[0] && mousePrevPos[1] != mouse.getPos()[1]){
            mousePrevPos = mouse.getPos();
            mouseIdleTime = clock.getTime();
        };
        if (clock.getTime() - mouseIdleTime >=60){return quitPsychoJS("Kicked out for being idle for too long")};

        for (let i = 0; i < Object.keys(lineKeys).length; i++){
            let l = lineKeys[i];
            let temp = Object.keys(l).length
            if (temp == 3 && pStim[i].opacity != 0.8){pStim[i].opacity= 0.8;console.log("Turning RED")}
            else if (temp != 3 && pStim[i].opacity!= 1){pStim[i].opacity= 1; console.log("TURNING WHITE")};
        };

        let clines = 0;
        for (let i = 0; i < Object.keys(linetKeys).length; i++){
            let l = linetKeys[i];
            let temp = 0;
            for (let j = 0; j < Object.keys(l).length; j++){
                if (l[j]!=null)
                    temp += 1;
            };
            clines += temp;
            if (temp == 3 && tStim[i].color != [1,-1,-1] != 'red'){tStim[i].color='red'}
            else if (tStim[i].color != 'white'){tStim[i].color='white'};
        };
        if (clines == 3*tasks.length){
            okroutRun = true;
            questStim.autoDraw = true;
        }

        if (okroutRun){
            keys = routOK();
            if (keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    for (let j = 0; j < 3; j++){lines[i][j].autoDraw = false};
                    lines[i] = {};
                };
                for (let i = 0; i < people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 3; j++){
                        lines[i][j] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:[tStim[i].pos[0]+0.25+0.25*j,tStim[i].pos[1]],size:[0.1,0.1]});
                        lines[i][j].autoDraw = true;
                        linetKeys[i][j] = null;
                    };
                };
                questStim.autoDraw = false;
            }
            else if (keys == 'k'){running = false};
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        };
        if (mouse.getPressed()[0] == 1 && mouseIsDown == false){
            mouseIsDown = true;
            mousePersonIndex = -1;
            for (let key = 0; key < people.length; key++){
                let item = pStim[key];
                if (item.contains(mouse)){
                    item.size = [item.size[0]*1.5,item.size[1]*1.5];
                    mousePersonIndex = key;
                    mouseIsPersonDown = true;
                    break;
                };
            };
        };

        if (mouse.getPressed()[0] == 0 && ! mouseIsTaskDown && ! mouseIsPersonDown){mouseIsDown = false};

        if (mouse.getPressed()[0] == 0 && mouseIsPersonDown){
            if (mousePersonIndex == -1){ mouseIsDown = false; mouseIsPersonDown = false}
            else{
                count = 0;
                mouseIsDown = false;
                mouseIsPersonDown = false;
                pStim[mousePersonIndex].size = [pStim[mousePersonIndex].size[0]/1.5,pStim[mousePersonIndex].size[1]/1.5];
                let key = -1;
                let rank = -1;
                for (let k = 0; k < 5 ; k++){
                    let item = lines[k];
                    for (let kk = 0; kk < 3; kk++){
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
                        let pastkey = lineKeys[mousePersonIndex][rank];
                        delete lineKeys[mousePersonIndex][rank];
                        if (rank in linetKeys[pastkey]){linetKeys[pastkey][rank] = null};
                        let pos = [tStim[pastkey].pos[0] + 0.25+0.25*rank,tStim[pastkey].pos[1]];
                        lines[pastkey][rank].autoDraw = false;
                        lines[pastkey][rank] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:pos,size:[0.1,0.1]});
                        lines[pastkey][rank].autoDraw = true;
                    }
                    // If this person was already assigned this task before
                    let pastrank = checkTs(mousePersonIndex, linetKeys[key]);
                    if (pastrank != -1){
                        if (pastrank in linetKeys[key]){linetKeys[key][pastrank] = null};
                        if (pastrank in lineKeys[mousePersonIndex]){delete lineKeys[mousePersonIndex][pastrank]};
                        let pos = [tStim[key].pos[0] + 0.25+0.25*pastrank,tStim[key].pos[1]];
                        lines[key][pastrank].autoDraw = false;
                        lines[key][pastrank] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:pos,size:[0.1,0.1]});
                        lines[key][pastrank].autoDraw = true;
                    };
                    // If someone is already occupying this task rank, properly
                    // overwrite their occupation wit the new person
                    if (rank in linetKeys[key] && linetKeys[key][rank]){delete lineKeys[linetKeys[key][rank]][rank]};
                    lineKeys[mousePersonIndex][rank] = key;
                    linetKeys[key][rank] = mousePersonIndex;
                    lines[key][rank].autoDraw = false;
                    lines[key][rank] = new visual.ImageStim({win:psychoJS.window, image:people[mousePersonIndex],pos:lines[key][rank].pos,size:[0.1,0.1]});
                    lines[key][rank].autoDraw = true;
                    console.log(key,"to",mousePersonIndex);
                };
                mousePersonIndex = -1;
            };
        }; 
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }else{
        let RT = clock.getTime() - timeRank;
        psychoJS.experiment.addData("rankRT",RT);
        for (let i = 0; i < Object.keys(lines).length; i++){
            for (let j = 0; j < Object.keys(lines[i]).length;j++){
                lines[i][j].autoDraw = false;
            }
            pStim[i].autoDraw = false;
            tStim[i].autoDraw = false;
        }
        for (let i = 0; i < 3; i++){
            rankStims[i].autoDraw = false;
        }

        for (let key = 0; key < lineKeys.length; key++){
            let item = lineKeys[key];
            allKeys = item.keys();
            sortedKeys = allKeys.sort();
            newdict = {};
            for (let i = 0; i < sortedKeys; i++){newdict[i] = item[sortedKeys[i]]};
            lineKeys[key] = newdict;
        };
        questStim.autoDraw = false;
        psychoJS.experiment.addData("rankDec",lineKeys);
        return Scheduler.Event.NEXT;
    }
};

var textConf,slider;
async function routCConfbeg(){
    notReady = true;
    timeCF = clock.getTime();
    textConf = new visual.TextStim({win:psychoJS.window, name:'endText',
                text:'How confident are you? Adjust the slider, and press spacebar to continue',
                font:'Arial',
                units:'height', pos:[0, 0.35], height:0.05, wrapWidth:null, ori:0,
                color:'white', colorSpace:'rgb', opacity:1,
                languageStyle:'LTR',
                depth:0.0});
    slider = new visual.Slider({win:psychoJS.window,labels: ["1", "2", "3","4","5","6","7"],ticks:[1,2,3,4,5,6,7],granularity:0,pos:[0,0],size:[1,0.1]});
    slider.autoDraw = true;
    textConf.autoDraw = true;
    return Scheduler.Event.NEXT;
}

function routCConf(){
    let ret = routDc();
    // Kick user out if they take too long to report their confidence
    if (clock.getTime() - timeCF >= 60){return quitPsychoJS("Kicked out for being idle for too long")};

    if (ret != null){
        psychoJS.experiment.addData("rankconf",ret[0]);
        psychoJS.experiment.addData("rankconfRT",ret[1]);
        slider.autoDraw = false;
        textConf.autoDraw = false;
        notReady = false;
        slider.reset();
        return Scheduler.Event.NEXT;
    }
    else{
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }
};


var pind,eind,corruption,otherchoice,bwgroup
var choices,confidences,RTs,confRTs,correct;
var doingConf,selectedLR,leftorRight;
var choice;
var Stimuls;
var situationIm,socgroupsIm,locationIm;

async function routDbeg(trials){

    pind = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,5)));
    // Episode Select
    eind = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2)));
    // Reference cue
    corruption = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,3)));
    // Query cues
    otherchoice = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2)));
    // Between or within person corruption
    bwgroup = shuffler([...Array(trials).keys()].map((i)=>getRandInt(0,2)));
    choices = [];
    confidences = [];
    RTs = [];
    confRTs = [];
    correct = [];
    trialT = 0;
    choice = 0;
    doingConf = false;
    okroutRun = false;
    selectedLR = false;
    postselect = false;
    Stimuls = [];
    psychoJS.experiment.addData("Reference",corruption);
    psychoJS.experiment.addData("Query", otherchoice);
    psychoJS.experiment.addData("BWgroup", bwgroup);
    return Scheduler.Event.NEXT;
}

function routD(trials){
    let t = trialT;
    if (trialT >= trials){
        psychoJS.experiment.addData("Choice",choices);
        psychoJS.experiment.addData("correctChoice",correct);
        psychoJS.experiment.addData("retrievalConf",confidences);
        psychoJS.experiment.addData("retrievalRT",RTs);
        psychoJS.experiment.addData("retrievalConfRT",confRTs);
        return Scheduler.Event.NEXT;

    }

    if(postselect){
        fixation.autoDraw = true;
        let ret = routA(1,1);
        if (ret == Scheduler.Event.FLIP_REPEAT){
            return ret;
        }else{
            fixation.autoDraw = false;
            postselect = false;
            doingConf = false;
            selectedLR = false;
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        }
    }
    if (doingConf){
        let ret = routDc();
        // Kick user out if they take too long to report their confidence
        if (clock.getTime() - timeCF >= 60){return quitPsychoJS("Kicked out for being idle for too long")};
        if (ret != null){
            confidences.push(ret[0]);
            confRTs.push(ret[1]);
            slider.autoDraw = false;
            textConf.autoDraw = false;
            doingConf = false;
            notReady = false;
            postselect = true;
            slider.reset();
            tFixation = clock.getTime();
            choice = 0;
            trialT += 1;
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        }
        else{
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT;
        }
    }
    if (!selectedLR){
        leftorRight = getRandInt(0,2)*2-1;
        correct.push(leftorRight);
        selectedLR = true;
        let p = pind[t];
        let e = eind[t];
        let corr = corruption[t];
        let oc = otherchoice[t];
        let bw = bwgroup[t];
        let c = 0;
        let chooses = [];
        let choose;
        console.log(t,trials,p,e,corr,oc,bw,c);
        if (corr == 0){
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:sitays[p][e]}));
            if (oc == 0){
                if (bw == 1){
                    for (let i=0; i < groupays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(groupays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = groupays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:groupays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            }
            else if (oc == 1){
                if (bw == 1){
                    for (let i=0; i < locays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(locays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = locays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:locays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            };
        }
        else if (corr == 1){
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:groupays[p][e]}));
            if (oc == 0){
                if (bw == 1){
                    for (let i=0; i < sitays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(sitays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = sitays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:sitays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            }
            else if (oc == 1){
                if (bw == 1){
                    for (let i=0; i < locays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(locays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = locays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:locays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            };
        }
        else if (corr == 2){
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:locays[p][e]}));
            if (oc == 0){
                if (bw == 1){
                    for (let i=0; i < sitays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(sitays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = sitays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:sitays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            }
            else if (oc == 1){
                if (bw == 1){
                    for (let i=0; i < groupays.length; i++){for (let j = 0; j < 2; j++){if (i != p){chooses.push(groupays[i][j])}}}
                    choose = chooses[getRandInt(0,chooses.length)];
                    console.log("HELLO2");
                }
                else{console.log("HELLO");choose = groupays[p][e^1]};
                console.log(bw);
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:groupays[p][e]}));
                Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
            };
        };
        for (let k = 0; k < Stimuls.length; k++){Stimuls[k].size = [.33, .33]};
        Stimuls[0].pos = Bim_positions[0];
        if (leftorRight == -1){
            Stimuls[1].pos = Bim_positions[3];
            Stimuls[2].pos = Bim_positions[1];
        }
        else{
            Stimuls[1].pos = Bim_positions[1];
            Stimuls[2].pos = Bim_positions[3];
        };
        Stimuls[0].autoDraw = true;
        Stimuls[1].autoDraw = true;
        Stimuls[2].autoDraw = true;
        timeDec = clock.getTime();
    }

    if (choice == 0){
        // Kick user out of experiment if they take too long to reply
        if (clock.getTime() - timeDec > 60){return quitPsychoJS("Kicked out for being idle for too long")};
        for (let s = 0; s < Stimuls.length; s++){Stimuls[s].draw()};
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == 'escape'){return quitPsychoJS()};
            if (ready.keys == 'k'){
                Stimuls[0].autoDraw = false;
                Stimuls[1].autoDraw = false;
                Stimuls[2].autoDraw = false;
                return Scheduler.Event.NEXT;
            };
            if (ready.keys == 'left'){
                choice = -1;
                let RT = clock.getTime() - timeDec;
                choices.push(choice)
                RTs.push(RT)
                Stimuls[0].autoDraw = false;
                Stimuls[1].autoDraw = false;
                Stimuls[2].autoDraw = false;
                Stimuls = [];
                doingConf = true;
                slider.autoDraw = true;
                textConf.autoDraw = true;
                notReady = true;
                timeCF = clock.getTime()
            }
            else if (ready.keys == 'right'){
                choice = 1;
                let RT = clock.getTime() - timeDec;
                choices.push(choice)
                RTs.push(RT)
                Stimuls[0].autoDraw = false;
                Stimuls[1].autoDraw = false;
                Stimuls[2].autoDraw = false;
                Stimuls = [];
                doingConf = true;
                slider.autoDraw = true;
                textConf.autoDraw = true;
                notReady = true;
                timeCF = clock.getTime()
            };
        };
        let mRT = 0;for(let z = 0; z < RTs.length;z++){mRT += RTs[z]};
        // Kick user out of experiment if they are responding way too fast on
        // average.
        if (mRT/RTs.length <0.1 && RTs.length > 5){return quitPsychoJS("Kicked out for suspiciously fast responses")};
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    };
    return Scheduler.Event.NEXT;
};
function routDc(){
    let ret = null;
    if (notReady){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == 'space'){
                let RT = clock.getTime() - timeCF;
                notReady = false;
                return [slider.getRating(),RT]
            };
        };
    };
    return ret; 
}

function setText(fill){
    instrText.text = fill;
    instrText.autoDraw = true;
    notReady = true
    return Scheduler.Event.NEXT;
}
async function routText(fill){
    
    if(notReady){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == "escape"){return quitPsychoJS()}
            if (ready.keys == "k"){
                notReady = false;
                instrText.autoDraw = false;
                return Scheduler.Event.NEXT;
            }
        };
    };
    frames += 1;
    return Scheduler.Event.FLIP_REPEAT;
};

async function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  psychoJS.experiment.addData("FinishedExperiment",isCompleted);
  if (psychoJS.experiment.isEntryEmpty()) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});

  return Scheduler.Event.QUIT;
};
