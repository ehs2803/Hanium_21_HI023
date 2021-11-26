package com.example.aiclean;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class DeviceActivity extends AppCompatActivity {
    LinearLayout container1;
    LinearLayout container2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ActionBar actionBar = getSupportActionBar();
        actionBar.hide();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data");

        container1 = findViewById(R.id.container1);
        container2 = findViewById(R.id.container2);

        try {
            JSONArray jsonArray = new JSONArray(data.message);
            for (int i=0; i < jsonArray.length(); i++)
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // Pulling items from the array
                String item1 = jsonObject.getString("type");
                String item2 = jsonObject.getString("name");
                String item3 = jsonObject.getString("id");

                if(item1.equals("cleaner")) continue;

                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.deviceitem, null);

                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView_name);
                textViewLabel1.setText(item2);

                TextView textViewLabel2 = (TextView)layoutExample.findViewById(R.id.textView_id);
                textViewLabel2.setText(item3);

                container1.addView(layoutExample);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        try {
            JSONArray jsonArray = new JSONArray(data.message);
            for (int i=0; i < jsonArray.length(); i++)
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // Pulling items from the array
                String item1 = jsonObject.getString("type");
                String item2 = jsonObject.getString("name");
                String item3 = jsonObject.getString("id");

                if(item1.equals("camera")) continue;

                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.deviceitem, null);

                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView_name);
                textViewLabel1.setText(item2);

                TextView textViewLabel2 = (TextView)layoutExample.findViewById(R.id.textView_id);
                textViewLabel2.setText(item3);

                container2.addView(layoutExample);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}