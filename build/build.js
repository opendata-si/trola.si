({
  baseUrl: "./",
  name: "requireLib",
  optimize: 'uglify',
  include: [
    "../js/app"
  ],
  mainConfigFile: "../js/main.js",
  paths: { requireLib: "../components/almond/almond" },
  out: "app.js"
})
