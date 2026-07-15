{
  inputs = {
    devshell.url = "github:numtide/devshell";
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    treefmt-nix.url = "github:numtide/treefmt-nix";
  };

  outputs = inputs @ {
    flake-parts,
    systems,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      imports = with inputs; [
        devshell.flakeModule
        treefmt-nix.flakeModule
      ];

      perSystem = {
        config,
        lib,
        pkgs,
        ...
      }: {
        devshells.default = {...}: {
          packages = lib.flatten [
            (with pkgs; [
              python314
              uv
              ty
            ])

            (with config.treefmt.build; [
              (builtins.attrValues programs)
              wrapper
            ])
          ];
        };

        treefmt.programs = {
          alejandra.enable = true;
          ruff.enable = true;
        };
      };

      systems = import systems;
    };
}
