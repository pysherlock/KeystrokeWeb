package in.environmental.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Objects;

import in.environmental.model.User;

public class UserDAOImpl implements UserDAO{
	
	Database db = new Database();
	
	@Override
	public User getUserByUsername(String username, String password, String processor, String memory, String os, String chrome, 
			String storage, String locIP, String pubIP, String country, String region, String zip, Boolean charge, int tabIndex, 
			Boolean removable, String transition, Boolean priv, Float width, Float height, String url, Float press, Float zoom, String click, 
			String selected, String lastCharacter, Boolean detach, Boolean closetab, Boolean bookmarkChange, Boolean volumeChange, 
			Float volume, Boolean muted, Boolean paused, Boolean speedChange, Float currentTime, Boolean ended, Boolean seek) {
		
		User user = new User();
		
		try {
			Connection connection = db.getConnection();
			PreparedStatement ps = connection.prepareStatement("SELECT * FROM users WHERE username LIKE ? AND password LIKE ?");
			ps.setString(1, username);
			ps.setString(2, password);
			ResultSet rs = ps.executeQuery();
			while(rs.next()) {
				double threshold= rs.getInt("score") * 0.85;
				int user_score=0;
				
				if (rs.getString("processor")!=null && Objects.equals(rs.getString("processor"), processor) 
						&& Objects.equals(rs.getString("memory"), memory) && Objects.equals(rs.getString("os"), os) 
						&& Objects.equals(rs.getString("chrome"), chrome) && Objects.equals(rs.getString("storage"), storage)) {
					user_score+=3;}
				
				if (rs.getString("pubIP")!=null && Objects.equals(rs.getString("pubIP"), pubIP) 
						&& Objects.equals(rs.getString("locIP"), locIP)) {
					user_score+=3;}
				
				if (rs.getString("country")!=null && Objects.equals(rs.getString("country"), country) 
						&& Objects.equals(rs.getString("region"), region) && Objects.equals(rs.getString("zip"), zip)) {
					user_score+=3;}
				
				if (rs.getString("charge")!=null && Objects.equals(rs.getBoolean("charge"), charge)){
					user_score+=1;
				}
				if (rs.getString("tabIndex")!=null && Objects.equals(rs.getInt("tabIndex"), tabIndex)){
					user_score+=2;
				}
				if (rs.getString("removable")!=null && Objects.equals(rs.getBoolean("removable"), removable)){
					user_score+=1;
				}
				if (rs.getString("transition")!=null && Objects.equals(rs.getString("transition"), transition)){
					user_score+=2;
				}
				if (rs.getString("priv")!=null && Objects.equals(rs.getBoolean("priv"), priv)){
					user_score+=1;
				}
				if (rs.getString("width")!=null && ( width > (rs.getFloat("width")-25)) && ( width < (rs.getFloat("width")+25))){
					user_score+=2;			
				}
				if (rs.getString("height")!=null && ( height > (rs.getFloat("height")-20)) && ( height < (rs.getFloat("height")+20))){
					user_score+=2;
				}
				if (rs.getString("url")!=null && Objects.equals(rs.getString("url"), url)){
					user_score+=4;
				}
				if (rs.getString("press")!=null && ( press > (rs.getFloat("press")-300)) && ( press < (rs.getFloat("press")+300))){
					user_score+=1;
				}
				if (rs.getString("zoom")!=null && Objects.equals(rs.getFloat("zoom"), zoom)){
					user_score+=2;
				}
				if (rs.getString("click")!=null && Objects.equals(rs.getString("click"), click)){
					user_score+=2;
				}
				if (rs.getString("selected")!=null && Objects.equals(rs.getString("selected"), selected)){
					user_score+=2;
				}
				if (rs.getString("lastCharacter")!=null && Objects.equals(rs.getString("lastCharacter"), lastCharacter)){
					user_score+=2;
				}
				if (rs.getString("detach")!=null && Objects.equals(rs.getBoolean("detach"), detach)){
					user_score+=1;
				}
				if (rs.getString("closetab")!=null && Objects.equals(rs.getBoolean("closetab"), closetab)){
					user_score+=1;
				}
				if (rs.getString("bookmarkChange")!=null && Objects.equals(rs.getBoolean("bookmarkChange"), bookmarkChange)){
					user_score+=1;
				}
				if (rs.getString("volumeChange")!=null && Objects.equals(rs.getBoolean("volumeChange"), volumeChange)){
					user_score+=1;
				}
				if (rs.getString("volume")!=null && (volume > (rs.getFloat("volume")-0.1)) && (volume < (rs.getFloat("volume")+0.1))){
					user_score+=2;
				}
				if (rs.getString("muted")!=null && Objects.equals(rs.getBoolean("muted"), muted)){
					user_score+=1;
				}
				if (rs.getString("paused")!=null && Objects.equals(rs.getBoolean("paused"), paused)){
					user_score+=1;
				}
				if (rs.getString("speedChange")!=null && Objects.equals(rs.getBoolean("speedChange"), speedChange)){
					user_score+=1;
				}
				if (rs.getString("currentTime")!=null && (currentTime > (rs.getFloat("currentTime")-1)) 
						&& (currentTime < (rs.getFloat("currentTime")+1))){
					user_score+=3;
				}
				if (rs.getString("ended")!=null && Objects.equals(rs.getBoolean("ended"), ended)){
					user_score+=1;
				}
				if (rs.getString("seek")!=null && Objects.equals(rs.getBoolean("seek"), seek)){
					user_score+=1;
				}
				
				//TODO send factors data and keystroke profile to Python server, 
				//TODO receive the verification result
				
				double Thr=Math.ceil(threshold);
				System.out.println("user_score: "+ user_score + "/" + rs.getInt("score") + "\nthreshold: " + Thr + "\n");
		    	if (user_score>threshold) {
		    		user.setId(rs.getInt("id"));
		    		user.setUsername(rs.getString("username"));
			    }
	   }} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return user;
	}

