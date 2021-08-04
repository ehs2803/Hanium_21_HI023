package com.example.cleanertest2;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class SensorActivity extends AppCompatActivity {

    TextView textView;

    LinearLayout container;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor);

        textView = findViewById(R.id.textView);
        container = findViewById(R.id.container);

        Intent intent = getIntent();
        processIntent(intent);

        for(int i=0;i<3;i++){
            LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            /* LayoutInflater inflater = LayoutInflater.from(MenuActivity.this);  LayoutInflate의 form 메서드를 호출 해도 가능 */

            inflater.inflate(R.layout.sensoritem, container, true);
        }

    }

    private void processIntent(Intent intent) {
        if (intent != null) {
            Bundle bundle = intent.getExtras();
            testData data = bundle.getParcelable("data");
            if (data != null) {
                textView.setText("전달 받은 데이터\nNumber : " + data.number
                        + "\nMessage : " + data.message);
            }
        }
    }
}