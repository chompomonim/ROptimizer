<%inherit file="base.mako" />

<form method="post" action="${request.route_url('login')}" method="post">
  <input type="text" name="username" />
  <input type="password" name="password" />
  <input type="submit" value="Login" />
</form>
