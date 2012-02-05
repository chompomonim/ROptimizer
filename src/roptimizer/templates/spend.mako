<%inherit file="base.mako" />

<ul data-role="listview" data-inset="true" data-theme="d" data-divider-theme="b">
  <li role="heading" data-role="list-divider">Money spent today</li>
  %for expense in expenses:
  <li>${expense.name} <span class="ui-li-count">€${expense.amount}</span></li>
  %endfor
  <li data-theme="c"><b>Total:</b> ${expenses_sum}</li>
</ul>

<form id="spent-form" method="post" action="${request.route_url('add_spending')}">
  <div data-role="fieldcontain">
    <input type="text" name="name" placeholder="What you spent money for?" />
    <input type="text" name="amount" placeholder="How much?" maxlength="8" id="money" />
  </div>
  <button name="submit" type="submit" data-icon="plus" data-inline="true">Add to spends</button>
</form>
