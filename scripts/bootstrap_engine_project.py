#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path


COMMON_FILES = {
    "assets/README.md": """\
    # Assets

    Store source art, audio, data, and export-ready files here when they are shared
    across pipelines. Engine-native imported assets may also live in engine-specific
    roots such as `Assets/` for Unity or `Content/` for Unreal.
    """,
    "design/gdd/README.md": """\
    # Game Design Documents

    Keep the concept document, systems index, and per-system GDD files here.
    Start with `game-concept.md`, then decompose the project with `map-systems`
    and `design-system`.
    """,
    "design/narrative/README.md": """\
    # Narrative Design

    Put character sheets, dialogue flows, quest notes, and lore documents here.
    """,
    "design/levels/README.md": """\
    # Level Design

    Store encounter layouts, map callouts, pacing notes, and level-by-level docs here.
    """,
    "docs/architecture/README.md": """\
    # Architecture Decisions

    Keep ADRs and architecture overviews here. Each gameplay system should point back
    to at least one architecture decision before production work scales up.
    """,
    "tests/README.md": """\
    # Tests

    Cross-engine test reports, automation output, and performance evidence live here.
    Engine-native tests may also live under `Assets/Tests/` or `Source/<Project>/Tests/`
    depending on the selected runtime.
    """,
    "tools/build/README.md": """\
    # Build Tooling

    Keep export scripts, build wrappers, and CI helpers here.
    """,
    "tools/asset-pipeline/README.md": """\
    # Asset Pipeline

    Put conversion scripts, import automation, and validation helpers for art/audio
    pipelines here.
    """,
    "prototypes/README.md": """\
    # Prototypes

    Throwaway experiments belong here. Prototype code should stay isolated from
    production runtime code.
    """,
    "production/sprints/README.md": """\
    # Sprint Plans

    Store sprint definitions, goals, and work breakdowns here.
    """,
    "production/milestones/README.md": """\
    # Milestones

    Store milestone definitions, acceptance criteria, and release targets here.
    """,
    "production/releases/README.md": """\
    # Releases

    Keep release checklists, launch plans, and release notes drafts here.
    """,
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "game-project"


def pascal_case(value: str) -> str:
    pieces = re.findall(r"[A-Za-z0-9]+", value)
    return "".join(piece[:1].upper() + piece[1:] for piece in pieces) or "CodexGame"


def title_case_from_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in slugify(value).split("-"))


def normalize_engine(value: str) -> str:
    cleaned = slugify(value)
    aliases = {
        "godot": "godot",
        "godot-4": "godot",
        "unity": "unity",
        "unity-6": "unity",
        "unreal": "unreal",
        "unreal-engine": "unreal",
        "ue5": "unreal",
        "unreal-engine-5": "unreal",
    }
    if cleaned not in aliases:
        raise ValueError(f"Unsupported engine: {value}")
    return aliases[cleaned]


def infer_project_name(root: Path) -> str:
    return title_case_from_slug(root.name)


def unity_editor_version(version: str) -> str:
    digits = re.findall(r"\d+", version)
    if not digits:
        return "6000.0.0f1"
    if version.startswith("6000"):
        return "6000.0.0f1"
    if version.startswith("2023"):
        return "2023.1.0f1"
    if digits[0] == "6":
        return "6000.0.0f1"
    return f"{digits[0]}.0.0f1"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def render_common_files(project_name: str, engine: str) -> dict[str, str]:
    files: dict[str, str] = {}
    for relative_path, content in COMMON_FILES.items():
        if engine == "unity" and relative_path == "assets/README.md":
            continue
        files[relative_path] = textwrap.dedent(content).strip() + "\n"

    files["docs/architecture/adr-0001-engine-bootstrap.md"] = textwrap.dedent(
        f"""\
        # ADR-0001: Bootstrap Runtime Skeleton

        - **Status:** Accepted
        - **Date:** [Update when reviewed]

        ## Context

        The project needs a real runtime skeleton for the selected engine so Codex can
        implement gameplay systems against concrete files instead of pure documentation.

        ## Decision

        Start from the `bootstrap-engine` scaffold for **{engine.title()}** and evolve
        the generated runtime files rather than keeping the repository in a docs-only state.

        ## Consequences

        - The repo gains engine-native entry files immediately.
        - Architecture, testing, and build automation can now target real project files.
        - Follow-up ADRs should refine subsystem boundaries once the first gameplay slice exists.
        """
    ).strip() + "\n"
    files["production/stage.txt"] = "Technical Setup"
    files["tools/build/bootstrap-notes.md"] = textwrap.dedent(
        f"""\
        # Bootstrap Notes

        Project: **{project_name}**
        Engine: **{engine.title()}**

        This repository now has an initial runtime scaffold. Review the generated files,
        open the project in the selected engine, and then continue with:

        1. `architecture-decision`
        2. `map-systems`
        3. `prototype` or a `team-*` workflow for the first slice
        """
    ).strip() + "\n"
    return files


