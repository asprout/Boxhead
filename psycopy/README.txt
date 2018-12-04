1) Open PscyoPy (http://psychopy.org/installation.html)

2) Make sure that you are in Coder View (on Mac, go to "View"->"Go to Coder View", and the shortcut is CMD+L)

3) Open the "tasks.py" file in PscyoPy

4) Click the green "Run" icon i the tool bar (or use CMD+R)

5) Enter the participants initials or number (even = experimental)

NOTE: In the control condition (PID is odd), a timer begins immediately as the introductory portion of the experiment is limited to 3 minutes, which is the approximate time it takes the experimental condition to complete their introductory portion (being added to Jibo's loop)


Task Descriptions (See application for actual variable values used)
In each case, the difficult version is always given BEFORE the easy version.

1) Paired association
	First they will be presented with each cue-response pair for x seconds. 
	Then, they will be tested to see if they can recognize which pairs are correct. 
	In this part, they should press the specified key if they think the answer is correct, else another specified key
	HARD: cue-response of Japanese character and romanization, instead its of English meaning

2) Word association
	They will be given a word, and they should write verbs related to the word for x seconds. 
	After each word they think of they should hit the "enter" key. Repeat with different words. 
	Manually done: check for "valid" responses as those that are actual single-word verbs
	HARD: words are harder to come up with verbs to use with

3) Reading comprehension
	They will first be asked to read articles. 
	They are given time limits for each page, but can click any key to move on the next page. They cannot move back pages.
	After reading, they will be asked a couple multiple-choice questions about each article. 
	They can use the appropriate letter key to record their response. 
	HARD: article more esoteric, and questions have 5 instead of 4 choices.
