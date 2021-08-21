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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

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

        try {
            JSONArray jsonArray = new JSONArray(data.message);
            for (int i=0; i < jsonArray.length(); i++)
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // Pulling items from the array
                String item1 = jsonObject.getString("name");
                String item2 = jsonObject.getString("temperature");
                String item3 = jsonObject.getString("humidity");

                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.sensoritem, null);

                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView);
                textViewLabel1.setText(item1);

                TextView textViewLabel2 = (TextView)layoutExample.findViewById(R.id.textView6);
                textViewLabel2.setText(item2);

                TextView textViewLabel3 = (TextView)layoutExample.findViewById(R.id.textView9);
                textViewLabel3.setText(item3);

                container.addView(layoutExample);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

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