package com.amadeus.cls.jaxrs.services.envLogin;

/**
 * Created by ypu on 23/11/2016.
 */

public class Test {

    public static void main(String[] args) {
        EnvUser envUser = new EnvUser("ypu", "gonzo_1982");
        try {
            Database db = new Database("jdbc:mysql://localhost:3306/mydb1", "root", "ypu123123");
            EnvAuthenticationService EnvAuth = new EnvAuthenticationService(db);
            boolean result = EnvAuth.envAuthenticate(envUser);
            if (result == true) {
                System.out.println("Login successfully");
            } else {
                System.out.println("Authentication failed");
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
}
