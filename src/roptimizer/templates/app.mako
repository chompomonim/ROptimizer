<%inherit file="base.mako" />

<%def name="pagetitle()">Welcome to ROptimizer</%def>

<h1>To spend: $${to_spend}</h1>

<h2>Period: ${period.name} ${period.id}</h2>
<h2>All expanses: ${expenses}<h2>

%if incomes:
   <ul>
   %for income in incomes: 
      <li>${income.name} ${income.amount}</li>
   %endfor
   </ul>
%endif
