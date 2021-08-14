package com.example.aiclean;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

public class SensorActivity extends AppCompatActivity {

    TextView textView;


    LinearLayout container;
    //ScrollView container;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sensor);

        textView = findViewById(R.id.textView);
        container = findViewById(R.id.container);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data");

        String str = data.message; //"3:aa:20:50:bb:25:40:cc:30:60:";//data.message;
        processIntent(intent);

        String getstr[] = str.split(":");
        int num = Integer.parseInt(getstr[0]);
        int index=1;
        for(int i=0;i<num;i++){
            LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.sensoritem, null);

            TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView);
            textViewLabel1.setText(getstr[index]);
            index++;

            TextView textViewLabel2 = (TextView)layoutExample.findViewById(R.id.textView6);
            textViewLabel2.setText(getstr[index]);
            index++;

            TextView textViewLabel3 = (TextView)layoutExample.findViewById(R.id.textView9);
            textViewLabel3.setText(getstr[index]);
            index++;

            container.addView(layoutExample);
        }
        /*
        for(int i=0;i<data.number;i++){
            LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            /* LayoutInflater inflater = LayoutInflater.from(MenuActivity.this);  LayoutInflate의 form 메서드를 호출 해도 가능 */

        //inflater.inflate(R.layout.sensoritem, container, true);
        //}*/

    }

    private void processIntent(Intent intent) {
        if (intent != null) {
            Bundle bundle = intent.getExtras();
            testData data = bundle.getParcelable("data");
            if (data != null) {
                textView.setText("전달 받은 데이터\nNumber : "
                        + "\nMessage : " + data.message);
            }
        }
    }
}