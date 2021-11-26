package com.example.aiclean;

import android.os.Parcel;
import android.os.Parcelable;

public class testData implements Parcelable {

    //int number;
    String message;

    public testData(){ }

    public testData(String msg) {
        //number = num;
        message = msg;
    }

    public testData(Parcel src) {
        //number = src.readInt();
        message = src.readString();
    }

    //public void setnumber(int n){ number=n;}
    public void setstring(String s){message=s;}
    public static final Creator CREATOR = new Creator() {

        public testData createFromParcel(Parcel in) {
            return new testData(in);
        }

        public testData[] newArray(int size) {
            return new testData[size];
        }

    };

    public int describeContents() {
        return 0;
    }

    public void writeToParcel(Parcel dest, int flags) {
        //dest.writeInt(number);
        dest.writeString(message);
    }

}