	@Override
	public int createOrUpdateUser(User u) {
		int result = 0;
		try {
			Connection connection = db.getConnection();
			PreparedStatement ps = connection.prepareStatement("SELECT * FROM users WHERE username LIKE ? ");
			ps.setString(1, u.getUsername());
			ResultSet rs = ps.executeQuery();
			if (rs.next()) { System.out.println("Use");result=-1; return result;}
			else {
				ps = connection.prepareStatement("INSERT INTO users (username, password, processor, memory, os, chrome, storage, locIP, "
		    		+ "pubIP,country,region,zip,charge,tabIndex,removable,transition,priv,width,height,url,press,zoom,click,selected,"
		    		+ "lastCharacter,detach,closetab,bookmarkChange,volumeChange,volume,muted,paused,speedChange,currentTime,ended,seek,score) "
		    		+ "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
		    
			ps.setString(1, u.getUsername());
			ps.setString(2, u.getPassword());
			if (u.getHardware_factor()==null) {
				ps.setString(3, null);
				ps.setString(4, null);
				ps.setString(5, null);
				ps.setString(6, null);
				ps.setString(7, null);
			}
			else{
			ps.setString(3, u.getProcessor());
			ps.setString(4, u.getMemory());
			ps.setString(5, u.getOs());
			ps.setString(6, u.getChrome());
			ps.setString(7, u.getStorage());}
			if (u.getIP_factor()==null) {
				ps.setString(8, null);
				ps.setString(9, null);}
			else{
			ps.setString(8, u.getLocIP());
			ps.setString(9, u.getPubIP());}
			if (u.getLocation_factor()==null) {
				ps.setString(10, null);
				ps.setString(11, null);
				ps.setString(12, null);}
			else{
			ps.setString(10, u.getCountry());
			ps.setString(11, u.getRegion());
			ps.setString(12, u.getZip());}
			if (u.getCharge_factor()==null) {
				ps.setString(13, null);
			}
			else{
			ps.setBoolean(13, u.getCharge());}
			if (u.getTabIndex_factor()==null) {
				ps.setString(14, null);
			}
			else{
			ps.setInt(14, u.getTabIndex());}
			if (u.getRemovable_factor()==null) {
				ps.setString(15, null);
			}
			else{
			ps.setBoolean(15, u.getRemovable());}
			if (u.getTransition_factor()==null) {
				ps.setString(16, null);
			}
			else{
			ps.setString(16, u.getTransition());}
			if (u.getPriv_factor()==null) {
				ps.setString(17, null);
			}
			else{
			ps.setBoolean(17, u.getPriv());}
			if (u.getWidth_factor()==null) {
				ps.setString(18, null);
			}
			else{
			ps.setFloat(18, u.getWidth());}
			if (u.getHeight_factor()==null) {
				ps.setString(19, null);
			}
			else{
			ps.setFloat(19, u.getHeight());}
			if (u.getUrl_factor()==null) {
				ps.setString(20, null);
			}
			else{
			ps.setString(20, u.getUrl());}
			if (u.getPress_factor()==null) {
				ps.setString(21, null);
			}
			else{
			ps.setFloat(21, u.getPress());}
			if (u.getZoom_factor()==null) {
				ps.setString(22, null);
			}
			else{
			ps.setFloat(22, u.getZoom());}
			if (u.getClick_factor()==null) {
				ps.setString(23, null);
			}
			else{
			ps.setString(23, u.getClick());}
			if (u.getSelected_factor()==null) {
				ps.setString(24, null);
			}
			else{
			ps.setString(24, u.getSelected());}
			if (u.getLastCharacter_factor()==null) {
				ps.setString(25, null);
			}
			else{
			ps.setString(25, u.getLastCharacter());}
			if (u.getDetach_factor()==null) {
				ps.setString(26, null);
			}
			else{
			ps.setBoolean(26, u.getDetach());}
			if (u.getClosetab_factor()==null) {
				ps.setString(27, null);
			}
			else{
			ps.setBoolean(27, u.getClosetab());}
			if (u.getBookmarkChange_factor()==null) {
				ps.setString(28, null);
			}
			else{
			ps.setBoolean(28, u.getBookmarkChange());}
			if (u.getVolumeChange_factor()==null) {
				ps.setString(29, null);
			}
			else{
			ps.setBoolean(29, u.getVolumeChange());}
			if (u.getVolume_factor()==null) {
				ps.setString(30, null);
			}
			else{
			ps.setFloat(30, u.getVolume());}
			if (u.getMuted_factor()==null) {
				ps.setString(31, null);
			}
			else{
			ps.setBoolean(31, u.getMuted());}
			if (u.getPaused_factor()==null) {
				ps.setString(32, null);
			}
			else{
			ps.setBoolean(32, u.getPaused());}
			if (u.getSpeedChange_factor()==null) {
				ps.setString(33, null);
			}
			else{
			ps.setBoolean(33, u.getSpeedChange());}
			if (u.getCurrentTime_factor()==null) {
				ps.setString(34, null);
			}
			else{
			ps.setFloat(34, u.getCurrentTime());}
			if (u.getEnded_factor()==null) {
				ps.setString(35, null);
			}
			else {
				ps.setBoolean(35, u.getEnded());
			}
			if (u.getSeek_factor()==null) {
				ps.setString(36, null);
			}
			else {
				ps.setBoolean(36, u.getSeek());}
				ps.setInt(37, u.getScore());
				System.out.println("user_score: "+ u.getScore());
				result = ps.executeUpdate();
			}	

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result; 
		
	}

}