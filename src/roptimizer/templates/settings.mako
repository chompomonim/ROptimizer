<%inherit file="base.mako" />

<div data-role="collapsible-set">

  %if periods:
  <div data-role="collapsible" data-collapsed="true">
    <h3>Periodic expenses:</h3>
    %if expenses:
    <ul data-role="listview" data-inset="true" data-theme="d" data-divider-theme="b">
      <li role="heading" data-role="list-divider">Periodic expenses</li>
      %for expense in expenses:
      <li>${expense.name} <span class="ui-li-count">€${expense.amount}</span></li>
      %endfor
    </ul>
    %endif

    <form id="income-expense" method="post" action="${request.route_url('add_periodic_expense')}">
      <div data-role="fieldcontain">
	<input type="text" name="name" placeholder="Name it" />
	<input type="text" name="amount" placeholder="How much?" class="money" />
      </div>
      <button name="submit" type="submit" data-icon="plus" data-inline="true">Add expense</button>
    </form>
  </div>

  <div data-role="collapsible">
    <h3>Incomes:</h3>
    <ul data-role="listview" data-inset="true" data-theme="d" data-divider-theme="b">
      <li role="heading" data-role="list-divider">Incomes in this period</li>
      %for income in incomes:
      <li>${income.name} <span class="ui-li-count">€${income.amount}</span></li>
      %endfor
    </ul>

    <form id="income-form" method="post" action="${request.route_url('add_income')}">
      <div data-role="fieldcontain">
	<input type="text" name="name" placeholder="Name it" />
	<input type="text" name="amount" placeholder="How much?" class="money" />
      </div>
      <button name="submit" type="submit" data-icon="plus" data-inline="true">Add income</button>
    </form>
  </div>
  %endif

  <div data-role="collapsible">
    <h3>Periods:</h3>
    <form id="active-period">
      <ol data-role="listview" data-inset="true">
	%for period in periods:
	<input
	   type="radio"
	   name="period"
	   value="${period.id}"
	   %if period.active:
	   checked
	   %endif
	   />
	<label for="${period.id}">${period.name}</label>
	%endfor
      </ol>
    </form>
    <form id="add-period" method="post" action="${request.route_url('add_period')}">
      <input type="text" name="period" placeholder="Add new period" />
      <button name="submit" type="submit" class="small">Add</button>
    </form>
  </div>
</div>
