<!doctype html>
<html>
  <head>
    <title>ROptimizer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0.1/jquery.mobile-1.0.1.min.css" />
    <link rel="stylesheet" href="${request.static_url('roptimizer:static/style.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="icon" href="${request.static_url('roptimizer:static/favicon.ico')}" type="image/x-icon">
    <script src="http://code.jquery.com/jquery-1.6.4.min.js"></script>
    <script encoding="utf-8" src="${request.static_url('roptimizer:static/js/jquery.mobile.js')}" type="text/javascript"></script>
    <script encoding="utf-8" src="${request.static_url('roptimizer:static/js/scripts.js')}" type="text/javascript"></script>
  </head>

  <body>
    <div data-role="page">
      <div data-role="header" data-position="inline" data-theme="b">
	<h1>&reg;ptimizer</h1>
	<a data-icon="home" href="${request.route_url('app')}">Home</a>
	<a data-icon="gear" href="${request.route_url('settings')}">Settings</a>
      </div><!-- /header -->
      <div data-role="content">
        ${next.body()}
      </div><!-- /content -->
    </div><!-- /page -->
  </body>
</html>
