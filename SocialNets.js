import {visual, core,util,data,hardware} from 'https://pavlovia.org/lib/psychojs-2023.1.3.js';
const { PsychoJS } = core;
const { Scheduler } = util;

// Random Integer
function getRandInt(bot,topp){
    bot = Math.ceil(bot);
    topp = Math.floor(topp);
    return Math.floor(Math.random()*(topp-bot)+bot);
};

// Shuffler
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
psychoJS.window.color = new util.Color('black')
let expName = 'SocialNets';
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
    {'name': 'exampleStim/people/1.png', 'path': 'exampleStim/people/1.png'},
    {'name': 'exampleStim/socgroups/1/1.jpg', 'path': 'exampleStim/socgroups/1/1.jpg'},
    {'name': 'exampleStim/socialSit/1/1.jpg', 'path': 'exampleStim/socialSit/1/1.jpg'},
    {'name': 'exampleStim/locations/1/1.jpg', 'path': 'exampleStim/locations/1/1.jpg'},

    {'name': 'party1/people/1.png', 'path': 'party1/people/1.png'},
    {'name': 'party1/people/2.png', 'path': 'party1/people/2.png'},
    {'name': 'party1/people/3.png', 'path': 'party1/people/3.png'},
    {'name': 'party1/people/4.png', 'path': 'party1/people/4.png'},
    {'name': 'party1/people/5.png', 'path': 'party1/people/5.png'},
    {'name': 'party1/socialSit/1/1.png', 'path': 'party1/socialSit/1/1.png'},
    {'name': 'party1/socialSit/2/1.png', 'path': 'party1/socialSit/2/1.png'},
    {'name': 'party1/socialSit/3/1.png', 'path': 'party1/socialSit/3/1.png'},
    {'name': 'party1/socialSit/4/1.png', 'path': 'party1/socialSit/4/1.png'},
    {'name': 'party1/socialSit/5/1.png', 'path': 'party1/socialSit/5/1.png'},
    {'name': 'party1/socialSit/1/2.png', 'path': 'party1/socialSit/1/2.png'},
    {'name': 'party1/socialSit/2/2.png', 'path': 'party1/socialSit/2/2.png'},
    {'name': 'party1/socialSit/3/2.png', 'path': 'party1/socialSit/3/2.png'},
    {'name': 'party1/socialSit/4/2.png', 'path': 'party1/socialSit/4/2.png'},
    {'name': 'party1/socialSit/5/2.png', 'path': 'party1/socialSit/5/2.png'},
    {'name': 'party1/locations/1/1.jpg', 'path': 'party1/locations/1/1.jpg'},
    {'name': 'party1/locations/2/1.jpg', 'path': 'party1/locations/2/1.jpg'},
    {'name': 'party1/locations/3/1.jpg', 'path': 'party1/locations/3/1.jpg'},
    {'name': 'party1/locations/4/1.jpg', 'path': 'party1/locations/4/1.jpg'},
    {'name': 'party1/locations/5/1.jpg', 'path': 'party1/locations/5/1.jpg'},
    {'name': 'party1/locations/1/2.jpg', 'path': 'party1/locations/1/2.jpg'},
    {'name': 'party1/locations/2/2.jpg', 'path': 'party1/locations/2/2.jpg'},
    {'name': 'party1/locations/3/2.jpg', 'path': 'party1/locations/3/2.jpg'},
    {'name': 'party1/locations/4/2.jpg', 'path': 'party1/locations/4/2.jpg'},
    {'name': 'party1/locations/5/2.jpg', 'path': 'party1/locations/5/2.jpg'},
    {'name': 'party1/socgroups/1/1.jpg', 'path': 'party1/socgroups/1/1.jpg'},
    {'name': 'party1/socgroups/2/1.jpg', 'path': 'party1/socgroups/2/1.jpg'},
    {'name': 'party1/socgroups/3/1.jpg', 'path': 'party1/socgroups/3/1.jpg'},
    {'name': 'party1/socgroups/4/1.jpg', 'path': 'party1/socgroups/4/1.jpg'},
    {'name': 'party1/socgroups/5/1.jpg', 'path': 'party1/socgroups/5/1.jpg'},
    {'name': 'party1/socgroups/1/2.jpg', 'path': 'party1/socgroups/1/2.jpg'},
    {'name': 'party1/socgroups/2/2.jpg', 'path': 'party1/socgroups/2/2.jpg'},
    {'name': 'party1/socgroups/3/2.jpg', 'path': 'party1/socgroups/3/2.jpg'},
    {'name': 'party1/socgroups/4/2.jpg', 'path': 'party1/socgroups/4/2.jpg'},
    {'name': 'party1/socgroups/5/2.jpg', 'path': 'party1/socgroups/5/2.jpg'},

    {'name': 'party2/people/1.png', 'path': 'party2/people/1.png'},
    {'name': 'party2/people/2.png', 'path': 'party2/people/2.png'},
    {'name': 'party2/people/3.png', 'path': 'party2/people/3.png'},
    {'name': 'party2/people/4.png', 'path': 'party2/people/4.png'},
    {'name': 'party2/people/5.png', 'path': 'party2/people/5.png'},
    {'name': 'party2/socialSit/1/1.png', 'path': 'party2/socialSit/1/1.png'},
    {'name': 'party2/socialSit/2/1.png', 'path': 'party2/socialSit/2/1.png'},
    {'name': 'party2/socialSit/3/1.png', 'path': 'party2/socialSit/3/1.png'},
    {'name': 'party2/socialSit/4/1.png', 'path': 'party2/socialSit/4/1.png'},
    {'name': 'party2/socialSit/5/1.png', 'path': 'party2/socialSit/5/1.png'},
    {'name': 'party2/socialSit/1/2.png', 'path': 'party2/socialSit/1/2.png'},
    {'name': 'party2/socialSit/2/2.png', 'path': 'party2/socialSit/2/2.png'},
    {'name': 'party2/socialSit/3/2.png', 'path': 'party2/socialSit/3/2.png'},
    {'name': 'party2/socialSit/4/2.png', 'path': 'party2/socialSit/4/2.png'},
    {'name': 'party2/socialSit/5/2.png', 'path': 'party2/socialSit/5/2.png'},
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

