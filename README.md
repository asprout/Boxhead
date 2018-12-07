# Boxhead
Project repository for HRI project in Intelligent Robotics Lab.
The goal of this project is to investigate if and how robots elicit the social facilitation effect in humans.
Specifically, we are interested in whether the sociality of the robot influences the performance of the participant.
### Manipulation: the Sociality of Jibo
  - In both conditions, Jibo is placed to the right of (and a little behind) the desktop the participant is asked to use, and performs passive movement and ESML (embodied speech) behaviors.
#### Experimental Condition:
  - INTRO: The participant is introduced to Jibo and added to Jibo's loop with the help of the experimenter. 
  - Jibo is facing in the general direction of the participant. 
  - Glancing behavior: Jibo looks at the participant, the desktop, and then the participant again.
  - Jibo's ESML behaviors include screen-based expressions (e.g. changing the eye shape to look happy, etc.)
#### Control Condition:
  - INTRO: The participant is given the tablet, which allows them to play around with fields to have Jibo move or speak as specified.
  - Jibo is facing to the right of the participant, such that it does not look at the participant.
  - Glancing behavior: Occurs with the same chance and with the same movements, but without targets (and away from the participant)
  - Jibo's ESML behaviors are limited to body movements.

### Measures: Performance on Tasks
  - In all tasks, the hard version always precedes the easier version (as doing the easy version first will make the hard one easier)
#### Paired Association
  - Cue-response pairs are presented for x seconds each, y times each, randomly in a training period
  - In the testing period, participants are asked to identify if a given pair is correct
  - HARD: cue-response pairs are Japanese hiragana characters and their romanizations (vs. their English meanings in the EASY task)
#### Word Association
  - Words are given, and the participants are asked to come up with as many related single-word verbs as possible in the given time.
  - HARD: words have fewer related verbs (e.g. "kite" instead of "wheel")
#### Reading Comprehension
  - Participants asked to answer multiple choice questions based on given articles 
  - HARD: the given article is more esoteric and uses more high-level vocabulary; 5 multiple-choice responses are given instead of 4.

  

## Deliverables
### 10/12
  - [x] Submit IRB
  - [x] Finalize task measures
  - [x] Formalize unique robot identities for conditions
  - [x] Code
    - [x] Robot introduction
### 11/02
  - [x] Code
    - [x] Control behaviors
    - [x] Experimental behaviors
    - [x] Participant tasks
   - [x] Run pilot experiment
   - [x] Begin recruiting participants
### 12/03
  - [x] Run participants
  - [x] Data analysis
  - [x] Final report 
  
## Code Documentation:
### Jibo code
The code we developed for the Jibo app is located at Boxhead/app/src/main/java/com/example/android/boxhead/MainActivity.kt
To run it, you will need to install Android Studio and open the Boxhead app (which consists of everything in this repository but the psychopy and Report folders), and then click 'run'. The app has been designed for a Samsung Galaxy Tab A tablet; it will work on other android devices, but may look different than intended.
It is commented with explanations as to the purpose of each part, but please email one of the repository owners if you have any questions.
  
### Tasks code
The code for the performance tasks used for our experiment is at Boxhead/psychopy/tasks.py
Please read the readme in the psychopy folder, and again feel free to contact us with any questions.

## Member Contributions:
Both members worked on the materials for the IRB and designing the experiment, e.g. the performance tasks and formalizing the robot identities. Both members equally participated in recruiting and running participants, and in creating the various presentations throughout the semester.
Ling was responsible for writing the code for Jibo and the tablet app, and material such as the participant debriefing forms, posters, and the experimental questionnaire (e.g. survey measures). She was also in charge of the data analysis (R code), and the write-up of the final report. Ling was also the finance manager of this team. 
Nathan worked on the code for the performance tasks used for the experiment. He was also responsible for the formatting of the final report, and was the primary contributer for the methodology and conclusion sections. 
