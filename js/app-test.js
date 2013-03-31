/*jshint bitwise:true, curly:true, eqeqeq:true, immed:true, latedef:true,
  newcap:true, noarg:true, noempty:true, nonew:true, plusplus:true,
  regexp:true, undef:true, strict:true, trailing:true, browser:true */
/*global buster:false, jQuery:false, createElement:false, removeElements:false,
  onLoad:false, getElementStyle: false, getElementsByAttribute:false,
  define:false, describe:false, it:false, beforeEach:false, afterEach:false */

define([
  'components/chai/chai',
  './app'
], function(chai, App, undefined) {
  "use strict";

  var expect = chai.expect,
      mocha = window.mocha;

  mocha.setup('bdd');

  describe("app.js", function() {
    beforeEach(function() {
    });
    afterEach(function() {
    });
    it("example", function() {
      expect(App).to.equal('success');
    });
  });

});