//    {'name': 'party3/people/1.png', 'path': 'party3/people/1.png'},
//    {'name': 'party3/people/2.png', 'path': 'party3/people/2.png'},
//    {'name': 'party3/people/3.png', 'path': 'party3/people/3.png'},
//    {'name': 'party3/people/4.png', 'path': 'party3/people/4.png'},
//    {'name': 'party3/people/5.png', 'path': 'party3/people/5.png'},
//    {'name': 'party3/socialSit/1/1.png', 'path': 'party3/socialSit/1/1.png'},
//    {'name': 'party3/socialSit/2/1.png', 'path': 'party3/socialSit/2/1.png'},
//    {'name': 'party3/socialSit/3/1.png', 'path': 'party3/socialSit/3/1.png'},
//    {'name': 'party3/socialSit/4/1.png', 'path': 'party3/socialSit/4/1.png'},
//    {'name': 'party3/socialSit/5/1.png', 'path': 'party3/socialSit/5/1.png'},
//    {'name': 'party3/socialSit/1/2.png', 'path': 'party3/socialSit/1/2.png'},
//    {'name': 'party3/socialSit/2/2.png', 'path': 'party3/socialSit/2/2.png'},
//    {'name': 'party3/socialSit/3/2.png', 'path': 'party3/socialSit/3/2.png'},
//    {'name': 'party3/socialSit/4/2.png', 'path': 'party3/socialSit/4/2.png'},
//    {'name': 'party3/socialSit/5/2.png', 'path': 'party3/socialSit/5/2.png'},
//    {'name': 'party3/locations/1/1.jpg', 'path': 'party3/locations/1/1.jpg'},
//    {'name': 'party3/locations/2/1.jpg', 'path': 'party3/locations/2/1.jpg'},
//    {'name': 'party3/locations/3/1.jpg', 'path': 'party3/locations/3/1.jpg'},
//    {'name': 'party3/locations/4/1.jpg', 'path': 'party3/locations/4/1.jpg'},
//    {'name': 'party3/locations/5/1.jpg', 'path': 'party3/locations/5/1.jpg'},
//    {'name': 'party3/locations/1/2.jpg', 'path': 'party3/locations/1/2.jpg'},
//    {'name': 'party3/locations/2/2.jpg', 'path': 'party3/locations/2/2.jpg'},
//    {'name': 'party3/locations/3/2.jpg', 'path': 'party3/locations/3/2.jpg'},
//    {'name': 'party3/locations/4/2.jpg', 'path': 'party3/locations/4/2.jpg'},
//    {'name': 'party3/locations/5/2.jpg', 'path': 'party3/locations/5/2.jpg'},
//    {'name': 'party3/socgroups/1/1.jpg', 'path': 'party3/socgroups/1/1.jpg'},
//    {'name': 'party3/socgroups/2/1.jpg', 'path': 'party3/socgroups/2/1.jpg'},
//    {'name': 'party3/socgroups/3/1.jpg', 'path': 'party3/socgroups/3/1.jpg'},
//    {'name': 'party3/socgroups/4/1.jpg', 'path': 'party3/socgroups/4/1.jpg'},
//    {'name': 'party3/socgroups/5/1.jpg', 'path': 'party3/socgroups/5/1.jpg'},
//    {'name': 'party3/socgroups/1/2.jpg', 'path': 'party3/socgroups/1/2.jpg'},
//    {'name': 'party3/socgroups/2/2.jpg', 'path': 'party3/socgroups/2/2.jpg'},
//    {'name': 'party3/socgroups/3/2.jpg', 'path': 'party3/socgroups/3/2.jpg'},
//    {'name': 'party3/socgroups/4/2.jpg', 'path': 'party3/socgroups/4/2.jpg'},
//    {'name': 'party3/socgroups/5/2.jpg', 'path': 'party3/socgroups/5/2.jpg'},

    {'name': 'party4/people/1.png', 'path': 'party4/people/1.png'},
    {'name': 'party4/people/2.png', 'path': 'party4/people/2.png'},
    {'name': 'party4/people/3.png', 'path': 'party4/people/3.png'},
    {'name': 'party4/people/4.png', 'path': 'party4/people/4.png'},
    {'name': 'party4/people/5.png', 'path': 'party4/people/5.png'},

//    {'name': 'party4/socialSit/1/1.png', 'path': 'party4/socialSit/1/1.png'},
//    {'name': 'party4/socialSit/2/1.png', 'path': 'party4/socialSit/2/1.png'},
//    {'name': 'party4/socialSit/3/1.png', 'path': 'party4/socialSit/3/1.png'},
//    {'name': 'party4/socialSit/4/1.png', 'path': 'party4/socialSit/4/1.png'},
//    {'name': 'party4/socialSit/5/1.png', 'path': 'party4/socialSit/5/1.png'},
//    {'name': 'party4/socialSit/1/2.png', 'path': 'party4/socialSit/1/2.png'},
//    {'name': 'party4/socialSit/2/2.png', 'path': 'party4/socialSit/2/2.png'},
//    {'name': 'party4/socialSit/3/2.png', 'path': 'party4/socialSit/3/2.png'},
//    {'name': 'party4/socialSit/4/2.png', 'path': 'party4/socialSit/4/2.png'},
//    {'name': 'party4/socialSit/5/2.png', 'path': 'party4/socialSit/5/2.png'},
//    {'name': 'party4/locations/1/1.jpg', 'path': 'party4/locations/1/1.jpg'},
//    {'name': 'party4/locations/2/1.jpg', 'path': 'party4/locations/2/1.jpg'},
//    {'name': 'party4/locations/3/1.jpg', 'path': 'party4/locations/3/1.jpg'},
//    {'name': 'party4/locations/4/1.jpg', 'path': 'party4/locations/4/1.jpg'},
//    {'name': 'party4/locations/5/1.jpg', 'path': 'party4/locations/5/1.jpg'},
//    {'name': 'party4/locations/1/2.jpg', 'path': 'party4/locations/1/2.jpg'},
//    {'name': 'party4/locations/2/2.jpg', 'path': 'party4/locations/2/2.jpg'},
//    {'name': 'party4/locations/3/2.jpg', 'path': 'party4/locations/3/2.jpg'},
//    {'name': 'party4/locations/4/2.jpg', 'path': 'party4/locations/4/2.jpg'},
//    {'name': 'party4/locations/5/2.jpg', 'path': 'party4/locations/5/2.jpg'},
//    {'name': 'party4/socgroups/1/1.jpg', 'path': 'party4/socgroups/1/1.jpg'},
//    {'name': 'party4/socgroups/2/1.jpg', 'path': 'party4/socgroups/2/1.jpg'},
//    {'name': 'party4/socgroups/3/1.jpg', 'path': 'party4/socgroups/3/1.jpg'},
//    {'name': 'party4/socgroups/4/1.jpg', 'path': 'party4/socgroups/4/1.jpg'},
//    {'name': 'party4/socgroups/5/1.jpg', 'path': 'party4/socgroups/5/1.jpg'},
//    {'name': 'party4/socgroups/1/2.jpg', 'path': 'party4/socgroups/1/2.jpg'},
//    {'name': 'party4/socgroups/2/2.jpg', 'path': 'party4/socgroups/2/2.jpg'},
//    {'name': 'party4/socgroups/3/2.jpg', 'path': 'party4/socgroups/3/2.jpg'},
//    {'name': 'party4/socgroups/4/2.jpg', 'path': 'party4/socgroups/4/2.jpg'},
//    {'name': 'party4/socgroups/5/2.jpg', 'path': 'party4/socgroups/5/2.jpg'},
  ]
});



const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

var TASKNAME = ["Birthday Party", 
    "Fishing Crew", 
    "School Project",
    "Home Construction"];

var tasksAll = [["DJ", "Desserts", "Barbecue", "Decorations", "Clean Up"],
            ["Fisher", "Deckhand", "Cook", "Captain", "Radio Operator"],
            ["Experimenter", "Presentation Maker", "Report Writer", "Data Analyst", "Participant Recruiter"],
            ["Contractor", "Architect", "Interior Decorations", "Landscaper", "Realtor"]];

