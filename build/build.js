({
  baseUrl: "./",
  name: "requireLib",
  optimize: "none",
  include: [
    "../js/require.config",
    "../js/app"
  ],
  mainConfigFile: "../js/main.js",
  paths: { requireLib: "../components/almond/almond" },
  out: "app.js"
})
