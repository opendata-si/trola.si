(function () {
  "use strict";

  requirejs.config({
    paths: {
      "jquery": "../components/jquery/jquery",
      "underscore": "../components/underscore-amd/underscore",
      "backbone": "../components/backbone-amd/backbone"
    }
  });

  require(['./app']);

}());
