<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"
 	import = "in.environmental.model.User"   
    
 %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Login and registartion</title>
<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<link rel="stylesheet" href="style.css">
</head>
<body>
	<%
			User user = (User)session.getAttribute("user");
			if(user!=null){ %>
		
		    <h3 style="font-size:30px">Welcome <% out.print(user.getUsername()); %></h3>
		    <a href="LoginController?query=logout" style="width:500px;background:rgba(0,0,0,0);border:rgba(0,0,0,0);text-align:left;">Logout</a>
		    
		    <% }else{ %> 
		    	<h3>Your don't have permission to access this page</h3>
		    <% } %>
	
	
</body>
</html>