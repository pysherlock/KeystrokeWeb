package com.amadeus.cls.jaxrs.services.envLogin;

/**
 * Created by ypu on 23/11/2016.
 */
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Database {

    private String URL;
    private String Username;
    private String Password;
    private Connection connection;

    public Database(String URL, String user, String pwd) throws ClassNotFoundException, SQLException,
            InstantiationException, IllegalAccessException {
        this.Username = user;
        this.Password = pwd;
        this.URL = URL;
        Class.forName("com.mysql.jdbc.Driver");
        this.connection = DriverManager.getConnection(this.URL, this.Username, this.Password);
    }

    public Connection getConnection() {
        return this.connection;
    }

    public String getUsername() {
        return Username;
    }

    public String getPassword() {
        return Password;
    }

    public String getURL() {
        return URL;
    }
}
