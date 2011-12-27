<%inherit file="base.mako" />

<h2>Settings</h2>

%if periods:
<h3>Periodic expenses:</h3>
%if expenses:
<ol>
  %for expense in expenses:
  <li>${expense.name} - $${expense.amount}</li>
  %endfor
</ol>
%endif

<form id="income-expense" method="post" action="${request.route_url('add_periodic_expense')}">
  <div>
    <input type="text" name="name" placeholder="Name it" /> -
    $<input type="text" name="amount" placeholder="How much?" maxlength="8" style="width:80px;" />
  </div>
  <button name="submit" type="submit" class="small">Add expnese</button>
</form>


<h3>Incomes:</h3>
<ol>
  %for income in incomes:
  <li>${income.name} - $${income.amount}</li>
  %endfor
</ol>

<form id="income-form" method="post" action="${request.route_url('add_income')}">
  <div>
    <input type="text" name="name" placeholder="Name it" /> -
    $<input type="text" name="amount" placeholder="How much?" maxlength="8" style="width:80px;" />
  </div>
  <button name="submit" type="submit" class="small">Add income</button>
</form>
%endif

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
