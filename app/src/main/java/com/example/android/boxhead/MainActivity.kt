package com.example.android.boxhead

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.os.CountDownTimer
import android.util.Log
import com.jibo.apptoolkit.protocol.CommandLibrary
import com.jibo.apptoolkit.protocol.OnConnectionListener
import com.jibo.apptoolkit.protocol.model.EventMessage
import com.jibo.apptoolkit.android.JiboRemoteControl
import com.jibo.apptoolkit.android.model.api.Robot
import java.io.InputStream
import android.widget.Toast
import com.example.android.boxhead.R.id.inputName
import com.example.android.boxhead.R.id.inputPID
import com.jibo.apptoolkit.protocol.model.Command
import kotlinx.android.synthetic.main.activity_main.*
import java.util.*
import kotlin.math.log

class MainActivity : AppCompatActivity(), OnConnectionListener, CommandLibrary.OnCommandResponseListener {

    // Variable for using the command library
    private var mCommandLibrary: CommandLibrary? = null
    // List of robots associated with a user's account
    private var mRobots: ArrayList<Robot>? = null
    private var myBotNum: Int = 0
    // Time of last Jibo movement, to prevent calls canceling each other out
    private var lastMoveTime: Long = 0
    // Variable to time Jibo's screen display and revert to normal eye at end
    private var displayTimer: CountDownTimer? = object : CountDownTimer(8000, 1000) {
        override fun onFinish() { // after some time of displaying text, display the eye again
            mCommandLibrary?.display(Command.DisplayRequest.EyeView("eye"), null)
        }
        override fun onTick(millisUntilFinished: Long) {}
    }

    // Variables for the experiment
    private var pid: Int? = null
    private var pidName: String? = null

