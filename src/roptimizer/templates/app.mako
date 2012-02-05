<%inherit file="base.mako" />

<%def name="pagetitle()">Welcome to ROptimizer</%def>

%if money_left > 0:
<div class="to-spend center">
  <div class="counter">
    <b>To spend today:</b>
    <h1>€${left_today}</h1>
  </div>

  <div class="more-info">
    <div>Spent today: $${spent_today}</div>
    <div>Money left: $${money_left}</div>
    <div>Average per day: $${to_spend}</div>
    <div>Days left: ${days_left}</div>
  </div>
</div>


<% q = {'period': period.id} %>
<a data-role="button" data-icon="arrow-r" href="${request.route_url('spend', _query=q)}">Spend now</a>

%else:
<div class="to-spend center">
  <h1 style="color: red;">You don't have money enymore!!!</h1>
  <div class="more-info">
    <div><b>Debt: €${0-money_left}</b></div>
    <div>Days left: ${days_left}</div>
  </div>
</div>

%endif


