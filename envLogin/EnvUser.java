package com.amadeus.cls.jaxrs.services.envLogin;

/**
 * Created by ypu on 23/11/2016.
 */
public class EnvUser {
    protected String username, password, processor, memory, os, chrome, storage, locIP, pubIP,
            country, region, zip, transition, url, click, selected, lastCharacter;
    protected String keystroke;
    protected Boolean charge, removable, priv, detach, closetab, bookmarkChange,
            volumeChange, muted, paused, speedChange, ended, seek;
    protected int tabIndex;
    protected Float width, height, press, zoom, volume, currentTime;
    protected Boolean hardware_factor, IP_factor, location_factor, charge_factor, tabIndex_factor, removable_factor,
            priv_factor, width_factor, height_factor, url_factor, press_factor, zoom_factor, click_factor,
            selected_factor, lastCharacter_factor, detach_factor, closetab_factor, bookmarkChange_factor,
            volumeChange_factor, volume_factor, muted_factor, paused_factor, speedChange_factor, currentTime_factor,
            ended_factor, seek_factor, keystroke_factor;

    public EnvUser() {}

    public EnvUser(String user, String pwd) {
        this.username = user;
        this.password = pwd;
    }

}