var parties = 2;
flowScheduler.add(setText,"In this experiment, you will be presented 3 images comprising a location, group, and activity corresponding to an individual. Your job is to create a story given these paired images. This will be important for accurately assigning and ranking roles to an individual for a given task.");
flowScheduler.add(routText);
flowScheduler.add(setText, "We will give you one example set of images in a Home Construction scenario to help you understand the experiment.");
flowScheduler.add(routText);
flowScheduler.add(routBExbeg);
flowScheduler.add(routBEx,8);
flowScheduler.add(setText,"A man (RED) is constructing a house (GREEN) on a beach resort (PURPLE) after attending a robotics club with some friends (BLUE)","ExB");
flowScheduler.add(routText,"ExB");
flowScheduler.add(routCbeg,3,"Ex");
flowScheduler.add(setText, "Given a Home Construction scenario, this man will be ranked first for the role of contractor, and second for the role of architect.\n  You will also rank the other individuals using the stories you create with their activity, location, and group images.")
flowScheduler.add(routText,"ExC");
for (let j = 1; j < parties+1; j++){
    flowScheduler.add(setText,"You'll now view sets of 3 images comprising locations, groups and activities corresponding to an individual. When viewing the 3 images, please imagine the listed person performing the given activity in the displayed location with the presented group of people. Please try to remember these events that you imagine. You will later need to accurately assign specific roles to the individuals seen for a " + TASKNAME[j-1] + ".");
    flowScheduler.add(routText);
    flowScheduler.add(routAbeg)
    flowScheduler.add(routA,1,1);
    flowScheduler.add(routAEnd)
    flowScheduler.add(routBbeg,1,j);
    flowScheduler.add(routB,2,8);
    flowScheduler.add(setText,"Based on the set of images you have just seen for each individual, please rank which individual would be the first and second best for each role in " + TASKNAME[j-1] + ". To rank the individual for a role, you'll need to click the photo of an individual and drop them to the rank placeholder for the role.");
    flowScheduler.add(routText);
    flowScheduler.add(setText,"Please rank them as quickly and accurately as possible. You can always overwrite an assigned rank for a role by dragging a person from the right column to the ranking. Also, note that individuals can be ranked first or second only once.")
    flowScheduler.add(routText);
    flowScheduler.add(routCbeg,j);
    flowScheduler.add(routC);
    flowScheduler.add(routCConfbeg);
    flowScheduler.add(routCConf);
    flowScheduler.add(setText,"You'll now view a series of reference images. You will need to choose which of the two images at the bottom left and right of the screen was previously paired with a reference image. Please answer as quickly and accurately as possible by either pressing the left or right arrow on the keyboard.")
    flowScheduler.add(routText);
    flowScheduler.add(routDbeg,10);
    flowScheduler.add(routD,40);
}
flowScheduler.add(selfRankBeg);
flowScheduler.add(selfRank);
flowScheduler.add(quitPsychoJS, '', true);
dialogCancelScheduler.add(quitPsychoJS, '', false);
var _ready_allKeys;
const clock = new util.Clock();

var Bim_positions;

var BLim_positions;
let lArr = [...Array(5).keys()].map((k) => (k-2)/7.5);

var Cpim_positions = {};

var Ctim_positions = {}

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
var tSelfRank;

const fixation = new visual.TextStim({win: psychoJS.window,name:'Text',
        text:"+",
        font:'Arial',
        units:'height', pos:[0, 0], height:0.05, wrapWidth:null, ori:0,
        color:'white', colorSpace:'rgb', opacity:1,
        languageStyle:'LTR',
        depth:0.0});

var instrText = new visual.TextStim({win:psychoJS.window, name:'Text',
        font:'Arial',
        units:'height', pos:[0, 0], height:0.05, wrapWidth:1.5, ori:0,
        color:'white', colorSpace:'rgb', opacity:1,
        languageStyle:'LTR',
        depth:0.0});

var selfRankText = new visual.TextStim({win:psychoJS.window, name:'Text',
        font:'Arial',
        units:'height', pos:[0, .15], height:0.05, wrapWidth:1.5, ori:0,
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
    if (psychoJS.experiment.isEntryEmpty()) {
      psychoJS.experiment.nextEntry();
    }

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
var party;
var lStim;
let labels = ["Activity", "Group", "Location"];
var TextStims = [];

var locs,socs,sits,trials;
var trialT;
var selected,postselect,iters,indices;
var groupays,locays,sitays;
var winPrevSize,choosePeople;

var rankDisp;
var rankDPos;
var mouseTaskPress;

async function routBbeg(time,nParty){
    let party = "party" + nParty;
    winPrevSize = psychoJS.window.size.map((s)=>s);
    Bim_positions = {0: [0, 0.3],
                1: [0.6, -0.15],
                2: [-0.0, -0.15],
                3: [-0.6, -0.15]};


    BLim_positions = {1: [0.6, -0.45],
                2: [-0.0, -0.45],
                3: [-0.6, -0.45]};
	TextStims = []
    for (let i = 0; i < labels.length; i++){
        let t = labels[i];
        TextStims.push(new visual.TextStim({win: psychoJS.window,text:t,height:0.05,pos:BLim_positions[i+1],name:t,wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0}));
    };

    people = [...Array(5).keys()].map((k)=>party+"/people/"+(k+1)+".png");
    seen = [...Array(people.length).keys()].map((k) => 0);
    situation = [...Array(5).keys()].map((s)=>party+"/socialSit/"+(s+1));
    situation = shuffler(situation);
    sitimages = situation.map((s)=>shuffler([...Array(2).keys()]).map((ss)=> (ss+1)+".png"));

    localation = [...Array(5).keys()].map((s)=>party+"/locations/"+(s+1));
    localation = shuffler(localation);
    locimages = localation.map((s)=>shuffler([...Array(2).keys()]).map((ss)=> (ss+1)+".jpg"));

    socgroups = [...Array(5).keys()].map((s)=>party+"/socgroups/"+(s+1));
    socgroups = shuffler(socgroups);
    socimages = socgroups.map((s)=>shuffler([...Array(2).keys()]).map((ss)=> (ss+1)+".jpg"));

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
            lStim.push([people[i], sitays[i][j],groupays[i][j],locays[i][j]]);
        };
    };
    let stimlist = [people,sitays,groupays,locays];

    // What a wild line. I had this in python to do a deep copy, wonder if it's
    // necessary here too?
    let Stims = [...Array(stimlist.length).keys()].map((i)=>[...Array(stimlist[i].length).keys()].map((j)=>stimlist[i][j]));
    psychoJS.experiment.addData("Stimuli",Stims);
    trialT = 0
    tFixation = clock.getTime();
    selected = false;
    postselect = true;
    choosePeople = [...Array(5).keys()].map((i)=>i);
    return Scheduler.Event.NEXT;
}
var person,Person,indsit,indloc,indsoc,socim,locim,sgroupim,SocialSit,SocialGroup,Location;
var experson,exlocation,exgroup,exsituation;
var BPerson,BGroup,BLoc,BSit;
async function routBExbeg(){
    winPrevSize = psychoJS.window.size.map((s)=>s);
    Bim_positions = {0: [0, 0.3],
                1: [0.6, -0.15],
                2: [-0.0, -0.15],
                3: [-0.6, -0.15]};


    BLim_positions = {1: [0.6, -0.45],
                2: [-0.0, -0.45],
                3: [-0.6, -0.45]};

	TextStims = []
    for (let i = 0; i < labels.length; i++){
        let t = labels[i];
        TextStims.push(new visual.TextStim({win: psychoJS.window,text:t,height:0.05,pos:BLim_positions[i+1],name:t,wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0}));
    };

    experson = "exampleStim/people/1.png";
    exsituation = "exampleStim/socialSit/1/1.jpg";
    exlocation = "exampleStim/locations/1/1.jpg";
	exgroup = "exampleStim/socgroups/1/1.jpg";

    indices = [...Array(3).keys()].map((k)=>k+1);

    trialT = 0
    tFixation = clock.getTime();
    selected = false;
    postselect = true;
    choosePeople = [...Array(5).keys()].map((i)=>i);
    return Scheduler.Event.NEXT;
}