def godot_files(project_name: str, version: str, mode: str) -> dict[str, str]:
    icon_svg = textwrap.dedent(
        """\
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc">
          <title id="title">Bootstrap Icon</title>
          <desc id="desc">A green game badge used for a freshly bootstrapped project.</desc>
          <rect width="256" height="256" rx="42" fill="#0F1F16"/>
          <rect x="28" y="28" width="200" height="200" rx="30" fill="#14532D"/>
          <circle cx="98" cy="128" r="20" fill="#DCFCE7"/>
          <circle cx="158" cy="128" r="20" fill="#DCFCE7"/>
          <path d="M72 182c18-18 42-28 56-28s38 10 56 28" fill="none" stroke="#A7F3D0" stroke-linecap="round" stroke-width="10"/>
          <path d="M82 74h92" stroke="#86EFAC" stroke-linecap="round" stroke-width="10"/>
        </svg>
        """
    ).strip() + "\n"

    project_mode = "3D" if mode == "3d" else "2D"
    project_godot = textwrap.dedent(
        f"""\
        ; Engine configuration file.
        ; Best edited using the editor UI and not directly.
        ;
        ; Format:
        ;   [section] ; section goes between []
        ;   param=value ; assign values to parameters

        config_version=5

        [application]

        config/name="{project_name}"
        run/main_scene="res://src/scenes/bootstrap_scene.tscn"
        config/features=PackedStringArray("{version}")
        config/icon="res://assets/ui/app-icon.svg"

        [autoload]

        GameRoot="*res://src/core/game_root.gd"

        [display]

        window/size/viewport_width=1280
        window/size/viewport_height=720
        window/stretch/mode="canvas_items"

        [rendering]

        renderer/rendering_method="forward_plus"
        renderer/rendering_method.mobile="mobile"
        """
    ).strip() + "\n"

    boot_script = textwrap.dedent(
        f"""\
        extends Node2D

        const BOOTSTRAP_MESSAGE := "{project_name} bootstrap ready ({project_mode})"

        func _ready() -> void:
            var label := Label.new()
            label.text = BOOTSTRAP_MESSAGE
            label.position = Vector2(32, 32)
            add_child(label)
        """
    ).strip() + "\n"

    root_script = textwrap.dedent(
        f"""\
        extends Node

        const PROJECT_NAME := "{project_name}"
        const ENGINE_VERSION := "{version}"

        func describe_stack() -> Dictionary:
            return {{
                "engine": "Godot",
                "version": ENGINE_VERSION,
                "mode": "{project_mode}",
                "main_scene": "res://src/scenes/bootstrap_scene.tscn",
            }}
        """
    ).strip() + "\n"

    scene = textwrap.dedent(
        """\
        [gd_scene load_steps=2 format=3]

        [ext_resource type="Script" path="res://src/core/bootstrap_scene.gd" id="1"]

        [node name="BootstrapScene" type="Node2D"]
        script = ExtResource("1")
        """
    ).strip() + "\n"

    return {
        "project.godot": project_godot,
        "assets/ui/app-icon.svg": icon_svg,
        "src/README.md": "# Runtime Source\n\nGodot gameplay code and scenes live under `src/`.\n",
        "src/core/game_root.gd": root_script,
        "src/core/bootstrap_scene.gd": boot_script,
        "src/scenes/bootstrap_scene.tscn": scene,
        "tests/unit/README.md": "# Godot Unit Tests\n\nUse GUT or another chosen framework for gameplay and formula tests.\n",
    }