    // Authentication
    private val onAuthenticationListener = object : JiboRemoteControl.OnAuthenticationListener {

        override fun onSuccess(robots: ArrayList<Robot>) {

            // Add the list of user's robots to the robots array
            mRobots = ArrayList(robots)

            // Print a list of all robots associated with the account and their index in the array
            // so we can choose the one we want to connect to
            var i = 0
            var botList = ""
            while (i < mRobots!!.size) {
                botList += i.toString() + ": " + mRobots!!.get(i).robotName + "\n"
                if (mRobots!!.get(i).robotName == "Chrome-Data-Pitaya-Calico") {
                    myBotNum = i
                    log("Chrome found")
                }
                i++
            }

            Toast.makeText(this@MainActivity, botList, Toast.LENGTH_SHORT).show()
            log(botList)

            // Disable Log In and enable Connect and Log Out buttons when authenticated
            buttonLogin?.isEnabled = false
            buttonConnect?.isEnabled = true
            buttonLogout?.isEnabled = true
        }

        // If there's an authentication error
        override fun onError(throwable: Throwable) {
            // Log the error to the app
            Toast.makeText(this@MainActivity, "API onError:" + throwable.localizedMessage, Toast.LENGTH_SHORT).show()
        }

        // If there's an authentication cancellation
        override fun onCancel() {
            // Log the cancellation to the app
            Toast.makeText(this@MainActivity, "Authentication canceled", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Assign all buttons a function when clicked
        buttonLogin.setOnClickListener { onLoginClick() }
        buttonConnect.setOnClickListener { onConnectClick() }
        buttonDisconnect.setOnClickListener { onDisconnectClick() }
        buttonLogout.setOnClickListener { onLogOutClick() }
        buttonSubmit.setOnClickListener { onSubmitClick() }
        buttonConfirm.setOnClickListener { onConfirmClick() }
        buttonMove.setOnClickListener { onMoveClick() }
        buttonSpeak.setOnClickListener { onSpeakClick() }

        // Start with only the Log In button enabled
        buttonLogin.isEnabled = true
        buttonConnect.isEnabled = false
        buttonDisconnect.isEnabled = false
        buttonLogout.isEnabled = false
    }

    // Our connectivity functions

    // Log In
    fun onLoginClick() {
        JiboRemoteControl.instance.signIn(this, onAuthenticationListener)
    }

    // Connect
    fun onConnectClick() {

        // Make sure there is at least one robot on the account
        if (mRobots?.size == 0) {
            Toast.makeText(this@MainActivity, "No robots found for this account", Toast.LENGTH_SHORT).show()
        }
        // Connect to the first robot on the account.
        // To connect to a different robot, replace `0` in the code below with the index
        // printed on-screen next to the correct robot name
        else {
            var myBot = mRobots!![myBotNum]
            JiboRemoteControl.instance.connect(myBot, this)
        }

        // Disable the connect button while we're connecting
        // to prevent double-clicking
        buttonConnect?.isEnabled = false
    }

    // Disconnect
    fun onDisconnectClick() {
        JiboRemoteControl.instance.disconnect()

        // Disable the disconnect button while disconnecting
        buttonDisconnect?.isEnabled = false
    }

    // Log out
    fun onLogOutClick() {
        JiboRemoteControl.instance.logOut()

        // Once we're logged out, only enable Log In button
        buttonLogin?.isEnabled = true
        buttonLogout?.isEnabled = false
        buttonConnect?.isEnabled = false
        buttonDisconnect?.isEnabled = false

        // Log that we've logged out to the app
        Toast.makeText(this@MainActivity, "Logged Out", Toast.LENGTH_SHORT).show()
    }

    override fun onConnected() {}

    override fun onSessionStarted(commandLibrary: CommandLibrary) {
        mCommandLibrary = commandLibrary
        runOnUiThread {
            // Once we're connected and ready for commands, enable disconnect
            buttonDisconnect?.isEnabled = true

            // Log that we're connected to the app
            Toast.makeText(this@MainActivity, "Connected", Toast.LENGTH_SHORT).show()
        }
        // start running the background activity
        val backgroundTimer = Timer()
        backgroundTimer.schedule(BackgroundActivity(), 2000, 6000)
    }

    override fun onConnectionFailed(throwable: Throwable) {
        runOnUiThread {
            // If connection fails, re-enable the Connect button so we can try again
            buttonConnect?.isEnabled = true

            // Log the error to the app
            Toast.makeText(this@MainActivity, "Connection failed", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onDisconnected(i: Int) {
        runOnUiThread {
            // Re-enable Connnect & Say when we're disconnected
            buttonConnect?.isEnabled = true

            // Log that we've disconnected from the app
            Toast.makeText(this@MainActivity, "Disconnected", Toast.LENGTH_SHORT).show()
        }
    }

    /* BACKGROUND ACTIVITY FUNCTION (occurs every x seconds) */
    inner class BackgroundActivity : TimerTask() {

        override fun run() {
            // when called, while the Begin button is clicked, perform the behaviors by probability
            runOnUiThread {
                if (mCommandLibrary != null && buttonBegin.isChecked) {
                    if (!glanceBehavior(25)) {
                        if (!esmlPassive(50))
                            passiveMovement(60)
                    }
                }
            }
        }
    }

    private fun log(msg: String) {
        Log.d("Boxhead", msg)
    }

    /* Project-specific functions */

    fun onSubmitClick() { // Called when the Submit button is clicked
        // Displays the name and PID entered into the tablet, if properly inputted
        if (mCommandLibrary != null && inputName.text != null && inputPID.text != null) {
            pidName = inputName.text.toString()
            if (pidName == "" || inputPID.text?.toString() == "")
                return
            pid = inputPID.text.toString()?.toInt()
            displayText("Hi " + pidName + ". Please confirm your ID: " + pid)
            log("Submit button clicked.")
        }
    }

    fun onConfirmClick() { // Called when the Confirm button is clicked
        // Assign variables
        if (mCommandLibrary != null && inputName.text != null && inputPID.text != null ) {
            pidName = inputName.text.toString()
            if (pidName == "" || inputPID.text?.toString() == "")
                return
            pid = inputPID.text.toString()?.toInt()
            displayText("Confirmed: " + pidName + ", PID:" + pid)
            log("Confirm button clicked.")
        }
    }

    private fun onSpeakClick() : String? { // Called when the Speak button is clicked
        if (sayText.text != null) // If proper input, has Jibo say the name in the sayText field
            return say(sayText.text?.toString())
        return null
    }

    private fun onMoveClick() : String? { // Called when the Move button is clicked
        val posX = moveX.text.toString()
        val posY = moveY.text.toString()
        val posZ = moveZ.text.toString()
        if (posX != "" && posY != "" && posZ != "") {
            // if proper input, has Jibo move to the input (X, Y, Z) position
            log("Moving to position: " + posX + " " + posY + " " + posZ)
            return onMoveClick(intArrayOf(posX.toInt(), posY.toInt(), posZ.toInt()))
        }
        return null
    }

    private fun onMoveClick(position: IntArray) : String? { // moves Jibo based on given position
        if (mCommandLibrary != null){
            lastMoveTime = System.currentTimeMillis()
            log("Moving to position: " + position[0] + " " + position[1] + " " + position[2])
            return mCommandLibrary?.lookAt(Command.LookAtRequest.PositionTarget(position), this)
        }
        return null
    }

    private fun canMove() : Boolean { // returns true if 3s has passed since last move
        if (System.currentTimeMillis() - lastMoveTime > 3000) return true
        return false
    }

    // returns a random number in the range of [lb, ub]
    private fun randNumInRange(lb : Int, ub : Int): Int {
        return (Math.random() * (ub - lb + 1)).toInt() + lb
    }

    // has Jibo perform a passive movement with probability prob (out of 100),
    // where a passive movement is to turn to any of the positions in a specified range
    private fun passiveMovement(prob : Int): Boolean {
        if (Math.random() * 100 > prob || !canMove())
            return false
        // control: x: -1 to 2, y: 2 to 5
        // exp: x: 1 to 4, y: -2 to 1
        log("Performing passive movement")
        if (radioControl.isChecked){
            onMoveClick(intArrayOf(randNumInRange(-1, 2), randNumInRange(2, 5), randNumInRange(-1, 1)))
        } else {
            onMoveClick(intArrayOf(randNumInRange(1, 4), randNumInRange(-2, 1), randNumInRange(-1, 1)))
        }
        return true
    }

    // function returns a random item from an array of strings 'list'
    private fun getRandom(list: List<String>?): String {
        if (list == null)
            return ""
        return list[(Math.random() * list.size).toInt()]
    }

    // has Jibo perform a passive ESML behavior with probability prob (out of 100)
    // where for the experimental condition, behaviors may also include screen behaviors
    // (such as showing changes in eye shape)
    private fun esmlPassive(prob: Int) : Boolean {
        if (mCommandLibrary != null) {
            val controlESML = listOf("<anim cat='laughing' endNeutral='true' layers='body'/>",
                    "<anim cat='frustrated' endNeutral='true' layers='body'/>", "<anim cat='affection' endNeutral='true' layers='body'/>",
                    "<anim cat='relieved' endNeutral='true' layers='body'/>",
                    "<anim cat='happy' endNeutral='true' layers='body'/>", "<anim cat='excited' endNeutral='true' layers='body'/>",
                    "<anim cat='confused' endNeutral='true' layers='body'/>", "<anim cat='embarrassed' endNeutral='true' layers='body'/>")
            val expESML = listOf("<anim cat='laughing' endNeutral='true'/>", "<anim cat='frustrated' endNeutral='true' layers='body'/>",
                    "<anim cat='affection' endNeutral='true' layers='body'/>", "<anim cat='relieved' endNeutral='true'/>",
                    "<anim cat='happy' endNeutral='true'/>", "<anim cat='excited' endNeutral='true'/>",
                    "<anim cat='confused' endNeutral='true'/>", "<anim cat='embarrassed' endNeutral='true'/>")
            // confused, embarrassed
            if (Math.random() * 100 < prob && canMove()) {
                var text = getRandom(controlESML)
                if (radioExperimental.isChecked)
                    text = getRandom(expESML)
                lastMoveTime = System.currentTimeMillis()
                mCommandLibrary?.say(text, this)
                log("Passive ESML behavior: $text")
                return true
            }
        }
        return false
    }

    // with prob/100 probability, performs a glance behavior from one area to another, then back
    // (in this experiment, looks at the participant, screen, and then back)
    private fun glanceBehavior(prob: Int): Boolean {
        if (Math.random() * 100 < prob) {
            log("Glancing behavior activated")
            var returnPos = intArrayOf(3, 0, 1)
            if (radioControl.isChecked)
                returnPos = intArrayOf(3, 5, 1)
            onMoveClick(returnPos)
            val glanceTimer = object : CountDownTimer(6000, 1000) {
                override fun onFinish() { onMoveClick(returnPos) ; log("Glance completed; now looking back.") }
                override fun onTick(millisUntilFinished: Long) {
                    if ((millisUntilFinished/1000).toInt() == 3)
                        if (radioControl.isChecked)
                            onMoveClick(intArrayOf(0, 5, 1))
                        else
                            onMoveClick(intArrayOf(2, -1, 1))
                }
            }
            glanceTimer.start()
            return true
        }
        return false
    }

    // displays text on Jibo's screen for a short amount of time
    private fun displayText(text: String){
        if (mCommandLibrary != null){
            val displayText = text.replace("(.{40,}? )".toRegex(), "$1\n")
            val toDisplay = Command.DisplayRequest.TextView("display", displayText)
            mCommandLibrary?.display(toDisplay, this)
            displayTimer?.cancel()
            displayTimer?.start() // start timer for when to display the eye again
            log("Displayed: $text")
        }
    }

    // Tells Jibo to speak text
    private fun say(text : String?) : String? {
        if (mCommandLibrary != null && text != null && text != "") {
            log("Said: $text")
            return mCommandLibrary?.say(text, this)
        } else if (text != null)
            log("Say() not executed for: '" + text.substring(0, minOf(text.length, 40)) + "...'")
        return null
    }

    /* onCommandResponseListener overrides! */
    override fun onSuccess(s: String) {
        runOnUiThread { }
    }

    override fun onError(s: String, s1: String) {
        runOnUiThread {
            // Log the error to the app
            Toast.makeText(this@MainActivity, "error : $s $s1", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onEventError(s: String, errorData: EventMessage.ErrorEvent.ErrorData) {

        runOnUiThread {
            // Log the error to the app
            Toast.makeText(this@MainActivity, "error : " + s + " " + errorData.errorString, Toast.LENGTH_SHORT).show()
        }
    }

    override fun onSocketError() {
        runOnUiThread {
            // Log the error to the app
            Toast.makeText(this@MainActivity, "socket error", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onEvent(s: String, baseEvent: EventMessage.BaseEvent) {}

    override fun onPhoto(s: String, takePhotoEvent: EventMessage.TakePhotoEvent, inputStream: InputStream) {}

    override fun onVideo(s: String, videoReadyEvent: EventMessage.VideoReadyEvent, inputStream: InputStream) {}

    override fun onListen(s: String, s1: String) {}

    override fun onParseError() {}

}