function routBEx(trialtime){
    let lind = trialT
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
            if (lind <= 5){for (let j = 0; j < TextStims.length;j++){TextStims[j].autoDraw = true}}
            return Scheduler.Event.FLIP_REPEAT;
        }
    }
    if (!selected){

        selected = true;
        tBegin = clock.getTime();
        let Psize;
        let Ssize;
        let Bcopy;
        winPrevSize = psychoJS.window.size;
        Bcopy = JSON.parse(JSON.stringify(Bim_positions));
        let offset = [0,-0.2]
        let height = 0.05
        let ratio = [1,1];
        for(let k=0; k< Object.keys(Bcopy).length;k++){for(let kk=0;kk<Bcopy[k].length;kk++){Bcopy[k][kk] = Bcopy[k][kk]*ratio[kk]}};
        for(let k=1; k< Object.keys(Bcopy).length;k++){TextStims[k-1].height = height*ratio[1]};
        Psize = [0.36*ratio[0],0.36*ratio[1]];
        Ssize = [0.475*ratio[0],0.475*ratio[1]];
        let BPsize = [2*0.36*ratio[0], 2*0.36*ratio[1]];
        let BSsize = [2*0.475*ratio[0],2*0.475*ratio[1]];

        Person = new visual.ImageStim({win:psychoJS.window,image:experson,size:Psize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[0],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        SocialSit = new visual.ImageStim({win:psychoJS.window,image:exsituation,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[0]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        SocialGroup = new visual.ImageStim({win:psychoJS.window,image:exgroup,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[1]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        Location = new visual.ImageStim({win:psychoJS.window,image:exlocation,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[2]], color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });

        BPerson = new visual.Rect({win:psychoJS.window,size:BPsize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[0],  fillColor : new util.Color([0, 0, 0]), lineColor : new util.Color([1,0,0]) , lineWidth : 10, opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        BSit = new visual.Rect({win:psychoJS.window,size:BSsize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[1],  fillColor : new util.Color([0, 0, 0]), lineColor : new util.Color([0, 1, 0]) , lineWidth : 10, opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        BGroup = new visual.Rect({win:psychoJS.window,size:BSsize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[2],  fillColor : new util.Color([0, 0, 0]), lineColor : new util.Color([0, 0, 1]) , lineWidth : 10, opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });
        BLoc = new visual.Rect({win:psychoJS.window,size:BSsize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[3],  fillColor : new util.Color([0, 0, 0]), lineColor : new util.Color([1, 0, 1]) , lineWidth : 10, opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 });

        SocialSit.autoDraw = true;
        Person.autoDraw = true;
        SocialGroup.autoDraw = true;
        Location.autoDraw = true;

        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }

    if (clock.getTime() - tBegin < trialtime){
        if(psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
            let Psize;
            let Ssize;
            let Bcopy;
            winPrevSize = psychoJS.window.size;
            Bcopy = JSON.parse(JSON.stringify(Bim_positions));
            let offset = [0,-0.2]
            let height = 0.05
            let ratio = [1,1];
            for(let k=0; k< Object.keys(Bcopy).length;k++){for(let kk=0;kk<Bcopy[k].length;kk++){Bcopy[k][kk] = Bcopy[k][kk]*ratio[kk]}};
            Psize = [0.36*ratio[0],0.36*ratio[1]];
            Ssize = [0.475*ratio[0],0.475*ratio[1]];
            Person.size = Psize;
            SocialSit.size = Ssize;
            Location.size = Ssize;
            SocialGroup.size = Ssize;
            SocialSit.pos = Bcopy[indices[1]];
            SocialGroup.pos = Bcopy[indices[1]];
            Location.pos = Bcopy[indices[2]];
        }

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
		        SocialSit.opacity /= 4
				Person.opacity = 1;
		        Person.opacity /= 4
		        SocialGroup.opacity /= 4
		        Location.opacity/= 4
                BSit.autoDraw = true;
                BPerson.autoDraw = true;
                BGroup.autoDraw = true;
                BLoc.autoDraw = true;
		        BSit.opacity /= 3.5
		        BPerson.opacity /= 3.5
		        BGroup.opacity /= 3.5
		        BLoc.opacity/= 3.5

		        for (let j = 0; j < TextStims.length;j++){TextStims[j].opacity /= 4}

                return Scheduler.Event.NEXT}
        }
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    }else{
        trialT += 1
        tFixation = clock.getTime();
        selected = false;
        SocialSit.opacity /= 4
		Person.opacity = 1;
        Person.opacity /= 4
        SocialGroup.opacity /= 4
        Location.opacity/= 4
        BSit.autoDraw = true;
        BPerson.autoDraw = true;
        BGroup.autoDraw = true;
        BLoc.autoDraw = true;
		BSit.opacity /= 3.5
		BPerson.opacity /= 3.5
		BGroup.opacity /= 3.5
		BLoc.opacity/= 3.5

        for (let j = 0; j < TextStims.length;j++){TextStims[j].opacity /= 4}
        postselect = true;
        if (trialT > 0){
            trialT = 0;
            return Scheduler.Event.NEXT;
        }else{
            frames += 1;
            return Scheduler.Event.FLIP_REPEAT
        };
    };
};

function routB(iterations,trialtime){
    let lind = trialT
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
            for (let j = 0; j < TextStims.length;j++){TextStims[j].autoDraw = true}
            return Scheduler.Event.FLIP_REPEAT;
        }
    }
    if (!selected){
        if (lind % lStim.length == 0){
            lStim = shuffler(lStim);
        }

        selected = true;
        tBegin = clock.getTime();
        let t = lind % lStim.length;
        [person,socim,sgroupim,locim] = lStim[t];
        if (lind >= 5)
            indices = shuffler(indices);
        let Psize;
        let Ssize;
        let Bcopy;
		let BLcopy;
        winPrevSize = psychoJS.window.size;
        Bcopy = JSON.parse(JSON.stringify(Bim_positions));
        BLcopy = JSON.parse(JSON.stringify(BLim_positions));
        let offset = [0,-0.2]
        let height = 0.05
        let ratio = [1,1];
        for(let k=0; k< Object.keys(Bcopy).length;k++){for(let kk=0;kk<Bcopy[k].length;kk++){Bcopy[k][kk] = Bcopy[k][kk]*ratio[kk]}};
        for(let k=1; k< Object.keys(BLcopy).length;k++){for(let kk=0;kk<BLcopy[k].length;kk++){BLcopy[k][kk] = BLcopy[k][kk]*ratio[kk]}};
        for(let k=1; k< Object.keys(Bcopy).length;k++){TextStims[k-1].height = height*ratio[1]};
        for(let k=1; k< Object.keys(Bcopy).length;k++){TextStims[k-1].pos = BLcopy[indices[k-1]]};
        Psize = [0.36*ratio[0],0.36*ratio[1]];
        Ssize = [0.475*ratio[0],0.475*ratio[1]];

        Person = new visual.ImageStim({win:psychoJS.window,image:person,size:Psize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[0],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit = new visual.ImageStim({win:psychoJS.window,image:socim,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[0]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialGroup = new visual.ImageStim({win:psychoJS.window,image:sgroupim,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[1]],  color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        Location = new visual.ImageStim({win:psychoJS.window,image:locim,size:Ssize, mask : undefined, anchor : 'center', ori : 0, pos: Bcopy[indices[2]], color : new util.Color([1, 1, 1]), opacity : 1, flipHoriz : false, flipVert : false, texRes : 128, interpolate : true, depth : -1.0 
});
        SocialSit.autoDraw = true;
        Person.autoDraw = true;
        SocialGroup.autoDraw = true;
        Location.autoDraw = true;
        frames += 1;
//        if (lind == 5){for (let j = 0; j < TextStims.length; j++){TextStims[j].autoDraw = false}};
        return Scheduler.Event.FLIP_REPEAT;
    }

    if (clock.getTime() - tBegin < trialtime){
        if(psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
            let Psize;
            let Ssize;
            let Bcopy;
            winPrevSize = psychoJS.window.size;
            Bcopy = JSON.parse(JSON.stringify(Bim_positions));
            let offset = [0,-0.2]
            let height = 0.05
            let ratio = [1,1];
            for(let k=0; k< Object.keys(Bcopy).length;k++){for(let kk=0;kk<Bcopy[k].length;kk++){Bcopy[k][kk] = Bcopy[k][kk]*ratio[kk]}};
            Psize = [0.36*ratio[0],0.36*ratio[1]];
            Ssize = [0.475*ratio[0],0.475*ratio[1]];
            Person.size = Psize;
            SocialSit.size = Ssize;
            Location.size = Ssize;
            SocialGroup.size = Ssize;
            SocialSit.pos = Bcopy[indices[1]];
            SocialGroup.pos = Bcopy[indices[1]];
            Location.pos = Bcopy[indices[2]];
        }

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
        if (trialT > 2*trials*iterations){
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
var pStim,tStim,tasks,rankStims,questStim,running;
var c,mousePersonIndex, mouseTaskIndex, count,mouseIsDown,mouseIsTaskDown,mouseIsPersonDown,okroutRun;
var lineKeys, linetKeys,lines,personRank;
var mouseIdleTime,mousePrevPos;
async function routCbeg(nParty,Ex){
    tasks = tasksAll[nParty-1]
    pStim = {};
    tStim = {};

    for (let i = 0; i < lArr.length; i++){
        Cpim_positions[i] = [0.5,lArr[i]];
    };

    for (let i = 0; i < lArr.length; i++){
        Ctim_positions[i] = [-0.5,lArr[i]];
    };

    if (typeof Ex !== 'undefined'){
        people = [...Array(5).keys()].map((i)=>"party4/people/"+(i+1)+".png");
        tasks = tasksAll[3]
    }
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
    winPrevSize = psychoJS.window.size.map((s)=>s);
    for (let i = 0; i < tasks.length; i++){
        lineKeys[i] = {};
        personRank[i] = [false,false,false];
        lines[i] = {};
    };
    for (let i = 0; i < people.length; i++){linetKeys[i] = {}};

    for (let i =0; i < tasks.length; i++){
        for (let j = 0; j < 2; j++){
            let jj = j;
            if (j == 1){
                jj += 1;
            }
            lines[i][j] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:[tStim[i].pos[0]+0.25+0.25*jj,tStim[i].pos[1]],size:[0.1,0.1]});
            lines[i][j].autoDraw = true
            linetKeys[i][j] = null;
        };
    };
    rankStims = [];
    for (let j = 0; j < 2; j++){
        let jj = j;
        if (j == 1){
            jj += 1;
        }
        let pos = [tStim[people.length-1].pos[0] + 0.25+0.25*jj,0.4];
        rankStims.push(new visual.TextStim({win:psychoJS.window,text:j+1,pos:pos,
                    height:0.05, wrapWidth:null, ori:0, color:'white',
                    colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0,font:'Arial', units:'height'}));
        rankStims[j].autoDraw = true;
    };
    questStim = new visual.TextStim({win:psychoJS.window, name:'endText', text:'If this looks correct to you, please press \'k\', otherwise press \'r\'', font:'Arial', units:'height', pos:[tStim[0].pos[0]+0.5, tStim[0].pos[1]-0.15], height:0.04, wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0});

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
    if (typeof Ex !== 'undefined'){
        lines[0][0].autoDraw = false;
        lines[0][0] = new visual.ImageStim({win:psychoJS.window, image:people[0],pos:lines[0][0].pos,size:[0.1,0.1]});
        lines[0][0].autoDraw = true;
        lines[1][1].autoDraw = false;
        lines[1][1] = new visual.ImageStim({win:psychoJS.window, image:people[0],pos:lines[1][1].pos,size:[0.1,0.1]});
        lines[1][1].autoDraw = true;
        for (let i = 0; i < Object.keys(lines).length; i++){
            for (let j = 0; j < Object.keys(lines[i]).length;j++){
                lines[i][j].opacity /= 4;
            }
            pStim[i].opacity /= 4;
            tStim[i].opacity /= 4;
        }
        for (let i = 0; i < 2; i++){
            rankStims[i].opacity /= 4;
        }

    }
    return Scheduler.Event.NEXT;
}

function routC(){

    if (running){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);

        if (psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
            winPrevSize = psychoJS.window.size.map((s)=>s);
            let Copy_Cpim_positions = JSON.parse(JSON.stringify(Cpim_positions));
            let Copy_Ctim_positions = JSON.parse(JSON.stringify(Ctim_positions));
            let ratio = [1,1];
            for (let i = 0; i < people.length; i++){
                for (let j = 0; j < Cpim_positions[i].length; j++){Copy_Cpim_positions[i][j] = Copy_Cpim_positions[i][j]*ratio[j]};
                pStim[i].pos = Copy_Cpim_positions[i];
                pStim[i].size = [0.1*ratio[0],0.1*ratio[1]];
            };
            for (let i = 0; i < tasks.length; i++){
                for (let j = 0; j < Ctim_positions[i].length; j++){Copy_Ctim_positions[i][j] = Copy_Ctim_positions[i][j]*ratio[j]}
                tStim[i].pos = Copy_Ctim_positions[i];
                tStim[i].height = 0.05*ratio[1];
            };
            for(let j = 0; j < 2; j++){
                let jj = j;
                if (j == 1){
                    jj += 1;
                }
                rankStims[j].pos = [tStim[people.length-1].pos[0] + (0.25+0.25*jj)*ratio[0],0.4*ratio[1]];
                rankStims[j].height = 0.05*ratio[1]
            };
            for (let i =0; i < tasks.length; i++){
                for (let j = 0; j < 2; j++){
                    lines[i][j].pos = [tStim[i].pos[0]+(0.25+0.25*j)*ratio[0],tStim[i].pos[1]];
                    lines[i][j].size = [0.1*ratio[0],0.1*ratio[1]];
                }
            }
        }
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == 'escape'){return quitPsychoJS()};
            if (ready.keys == 'k'){running = false};
            if (ready.keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    for (let j = 0; j < 2; j++){lines[i][j].autoDraw=false}
                    lines[i] = {};
                };
                for (let i = 0; i< people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 2; j++){
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
            if (temp == 2 && pStim[i].opacity != 0.8){pStim[i].opacity= 0.8;}
            else if (temp != 2 && pStim[i].opacity!= 1){pStim[i].opacity= 1;};
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
            if (temp == 2 && tStim[i].color != [1,-1,-1] != 'red'){tStim[i].color='red'}
            else if (tStim[i].color != 'white'){tStim[i].color='white'};
        };
        if (clines == 2*tasks.length){
            okroutRun = true;
            questStim.autoDraw = true;
        }

        if (okroutRun){
            keys = routOK();
            if (keys == 'r'){
                for (let i = 0; i < tasks.length; i++){
                    lineKeys[i] = {};
                    for (let j = 0; j < 2; j++){lines[i][j].autoDraw = false};
                    lines[i] = {};
                };
                for (let i = 0; i < people.length; i++){linetKeys[i] = {}};
                for (let i = 0; i < tasks.length; i++){
                    for (let j = 0; j < 2; j++){
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
                    for (let kk = 0; kk < 2; kk++){
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
                let ratio = [1,1];
                if (key != -1 && rank != -1){
                    // If this person already has this rank occupied
                    if (rank in lineKeys[mousePersonIndex]){
                        let pastkey = lineKeys[mousePersonIndex][rank];
                        delete lineKeys[mousePersonIndex][rank];
                        if (rank in linetKeys[pastkey]){linetKeys[pastkey][rank] = null};
                        let pos;
                        if (rank == 0){
                            pos = [tStim[pastkey].pos[0] + (0.25+0.25*rank)*ratio[0],tStim[pastkey].pos[1]];
                        }else{
                            pos = [tStim[pastkey].pos[0] + (0.25+0.25*(rank+1))*ratio[0],tStim[pastkey].pos[1]];
                        }
                        lines[pastkey][rank].autoDraw = false;
                        lines[pastkey][rank] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:pos,size:[0.1*ratio[0],0.1*ratio[1]]});
                        lines[pastkey][rank].autoDraw = true;
                    }
                    // If this person was already assigned this task before
                    let pastrank = checkTs(mousePersonIndex, linetKeys[key]);
                    if (pastrank != -1){
                        if (pastrank in linetKeys[key]){linetKeys[key][pastrank] = null};
                        if (pastrank in lineKeys[mousePersonIndex]){delete lineKeys[mousePersonIndex][pastrank]};
                        let pos;
                        if (pastrank==0){
                            pos = [tStim[key].pos[0] + (0.25+0.25*pastrank)*ratio[0],tStim[key].pos[1]];
                        }else{
                            pos = [tStim[key].pos[0] + (0.25+0.25*(pastrank+1))*ratio[0],tStim[key].pos[1]];
                        }
                        lines[key][pastrank].autoDraw = false;
                        lines[key][pastrank] = new visual.Rect({win:psychoJS.window, fillColor:'white',pos:pos,size:[0.1*ratio[0],0.1*ratio[1]]});
                        lines[key][pastrank].autoDraw = true;
                    };
                    // If someone is already occupying this task rank, properly
                    // overwrite their occupation wit the new person
                    if (rank in linetKeys[key] && linetKeys[key][rank]){delete lineKeys[linetKeys[key][rank]][rank]};
                    lineKeys[mousePersonIndex][rank] = key;
                    linetKeys[key][rank] = mousePersonIndex;
                    lines[key][rank].autoDraw = false;
                    lines[key][rank] = new visual.ImageStim({win:psychoJS.window, image:people[mousePersonIndex],pos:lines[key][rank].pos,size:[0.1*ratio[1],0.1*ratio[1]]});
                    lines[key][rank].autoDraw = true;
                    console.log(key,"to",mousePersonIndex,"with rank",rank);
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
        for (let i = 0; i < 2; i++){
            rankStims[i].autoDraw = false;
        }

        psychoJS.experiment.addData("rankDec",JSON.stringify(lineKeys));
        questStim.autoDraw = false;
        return Scheduler.Event.NEXT;
    }
};

var textConf,slider;
async function routCConfbeg(){
    notReady = true;
    timeCF = clock.getTime();
    textConf = new visual.TextStim({win:psychoJS.window, name:'endText',
                text:'How confident are you? Click the slider, and drag the red circle to your confidence level. Then press spacebar to continue',
                font:'Arial',
                units:'height', pos:[0, 0.25], height:0.05, wrapWidth:null, ori:0,
                color:'white', colorSpace:'rgb', opacity:1,
                languageStyle:'LTR',
                depth:0.0});
    slider = new visual.Slider({win:psychoJS.window,lineColor:'white',labelColor:'white',labels: ["1", "2", "3", "4", "5", "6", "7"],ticks:[1,2,3,4,5,6,7],granularity:0,pos:[0,0],size:[1,0.1]});
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
var Stimuls, confRats;
var situationIm,socgroupsIm,locationIm;
var Schooses,Lchooses;

async function routDbeg(trials){

    let toFill = shuffler([...Array(4*trials).keys()]);
    correct = [...Array(4*trials).keys()].map((i)=>-1);
    for (let i = 0; i < 2*trials;i++){
        correct[i] = 1;
    }
    correct = shuffler(correct);
    pind = [...Array(4*trials).keys()].map((i) => 0);
    let P = 0;
    for(let i = 0; i < 4*trials; i++){
        if (i > 0 && i % (4*trials/5) == 0){
            P += 1;
        }
        pind[toFill[i]] = P;
    }

    // Episode Select
    eind = shuffler([...Array(4*trials).keys()].map((i)=>0));
    let filtArr = [...Array(4*trials).keys()];
    // Reference cue
    otherchoice = [...Array(4*trials).keys()].map((i)=>0);
    bwgroup = [...Array(4*trials).keys()].map((i)=>0);
    let P1ch = shuffler(filtArr.filter((p) => pind[p] == 0));
    let P2ch = shuffler(filtArr.filter((p) => pind[p] == 1));
    let P3ch = shuffler(filtArr.filter((p) => pind[p] == 2));
    let P4ch = shuffler(filtArr.filter((p) => pind[p] == 3));
    let P5ch = shuffler(filtArr.filter((p) => pind[p] == 4));

    for(let i = 0; i < P1ch.length/2; i++){
        otherchoice[P1ch[i]] = 1;
        otherchoice[P2ch[i]] = 1;
        otherchoice[P3ch[i]] = 1;
        otherchoice[P4ch[i]] = 1;
        otherchoice[P5ch[i]] = 1;
    }
    let P1och =  P1ch.filter((i) => otherchoice[i] == 1);
    let P1noch = P1ch.filter((i) => otherchoice[i] == 0);
    let P2och =  P2ch.filter((i) => otherchoice[i] == 1);
    let P2noch = P2ch.filter((i) => otherchoice[i] == 0);
    let P3och = P3ch.filter((i) => otherchoice[i] == 1);
    let P3noch = P3ch.filter((i) => otherchoice[i] == 0);
    let P4och = P4ch.filter((i) => otherchoice[i] == 1);
    let P4noch = P4ch.filter((i) => otherchoice[i] == 0);
    let P5och = P5ch.filter((i) => otherchoice[i] == 1);
    let P5noch = P5ch.filter((i) => otherchoice[i] == 0);

    for(let i = 0; i < P1och.length/2;  i++){
        bwgroup[P1och[i]] = 1;
        bwgroup[P1noch[i]] = 1;
        bwgroup[P2och[i]] = 1;
        bwgroup[P2noch[i]] = 1;
        bwgroup[P3och[i]] = 1;
        bwgroup[P3noch[i]] = 1;
        bwgroup[P4och[i]] = 1;
        bwgroup[P4noch[i]] = 1;
        bwgroup[P5och[i]] = 1;
        bwgroup[P5noch[i]] = 1;
    }

    let P1eioch = P1och.filter((i) => bwgroup[i] == 1);
    let P1einoch = P1noch.filter((i) => bwgroup[i] == 1);
    let P2eioch = P2och.filter((i) => bwgroup[i] == 1);
    let P2einoch = P2noch.filter((i) => bwgroup[i] == 1);
    let P3eioch = P3och.filter((i) => bwgroup[i] == 1);
    let P3einoch = P3noch.filter((i) => bwgroup[i] == 1);
    let P4eioch = P4och.filter((i) => bwgroup[i] == 1);
    let P4einoch = P4noch.filter((i) => bwgroup[i] == 1);
    let P5eioch = P5och.filter((i) => bwgroup[i] == 1);
    let P5einoch = P5noch.filter((i) => bwgroup[i] == 1);

    let P1eooch = P1och.filter((i) => bwgroup[i]  == 0);
    let P1eonoch = P1noch.filter((i) => bwgroup[i]  == 0);
    let P2eooch = P2och.filter((i) => bwgroup[i]  == 0);
    let P2eonoch = P2noch.filter((i) => bwgroup[i]  == 0);
    let P3eooch = P3och.filter((i) => bwgroup[i]  == 0);
    let P3eonoch = P3noch.filter((i) => bwgroup[i]  == 0);
    let P4eooch = P4och.filter((i) => bwgroup[i]  == 0);
    let P4eonoch = P4noch.filter((i) => bwgroup[i]  == 0);
    let P5eooch = P5och.filter((i) => bwgroup[i]  == 0);
    let P5eonoch = P5noch.filter((i) => bwgroup[i]  == 0);


    for(let i = 0; i < P1eioch.length/2;  i++){
        eind[P1eioch[i]] = 1;eind[P1einoch[i]] = 1;eind[P2eioch[i]] = 1;eind[P2einoch[i]] = 1;eind[P3eioch[i]] = 1;
        eind[P3einoch[i]] = 1;eind[P4eioch[i]] = 1;eind[P4einoch[i]] = 1;eind[P5eioch[i]] = 1;eind[P5einoch[i]] = 1;
        eind[P1eooch[i]] = 1;eind[P1eonoch[i]] = 1;eind[P2eooch[i]] = 1;eind[P2eonoch[i]] = 1;eind[P3eooch[i]] = 1;
        eind[P3eonoch[i]] = 1;eind[P4eooch[i]] = 1;eind[P4eonoch[i]] = 1;eind[P5eooch[i]] = 1;eind[P5eonoch[i]] = 1;
    }

    for(let i = 1; i < pind.length - 1; i++){
        if(pind[i] == pind[i-1]){
            if(bwgroup[i] != bwgroup[i-1]){
                if(otherchoice[i] == otherchoice[i-1]){
                    let tempb = bwgroup[i].valueOf();
                    let tempo = otherchoice[i].valueOf();
                    bwgroup[i] = bwgroup[i+1].valueOf();
                    otherchoice[i] = otherchoice[i+1].valueOf();
                    otherchoice[i+1] = tempo;
                    bwgroup[i+1] = tempb;
                }
            }
        }
    }

    choices = [];
    confidences = [];
    RTs = [];
    confRTs = [];
    trialT = 0;
    choice = 0;
    doingConf = false;
    okroutRun = false;
    selectedLR = false;
    postselect = false;
    Stimuls = [];
    psychoJS.experiment.addData("Query", otherchoice);
    psychoJS.experiment.addData("BWgroup", bwgroup);
    psychoJS.experiment.addData("Eind",eind);
    psychoJS.experiment.addData("Pind",pind);
    confRats = 0
    Schooses = [[],[],[],[],[]];
    Lchooses = [[],[],[],[],[]];
    for(let p = 0; p < 5; p++){for (let i=0; i < groupays.length; i++){for (let j = 0; j < 2; j++){if (i != p){Schooses[p].push(groupays[i][j])}}};Schooses[p]=shuffler(Schooses[p])}
    for(let p = 0; p < 5; p++){for (let i=0; i < locays.length; i++){for (let j = 0; j < 2; j++){if (i != p){Lchooses[p].push(locays[i][j])}}};Lchooses[p]=shuffler(Lchooses[p])}
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
        leftorRight = correct[t]
        selectedLR = true;
        let p = pind[t];
        let e = eind[t];
        let oc = otherchoice[t];
        let bw = bwgroup[t];
        let c = 0;
        let chooses = [];
        let choose;
        Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:sitays[p][e]}));
        if (oc == 0){
            if (bw == 1){
                choose = Schooses[p][getRandInt(0,Schooses[p].length-1)];
            }
            else{choose = groupays[p][e^1]};
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:groupays[p][e]}));
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
        }
        else if (oc == 1){
            if (bw == 1){
                choose = Lchooses[p][getRandInt(0,Lchooses[p].length-1)];
            }
            else{choose = locays[p][e^1]};
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:locays[p][e]}));
            Stimuls.push(new visual.ImageStim({win:psychoJS.window,image:choose}));
        };

        for (let k = 1; k < Stimuls.length; k++){Stimuls[k].size = [.45, .45]};
        Stimuls[0].size = [.4,.4];
        Stimuls[0].pos = [Bim_positions[0][0],Bim_positions[0][1]-0.05];
        if (leftorRight == -1){
            Stimuls[1].pos = [Bim_positions[3][0],Bim_positions[3][1]-0.05];
            Stimuls[2].pos = [Bim_positions[1][0],Bim_positions[1][1]-0.05];
        }
        else{
            Stimuls[1].pos = [Bim_positions[1][0],Bim_positions[1][1]-0.05];
            Stimuls[2].pos = [Bim_positions[3][0],Bim_positions[3][1]-0.05];
        };
        Stimuls[0].autoDraw = true;
        Stimuls[1].autoDraw = true;
        Stimuls[2].autoDraw = true;
        timeDec = clock.getTime();
    }

    if (choice == 0){
        if (psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
            winPrevSize = psychoJS.window.size.map((s)=>s);
            let ratio = [1,1];
            Stimuls[0].pos =[Bim_positions[0][0]*ratio[0],Bim_positions[0][1]*ratio[1]-0.05];
            if (correct[correct.length-1] == -1){
                Stimuls[1].pos =[Bim_positions[3][0]*ratio[0],Bim_positions[3][1]*ratio[1]-0.05];
                Stimuls[2].pos = [Bim_positions[1][0]*ratio[0],Bim_positions[1][1]*ratio[1]-0.05];
            }else{
                Stimuls[2].pos = [Bim_positions[3][0]*ratio[0],Bim_positions[3][1]*ratio[1]-0.05];
                Stimuls[1].pos = [Bim_positions[1][0]*ratio[0],Bim_positions[1][1]*ratio[1]-0.05];
            };
            Stimuls[0].size = [0.40*ratio[0],0.40*ratio[1]]
            Stimuls[1].size = [0.45*ratio[0],0.45*ratio[1]]
            Stimuls[2].size = [0.45*ratio[0],0.45*ratio[1]]
        }

        // Kick user out of experiment if they take too long to reply
        let currTime = clock.getTime()
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);

        if (currTime - timeDec > 60){return quitPsychoJS("Kicked out for being idle for too long")};
        if (currTime - timeDec > 11){
            choice = correct[t]^1
            let RT = clock.getTime() - timeDec;
            choices.push(choice)
            RTs.push(RT)
            confidences.push(0);
            confRTs.push(0);
            Stimuls[0].autoDraw = false;
            Stimuls[1].autoDraw = false;
            Stimuls[2].autoDraw = false;
            Stimuls = [];
            slider.autoDraw = false;
            textConf.autoDraw = false;
            doingConf = false;
            notReady = false;
            postselect = true;
            slider.reset();
            tFixation = clock.getTime();
            choice = 0;
            trialT += 1;
        }else if (_ready_allKeys.length > 0) {
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
                if (false){
                    slider.autoDraw = false;
                    textConf.autoDraw = false;
                    doingConf = false;
                    notReady = false;
                    postselect = true;
                    slider.reset();
                    tFixation = clock.getTime();
                    choice = 0;
                    trialT += 1;
                }
                else{
                    doingConf = true;
                    confRats +=1;
                    slider.autoDraw = true;
                    textConf.autoDraw = true;
                    notReady = true;
                    timeCF = clock.getTime();
                }
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
                if (false){
                    slider.autoDraw = false;
                    textConf.autoDraw = false;
                    doingConf = false;
                    notReady = false;
                    postselect = true;
                    slider.reset();
                    tFixation = clock.getTime();
                    choice = 0;
                    trialT += 1;
                }
                else{
                    doingConf = true;
                    confRats +=1;
                    slider.autoDraw = true;
                    textConf.autoDraw = true;
                    notReady = true;
                    timeCF = clock.getTime();
                }
            };
        };
        if (RTs.length > 5){
            let mRT = 0;for(let z = RTs.length-5; z < RTs.length;z++){mRT += RTs[z]};
            // Kick user out of experiment if they are responding way too fast on
            // average.
            if (mRT/5 <0.1  || mRT/5 > 10){return quitPsychoJS("Kicked out for too many consecutive outlier response times")};
        }
        frames += 1;
        return Scheduler.Event.FLIP_REPEAT;
    };
    return Scheduler.Event.NEXT;
};
function routDc(){
    if (psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
        winPrevSize = psychoJS.window.size.map((s)=>s);
        let ratio = [1,1];
        textConf.height = 0.05*ratio[1];
        slider.size = [1*ratio[0],0.1*ratio[1]];
    }
    let ret = null;
    if (notReady){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == 'space'){
                if (typeof slider.getRating() !== 'undefined'){
                    let RT = clock.getTime() - timeCF;
                    notReady = false;
                    return [slider.getRating(),RT];
                }
            };
        };
    };
    return ret; 
}

