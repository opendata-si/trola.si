(function () {
  "use strict";

  requirejs.config({
    baseUrl: "js/",
    paths: {
      "jquery": "components/jquery/jquery",
      "underscore": "components/underscore-amd/underscore",
      "backbone": "components/backbone-amd/backbone"
    }
  });

  require(['./app'], function (app) {
    app.initialize();
  });

}());
