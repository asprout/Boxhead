package com.example.android.boxhead

import android.app.Application
import com.jibo.apptoolkit.android.JiboRemoteControl

class BoxheadApp : Application() {

    override fun onCreate() {
        super.onCreate()

        JiboRemoteControl.init(this, getString(R.string.appId), getString(R.string.appSecret))
    }
}