function setText(fill){
    ready.clearEvents();
    instrText.text = fill + "\n Press any key to Continue";
    instrText.wrapwidth = 10;
    instrText.autoDraw = true;
    notReady = true
    winPrevSize = psychoJS.window.size;
    return Scheduler.Event.NEXT;
}
async function routText(arg){
    if (psychoJS.window.size[0] != winPrevSize[0] || psychoJS.window.size[1] != winPrevSize[1]){
        winPrevSize = psychoJS.window.size.map((s)=>s);
        let ratio = [1,1];
        instrText.height = ratio[1]*0.05;
    }

    if(notReady){
        let keys = ready.getKeys({keyList:[], waitRelease:false});
        _ready_allKeys = [].concat(keys);
        if (_ready_allKeys.length > 0) {
            ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
            ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
            ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
            if (ready.keys == "escape"){return quitPsychoJS()}
            else{
                notReady = false;
                instrText.autoDraw = false;
                console.log(typeof arg,arg);
				if (typeof arg !== 'undefined' && arg === "ExB"){
                    BSit.autoDraw = false;
                    BPerson.autoDraw = false;
                    BGroup.autoDraw = false;
                    BLoc.autoDraw = false;

	                SocialSit.autoDraw = false
	                Person.autoDraw = false
	                SocialGroup.autoDraw = false
	                Location.autoDraw = false
	                for (let j = 0; j < TextStims.length; j++){TextStims[j].autoDraw = false};
				}else if(typeof arg !== 'undefined' && arg === "ExC"){
                    for (let i = 0; i < Object.keys(lines).length; i++){
                        for (let j = 0; j < Object.keys(lines[i]).length;j++){
                            lines[i][j].autoDraw = false;
                        }
                        pStim[i].autoDraw = false;
                        tStim[i].autoDraw = false;
                    }
                    for (let i = 0; i < 2; i++){
                        rankStims[i].autoDraw = false;
                    }
                }

                return Scheduler.Event.NEXT;
            }
        };
    };
    frames += 1;
    return Scheduler.Event.FLIP_REPEAT;
};

