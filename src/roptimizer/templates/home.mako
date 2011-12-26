<%inherit file="base.mako" />

%if periods:
   <ul>
   %for period in periods: 
      <li>Period: ${period.name} ${period.id}</li>
   %endfor
   </ul>
%endif

<form method="post" action="${request.route_url('home')}" method="post">
  <input type="text" name="username" />
  <input type="password" name="password" />
  <input type="submit" value="Login" />
</form>
