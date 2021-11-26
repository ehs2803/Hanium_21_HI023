package com.example.testapp_7_18

import android.os.Bundle
import android.os.Handler
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class StartActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_start)
    }
    fun startclick(view: View){
        Toast.makeText(view.context, "살균을 시작합니다.", Toast.LENGTH_LONG).show()
        val mHandler = Handler()
        mHandler.postDelayed(Runnable {
            Toast.makeText(view.context, "살균이 완료됐습니다.", Toast.LENGTH_LONG).show()
        }, 3000) // 3초후

    }
}