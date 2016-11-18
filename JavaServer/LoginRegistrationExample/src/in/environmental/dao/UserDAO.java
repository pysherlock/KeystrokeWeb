package in.environmental.dao;

import in.environmental.model.User;

public interface UserDAO {
	
	public User getUserByUsername(String username, String password, String processor, String memory, String os, 
			String chrome, String storage, String locIP, String pubIP, String country, String region, String zip,
			Boolean charge, int tabIndex, Boolean removable, String transition, Boolean priv, Float width, Float height, 
			String url, Float press, Float zoom, String click, String selected, String lastCharacter, Boolean detach, 
			Boolean closetab, Boolean bookmarkChange, Boolean volumeChange, Float volume, Boolean muted, Boolean paused, 
			Boolean speedChange, Float currentTime, Boolean ended, Boolean seek);
	
	public int createOrUpdateUser(User u);
}
