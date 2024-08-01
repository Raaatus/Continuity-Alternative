package com.example.test;

import android.os.AsyncTask;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class NotificationListener extends NotificationListenerService {

    private static final String TAG = "NotificationListener";

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        Log.i(TAG, "Notification Posted: " + sbn.getPackageName());

        sendNotificationToServer(sbn);
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        Log.i(TAG, "Notification Removed: " + sbn.getPackageName());
    }

    private void sendNotificationToServer(StatusBarNotification sbn) {
        try {
            JSONObject json = new JSONObject();
            json.put("packageName", sbn.getPackageName());
            json.put("tickerText", sbn.getNotification().tickerText);
            json.put("Titre",sbn.getNotification().extras.getCharSequence(sbn.getNotification().EXTRA_TITLE));
            json.put("timestamp", System.currentTimeMillis());

            String serverUrl = MainActivity.getServerUrl(this);

            new SendNotificationTask().execute(serverUrl, json.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static class SendNotificationTask extends AsyncTask<String, Void, Void> {
        @Override
        protected Void doInBackground(String... params) {
            String serverUrl = params[0];
            String jsonData = params[1];
            try {
                URL url = new URL(serverUrl);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/json; utf-8");
                connection.setDoOutput(true);

                try (OutputStream os = connection.getOutputStream()) {
                    byte[] input = jsonData.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = connection.getResponseCode();
                Log.i(TAG, "Response Code: " + responseCode);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
