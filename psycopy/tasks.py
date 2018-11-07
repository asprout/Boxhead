# encoding=utf-8
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random

# global variables

# experiment info initialization
expInfo = {'participant':'','group':'','id':''}
expInfo['dateStr'] = data.getDateStr()  # add the current time

# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Pre-Task Test', fixed=['dateStr'])
if dlg.OK:
    pass
else:
    core.quit()  # the user hit cancel so exit

# setting up the window and clocks
win = visual.Window(allowGUI=True, fullscr=True, 
                        monitor='testMonitor', units='deg')
globalClock = core.Clock()
trialClock = core.Clock()

# wait for enter function
def waitForEnter():
    thisResp = None
    while thisResp == None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey == 'return':
                thisResp = True
        event.clearEvents()


# # # # # # # # # # # # #
# paired assocation task:
# # # # # # # # # # # # #

#easy_cues      = [u"か", u"さ", u"た",  u"な", u"は", u"ま", u"や", u"ら",  u"わ"]
#easy_responses = ["ka", "sa", "ta", "na", "ha", "ma", "ya", "ra", "wa"]

#hard_cues      = [u"うえ", u"した", u"ひと", u"つき", u"やま", u"かわ", u"いす", u"かお", u"くち"]
#hard_responses = ["up", "down", "person", "moon", "mountain", "river", "chair", "face", "mouth"]

cues           = [u"うえ", u"した", u"ひと",  u"つき",  u"やま",     u"かわ", u"いす",  u"かお", u"くち",  u"みみ", u"あし", u"あめ", u"こえ",  u"えき",    u"いま", u"なか",   u"そと",    u"あさ",   u"よる",  u"ねこ", u"くも",  u"あめ", u"かさ",    u"ちず"]
hard_responses = ["ue",   "shita", "hito",  "tsuki", "yama",     "kawa",  "isu",   "kao",   "kuchi", "mimi", "ashi", "ame",   "koe",   "eki",     "ima",   "naka",   "soto",    "asa",     "yoru",  "neko",  "kumo",  "ame",  "kasa",    "chizu"]
easy_responses = ["up",   "down", "person", "moon",  "mountain", "river", "chair", "face",  "mouth", "ear",  "feet", "candy", "voice", "station", "now",   "inside", "outside", "morning", "night", "cat",   "cloud", "rain", "umbrella", "map"]

def pa_getInput(cue, response, same):
    # get input from user
    trialClock.reset()
    
    cue_message = visual.TextStim(win, pos=[0,3], font="Songti SC", text=cue)
    cue_message.draw()
    
    response_message = visual.TextStim(win, pos=[0,0], font="Courier", text=response)
    response_message.draw()
    
    win.flip()
    
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='up':
                if same:
                    thisResp = 1 # correct
                else:
                    thisResp = -1 # incorrect
            elif thisKey=='down':
                if same:
                    thisResp = -1 # incorrect
                else:
                    thisResp = 1 # correct
#            elif thisKey in ['q', 'escape']:
#                core.quit()  # abort experiment
        event.clearEvents()
        
    trialTime = trialClock.getTime()
    
#    win.flip()

    return (thisResp, trialTime)
    
def pa_train(cues, responses):
    # number of times each pair is shown
    num_trainings = 3
    # number of seconds each pair is shown
    time_per_pair = 1
    
    for j in range(num_trainings):
        # randomize order of cues each time
        trial_order = list(range(len(cues)))
        random.shuffle(trial_order)
        
        for i in trial_order:
            cue_message = visual.TextStim(win, pos=[0,3], font="Songti SC", text=cues[i])
            response_message = visual.TextStim(win, pos=[0,0], font="Courier", text=responses[i])
            cue_message.draw()
            response_message.draw()
            
            win.flip()
            
            core.wait(time_per_pair)
        
def pa_trial(cues, responses, i):
    # choose respective cue
    given_cue = i
    
    # flip coin, probably need to normalize
    flip = random.random()
    
    # based on flip, set same to True or False
    same = True
    if (flip >= 0.5):
        same = False
            
    cue = cues[given_cue]
    response = responses[given_cue]
    
    if (not same):
        while (response == responses[given_cue]):
            response = responses[random.randint(0, len(cues) - 1)]
    
    inputs = pa_getInput(cue, response, same)
    
    correctness = "False"
    if (inputs[0] == 1):
        correctness = "True"
        
    return (cue, inputs[1], correctness)
    
