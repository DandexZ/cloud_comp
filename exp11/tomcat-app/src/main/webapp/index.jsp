<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Tomcat Server</title>
</head>
<body>
    <h1>当前服务器: <%= System.getenv("server.name") %></h1>
    <p>请求时间: <%= new java.util.Date() %></p>
    <p>Session ID: <%= session.getId() %></p>
</body>
</html>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Tomcat Instance</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: inline-block;
        }
        .server-info {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Tomcat Server</h1>
        <div class="server-info">
            <h2>Server Information</h2>
            <p><strong>Host:</strong> <%= request.getLocalAddr() %></p>
            <p><strong>Port:</strong> <%= request.getLocalPort() %></p>
            <p><strong>Server Name:</strong> <%= System.getProperty("server.name", "Tomcat-" + request.getLocalPort()) %></p>
            <p><strong>Session ID:</strong> <%= session.getId() %></p>
            <p><strong>Request Count:</strong> 
                <%
                    Integer count = (Integer) session.getAttribute("count");
                    if (count == null) {
                        count = 1;
                    } else {
                        count++;
                    }
                    session.setAttribute("count", count);
                    out.print(count);
                %>
            </p>
        </div>
        <p>Current Time: <%= new java.util.Date() %></p>
    </div>
</body>
</html>