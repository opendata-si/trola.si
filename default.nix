with (import <nixpkgs> {});

with pythonPackages;

let
  mimerender = buildPythonPackage {
    name = "mimerender";

    src = fetchurl {
      url = "https://pypi.python.org/packages/90/93/04da69a3a9adae4aae66cf9884f09d82e318018673ba9193a593db01e0ee/mimerender-0.6.0.tar.gz";
      sha256 = "1imim78dypbl9fvrz21j8f13q8i96dx90m7f5ib3z371zrz3gwg7";
    };

    propagatedBuildInputs = [ python_mimeparse ];
  };
in buildPythonPackage {
  name = "trola.si";

  src = ./.;

  propagatedBuildInputs = [ flask mock requests raven blinker nose coverage mimerender sphinx sphinxcontrib_httpdomain simplejson ];
}
