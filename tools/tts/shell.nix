{ pkgs ? import <nixpkgs> {} }:

let
  runtimeLibs = with pkgs; [
    zlib
    gcc.cc.lib      # libstdc++ needed by ONNX Runtime wheels
  ];
in

pkgs.mkShell {
  packages = with pkgs; [
    python312
    uv
    git
    ffmpeg
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath runtimeLibs}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  '';
}
