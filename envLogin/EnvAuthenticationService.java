package com.amadeus.cls.jaxrs.services.envLogin;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Objects;
import org.json.JSONObject;

/**
 * Created by ypu on 22/11/2016.
 */
public class EnvAuthenticationService {

    private Database DB;

    public EnvAuthenticationService(){}

    public EnvAuthenticationService(Database db) {
        this.DB = db;
    }

    public boolean envAuthenticate(EnvUser envUser) {

        try {
            Connection connection = DB.getConnection();
//            PreparedStatement ps = connection.prepareStatement("SELECT * FROM users WHERE username LIKE ? AND password LIKE ?");
            PreparedStatement ps = connection.prepareStatement("SELECT * FROM users WHERE username LIKE ?");
            ps.setString(1, envUser.username);
            ResultSet rs = ps.executeQuery();

            while(rs.next()) {

                // For Test, only check the password
                // TODO: build a client here, communicate with verification server with json
                // TODO: send factors data and keystroke profile to Python server,
                // TODO: receive the verification result

                if(rs.getString("password").equals(envUser.password)) {
                    // TODO: the envPassword to Python server through socket, json
                    JSONObject envuser = new JSONObject();
                    envuser.put("username", envUser.username);
                    envuser.put("password", envUser.password);

                    EnvAuthenticationClient.SendEnvUser(envuser);
                    return true;
                }

                double threshold= rs.getInt("score") * 0.85;
                int user_score=0;

                if (rs.getString("processor")!=null && Objects.equals(rs.getString("processor"), envUser.processor)
                        && Objects.equals(rs.getString("memory"), envUser.memory) && Objects.equals(rs.getString("os"), envUser.os)
                        && Objects.equals(rs.getString("chrome"), envUser.chrome) && Objects.equals(rs.getString("storage"), envUser.storage)) {
                    user_score+=3;}

                if (rs.getString("pubIP")!=null && Objects.equals(rs.getString("pubIP"), envUser.pubIP)
                        && Objects.equals(rs.getString("locIP"), envUser.locIP)) {
                    user_score+=3;}

                if (rs.getString("country")!=null && Objects.equals(rs.getString("country"), envUser.country)
                        && Objects.equals(rs.getString("region"), envUser.region) && Objects.equals(rs.getString("zip"), envUser.zip)) {
                    user_score+=3;}

                if (rs.getString("charge")!=null && Objects.equals(rs.getBoolean("charge"), envUser.charge)){
                    user_score+=1;
                }
                if (rs.getString("tabIndex")!=null && Objects.equals(rs.getInt("tabIndex"), envUser.tabIndex)){
                    user_score+=2;
                }
                if (rs.getString("removable")!=null && Objects.equals(rs.getBoolean("removable"), envUser.removable)){
                    user_score+=1;
                }
                if (rs.getString("transition")!=null && Objects.equals(rs.getString("transition"), envUser.transition)){
                    user_score+=2;
                }
                if (rs.getString("priv")!=null && Objects.equals(rs.getBoolean("priv"), envUser.priv)){
                    user_score+=1;
                }
                if (rs.getString("width")!=null && ( envUser.width > (rs.getFloat("width")-25)) && ( envUser.width < (rs.getFloat("width")+25))){
                    user_score+=2;
                }
                if (rs.getString("height")!=null && ( envUser.height > (rs.getFloat("height")-20)) && ( envUser.height < (rs.getFloat("height")+20))){
                    user_score+=2;
                }
                if (rs.getString("url")!=null && Objects.equals(rs.getString("url"), envUser.url)){
                    user_score+=4;
                }
                if (rs.getString("press")!=null && ( envUser.press > (rs.getFloat("press")-300)) && ( envUser.press < (rs.getFloat("press")+300))){
                    user_score+=1;
                }
                if (rs.getString("zoom")!=null && Objects.equals(rs.getFloat("zoom"), envUser.zoom)){
                    user_score+=2;
                }
                if (rs.getString("click")!=null && Objects.equals(rs.getString("click"), envUser.click)){
                    user_score+=2;
                }
                if (rs.getString("selected")!=null && Objects.equals(rs.getString("selected"), envUser.selected)){
                    user_score+=2;
                }
                if (rs.getString("lastCharacter")!=null && Objects.equals(rs.getString("lastCharacter"), envUser.lastCharacter)){
                    user_score+=2;
                }
                if (rs.getString("detach")!=null && Objects.equals(rs.getBoolean("detach"), envUser.detach)){
                    user_score+=1;
                }
                if (rs.getString("closetab")!=null && Objects.equals(rs.getBoolean("closetab"), envUser.closetab)){
                    user_score+=1;
                }
                if (rs.getString("bookmarkChange")!=null && Objects.equals(rs.getBoolean("bookmarkChange"), envUser.bookmarkChange)){
                    user_score+=1;
                }
                if (rs.getString("volumeChange")!=null && Objects.equals(rs.getBoolean("volumeChange"), envUser.volumeChange)){
                    user_score+=1;
                }
                if (rs.getString("volume")!=null && (envUser.volume > (rs.getFloat("volume")-0.1)) && (envUser.volume < (rs.getFloat("volume")+0.1))){
                    user_score+=2;
                }
                if (rs.getString("muted")!=null && Objects.equals(rs.getBoolean("muted"), envUser.muted)){
                    user_score+=1;
                }
                if (rs.getString("paused")!=null && Objects.equals(rs.getBoolean("paused"), envUser.paused)){
                    user_score+=1;
                }
                if (rs.getString("speedChange")!=null && Objects.equals(rs.getBoolean("speedChange"), envUser.speedChange)){
                    user_score+=1;
                }
                if (rs.getString("currentTime")!=null && (envUser.currentTime > (rs.getFloat("currentTime")-1))
                        && (envUser.currentTime < (rs.getFloat("currentTime")+1))){
                    user_score+=3;
                }
                if (rs.getString("ended")!=null && Objects.equals(rs.getBoolean("ended"), envUser.ended)){
                    user_score+=1;
                }
                if (rs.getString("seek")!=null && Objects.equals(rs.getBoolean("seek"), envUser.seek)){
                    user_score+=1;
                }

                double Thr=Math.ceil(threshold);
                System.out.println("user_score: "+ user_score + "/" + rs.getInt("score") + "\nthreshold: " + Thr + "\n");
                if (user_score>threshold) {
                    return true;
                }
            }} catch (Exception e) {
            // TODO Auto-generated catch block
                e.printStackTrace();
        }
        return false;
    }


}
