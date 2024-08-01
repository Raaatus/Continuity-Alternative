package com.example.test;

import android.os.AsyncTask;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.provider.Settings;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {

    private EditText editTextIpAddress;
    private EditText editTextPort;
    private Button buttonSave;
    private Button buttonTestConnection;

    private SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editTextIpAddress = findViewById(R.id.editTextIpAddress);
        editTextPort = findViewById(R.id.editTextPort);
        buttonSave = findViewById(R.id.buttonSave);
        buttonTestConnection = findViewById(R.id.buttonTestConnection);

        sharedPreferences = getSharedPreferences("ServerSettings", Context.MODE_PRIVATE);

        // Load saved IP address and port
        String savedIpAddress = sharedPreferences.getString("ipAddress", "");
        int savedPort = sharedPreferences.getInt("port", 5000);

        editTextIpAddress.setText(savedIpAddress);
        editTextPort.setText(String.valueOf(savedPort));

        buttonSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String ipAddress = editTextIpAddress.getText().toString();
                int port = Integer.parseInt(editTextPort.getText().toString());

                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putString("ipAddress", ipAddress);
                editor.putInt("port", port);
                editor.apply();

                // Optionally, show a message to the user that settings have been saved
            }
        });

        buttonTestConnection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String ipAddress = editTextIpAddress.getText().toString();
                int port = Integer.parseInt(editTextPort.getText().toString());
                String serverUrl = "http://" + ipAddress + ":" + port;

                new TestServerConnectionTask().execute(serverUrl);
            }
        });

        if (!isNotificationServiceEnabled()) {
            Intent intent = new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS);
            startActivity(intent);
        }
    }

    private boolean isNotificationServiceEnabled() {
        String pkgName = getPackageName();
        final String flat = Settings.Secure.getString(getContentResolver(),
                "enabled_notification_listeners");
        return !TextUtils.isEmpty(flat) && flat.contains(pkgName);
    }

    public static String getServerUrl(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("ServerSettings", Context.MODE_PRIVATE);
        String ipAddress = sharedPreferences.getString("ipAddress", "192.168.1.22");
        int port = sharedPreferences.getInt("port", 5000);
        return "http://" + ipAddress + ":" + port + "/notification";
    }

    private class TestServerConnectionTask extends AsyncTask<String, Void, Boolean> {
        @Override
        protected Boolean doInBackground(String... params) {
            String serverUrl = params[0];
            try {
                URL url = new URL(serverUrl);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("GET");
                connection.setConnectTimeout(5000); // 5 seconds timeout
                connection.connect();

                int responseCode = connection.getResponseCode();
                return responseCode == HttpURLConnection.HTTP_OK;
            } catch (Exception e) {
                e.printStackTrace();
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean isOnline) {
            if (isOnline) {
                Toast.makeText(MainActivity.this, "Server is online!", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(MainActivity.this, "Server is offline!", Toast.LENGTH_SHORT).show();
            }
        }
    }
}
