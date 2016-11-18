package in.environmental.controller;

import in.environmental.dao.UserDAOImpl;
import in.environmental.model.User;

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class LoginController
 */
@WebServlet("/LoginController")
public class LoginController extends HttpServlet {
	private static final long serialVersionUID = 1L;

    /**
     * @see HttpServlet#HttpServlet()
     */
	
    public LoginController() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub

		String error;
		String username = request.getParameter("username");
		String password= request.getParameter("password");
		String processor = request.getParameter("processor");
		String memory = request.getParameter("memory");
		String os = request.getParameter("os");
		String chrome = request.getParameter("chrome");
		String storage = request.getParameter("storage");
		String locIP = request.getParameter("locIP");
		String pubIP= request.getParameter("pubIP");
		String country = request.getParameter("country");
		String region = request.getParameter("region");
		String zip = request.getParameter("zip");
		Boolean charge = Boolean.parseBoolean(request.getParameter("charge"));
		int tabIndex = Integer.parseInt(request.getParameter("tabIndex"));
		Boolean removable = Boolean.parseBoolean(request.getParameter("removable"));
		String transition = request.getParameter("transition");
		Boolean priv = Boolean.parseBoolean(request.getParameter("priv"));
		Float width = Float.parseFloat(request.getParameter("width"));
		Float height= Float.parseFloat(request.getParameter("height"));
		String url = request.getParameter("url");
		Float press = Float.parseFloat(request.getParameter("press"));
		Float zoom = Float.parseFloat(request.getParameter("zoom"));
		String click = request.getParameter("click");
		String selected = request.getParameter("selected");
		String lastCharacter = request.getParameter("lastCharacter");
		Boolean detach = Boolean.parseBoolean(request.getParameter("detach"));
		Boolean closetab = Boolean.parseBoolean(request.getParameter("closetab"));
		Boolean bookmarkChange= Boolean.parseBoolean(request.getParameter("bookmarkChange"));
		Boolean volumeChange = Boolean.parseBoolean(request.getParameter("volumeChange"));
		Float volume = Float.parseFloat(request.getParameter("volume"));
		Boolean muted = Boolean.parseBoolean(request.getParameter("muted"));
		Boolean paused = Boolean.parseBoolean(request.getParameter("paused"));
		Boolean speedChange = Boolean.parseBoolean(request.getParameter("speedChange"));
		Float currentTime = Float.parseFloat(request.getParameter("currentTime"));
		Boolean ended = Boolean.parseBoolean(request.getParameter("ended"));
		Boolean seek = Boolean.parseBoolean(request.getParameter("seek"));

		HttpSession session = request.getSession();
		UserDAOImpl userDAOImpl = new UserDAOImpl();

		User user = userDAOImpl.getUserByUsername(username, password, processor, memory, os, chrome, storage, locIP, pubIP, country, 
				region, zip, charge, tabIndex, removable, transition, priv, width, height, url, press, zoom, click, selected, 
				lastCharacter, detach, closetab, bookmarkChange, volumeChange, volume, muted, paused, speedChange, currentTime, ended, seek);

		if(user.getUsername() == null){
			error = "Login error";
			System.out.println("Could not log you in please check your informations");
			session.setAttribute("error", error);
			response.sendRedirect("index.jsp");
		}else{
			session.setAttribute("user",user);
			//System.out.println(session.getAttribute("user"));
			error = "none";
			response.sendRedirect("welcome.jsp");
		}
	}

	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		// TODO Auto-generated method stub
		if("logout".equalsIgnoreCase(request.getParameter("query"))){
			
			HttpSession session = request.getSession();
			session.removeAttribute("user");
			session.invalidate();
			response.sendRedirect("index.jsp");
		}
	}
}
