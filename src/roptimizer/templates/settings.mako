<%inherit file="base.mako" />

<h2>Settings</h2>

<b>All periods:</b>
<ol>
  %for period in periods:
  <li>${period.name}</li>
  %endfor
</ol>

<form id="add-period" method="post" action="${request.route_url('add_period')}">
  <input type="text" name="period" placeholder="Add new period" /> -
  <button name="submit" type="submit" class="small">Add</button>
</form>
