package com.example.aiclean;

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
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_clean);

        container = findViewById(R.id.container);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data");

        String str = data.message; //"3/aa:bb:cc:/STE-0-0000:STE-1-1111:STE-2-2222:";
        String strs[] = str.split("/");

        String getname[] = strs[1].split(":");
        String getid[] = strs[2].split(":");
        int num = Integer.parseInt(strs[0]);

        for(int i=0;i<num;i++){
            LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.cleanitem, null);

            TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textView);
            textViewLabel1.setText(getname[index]);
            String extra = getid[index];
            index++;

            Button button = (Button)layoutExample.findViewById(R.id.button3);
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    button.setBackgroundColor(Color.GRAY);
                    //String extra = getid[index];
                    String urlStr = "http://192.168.123.4:5000/clean?id="+extra;
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