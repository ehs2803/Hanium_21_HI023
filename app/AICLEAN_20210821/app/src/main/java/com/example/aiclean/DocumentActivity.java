package com.example.aiclean;

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

public class DocumentActivity extends AppCompatActivity {
    LinearLayout container;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_document);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data");

        container = findViewById(R.id.container);

        try {
            JSONArray jsonArray = new JSONArray(data.message);
            for (int i=0; i < jsonArray.length(); i++)
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // Pulling items from the array
                String item1 = jsonObject.getString("id");
                String item2 = jsonObject.getString("time");
                String item3 = jsonObject.getString("way");
                String item4 = jsonObject.getString("strength");

                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.documentitem, null);

                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView_name);
                textViewLabel1.setText(item1);

                TextView textViewLabel2 = (TextView)layoutExample.findViewById(R.id.textView_time);
                textViewLabel2.setText(item2);

                TextView textViewLabel3 = (TextView)layoutExample.findViewById(R.id.textView_way);
                textViewLabel3.setText(item3);

                TextView textViewLabel4 = (TextView)layoutExample.findViewById(R.id.textView_strength);
                textViewLabel4.setText(item4);

                container.addView(layoutExample);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }
}