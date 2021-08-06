package com.example.testevent;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    LinearLayout container;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        container = findViewById(R.id.container);

        String str[] ={"a","b","c"};
        for(int i=0;i<3;i++){
            LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            /* LayoutInflater inflater = LayoutInflater.from(MenuActivity.this);  LayoutInflate의 form 메서드를 호출 해도 가능 */

            //inflater.inflate(R.layout.sensoritem, container, true);
            LinearLayout layoutExample = (LinearLayout)inflater.inflate(R.layout.sensoritem, null);

            Button button = (Button)layoutExample.findViewById(R.id.button3);
            int finalI = i;
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    TextView textViewLabel = (TextView)layoutExample.findViewById(R.id.textView);
                    //String str = Integer.toString(finalI);

                    textViewLabel.setText(str[finalI]);
                }
            });

            container.addView(layoutExample);
        }
    }
}