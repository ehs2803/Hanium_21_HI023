package com.example.testapp_7_18

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
    fun clickSensor(view: View){
        Toast.makeText(view.context,  "온습도 센서를 서버에서 받아옵니다.", Toast.LENGTH_LONG).show()
        var intent = Intent(this, SensorActivity::class.java)
        startActivity(intent)
    }
    fun clickStart(view: View){
        var intent = Intent(this, StartActivity::class.java)
        startActivity(intent)
    }
    fun clickDocument(view: View){
        var intent = Intent(this, DocumentActivity::class.java)
        startActivity(intent)
    }
}