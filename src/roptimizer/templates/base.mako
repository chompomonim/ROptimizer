<!doctype html>
<html>
  <head>
    <title>ROptimizer</title>
    <link rel="stylesheet" href="${request.static_url('roptimizer:static/style.css')}" type="text/css" media="screen" charset="utf-8">
    <link rel="icon" href="${request.static_url('roptimizer:static/favicon.ico')}" type="image/x-icon">
    <script encoding="utf-8" src="${request.static_url('roptimizer:static/js/jquery.js')}" type="text/javascript"></script>
    <script encoding="utf-8" src="${request.static_url('roptimizer:static/js/scripts.js')}" type="text/javascript"></script>
  </head>
  <body>
    <div class="content">
        ${next.body()}
    </div>

    <footer>
      <b>&reg;</b>ptimizer 
      <a class="menu" href="${request.route_url('app')}">Home</a>
      <a class="menu" href="${request.route_url('settings')}">Settings</a>
</footer>
  </body>
</html>
