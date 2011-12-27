<%inherit file="base.mako" />

<h2>Money spent today</h2>

<ul>
  %for expense in expenses:
  <li>${expense.name} - $${expense.amount}</li>
  %endfor
</ul>

<form id="spent-form" method="post" action="${request.route_url('add_spending')}">
  <div>
    <input type="text" name="name" placeholder="Name it" /> -
    $<input type="text" name="amount" placeholder="How much?" maxlength="8" style="width:80px;" />
  </div>
  <button name="submit" type="submit" class="small">Add to spends</button>
</form>