var whatSelfRanks;
var selfRankRT;
function selfRankBeg(){
    trialT = 0;
    selfRankText.text = "If you were going to involve yourself in a " + TASKNAME[0].toUpperCase() + ", which role would you place yourself in? Click on the labels below to select your role. The text will highlight GREEN for your first choice, and BLUE for your second choice"
    selfRankText.text += "\n If for any reason you need to reset your select, please press 'r'"
    selfRankText.autoDraw = true;
    rankDisp = []
    rankDPos = [[-0.6,-0.35],[-0.3,-0.35],[0,-0.35],[0.3,-0.35],[0.6,-0.35]]
    for(let i = 0; i < 5; i++){
        let temp = new visual.TextStim({win:psychoJS.window,text:tasksAll[0][i],pos:rankDPos[i], height:0.05, wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0,font:'Arial', units:'height'})
        temp.autoDraw = true;
        rankDisp.push(temp);
    }
    mouseIsDown = false;
    mouseIsTaskDown = false;
    whatSelfRanks = [[],[]];
    mouseTaskPress = -1;
    selfRankRT = []
    tSelfRank = clock.getTime();
    doingConf = false;
    questStim.color = 'red'
    questStim.pos = [questStim.pos[0],questStim.pos[1]+0.2]
    return Scheduler.Event.NEXT;
}

