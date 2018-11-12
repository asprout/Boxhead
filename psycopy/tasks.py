# encoding=utf-8
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random

# global variables

# experiment info initialization
expInfo = {'id':''}
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
def waitForRight():
    thisResp = None
    while thisResp == None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey == 'right':
                thisResp = True
        event.clearEvents()

def display_and_wait(string):
    # Task description: training
    instruction_message = visual.TextStim(win, pos=[0,0], font="Courier", text=string)
    instruction_message.draw()
    win.flip()
    
    waitForRight()

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
            if thisKey=='f':
                if same:
                    thisResp = 1 # correct
                else:
                    thisResp = -1 # incorrect
            elif thisKey=='j':
                if same:
                    thisResp = -1 # incorrect
                else:
                    thisResp = 1 # correct
        event.clearEvents()
        
    trialTime = trialClock.getTime()

    return (thisResp, trialTime)
    
def pa_train(cues, responses):
    # number of times each pair is shown
    num_trainings = 4
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
    
pa_task_introduction = "In this task, you will be presented with pairs of cues and responses, and your goal is to remember as many cue-response pairs as you can. There will be 6 trials of this task. In each trial there is a training part, where you will be given cue and response pairs and should aim to remember them as best you can, and a testing part where you will be tested on your memory of the correct cue-response pairs.\n\nPress the 'right' arrow to continue"

pa_training_instructions = "You will now be presented with cue and response pairs. The cue will be displayed on the top and the response will be displayed below the cue. You will be given about 30 seconds to try to learn these cue-response pairs.\n\nPress the 'right' arrow to begin"

pa_testing_instructions  = "Now you will be presented with cue-response pairs, for which the listed response may be the incorrect or correct response for that cue. If you believe the correct response is listed for that given cue, press the 'f' key. Else, press the 'j' key if you think the incorrect reponse is listed for the given cue.\n\nPress the 'right' arrow to begin"

