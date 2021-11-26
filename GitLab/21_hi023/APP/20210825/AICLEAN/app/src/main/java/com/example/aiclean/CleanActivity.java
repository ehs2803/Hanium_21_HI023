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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ActionBar actionBar = getSupportActionBar();
        actionBar.hide();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_clean);
        container = findViewById(R.id.container);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        testData data = bundle.getParcelable("data"); // 이전 화면에서 데이터 얻기

        try {
            JSONArray jsonArray = new JSONArray(data.message); // json 배열로 바꾸기
            for (int i=0; i < jsonArray.length(); i++) // json 객체 수 만큼 반복
            {
                JSONObject jsonObject = jsonArray.getJSONObject(i); // i번째 객체 얻기

                String item1 = jsonObject.getString("id"); // 살균기 id 얻기
                String item2 = jsonObject.getString("name"); // 장소 이름 얻기

                // cleanitem layout 만들기
                LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.cleanitem, null);
                // layout 내 textview 글자 설정 - 살균 장소 이름으로 초기화
                TextView textViewLabel1 = (TextView)layoutExample.findViewById(R.id.textViewname);
                textViewLabel1.setText(item2);

                // 버튼에 http통신 이벤트 추가
                Button button = (Button)layoutExample.findViewById(R.id.button);
                button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) { // 버튼을 누른경우
                        button.setBackgroundColor(Color.GRAY); // 버튼색 회색으로 바꾸기
                        String urlStr = "http://192.168.0.23:5000/clean?id="+item1;
                        button.setText("살균 완료"); // 버튼에 "살균 완료" 글자 표시
                        button.setEnabled(false);   // 버튼 비활성화
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                request(urlStr);
                            } // http통신으로 살균명령
                        }).start();

                    }
                });

                container.addView(layoutExample); // layout 추가

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