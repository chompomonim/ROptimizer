<%inherit file="base.mako" />

<h2>Settings</h2>




<h3>All periods:</h3>
<ol>
  %for period in periods:
  <li>${period.name}</li>
  %endfor
</ol>

<form id="add-period" method="post" action="${request.route_url('add_period')}">
  <input type="text" name="period" placeholder="Add new period" />
  <button name="submit" type="submit" class="small">Add</button>
</form>
