package com.example.android.boxhead

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import com.jibo.apptoolkit.protocol.CommandLibrary
import com.jibo.apptoolkit.protocol.OnConnectionListener
import com.jibo.apptoolkit.protocol.model.EventMessage
import com.jibo.apptoolkit.android.JiboRemoteControl
import com.jibo.apptoolkit.android.model.api.Robot
import java.io.InputStream
import android.widget.Toast
import com.jibo.apptoolkit.protocol.model.Command
import kotlinx.android.synthetic.main.activity_main.*
import java.util.ArrayList

class MainActivity : AppCompatActivity(), OnConnectionListener, CommandLibrary.OnCommandResponseListener {

    // Variable for using the command library
    private var mCommandLibrary: CommandLibrary? = null
    // List of robots associated with a user's account
    private var mRobots: ArrayList<Robot>? = null

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
            var botList = "";
            while (i < mRobots!!.size) {
                botList += i.toString() + ": " + mRobots!!.get(i).getRobotName() + "\n"
                i++
            }

            Toast.makeText(this@MainActivity, botList, Toast.LENGTH_SHORT).show()

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
        buttonLogout.setOnClickListener{ onLogOutClick() }
        buttonSubmit.setOnClickListener{ onSubmitClick() }

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
            var myBot = mRobots!![0]
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


    // Say Hello World
    fun onSubmitClick() {
        // Assign variables
        pidName = inputName.text?.toString()
        pid = inputPID.text?.toString()?.toInt()

        if (mCommandLibrary != null) {
            val displayText = Command.DisplayRequest.TextView("display", pidName)
            mCommandLibrary?.display(displayText, this)
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
