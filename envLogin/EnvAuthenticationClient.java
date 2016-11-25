package com.amadeus.cls.jaxrs.services.envLogin;

import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * Created by ypu on 25/11/2016.
 */
public class EnvAuthenticationClient {

    public static final String IP_SERVER = "127.0.0.1";
    public static final int PORT_SERVER = 7777;

    public static void SendEnvUser(JSONObject envpassword){
        try {
            Socket cli = new Socket(IP_SERVER, PORT_SERVER);
            OutputStreamWriter out = new OutputStreamWriter(cli.getOutputStream(), StandardCharsets.UTF_8);
            out.write(envpassword.toString());

        } catch(IOException e) {
            e.printStackTrace();
        }

    }

}
