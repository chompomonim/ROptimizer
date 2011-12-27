<%inherit file="base.mako" />

<%def name="pagetitle()">Welcome to ROptimizer</%def>

%if money_left > 0:
<div class="to-spend">
  <h1>To spend today: $${left_today}</h1>
  <div>Spent today: $${spent_today}</div>
  <div>Money left: $${money_left}</div>
  <div>Average per day: $${to_spend}</div>
  <div>Days left: ${days_left}
</div>

<div class="center">
  <% q = {'period': period.id} %>
  <a class="button" href="${request.route_url('spend', _query=q)}">Spent now</a>
</div>

%else:
<div class="to-spend">
  <h1 style="color: red;">You don't have money enymore!!!</h1>
  <div><b>Debt: $${0-money_left}</b></div>
  <div>Days left: ${days_left}
</div>


%endif


