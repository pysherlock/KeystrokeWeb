package in.environmental.model;

public class User {
	
	private int id;
	private String username;
	private String password;
	private String processor;
	private String memory;
	private String os;
	private String chrome;
	private String storage;
	private String locIP;
	private String pubIP;
	private String country;
	private String region;
	private String zip;
	private Boolean charge;
	private int tabIndex;
	private Boolean removable;
	private String transition;
	private Boolean priv;
	private Float width;
	private Float height;
	private String url;
	private Float press;
	private Float zoom;
	private String click;
	private String selected;
	private String lastCharacter;
	private Boolean detach;
	private Boolean closetab;
	private Boolean bookmarkChange;
	private Boolean volumeChange;
	private Float volume;
	private Boolean muted;
	private Boolean paused;
	private Boolean speedChange;
	private Float currentTime;
	private Boolean ended;
	private Boolean seek;
	private String hardware_factor;
	private String IP_factor;
	private String location_factor;
	private String charge_factor;
	private String tabIndex_factor;
	private String removable_factor;
	private String transition_factor;
	private String priv_factor;
	private String width_factor;
	private String height_factor;
	private String url_factor;
	private String press_factor;
	private String zoom_factor;
	private String click_factor;
	private String selected_factor;
	private String lastCharacter_factor;
	private String detach_factor;
	private String closetab_factor;
	private String bookmarkChange_factor;
	private String volumeChange_factor;
	private String volume_factor;
	private String muted_factor;
	private String paused_factor;
	private String speedChange_factor;
	private String currentTime_factor;
	private String ended_factor;
	private String seek_factor;
	private int score;
	public User(){
		
	}
	
	public User(String username, String password, String processor, String memory, String os, String chrome, String storage, 
			String locIP, String pubIP, String country, String region, String zip, Boolean charge, int tabIndex, Boolean removable, 
			String transition, Boolean priv, Float width, Float height, String url, Float press, Float zoom, String click, String selected,
		    String lastCharacter, Boolean detach, Boolean closetab, Boolean bookmarkChange, Boolean volumeChange, Float volume, 
		    Boolean muted, Boolean paused, Boolean speedChange, Float currentTime, Boolean ended, Boolean seek, String hardware_factor, 
		    String IP_factor, String location_factor, String charge_factor, String tabIndex_factor, String removable_factor, 
		    String transition_factor, String priv_factor, String width_factor, String height_factor, String url_factor, String press_factor, 
		    String zoom_factor, String click_factor, String selected_factor, String lastCharacter_factor, String detach_factor, 
		    String closetab_factor, String bookmarkChange_factor, String volumeChange_factor , String volume_factor, String muted_factor, 
		    String paused_factor, String speedChange_factor, String currentTime_factor, String ended_factor, String seek_factor, int score) {
		
		this.username = username;
		this.password = password;
		this.processor = processor;
		this.memory = memory;
		this.os = os;
		this.chrome = chrome;
		this.storage = storage;
		this.locIP = locIP;
		this.pubIP = pubIP;
		this.country = country;
		this.region = region;
		this.zip = zip;
		this.charge = charge;
		this.tabIndex = tabIndex;
		this.removable = removable;
		this.transition = transition;
		this.priv = priv;
		this.width = width;
		this.height = height;
		this.url = url;
		this.press = press;
		this.zoom = zoom;
		this.click = click;
		this.selected = selected;
		this.lastCharacter = lastCharacter;
		this.detach = detach;
		this.closetab = closetab;
		this.bookmarkChange = bookmarkChange;
		this.volumeChange = volumeChange;
		this.volume = volume;
		this.muted = muted;
		this.paused = paused;
		this.speedChange = speedChange;
		this.currentTime = currentTime;
		this.ended = ended;
		this.seek = seek;
		this.hardware_factor = hardware_factor;
		this.IP_factor = IP_factor;
		this.location_factor = location_factor;
		this.charge_factor = charge_factor;
		this.tabIndex_factor = tabIndex_factor;
		this.removable_factor = removable_factor;
		this.transition_factor = transition_factor;
		this.priv_factor = priv_factor;
		this.width_factor = width_factor;
		this.height_factor = height_factor;
		this.url_factor = url_factor;
		this.press_factor = press_factor;
		this.zoom_factor = zoom_factor;
		this.click_factor = click_factor;
		this.selected_factor = selected_factor;
		this.lastCharacter_factor = lastCharacter_factor;
		this.detach_factor = detach_factor;
		this.closetab_factor = closetab_factor;
		this.bookmarkChange_factor = bookmarkChange_factor;
		this.volumeChange_factor = volumeChange_factor;
		this.volume_factor = volume_factor;
		this.muted_factor = muted_factor;
		this.paused_factor = paused_factor;
		this.speedChange_factor = speedChange_factor;
		this.currentTime_factor = currentTime_factor;
		this.ended_factor = ended_factor;
		this.seek_factor = seek_factor;
		this.score = score;
	}
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	
	public String getProcessor() {
		return processor;
	}
	public void setProcessor(String processor) {
		this.processor = processor;
	}
	public String getMemory() {
		return memory;
	}
	public void setMemory(String memory) {
		this.memory = memory;
	}
	public String getOs() {
		return os;
	}
	public void setOs(String os) {
		this.os = os;
	}
	public String getChrome() {
		return chrome;
	}
	public void setChrome(String chrome) {
		this.chrome = chrome;
	}

