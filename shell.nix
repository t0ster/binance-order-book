let
  pkgs = import <nixpkgs> {};
  my-python-packages = python-packages: with python-packages; [
    pip
    isort
    black
  ];
  python-with-my-packages = pkgs.python311.withPackages my-python-packages;
in pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    python-with-my-packages
  ];
}