def pa_experiment(task_num):
    # make a text file to save data
    fileName = expInfo['id'] + '_pa_'+ expInfo['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('cue,time,correctness\n')

    # Task introduction
    display_and_wait(pa_task_introduction)

    # hard tasks
    # Right now 3 trials of 8 pairs
    for i in range(3):
        # list slice to get one third of the cues/responses
        trial_cues = cues[i*8:(i+1)*8]
        trial_responses = hard_responses[i*8:(i+1)*8]

        # Task description: training
        display_and_wait("Task "+task_num+"\n\nTrial "+str(i+1)+" out of 6: Training\n\n" + pa_training_instructions)

        pa_train(trial_cues, trial_responses)
    
        # Task description: testing
        display_and_wait("Task "+task_num+"\n\nTrial "+str(i+1)+" out of 6: Testing\n\n" + pa_testing_instructions)

        for cue in range(len(trial_cues)):
            output = pa_trial(trial_cues, trial_responses, cue)
            dataFile.write('%i,%.3f,%s\n' %(cue, output[1], output[2]))

    # easy tasks
    # Right now 3 trials of 8 pairs
    for i in range(3):
        # list slice to get one third of the cues/responses
        trial_cues = cues[i*8:(i+1)*8]
        trial_responses = easy_responses[i*8:(i+1)*8]

        # Task description: training
        display_and_wait("Task "+task_num+"\n\nTrial "+str(i+4)+" out of 6: Training\n\n" + pa_training_instructions)

        pa_train(trial_cues, trial_responses)
    
        # Task description: testing
        display_and_wait("Task "+task_num+"\n\nTrial "+str(i+4)+" out of 6: Testing\n\n" + pa_training_instructions)

        for cue in range(len(trial_cues)):
            output = pa_trial(trial_cues, trial_responses, cue)
            dataFile.write('%i,%.3f,%s\n' %(cue, output[1], output[2]))
        
    dataFile.close()

# # # # # # # # # # # # #
# word association task:
# # # # # # # # # # # # #
easy_stimuli = ["rope", "ball", "wheel"]
hard_stimuli = ["kite", "scissors", "projector"]
counter = core.CountdownTimer()

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

wa_task_introduction = "In this task, you will be presented with a word, and your goal is to type as many verbs related to that word as possible. There will be 6 trials of this task. Your responses should all be single words, composed entirely out of letters. Use the keyboard to record your responses, and hit the 'enter' key after each word you type. While we will not count nonsense words or words that are not verbs, do not worry if you make any small typos. \n\nPress the 'right' arrow to continue"

wa_testing_message   = "You will be given 30 seconds to write as many verbs as you can think of. Remember to hit the 'enter' key after each word you type.\n\nPress the 'right' arrow to begin"

def wa_experiment(task_num):
    # make a text file to save data
    fileName = expInfo['id'] + '_wa_' + expInfo['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('stimulus,response,time\n')
    
    display_and_wait(wa_task_introduction)

    globalClock.reset()
    
    exp_letter = 'a'
    trial_time = 30
    trial = 1
    
    for stimulus in hard_stimuli:
        display_and_wait("Task "+task_num+"\n\nTrial "+str(trial)+" out of 6\n\n" + wa_testing_message)

        exp_letter = chr(ord(exp_letter) + 1)
        trial += 1

        counter.reset(trial_time)
        while (counter.getTime() > 0):
            output = wa_getInput(stimulus)
            dataFile.write('%s,%s,%.3f\n' %(stimulus, output[0], output[1]))
    
    for stimulus in easy_stimuli:
        display_and_wait("Task "+task_num+"\n\nTrial "+str(trial)+" out of 6\n\n" + wa_testing_message)

        exp_letter = chr(ord(exp_letter) + 1)
        trial += 1
        
        counter.reset(trial_time)
        while (counter.getTime() > 0):
            output = wa_getInput(stimulus)
            dataFile.write('%s,%s,%.3f\n' %(stimulus, output[0], output[1]))
    
    dataFile.close()
    
# # # # # # # # # # # # #
# reading comprehension: 
# # # # # # # # # # # # #

def splitPage(article):
    i = 1100
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
    
    question_message = visual.TextStim(win, font="Courier", text=question, pos=(0,4))
    question_message.draw()
    
    letter = "a"
    letters = []
    answer_height = 0
    for answer in answers:
        letters.append(letter)
        numeration = letter + ") "
        answer_message = visual.TextStim(win, font="Courier", text=numeration+answer, pos=(-5,answer_height), alignHoriz="left")
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
    fileName1 = expInfo['id'] + '_rc1_' + expInfo['dateStr']
    fileName2 = expInfo['id'] + '_rc2_' + expInfo['dateStr']
    
    dataFile1 = open(fileName1+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile1.write('article,time\n')

    question_message = visual.TextStim(win, font="Courier", text="Task " + task_num + "\n\n As a last pre-task, you will now be given a couple of short articles about robotics to read. After each article, you will be asked to answer a few questions in order to test your comprehension. You will be given a limited but sufficient amount of time to read each page - the purpose of this task is not to memorize every detail, but to simply understand the main ideas of the articles, so if you finish reading a page before the time is over, please move on to the next page by clicking any key.\n\nPress the 'right' arrow to continue", height=0.7)
    question_message.draw()

    win.flip()
    
    waitForRight()

    hard_article = u'''
The field of Human–Robot Collaboration (HRC) is tasked with designing proactive and autonomous robot collaborators able to complement the superior capabilities of human workers to maximize throughput, improve safety of the workplace, and reduce cognitive load on humans. The general application domain for HRC is composed of a robot that collaborates with humans on a joint task such as furniture  assembly, assembly lines, or other factory-related applications. However, state of the art technologies still rely on sterile and rigid interactions that resort to turn-taking behaviors, tele-operation, or more generally limited autonomy and decision making capabilities. 

Conversely, human–human interaction (HHI) during teamwork does not show this friction. Fluent and natural HHIs are multimodal, highly contextual and situated. This is particularly true when coordination during teamwork is attended through natural language. Humans resolve the natural ambiguities of speech by integrating verbal with non-verbal cues and, importantly, by grounding speech to the physical domain of the interaction — e.g. through implicature or lexical entrainment. 

Yet, despite evidence of the importance of situated natural language in HHI, achieving the same level of richness still represents a significant challenge for HRI in general and HRC in particular. Reasons for this are specific to HRC, e.g. the presence of noise in environments such as those commonly found in factories. Noisy environments may result in failure to recognize significant portions of an utterance—if not the totality of it. This not only leads to erroneous naming of specific actions and objects, but also makes the structure of sentences harder to parse by natural language understanding (NLU) algorithms that exploit syntax. Most notably, impediments to deploying effective HRC interactions are also to be found in the very nature of the communication itself. Communication during collaboration often occurs in a time constrained context, is highly goal-oriented, typically requires a high success rate in order to be effective, is domain-dependent, and often features mutual adaptation between peers. The time constraint during collaboration pressures agents to make shorter utterances that might not be well-formed sentences; the noise and the need for unambiguity favor some classes of words over others, often resulting in a highly domain-specific language. All these factors greatly hamper the deployment of standard NLU techniques to HRC. State-of-the-art technologies resort extensively to hand-coded domain knowledge, or require training on large datasets most of which are taken from descriptive text and are borrowed from different contexts that do not necessarily leverage the specific domain knowledge. Still, to achieve the level of fluency seen in HHIs, a core ability of future generations of robots will be for them to collaborate with humans through the situated interactions with which humans are most comfortable. 
    '''
    
    easy_article = u'''
In an effort to minimize injury and let carpenters focus on design and other bigger-picture tasks, a team from MIT's Computer Science and Artificial Intelligence Laboratory (CSAIL) has created AutoSaw, a system that lets you customize different items that can then be constructed with the help of robots.

Users can choose from a range of carpenter-designed templates for chairs, desks and other furniture -- and eventually could use AutoSaw for projects as large as a deck or a porch.

"If you're building a deck, you have to cut large sections of lumber to length, and that's often done on site," says CSAIL postdoc Jeffrey Lipton, who was a lead author on a related paper about the system. "Every time you put a hand near a blade, you're at risk. To avoid that, we've largely automated the process using a chop-saw and jigsaw."

The system also gives general users more flexibility in designing furniture to be able to fit space-constrained houses and apartments. For example, it could allow you to modify a desk to squeeze into an L-shaped living room, or customize a table to fit in your micro-kitchen.

"Robots have already enabled mass production, but with artificial intelligence (AI) they have the potential to enable mass customization and personalization in almost everything we produce," says CSAIL director and co-author Daniela Rus. "AutoSaw shows this potential for easy access and customization in carpentry."

The paper, which will be presented in May at the International Conference on Robotics and Automation (ICRA) in Brisbane, Australia, was co-written by Lipton, Rus and PhD student Adriana Schulz. Other co-authors include MIT professor Wojciech Matusik, PhD student Andrew Spielberg and undergraduate Luis Trueba.
    '''
    
    question_message = visual.TextStim(win, font="Courier", text="Article 1 of 2\n\nPress the 'right' arrow to begin", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForRight()

    rc_train(hard_article, "hard", dataFile1)
    
    question_message = visual.TextStim(win, font="Courier", text="Now you will answer some questions about the article you just read. Press the appropriate key for the answer choice you are choosing. For instance, press the 'c' key if you think choice 'c' is the correct answer.\n\nPress the 'right' arrow to begin", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForRight()
    
    dataFile2 = open(fileName2+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile2.write('time,correctness\n')
    
    output = multipleChoice("Which of these choices are examples of the joint tasks that humans can do with robots in the domain of HRC, according by the article?", 
                            ["Furniture assembly","Assembly lines","Car assembly", "a & b", "All of the above"], "d")

    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))

    output = multipleChoice("Which of these choices is NOT cited by the article as examples of what is current being used by state of the art technologies?", 
                            ["Turn-taking behaviors","Hand-coded domain knowledge","Deep learning", "Tele-operation", "b & c"], "c")
                                                      
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    output = multipleChoice("Which of these choices is NOT cited by the article an example of how robot collaborators can benefit humans?", 
                            ["Maximize throughput","Improve safety", "Improve quality", "Reduce cognitive load", "b & c"], "c")
                                                        
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
                            
    output = multipleChoice("Which of these choices are cited by the article an ways that humans resolve the natural ambiguities of speech?", 
                            ["Non-verbal cues", "Implicature", "Lexical entrainment","a & b only", "All of the above"], "e")
                                                        
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    question_message = visual.TextStim(win, font="Courier", text="Article 2 of 2\n\nPress the 'right' arrow to continue", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForRight()
    
    rc_train(easy_article, "easy", dataFile1)
    
    question_message = visual.TextStim(win, font="Courier", text="Now you will answer some questions about the article you just read. Press the appropriate key for the answer choice you are choosing. For instance, press the 'c' key if you think choice 'c' is the correct answer.\n\nPress the 'right' arrow to begin", pos=(0,4))
    question_message.draw()

    win.flip()
    
    waitForRight()


    output = multipleChoice("Which of these choices is NOT cited by the article as motivations for the development of AutoSaw?", 
                            ["To let users focus on design", "To increase output", "To minimize injury", "To let users focus on bigger-picture tasks"], "b")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    output = multipleChoice("Where was the AutoSaw technology developed?", 
                            ["Stanford", "Caltech", "MIT", "Yale"], "c")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
                            
    output = multipleChoice("How did the authors avoid having the user put their hand near the blades?", 
                            ["Automated process","Planning algorithms","Deep learning of cuts", "a & b"], "a")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    output = multipleChoice("What do the authors say that technologies like AutoSaw will enable?", 
                            ["Mass production","Mass customization","Mass recycling", "Mass Organization"], "b")
                            
    dataFile2.write('%s,%.3f\n' %(output[0], output[1]))
    
    dataFile1.close()
    dataFile2.close()

exp_intro_message = u'''
For this experiment, you will be working with Jibo, a small tabletop social robot. Jibo’s “loop” is a group of people Jibo can recognize by face and voice, and is who Jibo considers his family. To get started, please take a few minutes to add yourself to Jibo’s loop. An experimenter will help you complete this part of the experiment.'''

control_intro_message = u'''
For this experiment, you will be using Jibo, a small tabletop robot that can be programmed to move and speak, and do other behaviors. To get started, you will spend a few minutes to familiarize yourself with some simple Jibo commands on the tablet provided. Until told to do so, please do not click the “Begin” button on the tablet.

First, enter your name (or desired nickname) and given participant ID. Note that your identity (i.e. name) will not be associated with your PID or any of the performance measures when in the experimental analysis. Afterward confirming your name and PID, feel free to experiment with the “Speak” and “Move” buttons until time is over. We suggest trying to move Jibo in various directions.

When it is time to move on, future instructions will be displayed on this screen.
'''

pre_task_message = u'''
In this part of the experiment, you will complete a series of tasks that we will use to calculate baseline performance measures for each participant. You will only need this computer for this part of the experiment. Since you will not need a robot or tablet for this part, let's turn Jibo on to a non-interactive behavior mode. Please click the “Begin” button on Jibo when you are ready to begin, and then move on to the next page. If you need assistance at any time, please feel free to ask the experimenter.'''

def main():
    participant_id = int(expInfo['id'])

    if ((participant_id % 2) == 0): # experimental        introduction_message = visual.TextStim(win, font="Courier", text=exp_intro_message, height=0.8)        introduction_message.draw()        win.flip()        waitForRight()    else: # control        timer = core.CountdownTimer()        timer.reset(180)                while (timer.getTime() > 0):            timer_stim = visual.TextStim(win, text=str(int(timer.getTime())), pos=[14,10])            timer_stim.draw()                        introduction_message = visual.TextStim(win, font="Courier", text=control_intro_message, height=0.7)            introduction_message.draw()            
            win.flip()

    introduction_message = visual.TextStim(win, font="Courier", text=pre_task_message + "\n\nPress the 'right' arrow to continue", height=0.7)
    introduction_message.draw()
    win.flip()
    waitForRight()
    
    pa_experiment('1')
    wa_experiment('2')
    rc_experiment('3')

#     counterbalance_id = participant_id % 6
#     if (counterbalance_id == 0): # pa, wa, rc
# #        print("pa, wa, rc")
#         pa_experiment('1')
#         wa_experiment('2')
#         rc_experiment('3')
#     elif (counterbalance_id == 1): # pa, rc, wa
# #        print("pa, rc, wa")
#         pa_experiment('1')
#         rc_experiment('2')
#         wa_experiment('3')
#     elif (counterbalance_id == 2): # wa, pa, rc
# #        print("wa, pa, rc")
#         wa_experiment('1')
#         pa_experiment('2')
#         rc_experiment('3')
#     elif (counterbalance_id == 3): # wa, rc, pa
# #        print("wa, rc, pa")
#         wa_experiment('1')
#         rc_experiment('2')
#         pa_experiment('3')
#     elif (counterbalance_id == 4): # rc, pa, wa
# #        print("rc, pa, wa")
#         rc_experiment('1')
#         pa_experiment('2')
#         wa_experiment('3')
#     else: # rc, wa, pa
# #        print("rc, wa, pa")
#         rc_experiment('1')
#         wa_experiment('2')
#         pa_experiment('3')
    
    introduction_message = visual.TextStim(win, font="Courier", text="You've finished this part of the experiment! Please let an experimenter know that you are done.")
    introduction_message.draw()
    win.flip()
    waitForRight()
    
    win.close()
    core.quit()

if __name__ == '__main__':
    main()