def pa_experiment(task_num):
    # make a text file to save data
    fileName = expInfo['participant'] + '_pa_'+ expInfo['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('cue,time,correctness\n')
    
    # Task description: training
    instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Task "+task_num+".a\n\nIn this task, you will be presented with pairs of cues and responses, and you should aim to remember which responses are associated with which cues.\n\nPress the 'enter' key to continue")
    instruction_message.draw()
    win.flip()
    
    waitForEnter()

    pa_train(cues, hard_responses)
    
    # Task description: testing
    instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Now you will be presented with a pair of a cue and response. If the correct response is listed for that given cue, click the 'up' arrow. Else, click the 'down' arrow if you think the incorrect reponse is listen for the given cue.\n\nPress the 'enter' key to continue ")
    instruction_message.draw()
    win.flip()
    
    waitForEnter()

    for i in range(len(cues)):
        output = pa_trial(cues, hard_responses, i)
        dataFile.write('%i,%.3f,%s\n' %(i, output[1], output[2]))
#        dataFile.write('%s,%.3f,%s\n' %(output[0], output[1], output[2])) # unicode issue
        
    instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Task "+task_num+".b\n\nIn this task, you will be presented with pairs of cues and responses, and you should aim to remember which responses are associated with which cues.\n\nPress the 'enter' key to continue")
    instruction_message.draw()
    win.flip()
    
    waitForEnter()
        
    pa_train(cues, easy_responses)
    
    instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Now you will be presented with a pair of a cue and response. If the correct response is listed for that given cue, click the 'up' arrow. Else, click the 'down' arrow if you think the incorrect reponse is listen for the given cue.\n\nPress the 'enter' key to continue ")
    instruction_message.draw()
    win.flip()
    
    waitForEnter()
    
    for i in range(len(cues)):
        output = pa_trial(cues, easy_responses, i)
        dataFile.write('%i,%.3f,%s\n' %(i, output[1], output[2]))
#        dataFile.write('%s,%.3f,%s\n' %(output[0], output[1], output[2]))
        
    dataFile.close()

# # # # # # # # # # # # #
# word association task:
# # # # # # # # # # # # #
easy_stimuli = ["rope", "ball", "wheel"]
hard_stimuli = ["kite", "scissors", "projector"]
#easy_stimuli = ["rope", "ball"]
#hard_stimuli = ["kite", "scissors"]
counter = core.CountdownTimer()

def oa_getInput(image):
    # get input from user
    trialClock.reset()

    xpos = -2
    letters = []
    word = ""
    
    cue_message = visual.ImageStim(win, pos=[0,5], image=image, size=(10))
    cue_message.draw()
    
    timer = visual.TextStim(win, text=str(int(counter.getTime())), pos=[14,10])
    timer.draw()
        
    win.flip()

    while counter.getTime() > 0:
        cue_message.draw()
        
        timer = visual.TextStim(win, text=str(int(counter.getTime())), pos=[14,10])
        timer.draw()
        
        allKeys=event.waitKeys(maxWait=1)
        
        if (allKeys != None):
            thisKey = allKeys[0]
            
            if (thisKey in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']):
                letters.append(visual.TextStim(win, pos=[xpos,-2], font="Courier", text=thisKey))
                word += thisKey
                xpos += 0.5
            elif (thisKey == 'backspace' and len(letters) > 0):
                letters.pop()
                word = word[:-1]
                xpos -= 0.5
            elif (thisKey == 'return'):
                break
            
            for letter in letters:
                letter.draw()
                
            win.flip()
            event.clearEvents()  # clear other (eg mouse) events - they clog the buffer
        else:
            for letter in letters:
                letter.draw()
            win.flip()
        
    trialTime = trialClock.getTime()
    
    win.flip()

    return (word, trialTime)

def wa_getInput(stimulus):
    # get input from user
    trialClock.reset()

    xpos = -2
    letters = []
    word = ""
    
    cue_message = visual.TextStim(win, pos=[0,3], font="Courier", text=stimulus)
    cue_message.draw()
    
    timer = visual.TextStim(win, text=str(int(counter.getTime())), pos=[14,10])
    timer.draw()
        
    win.flip()

    while counter.getTime() > 0:
        cue_message.draw()
        
        timer = visual.TextStim(win, text=str(int(counter.getTime())), pos=[14,10])
        timer.draw()
        
        allKeys=event.waitKeys(maxWait=1)
        
        if (allKeys != None):
            thisKey = allKeys[0]
            
            if (thisKey in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']):
                letters.append(visual.TextStim(win, pos=[xpos,0], font="Courier", text=thisKey))
                word += thisKey
                xpos += 0.5
            elif (thisKey == 'backspace' and len(letters) > 0):
                letters.pop()
                word = word[:-1]
                xpos -= 0.5
            elif (thisKey == 'return'):
                break
            
            for letter in letters:
                letter.draw()
                
            win.flip()
            event.clearEvents()  # clear other (eg mouse) events - they clog the buffer
        else:
            for letter in letters:
                letter.draw()
            win.flip()
        
    trialTime = trialClock.getTime()
    
    win.flip()

    return (word, trialTime)

def wa_experiment(task_num):
    # make a text file to save data
    fileName = expInfo['participant'] + '_wa_' + expInfo['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('stimulus,response,time\n')

    globalClock.reset()
    
    exp_letter = 'a'
    trial_time = 30
    
    for stimulus in hard_stimuli:
        instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Task "+task_num+"."+exp_letter+"\n\nIn this task, you will be presented with a word and you will need to write verbs related to that word. Your answers must be single words, composed entirely of alphabetic letters. Use the keyboard to record your responses, and hit the 'enter' key after each word you type.\n\nPress the 'enter' key to continue")
        instruction_message.draw()
        win.flip()
        exp_letter = chr(ord(exp_letter) + 1)
        waitForEnter()
        
        counter.reset(trial_time)
        while (counter.getTime() > 0):
            output = wa_getInput(stimulus)
    #        output = oa_getInput("ball.jpg")
            dataFile.write('%s,%s,%.3f\n' %(stimulus, output[0], output[1]))
    
    for stimulus in easy_stimuli:
        instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text="Task "+task_num+"."+exp_letter+"\n\nIn this task, you will be presented with a word and you will need to write verbs related to that word. Your answers must be single words, composed entirely of alphabetic letters. Use the keyboard to record your responses, and hit the 'enter' key after each word you type.\n\nPress the 'enter' key to continue")
        instruction_message.draw()
        win.flip()
        exp_letter = chr(ord(exp_letter) + 1)
        waitForEnter()
        
        counter.reset(trial_time)
        while (counter.getTime() > 0):
            output = wa_getInput(stimulus)
            dataFile.write('%s,%s,%.3f\n' %(stimulus, output[0], output[1]))
    
    dataFile.close()
    
# # # # # # # # # # # # #
# reading comprehension: 
# # # # # # # # # # # # #

def splitPage(article):
    i = 1000
    segs = []
    
    seg = article[:i]
    rest = article[i:]
    
    while (rest and not rest[0].isspace()):
        seg += rest[0]
        rest = rest[1:]
    
    if (seg[0] == " "):
        seg = seg[1:]
    segs.append(seg)
        
    while (len(seg) >= i):
        seg = rest[:i]
        rest = rest[i:]
        
        while (rest and not rest[0].isspace()):
            seg += rest[0]
            rest = rest[1:]
            
        if (seg[0] == " "):
            seg = seg[1:]
        segs.append(seg)
    
    return segs
    
def rc_train(article, article_type, dataFile):
    segs = splitPage(article)
    
    for seg in segs:
        counter = 100
        allKeys = None
        trialClock.reset()
        
        while (allKeys == None and counter >= 0):
            page = visual.TextStim(win, font="Georgia", text=seg)
            page.height = 0.6
            page.draw()
        
            timer = visual.TextStim(win, text=str(counter), pos=[14,10])
            counter -= 1
        
            timer.draw()
            win.flip()
            
            allKeys=event.waitKeys(maxWait=1)
        
        dataFile.write('%s,%.3f\n' %(article_type,trialClock.getTime()))

def multipleChoice(question, answers, correct_answer):
    trialClock.reset()
    
    question_message = visual.TextStim(win, font="Georgia", text=question, pos=(0,4))
    question_message.draw()
    
    letter = "a"
    letters = []
    answer_height = 0
    for answer in answers:
        letters.append(letter)
        numeration = letter + ") "
        answer_message = visual.TextStim(win, font="Georgia", text=numeration+answer, pos=(-5,answer_height), alignHoriz="left")
        answer_message.draw()
        answer_height -= 1.2
        letter = chr(ord(letter) + 1)
        
    win.flip()
            
    thisResp = None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey==correct_answer:
                thisResp = 1 # correct
            elif thisKey in letters:
                thisResp = -1 # incorrect
        event.clearEvents()
    
    trialTime = trialClock.getTime()
    
    correctness = "False"
    if (thisResp == 1):
        correctness = "True"
    
    return (correctness, trialTime)

def rc_experiment(task_num):
    # make a text file to save data
    fileName1 = expInfo['participant'] + '_rc1_' + expInfo['dateStr']
    fileName2 = expInfo['participant'] + '_rc2_' + expInfo['dateStr']
    
    dataFile1 = open(fileName1+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile1.write('article,time\n')

    question_message = visual.TextStim(win, font="Georgia", text="Task " + task_num + "\n\n You will now read some articles. After each article you will be asked to answer some questions. You will be given a limited time to read each page, but you can move on to the next page by clicking any key.\n\nPress the 'enter' key to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForEnter()

    hard_article = u'''
The field of Human–Robot Collaboration (HRC) is tasked with designing proactive and autonomous robot collaborators able to complement the superior capabilities of human workers to maximize throughput, improve safety of the workplace, and reduce cognitive load on humans. The general application domain for HRC is composed of a robot that collaborates with humans on a joint task such as furniture  assembly, assembly lines, or other factory-related applications. However, state of the art technologies still rely on sterile and rigid interactions that resort to turn-taking behaviors, tele-operation, or more generally limited autonomy and decision making capabilities. 

Conversely, human–human interaction (HHI) during teamwork does not show this friction. Fluent and natural HHIs are multimodal, highly contextual and situated. This is particularly true when coordination during teamwork is at tended through natural language. Humans resolve the natural ambiguities of speech by integrating verbal with non-verbal cues and, importantly, by grounding speech to the physical domain of the interaction—e.g. through implicature or lexical entrainment. 

Yet, despite evidence of the importance of situated natural language in HHI, achieving the same level of richness still represents a significant challenge for HRI in general and HRC in particular. Reasons for this are specific to HRC, e.g. the presence of noise in environments such as those commonly found in factories. Noisy environments may result in failure to recognize significant portions of an utterance—if not the totality of it. This not only leads to erroneous naming of specific actions and objects, but also makes the structure of sentences harder to parse by natural language understanding (NLU) algorithms that exploit syntax. Most notably, impediments to deploying effective HRC interactions are also to be found in the very nature of the communication itself. Communication during collaboration often occurs in a time constrained context, is highly goal-oriented, typically requires a high success rate in order to be effective, is domain-dependent, and often features mutual adaptation between peers. The time constraint during collaboration pressures agents to make shorter utterances that might not be well-formed sentences; the noise and the need for unambiguity favor some classes of words over others, often resulting in a highly domain-specific language. All these factors greatly hamper the deployment of standard NLU techniques to HRC. State-of-the-art technologies resort extensively to hand-coded domain knowledge, or require training on large datasets most of which are taken from descriptive text and are borrowed from different contexts that do not necessarily leverage the specific domain knowledge. Still, to achieve the level of fluency seen in HHIs, a core ability of future generations of robots will be for them to collaborate withhumans through the situated interactions with which humans are most comfortable. 
    '''
    
    easy_article = u'''
In an effort to minimize injury and let carpenters focus on design and other bigger-picture tasks, a team from MIT's Computer Science and Artificial Intelligence Laboratory (CSAIL) has created AutoSaw, a system that lets you customize different items that can then be constructed with the help of robots.

Users can choose from a range of carpenter-designed templates for chairs, desks and other furniture -- and eventually could use AutoSaw for projects as large as a deck or a porch.

"If you're building a deck, you have to cut large sections of lumber to length, and that's often done on site," says CSAIL postdoc Jeffrey Lipton, who was a lead author on a related paper about the system. "Every time you put a hand near a blade, you're at risk. To avoid that, we've largely automated the process using a chop-saw and jigsaw."

The system also gives general users more flexibility in designing furniture to be able to fit space-constrained houses and apartments. For example, it could allow you to modify a desk to squeeze into an L-shaped living room, or customize a table to fit in your micro-kitchen.

"Robots have already enabled mass production, but with artificial intelligence (AI) they have the potential to enable mass customization and personalization in almost everything we produce," says CSAIL director and co-author Daniela Rus. "AutoSaw shows this potential for easy access and customization in carpentry."

The paper, which will be presented in May at the International Conference on Robotics and Automation (ICRA) in Brisbane, Australia, was co-written by Lipton, Rus and PhD student Adriana Schulz. Other co-authors include MIT professor Wojciech Matusik, PhD student Andrew Spielberg and undergraduate Luis Trueba.
    '''
    
    question_message = visual.TextStim(win, font="Georgia", text="Article 1\n\nPress the 'enter' key to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForEnter()

    rc_train(hard_article, "hard", dataFile1)
    
    question_message = visual.TextStim(win, font="Georgia", text="Now you will need to answer some questions. Press the appropriate key for the answer choice you are choosing. For instance, press the 'c' key if you think choice 'c' is the correct answer.\n\nPress the 'enter' key to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForEnter()
    
    dataFile2 = open(fileName2+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile2.write('time,correctness\n')
    
    output = multipleChoice("Which of the above is not cited by the article an example of the joint tasks that humans can do with robots?", 
                            ["Furniture assembly","Assembly lines","Food preparation"], "c")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
                            
    output = multipleChoice("What do humans use to resolve the natural ambiguities of speech?", 
                            ["Non-verbal cues","Implicature","Written instructions","a & b only", "All of the above"], "d")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    question_message = visual.TextStim(win, font="Georgia", text="Article 2\n\nPress the 'enter' key to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForEnter()
    
    rc_train(easy_article, "easy", dataFile1)
    
    question_message = visual.TextStim(win, font="Georgia", text="Now you will need to answer some questions. Press the appropriate key for the answer choice you are choosing. For instance, press the 'c' key if you think choice 'c' is the correct answer.\n\nPress the 'enter' to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForEnter()
    
    output = multipleChoice("Where was the AutoSaw technology developed?", 
                            ["Stanford","Caltech", "MIT", "Harvard", "Yale"], "c")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
                            
    output = multipleChoice("How did the authors avoid having the user put their hand near the blades?", 
                            ["Automated process","Planning algorithms for cuts","Deep learning of common cuts"], "a")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    dataFile1.close()
    dataFile2.close()

exp_intro_message = u'''
For this experiment, you will be working with Jibo, a small tabletop social robot. 

Jibo’s “loop” is a group of people Jibo can recognize by face and voice, and is who Jibo considers his family. To get started, please take a few minutes to add yourself to Jibo’s loop. [INSTRUCTIONS TO ADD TO JIBO’S LOOP?] 

If you need assistance at any time during this or any later parts of the experiment, please feel free to ask the experimenter.'''

con_intro_message = u'''
For this experiment, you will be using Jibo, a small tabletop robot that can be programmed to move and speak, among other abilities. To get started, please take a few minutes to familiarize yourself with some simple Jibo commands on the tablet provided. 

Until told to, please do not click the “Begin” button on the tablet.

First, enter your name (or nickname) and given participant ID. Note that your name will not be associated with your PID or any performance measures when we perform the experimental analysis. Afterwards, feel free to experiment with the “Speak” and “Move” buttons until time is over. We suggest trying to move Jibo in various directions.

When it is time to move on, future instructions will be displayed on this screen.'''

pre_task_message = u'''
In this part of the experiment, you will complete a series of pre-tasks that we will use as baseline performance measures. You will not need Jibo or the tablet for this part of the experiment. Please click the “Begin” button on Jibo when you are ready to start, and then move on to the next page.'''

def main():
    # print out the correct introductory page for each setting
    if (expInfo['group'] in ['a', 'A']):
        introduction_message = visual.TextStim(win, font="Courier", text=exp_intro_message, height=0.5)
        introduction_message.draw()
        win.flip()
        waitForEnter()
    else:
        introduction_message = visual.TextStim(win, font="Courier", text=con_intro_message, height=0.5)
        introduction_message.draw()
        win.flip()
        waitForEnter()
        
    introduction_message = visual.TextStim(win, font="Courier", text=pre_task_message + "\n\nPress the 'enter' key when you are ready to continue", height=0.8)
    introduction_message.draw()
    win.flip()
    waitForEnter()
    
    participant_id = int(expInfo['id'])
    counterbalance_id = participant_id % 6
    if (counterbalance_id == 0): # pa, wa, rc
#        print("pa, wa, rc")
        pa_experiment('1')
        wa_experiment('2')
        rc_experiment('3')
    elif (counterbalance_id == 1): # pa, rc, wa
#        print("pa, rc, wa")
        pa_experiment('1')
        rc_experiment('2')
        wa_experiment('3')
    elif (counterbalance_id == 2): # wa, pa, rc
#        print("wa, pa, rc")
        wa_experiment('1')
        pa_experiment('2')
        rc_experiment('3')
    elif (counterbalance_id == 3): # wa, rc, pa
#        print("wa, rc, pa")
        wa_experiment('1')
        rc_experiment('2')
        pa_experiment('3')
    elif (counterbalance_id == 4): # rc, pa, wa
#        print("rc, pa, wa")
        rc_experiment('1')
        pa_experiment('2')
        wa_experiment('3')
    else: # rc, wa, pa
#        print("rc, wa, pa")
        rc_experiment('1')
        wa_experiment('2')
        pa_experiment('3')
    
    win.close()
    core.quit()

if __name__ == '__main__':
    main()