def unity_files(project_name: str, version: str, module_name: str) -> dict[str, str]:
    manifest = {
        "dependencies": {
            "com.unity.test-framework": "1.1.33"
        }
    }
    bootstrap_cs = textwrap.dedent(
        f"""\
        using UnityEngine;

        namespace {module_name}.Runtime
        {{
            /// <summary>
            /// Minimal runtime entrypoint created by bootstrap-engine.
            /// Attach this component to the first scene bootstrap object.
            /// </summary>
            public sealed class Bootstrap : MonoBehaviour
            {{
                [SerializeField] private string bootstrapMessage = "{project_name} bootstrap ready";

                private void Start()
                {{
                    Debug.Log(bootstrapMessage);
                }}
            }}
        }}
        """
    ).strip() + "\n"
    bootstrap_test = textwrap.dedent(
        f"""\
        using NUnit.Framework;
        using UnityEngine;

        namespace {module_name}.Tests.EditMode
        {{
            public sealed class BootstrapTests
            {{
                [Test]
                public void BootstrapComponent_CanBeAddedToGameObject()
                {{
                    var host = new GameObject("BootstrapHost");
                    try
                    {{
                        var component = host.AddComponent<{module_name}.Runtime.Bootstrap>();
                        Assert.That(component, Is.Not.Null);
                    }}
                    finally
                    {{
                        Object.DestroyImmediate(host);
                    }}
                }}
            }}
        }}
        """
    ).strip() + "\n"

    scene_readme = textwrap.dedent(
        f"""\
        # Unity Scenes

        Create the first playable scene here and attach `{module_name}.Runtime.Bootstrap`
        to an initial root object. Add the scene to build settings once it exists.
        """
    ).strip() + "\n"

    return {
        "Assets/README.md": "# Unity Assets\n\nUnity runtime content lives under `Assets/`.\n",
        "Assets/Scenes/README.md": scene_readme,
        "Assets/Scripts/Runtime/Bootstrap.cs": bootstrap_cs,
        "Assets/Tests/EditMode/BootstrapTests.cs": bootstrap_test,
        "Packages/manifest.json": json.dumps(manifest, indent=2) + "\n",
        "ProjectSettings/ProjectVersion.txt": f"m_EditorVersion: {unity_editor_version(version)}\n",
        "tests/unit/README.md": "# Cross-Engine Tests\n\nStore CI evidence and non-Unity-native test notes here.\n",
    }


def unreal_files(project_name: str, version: str, module_name: str) -> dict[str, str]:
    uproject = {
        "FileVersion": 3,
        "EngineAssociation": version,
        "Category": "",
        "Description": f"Bootstrap runtime skeleton for {project_name}.",
        "Modules": [
            {
                "Name": module_name,
                "Type": "Runtime",
                "LoadingPhase": "Default",
            }
        ],
        "Plugins": [
            {
                "Name": "EnhancedInput",
                "Enabled": True,
            }
        ],
    }
    build_cs = textwrap.dedent(
        f"""\
        using UnrealBuildTool;

        public class {module_name} : ModuleRules
        {{
            public {module_name}(ReadOnlyTargetRules Target) : base(Target)
            {{
                PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

                PublicDependencyModuleNames.AddRange(new[]
                {{
                    "Core",
                    "CoreUObject",
                    "Engine",
                    "InputCore",
                    "EnhancedInput"
                }});
            }}
        }}
        """
    ).strip() + "\n"
    target_cs = textwrap.dedent(
        f"""\
        using UnrealBuildTool;
        using System.Collections.Generic;

        public class {module_name}Target : TargetRules
        {{
            public {module_name}Target(TargetInfo Target) : base(Target)
            {{
                Type = TargetType.Game;
                DefaultBuildSettings = BuildSettingsVersion.V5;
                IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
                ExtraModuleNames.Add("{module_name}");
            }}
        }}
        """
    ).strip() + "\n"
    editor_target_cs = textwrap.dedent(
        f"""\
        using UnrealBuildTool;
        using System.Collections.Generic;

        public class {module_name}EditorTarget : TargetRules
        {{
            public {module_name}EditorTarget(TargetInfo Target) : base(Target)
            {{
                Type = TargetType.Editor;
                DefaultBuildSettings = BuildSettingsVersion.V5;
                IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
                ExtraModuleNames.Add("{module_name}");
            }}
        }}
        """
    ).strip() + "\n"
    module_cpp = textwrap.dedent(
        f"""\
        #include "{module_name}.h"
        #include "Modules/ModuleManager.h"

        IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, {module_name}, "{module_name}");
        """
    ).strip() + "\n"
    module_h = textwrap.dedent(
        f"""\
        #pragma once

        #include "CoreMinimal.h"
        """
    ).strip() + "\n"
    gamemode_h = textwrap.dedent(
        f"""\
        #pragma once

        #include "CoreMinimal.h"
        #include "GameFramework/GameModeBase.h"
        #include "BootstrapGameMode.generated.h"

        UCLASS()
        class {module_name.upper()}_API ABootstrapGameMode : public AGameModeBase
        {{
            GENERATED_BODY()

        public:
            ABootstrapGameMode();
        }};
        """
    ).strip() + "\n"
    gamemode_cpp = textwrap.dedent(
        """\
        #include "BootstrapGameMode.h"

        ABootstrapGameMode::ABootstrapGameMode()
        {
        }
        """
    ).strip() + "\n"
    default_game = textwrap.dedent(
        f"""\
        [/Script/EngineSettings.GeneralProjectSettings]
        ProjectName={project_name}
        ProjectVersion=0.1.0
        CompanyName=
        Description=Bootstrap runtime skeleton generated by Codex Game Studio.

        [/Script/EngineSettings.GameMapsSettings]
        GlobalDefaultGameMode=/Script/{module_name}.BootstrapGameMode
        """
    ).strip() + "\n"
    default_engine = textwrap.dedent(
        f"""\
        [/Script/HardwareTargeting.HardwareTargetingSettings]
        TargetedHardwareClass=Desktop
        AppliedTargetedHardwareClass=Desktop
        DefaultGraphicsPerformance=Maximum
        AppliedDefaultGraphicsPerformance=Maximum

        [/Script/Engine.Engine]
        +ActiveGameNameRedirects=(OldGameName="TP_Blank",NewGameName="/Script/{module_name}")
        +ActiveGameNameRedirects=(OldGameName="/Script/TP_Blank",NewGameName="/Script/{module_name}")
        """
    ).strip() + "\n"

    return {
        f"{module_name}.uproject": json.dumps(uproject, indent=2) + "\n",
        "Content/README.md": "# Unreal Content\n\nPlace levels, materials, meshes, and Blueprint assets here.\n",
        "Config/DefaultGame.ini": default_game,
        "Config/DefaultEngine.ini": default_engine,
        f"Source/{module_name}.Target.cs": target_cs,
        f"Source/{module_name}Editor.Target.cs": editor_target_cs,
        f"Source/{module_name}/{module_name}.Build.cs": build_cs,
        f"Source/{module_name}/{module_name}.h": module_h,
        f"Source/{module_name}/{module_name}.cpp": module_cpp,
        f"Source/{module_name}/Public/BootstrapGameMode.h": gamemode_h,
        f"Source/{module_name}/Private/BootstrapGameMode.cpp": gamemode_cpp,
        f"Source/{module_name}/Tests/README.md": "# Unreal Tests\n\nPut automation specs and gameplay validation notes here.\n",
    }


