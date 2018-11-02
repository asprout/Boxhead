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
    // Times last Jibo movement
    private var lastMoveTime: Long = 0
    // Variable to time Jibo's screen display
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
        backgroundTimer.schedule(BackgroundActivity(), 6000, 6000)
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

    /* BACKGROUND ACTIVITY FUNCTION (occurs every 10 seconds) */
    inner class BackgroundActivity : TimerTask() {

        override fun run() {
            runOnUiThread {
                if (mCommandLibrary != null && buttonBegin.isChecked) {
                    if (radioExperimental.isChecked)
                        glanceBehavior(15)
                    esmlPassive(50)
                    passiveMovement(50)
                }
            }
        }
    }

    // Say Hello World
    fun onSubmitClick() {
        // Assign variables

        if (mCommandLibrary != null && inputName.text != null && inputPID.text != null ) {
            pidName = inputName.text.toString()
            if (pidName == "" || inputPID.text?.toString() == "")
                return
            pid = inputPID.text.toString()?.toInt()
            displayText("Hi " + pidName + ". Please confirm your ID: " + pid)
            log("Displayed: Hi " + pidName + ". Please confirm your ID:" + pid)
        }

        /*
        val testvals = listOf(-4, -3, -2, -1, 0, 1, 2, 3, 4)
        for (i in testvals.indices){
            for (j in testvals.indices) {
                displayText("Position: " + testvals[i] + ", " + testvals[j])
                onMoveClick(intArrayOf(testvals[i], testvals[j], 1))
                Thread.sleep(2000)
            }
        }*/
    }

    /* Project-specific functions */

    private fun log(msg: String) {
        Log.d("Boxhead", msg)
    }

    private fun onSpeakClick() : String? {
        if (sayText.text != null)
            return say(sayText.text?.toString())
        return null
    }

    private fun onMoveClick() : String? {
        val posX = moveX.text.toString()
        val posY = moveY.text.toString()
        val posZ = moveZ.text.toString()
        if (posX != "" && posY != "" && posZ != "")
            return onMoveClick(intArrayOf(posX.toInt(), posY.toInt(), posZ.toInt()))

        return null
    }

    private fun onMoveClick(position: IntArray) : String? { // moves based on given position
        if (mCommandLibrary != null){
            lastMoveTime = System.currentTimeMillis()
            return mCommandLibrary?.lookAt(Command.LookAtRequest.PositionTarget(position), this)
        }
        return null
    }

    private fun canMove() : Boolean {
        if (System.currentTimeMillis() - lastMoveTime > 2000) return true
        return false
    }

    private fun passiveMovement(prob : Int){
        if (Math.random() * 100 > prob || !canMove())
            return
        val movevals = listOf(-4, -3, -2, -1, 0, 1, 2, 3, 4)
        if (radioControl.isChecked){
            onMoveClick(intArrayOf(movevals[(Math.random() * 5).toInt()], movevals[(Math.random() * 8).toInt()], 1))
        } else {
            onMoveClick(intArrayOf(movevals[(Math.random() * 5 + 4).toInt()], movevals[(Math.random() * 8).toInt()], 1))
        }
    }

    private fun esmlPassive(prob: Int) {
        if (mCommandLibrary != null) {
            if (Math.random() * 100 < prob && canMove()) {
                val rand = Math.random() * 100
                var text = "<anim cat='laughing' endNeutral='true' layers='body'/>"
                when{
                    rand < 16 -> text = "<anim cat='frustrated' endNeutral='true' layers='body'/>"
                    rand < 32 -> text = "<anim cat='affection' endNeutral='true' layers='body'/>"
                    rand < 48 -> text = "<anim cat='relieved' endNeutral='true' layers='body'/>"
                    rand < 64 -> text = "<anim cat='happy' endNeutral='true' layers='body'/>"
                    rand < 70 -> text = "<anim cat='excited' endNeutral='true' layers='body'/>"
                }
                lastMoveTime = System.currentTimeMillis()
                mCommandLibrary?.say(text, this)
                log("Passive behavior: $text")
            }
        }
    }

    private fun glanceBehavior(prob: Int){
        if (Math.random() * 100 < prob) {
            log("Glancing behavior activated")
            val returnPos = intArrayOf(2, -1, 1)
            onMoveClick(returnPos)
            val glanceTimer = object : CountDownTimer( 5000, 1000) {
                override fun onFinish() { onMoveClick(returnPos) ; log("Glance completed; now looking back.") }
                override fun onTick(millisUntilFinished: Long) {
                    if ((millisUntilFinished/1000).toInt() == 2)
                        log("Performing glance")
                        onMoveClick(intArrayOf(3, 1, 1))
                }
            }
            glanceTimer.start()
        }
    }

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

    private fun say(text : String?) : String? {
        if (mCommandLibrary != null && text != null && text != "") {
            log("Said: $text")
            return mCommandLibrary?.say(text, this)
        } else if (text != null)
            log("Say() not executed for: '" + text.substring(0, minOf(text.length, 40)) + "...'")
        return null
    }

    // Interact Button
    private fun onInteractClick() {
        if (mCommandLibrary != null) {
            return
        }
    }

    /* onCommandResponseListener overrides!
    Code for Jibo to perform: */

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