	public String getStorage() {
		return storage;
	}
	public void setStorage(String storage) {
		this.storage = storage;
	}
	
	public String getLocIP() {
		return locIP;
	}
	public void setLocIP(String locIP) {
		this.locIP = locIP;
	}
	
	public String getPubIP() {
		return pubIP;
	}
	public void setPubIP(String pubIP) {
		this.pubIP = pubIP;
	}
	public String getCountry() {
		return country;
	}
	public void setCountry(String country) {
		this.country = country;
	}
	public String getRegion() {
		return region;
	}
	public void setRegion(String region) {
		this.region = region;
	}
	public String getZip() {
		return zip;
	}
	public void setZip(String zip) {
		this.zip = zip;
	}

	public Boolean getCharge() {
		return charge;
	}
	public void setCharge(Boolean charge) {
		this.charge = charge;
	}
	
	public int getTabIndex() {
		return tabIndex;
	}
	public void setTabIndex(int tabIndex) {
		this.tabIndex = tabIndex;
	}
	
	public Boolean getRemovable() {
		return removable;
	}
	public void setRemovable(Boolean removable) {
		this.removable = removable;
	}
	public String getTransition() {
		return transition;
	}
	public void setTransition(String transition) {
		this.transition = transition;
	}
	public Boolean getPriv() {
		return priv;
	}
	public void setPriv(Boolean priv) {
		this.priv = priv;
	}
	public Float getWidth() {
		return width;
	}
	public void setWidth(Float width) {
		this.width = width;
	}

	public Float getHeight() {
		return height;
	}
	public void setHeight(Float height) {
		this.height = height;
	}
	
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	
	public Float getPress() {
		return press;
	}
	public void setPress(Float press) {
		this.press = press;
	}
	public Float getZoom() {
		return zoom;
	}
	public void setZoom(Float zoom) {
		this.zoom = zoom;
	}
	public String getClick() {
		return click;
	}
	public void setClick(String click) {
		this.click = click;
	}
	public String getSelected() {
		return selected;
	}
	public void setSelected(String selected) {
		this.selected = selected;
	}

	public String getLastCharacter() {
		return lastCharacter;
	}
	public void setLastCharacter(String lastCharacter) {
		this.lastCharacter = lastCharacter;
	}
	
	public Boolean getDetach() {
		return detach;
	}
	public void setDetach(Boolean detach) {
		this.detach = detach;
	}
	
	public Boolean getClosetab() {
		return closetab;
	}
	public void setClosetab(Boolean closetab) {
		this.closetab = closetab;
	}
	public Boolean getBookmarkChange() {
		return bookmarkChange;
	}
	public void setBookmarkChange(Boolean bookmarkChange) {
		this.bookmarkChange = bookmarkChange;
	}
	public Boolean getVolumeChange() {
		return volumeChange;
	}
	public void setVolumeChange(Boolean volumeChange) {
		this.volumeChange = volumeChange;
	}
	public Float getVolume() {
		return volume;
	}
	public void setVolume(Float volume) {
		this.volume = volume;
	}

	public Boolean getMuted() {
		return muted;
	}
	public void setMuted(Boolean muted) {
		this.muted = muted;
	}
	
	public Boolean getPaused() {
		return paused;
	}
	public void setPaused(Boolean paused) {
		this.paused = paused;
	}
	
	public Boolean getSpeedChange() {
		return speedChange;
	}
	public void setSpeedChange(Boolean speedChange) {
		this.speedChange = speedChange;
	}
	public Float getCurrentTime() {
		return currentTime;
	}
	public void setCurrentTime(Float currentTime) {
		this.currentTime = currentTime;
	}
	public Boolean getEnded() {
		return ended;
	}
	public void setEnded(Boolean ended) {
		this.ended = ended;
	}
	public Boolean getSeek() {
		return seek;
	}
	public void setSeek(Boolean seek) {
		this.seek = seek;
	}
	public int getScore() {
		return score;
	}
	public void setScore(int score) {
		this.score = score;
	}
	public String getHardware_factor() {
		return hardware_factor;
	}
	public void setHardware_factor(String hardware_factor) {
		this.hardware_factor = hardware_factor;
	}
	public String getIP_factor() {
		return IP_factor;
	}
	public void setIP_factor(String IP_factor) {
		this.IP_factor = IP_factor;
	}
	public String getLocation_factor() {
		return location_factor;
	}
	public void setLocation_factor(String location_factor) {
		this.location_factor = location_factor;
	}
	public String getTabIndex_factor() {
		return tabIndex_factor;
	}
	public void setTabIndex_factor(String tabIndex_factor) {
		this.tabIndex_factor = tabIndex_factor;
	}
	