function selfRank(parties){
    if (trialT >=2){
        psychoJS.experiment.addData("selfRanks",whatSelfRanks);
        psychoJS.experiment.addData("selfRankRT",selfRankRT);
        return Scheduler.Event.NEXT;
    }
    if(whatSelfRanks[trialT].length <2){

         if (mouse.getPressed()[0] == 1 && mouseIsDown == false){
            mouseIsDown = true;
            mouseTaskPress = -1;
            for (let key = 0; key < rankDisp.length; key++){
                let item = rankDisp[key];
                if (item.contains(mouse)){
                    if (whatSelfRanks[trialT].length<1){
                        item.color = "green";
                        mouseTaskPress = key;
                    }else if (whatSelfRanks[trialT][0] != key){
                        item.color = "blue";
                        mouseTaskPress = key;
                    } 
                    break;
                };
            };
         };

         if (mouse.getPressed()[0] == 0 && mouseIsDown){
            mouseIsDown = false;
            let taskCoincide = false;
            if (mouseTaskPress != -1){
                for (let key = 0; key < rankDisp.length; key++){
                    let item = rankDisp[key];
                    if (item.contains(mouse)){
                        if (key == mouseTaskPress){
                            whatSelfRanks[trialT].push(key);
                            taskCoincide = true;
                        }
                        break;
                    };
                };
                if (!taskCoincide)
                    rankDisp[mouseTaskPress].color = "white";
             };
         };

         let keys = ready.getKeys({keyList:[], waitRelease:false});
         _ready_allKeys = [].concat(keys);
         if (_ready_allKeys.length > 0) {
             ready.keys = _ready_allKeys[_ready_allKeys.length - 1].name;  // just the last key pressed
             ready.rt = _ready_allKeys[_ready_allKeys.length - 1].rt;
             ready.duration = _ready_allKeys[_ready_allKeys.length - 1].duration;
             if (ready.keys == 'r'){
                 for (let key = 0; key < rankDisp.length; key++){
                     rankDisp[key].color = 'white'
                 }
                 whatSelfRanks[trialT] = []
             };
         };
         if(whatSelfRanks[trialT].length >=2){
             questStim.autoDraw = true;
         }
         return Scheduler.Event.FLIP_REPEAT;
    }else{
        let ret = routOK();
        if (ret == 'k'){
            questStim.autoDraw = false;
            selfRankRT.push(clock.getTime() - tSelfRank);
            tSelfRank = clock.getTime();
            trialT += 1;
            for(let i = 0; i < 5; i++){
                rankDisp[i].autoDraw = false;
            }
            rankDisp = []
            if (trialT <2){
                selfRankText.text = "If you were going to involve yourself in a " + TASKNAME[trialT].toUpperCase() + ", which role would you place yourself in? \n\n Click on the labels below to select your role. The text will highlight GREEN for your first choice, and BLUE for your second choice"
                selfRankText.text += "\n If for any reason you need to reset your selection, please press 'r'"
                for(let i = 0; i < 5; i++){
                    let temp = new visual.TextStim({win:psychoJS.window,text:tasksAll[trialT][i],pos:rankDPos[i], height:0.05, wrapWidth:null, ori:0, color:'white', colorSpace:'rgb', opacity:1, languageStyle:'LTR', depth:0.0,font:'Arial', units:'height'})
                    temp.autoDraw = true;
                    rankDisp.push(temp);
                }
            }
        }else if (ret == 'r'){
            questStim.autoDraw = false;
            for (let key = 0; key < rankDisp.length; key++){
                rankDisp[key].color = 'white'
            }
            whatSelfRanks[trialT] = []

        }
        return Scheduler.Event.FLIP_REPEAT;
    }
}


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
