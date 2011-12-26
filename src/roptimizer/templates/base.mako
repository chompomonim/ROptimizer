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
    <header> </header>

    <div class="content">
        ${next.body()}
    </div>

    <footer>
      <div class="inner">
        &copy; ROptimizer
      </div>
    </footer>
  </body>
</html>
