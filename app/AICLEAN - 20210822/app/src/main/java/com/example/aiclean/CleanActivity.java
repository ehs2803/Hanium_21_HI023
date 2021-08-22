package com.example.aiclean;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class CleanActivity extends AppCompatActivity {
    private static final String TAG="";
    LinearLayout container;
    int index=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ActionBar actionBar = getSupportActionBar();
        actionBar.hide();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_clean);

        container = findViewById(R.id.container);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data");

        try {
            JSONArray jsonArray = new JSONArray(data.message);
            for (int i=0; i < jsonArray.length(); i++)
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // Pulling items from the array
                String item1 = jsonObject.getString("id");
                String item2 = jsonObject.getString("name");

                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.cleanitem, null);

                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textViewname);
                textViewLabel1.setText(item2);

                Button button = (Button)layoutExample.findViewById(R.id.button);
                button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        button.setBackgroundColor(Color.GRAY);
                        //String extra = getid[index];
                        String urlStr = "http://192.168.123.3:5000/clean?id="+item1;
                        //button.setText(urlStr);
                        button.setText("이미 살균");
                        button.setEnabled(false);
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                request(urlStr);
                            }
                        }).start();

                    }
                });

                container.addView(layoutExample);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public void request(String urlStr) {
        String str="";
        StringBuilder output = new StringBuilder();
        try {
            URL url = new URL(urlStr);

            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            if (conn != null) {
                conn.setConnectTimeout(10000);
                conn.setRequestMethod("GET");
                conn.setDoInput(true);

                int resCode = conn.getResponseCode();
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                String line = null;
                while (true) {
                    line = reader.readLine();
                    if (line == null) {
                        break;
                    }
                    str=line;
                    //output.append(line + "\n");

                }
                reader.close();
                conn.disconnect();
            }
        } catch (Exception ex) {
            //println("예외 발생함 : " + ex.toString());
        }
        //println("응답 -> " + output.toString());
    }
}