def detect_existing_markers(root: Path) -> list[str]:
    markers: list[str] = []
    if (root / "project.godot").exists():
        markers.append("project.godot")
    if (root / "Packages" / "manifest.json").exists():
        markers.append("Packages/manifest.json")
    markers.extend(sorted(path.name for path in root.glob("*.uproject")))
    return markers


def build_file_map(engine: str, project_name: str, version: str, mode: str) -> dict[str, str]:
    module_name = pascal_case(project_name)
    files = render_common_files(project_name, engine)
    if engine == "godot":
        files.update(godot_files(project_name, version, mode))
    elif engine == "unity":
        files.update(unity_files(project_name, version, module_name))
    elif engine == "unreal":
        files.update(unreal_files(project_name, version, module_name))
    else:
        raise ValueError(f"Unsupported engine: {engine}")
    return files


def write_files(root: Path, files: dict[str, str], force: bool) -> list[Path]:
    conflicts = [root / relative_path for relative_path in files if (root / relative_path).exists()]
    if conflicts and not force:
        conflict_lines = "\n".join(f"- {path.relative_to(root)}" for path in conflicts)
        raise FileExistsError(
            "Refusing to overwrite existing bootstrap files without --force:\n" + conflict_lines
        )

    written: list[Path] = []
    for relative_path, content in files.items():
        path = root / relative_path
        ensure_parent(path)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create an engine-ready bootstrap skeleton for Godot, Unity, or Unreal."
    )
    parser.add_argument("--engine", required=True, help="Engine name: godot, unity, or unreal.")
    parser.add_argument(
        "--project-name",
        help="Display name for the project. Defaults to the current directory name.",
    )
    parser.add_argument(
        "--engine-version",
        default="latest-stable",
        help="Pinned engine version for generated files.",
    )
    parser.add_argument(
        "--mode",
        choices=("2d", "3d"),
        default="2d",
        help="Presentation mode for engines where it matters.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root to write into. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned file list without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.root).resolve()
    engine = normalize_engine(args.engine)
    project_name = args.project_name.strip() if args.project_name else infer_project_name(root)

    if engine == "unreal":
        args.mode = "3d"

    existing_markers = detect_existing_markers(root)
    files = build_file_map(engine, project_name, args.engine_version, args.mode)

    if args.dry_run:
        print(f"Engine: {engine}")
        print(f"Project: {project_name}")
        if existing_markers:
            print("Existing engine markers:")
            for marker in existing_markers:
                print(f"- {marker}")
        print("Planned files:")
        for relative_path in sorted(files):
            print(f"- {relative_path}")
        return 0

    try:
        written = write_files(root, files, force=args.force)
    except (FileExistsError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Bootstrapped {engine} project for {project_name}.")
    for path in sorted(written):
        print(f"- {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