	public String getRemovable_factor() {
		return removable_factor;
	}
	public void setRemovable_factor(String removable_factor) {
		this.removable_factor = removable_factor;
	}
	public String getTransition_factor() {
		return transition_factor;
	}
	public void setTransition_factor(String transition_factor) {
		this.transition_factor = transition_factor;
	}
	public String getPriv_factor() {
		return priv_factor;
	}
	public void setPriv_factor(String priv_factor) {
		this.priv_factor = priv_factor;
	}
	public String getWidth_factor() {
		return width_factor;
	}
	public void setWidth_factor(String width_factor) {
		this.width_factor = width_factor;
	}

	public String getHeight_factor() {
		return height_factor;
	}
	public void setHeight_factor(String height_factor) {
		this.height_factor = height_factor;
	}
	
	public String getUrl_factor() {
		return url_factor;
	}
	public void setUrl_factor(String url_factor) {
		this.url_factor = url_factor;
	}
	
	public String getPress_factor() {
		return press_factor;
	}
	public void setPress_factor(String press_factor) {
		this.press_factor = press_factor;
	}
	public String getZoom_factor() {
		return zoom_factor;
	}
	public void setZoom_factor(String zoom_factor) {
		this.zoom_factor = zoom_factor;
	}
	public String getClick_factor() {
		return click_factor;
	}
	public void setClick_factor(String click_factor) {
		this.click_factor = click_factor;
	}
	public String getSelected_factor() {
		return selected_factor;
	}
	public void setSelected_factor(String selected_factor) {
		this.selected_factor = selected_factor;
	}

	public String getLastCharacter_factor() {
		return lastCharacter_factor;
	}
	public void setLastCharacter_factor(String lastCharacter_factor) {
		this.lastCharacter_factor = lastCharacter_factor;
	}
	
	public String getDetach_factor() {
		return detach_factor;
	}
	public void setDetach_factor(String detach_factor) {
		this.detach_factor = detach_factor;
	}
	
	public String getClosetab_factor() {
		return closetab_factor;
	}
	public void setClosetab_factor(String closetab_factor) {
		this.closetab_factor = closetab_factor;
	}
	public String getBookmarkChange_factor() {
		return bookmarkChange_factor;
	}
	public void setBookmarkChange_factor(String bookmarkChange_factor) {
		this.bookmarkChange_factor = bookmarkChange_factor;
	}
	public String getVolumeChange_factor() {
		return volumeChange_factor;
	}
	public void setVolumeChange_factor(String volumeChange_factor) {
		this.volumeChange_factor = volumeChange_factor;
	}
	public String getVolume_factor() {
		return volume_factor;
	}
	public void setVolume_factor(String volume_factor) {
		this.volume_factor = volume_factor;
	}

	public String getMuted_factor() {
		return muted_factor;
	}
	public void setMuted_factor(String muted_factor) {
		this.muted_factor = muted_factor;
	}
	
	public String getPaused_factor() {
		return paused_factor;
	}
	public void setPaused_factor(String paused_factor) {
		this.paused_factor = paused_factor;
	}
	
	public String getSpeedChange_factor() {
		return speedChange_factor;
	}
	public void setSpeedChange_factor(String speedChange_factor) {
		this.speedChange_factor = speedChange_factor;
	}
	public String getCurrentTime_factor() {
		return currentTime_factor;
	}
	public void setCurrentTime_factor(String currentTime_factor) {
		this.currentTime_factor = currentTime_factor;
	}
	public String getEnded_factor() {
		return ended_factor;
	}
	public void setEnded_factor(String ended_factor) {
		this.ended_factor = ended_factor;
	}
	public String getSeek_factor() {
		return seek_factor;
	}
	public void setSeek_factor(String seek_factor) {
		this.seek_factor = seek_factor;
	}
	public String getCharge_factor() {
		return charge_factor;
	}
	public void setCharge_factor(String charge_factor) {
		this.charge_factor = charge_factor;
	}

	@Override
	public String toString() {
		return "User [id=" + id + ", username=" + username +  ", processor=" + processor + ", memory=" + memory 
				+  ", os=" + os + ", chrome=" + chrome +"]";
	}
	
}
