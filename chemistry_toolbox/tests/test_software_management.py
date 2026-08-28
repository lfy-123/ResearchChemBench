from __future__ import annotations

import io
import json
import os
import tarfile
import zipfile
from pathlib import Path

import pytest

from chemistry_toolbox.software_management.manager import SoftwareManager
from chemistry_toolbox.software_management.manifests import load_catalog
from chemistry_toolbox.software_management.migrate import migrate_legacy_cache
from chemistry_toolbox.software_management.legacy_layout import classify_legacy_path
from chemistry_toolbox.software_management.migrate_v2 import migrate_v2, relocate_v2
from chemistry_toolbox.software_management.paths import LAYOUT_DIRECTORIES
from chemistry_toolbox.software_management.repository_paths import rewrite_text


def write_catalog(path: Path, *, migration: str = "") -> None:
    path.write_text(
        f"""schema_version: 1
software:
  demo:
    display_name: Demo
    version: 1.0
    acquisition: manual
    license: MIT
    accepted_packages: [demo-*.tar.gz]
    installation:
      handler: archive
      target: installations/demo/1.0/linux-x86_64
      strip_single_directory: true
      executable_paths: [bin/demo]
    runtime:
      entrypoints:
        demo: bin/demo
    verification:
      - command: ["{{entrypoint:demo}}", --version]
        output_contains: demo 1.0
{migration}""",
        encoding="utf-8",
    )


def create_demo_archive(path: Path) -> None:
    script = b"#!/bin/sh\necho 'demo 1.0'\n"
    info = tarfile.TarInfo("demo-1.0/bin/demo")
    info.mode = 0o755
    info.size = len(script)
    with tarfile.open(path, "w:gz") as handle:
        handle.addfile(info, io.BytesIO(script))


def create_demo_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as handle:
        handle.writestr("demo-1.0/bin/demo", "#!/bin/sh\necho 'demo 1.0'\n")


def test_initialize_stage_install_and_verify(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    root = tmp_path / "cache"
    manager = SoftwareManager(root, catalog_path=catalog)

    manager.initialize()
    assert all((root / relative).is_dir() for relative in LAYOUT_DIRECTORIES)

    package = tmp_path / "demo-1.0.tar.gz"
    create_demo_archive(package)
    staged = manager.stage("demo", package)
    assert staged["status"] == "staged"

    installed = manager.install("demo")
    assert installed["status"] == "installed"
    assert installed["verification"]["status"] == "pass"
    assert manager.verify("demo")[0]["status"] == "pass"
    receipt = root / "receipts" / "demo" / "1.0.json"
    assert json.loads(receipt.read_text(encoding="utf-8"))["software_id"] == "demo"


def test_zip_entrypoint_is_made_executable(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    root = tmp_path / "cache"
    manager = SoftwareManager(root, catalog_path=catalog)
    manager.initialize()
    package = tmp_path / "demo-1.0.zip"
    create_demo_zip(package)

    installed = manager.install("demo", package=package)

    assert installed["verification"]["status"] == "pass"
    assert manager.verify("demo")[0]["status"] == "pass"


def test_copy_handler_creates_relative_alias(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    text = catalog.read_text(encoding="utf-8").replace(
        "      handler: archive\n      target:",
        "      handler: copy\n"
        "      target_name: demo.real\n"
        "      aliases: {bin/demo: demo.real}\n"
        "      target:",
    )
    catalog.write_text(text, encoding="utf-8")
    root = tmp_path / "cache"
    manager = SoftwareManager(root, catalog_path=catalog)
    manager.initialize()
    package = tmp_path / "demo-1.0.tar.gz"
    package.write_text("#!/bin/sh\necho 'demo 1.0'\n", encoding="utf-8")

    installed = manager.install("demo", package=package)

    alias = root / "installations/demo/1.0/linux-x86_64/bin/demo"
    assert installed["verification"]["status"] == "pass"
    assert alias.is_symlink()
    assert not alias.readlink().is_absolute()


def test_archive_rejects_path_traversal(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    root = tmp_path / "cache"
    manager = SoftwareManager(root, catalog_path=catalog)
    manager.initialize()
    archive = tmp_path / "demo-bad.tar.gz"
    info = tarfile.TarInfo("../../escape")
    info.size = 1
    with tarfile.open(archive, "w:gz") as handle:
        handle.addfile(info, io.BytesIO(b"x"))
    manager.stage("demo", archive)
    with pytest.raises(ValueError, match="escapes extraction root"):
        manager.install("demo")
    assert not (tmp_path / "escape").exists()


def test_failed_installation_verification_does_not_publish_destination(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    root = tmp_path / "cache"
    manager = SoftwareManager(root, catalog_path=catalog)
    manager.initialize()
    archive = tmp_path / "demo-invalid.tar.gz"
    script = b"#!/bin/sh\necho 'wrong version'\n"
    info = tarfile.TarInfo("demo-invalid/bin/demo")
    info.mode = 0o755
    info.size = len(script)
    with tarfile.open(archive, "w:gz") as handle:
        handle.addfile(info, io.BytesIO(script))
    manager.stage("demo", archive)

    with pytest.raises(RuntimeError, match="Installation verification failed"):
        manager.install("demo")

    assert not (root / "installations/demo/1.0/linux-x86_64").exists()


def test_manifest_rejects_absolute_installation_target(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    text = catalog.read_text(encoding="utf-8").replace(
        "installations/demo/1.0/linux-x86_64", "/tmp/demo"
    )
    catalog.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="cache-relative"):
        load_catalog(catalog)


def test_manifest_rejects_alias_path_traversal(tmp_path: Path):
    catalog = tmp_path / "catalog.yaml"
    write_catalog(catalog)
    text = catalog.read_text(encoding="utf-8").replace(
        "      handler: archive\n",
        "      handler: copy\n      aliases: {../escape: payload}\n",
    )
    catalog.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="alias path must be a cache-relative path"):
        load_catalog(catalog)


def test_legacy_migration_is_non_destructive_and_rewrites_internal_links(tmp_path: Path):
    legacy = tmp_path / "legacy"
    source = legacy / "demo" / "1.0"
    source.mkdir(parents=True)
    executable = source / "demo"
    executable.write_text("demo\n", encoding="utf-8")
    link = source / "demo-link"
    link.symlink_to(executable)
    catalog = tmp_path / "catalog.yaml"
    write_catalog(
        catalog,
        migration="""    migration:
      - source: demo/1.0
        destination: installations/demo/1.0/linux-x86_64
        role: installation
""",
    )
    destination = tmp_path / "v2"
    manager = SoftwareManager(destination, catalog_path=catalog)
    manager.initialize()
    report = migrate_legacy_cache(legacy, destination, manager.catalog.values())

    migrated = destination / "installations" / "demo" / "1.0" / "linux-x86_64"
    assert executable.read_text(encoding="utf-8") == "demo\n"
    assert (migrated / "demo").read_text(encoding="utf-8") == "demo\n"
    assert (migrated / "demo-link").is_symlink()
    assert not Path(os.readlink(migrated / "demo-link")).is_absolute()
    assert report["symlinks"]["rewritten"]


@pytest.mark.parametrize(
    ("legacy", "expected"),
    [
        ("orca/6.1.1/orca", "installations/orca/6.1.1/orca"),
        ("orca/download/orca.tar.xz", "packages/orca/download/orca.tar.xz"),
        ("goodvibes/4.3.0/source-4.3", "sources/goodvibes/4.3.0/source-4.3"),
        ("censo/smoke_prescreen3/result.out", "validation/censo/smoke_prescreen3/result.out"),
        ("demo/env/site-packages/pip/_internal/build_env/base.py", "installations/demo/env/site-packages/pip/_internal/build_env/base.py"),
        ("demo/env/site-packages/pip/_internal/operations/build/base.py", "installations/demo/env/site-packages/pip/_internal/operations/build/base.py"),
        ("charmm/50b2/install/source", "installations/charmm/50b2/install/source"),
        ("gamess/2024-r2-p1/source/rungms", "installations/gamess/2024-r2-p1/source/rungms"),
        ("gpaw/setups/PBE", "shared/scientific-data/gpaw-setups/PBE"),
        ("documentation/index.json", "documentation/index.json"),
        ("documentation_alias_fix_seed_20260720/index.json", None),
        ("gmx_mmpbsa/1.6.5/env/bin/python", None),
        ("amber/26/install/bin/amber.python", None),
        ("gamess/2024-r2-p1/failed-generation/rungms.from-root", None),
    ],
)
def test_v2_legacy_path_classification(legacy: str, expected: str | None):
    result = classify_legacy_path(legacy)
    assert (result.as_posix() if result else None) == expected


def test_v2_migration_rewrites_relative_links_across_roles(tmp_path: Path):
    legacy = tmp_path / "legacy"
    source = legacy / "demo" / "source"
    package = legacy / "demo" / "downloads"
    source.mkdir(parents=True)
    package.mkdir(parents=True)
    payload = package / "payload.dat"
    payload.write_text("payload\n", encoding="utf-8")
    script = source / "runner"
    script.write_text(
        "#!/inspire/hdd/global_user/example/.tool_envs/demo/bin/tcsh -f\necho demo\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    (source / "payload-link").symlink_to(Path("../downloads/payload.dat"))
    ignored = legacy / "easyspin"
    ignored.mkdir()
    (ignored / "ignored.dat").write_text("ignored\n", encoding="utf-8")
    airss_bin = legacy / "airss" / "0.9.3" / "bin"
    airss_payload = legacy / "airss" / "0.9.3" / "libexec" / "airss"
    airss_bin.mkdir(parents=True)
    airss_payload.mkdir(parents=True)
    (airss_payload / "buildcell").write_text("payload\n", encoding="utf-8")
    wrapper = airss_bin / "buildcell"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'exec "/inspire/hdd/global_user/example/ResearchChemBench/.software_cache/'
        'airss/0.9.3/libexec/airss/buildcell" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    pyfrag_source = legacy / "pyfrag" / "2019" / "source"
    pyfrag_source.mkdir(parents=True)
    (pyfrag_source / "pyfrag.py").write_text("pass\n", encoding="utf-8")
    rmg_state = legacy / "rmg" / "home" / ".rmg"
    rmg_state.mkdir(parents=True)
    legacy_cache = ".software_" + "cache"
    (rmg_state / "rmgrc").write_text(
        "database.directory: /inspire/hdd/global_user/example/ResearchChemBench/"
        f"{legacy_cache}/rmg/database/4.0.0/input\n",
        encoding="utf-8",
    )

    destination = tmp_path / "v2"
    report = migrate_v2(legacy, destination)
    migrated_link = destination / "sources" / "demo" / "source" / "payload-link"
    assert migrated_link.resolve() == destination / "packages" / "demo" / "downloads" / "payload.dat"
    assert not (destination / "installations" / "easyspin").exists()
    assert report["unresolved_symlinks"] == []
    assert payload.read_text(encoding="utf-8") == "payload\n"
    migrated_script = destination / "sources" / "demo" / "source" / "runner"
    assert migrated_script.read_text(encoding="utf-8").startswith(
        "#!/usr/bin/env -S tcsh -f\n"
    )
    assert script.read_text(encoding="utf-8").startswith("#!/inspire/")
    assert migrated_script.stat().st_ino != script.stat().st_ino
    migrated_wrapper = destination / "installations/airss/0.9.3/bin/buildcell"
    assert "${script_dir}/../libexec/airss/buildcell" in migrated_wrapper.read_text(
        encoding="utf-8"
    )
    assert "/inspire/hdd/global_user/" not in migrated_wrapper.read_text(encoding="utf-8")
    compatibility_link = destination / "installations/pyfrag/2019/source"
    assert compatibility_link.is_symlink()
    assert compatibility_link.resolve() == destination / "sources/pyfrag/2019/source"
    portable_rmgrc = destination / "state/rmg/home/.rmg/rmgrc"
    assert portable_rmgrc.read_text(encoding="utf-8") == (
        "database.directory: $RESEARCHCHEMBENCH_SOFTWARE_ROOT/"
        "installations/rmg/database/4.0.0/input\n"
    )


def test_gamess_relocation_uses_runtime_profile_paths_and_is_idempotent(tmp_path: Path):
    root = tmp_path / "managed-cache"
    source = root / "installations/gamess/2024-r2-p1/source"
    build = root / "build/gamess/2024-r2-p1/build"
    source.mkdir(parents=True)
    build.mkdir(parents=True)
    legacy_root = "/legacy/build-host/ResearchChemBench"
    legacy_cache = f"{legacy_root}/.software_cache/gamess/2024-r2-p1"
    (source / "rungms").write_text(
        "#!/usr/bin/env -S tcsh -f\n"
        f"source {legacy_cache}/build/install.info\n"
        f"set SCR={legacy_cache}/scratch\n"
        f"set USERSCR={legacy_cache}/restart\n"
        f"set GMSPATH={legacy_cache}/build\n",
        encoding="utf-8",
    )
    (source / "Makefile").write_text(
        f"GMS_PATH := $(shell {legacy_root}/.tool_envs/gamess/bin/tcsh "
        "-fc 'source install.info && echo $$GMS_PATH')\n",
        encoding="utf-8",
    )
    install_info = (
        "#!/usr/bin/env -S tcsh\n"
        f"setenv GMS_PATH {legacy_cache}/source\n"
        f"setenv GMS_BUILD_DIR {legacy_cache}/build\n"
        f"setenv GMS_MATHLIB_PATH {legacy_root}/.tool_envs/gamess/lib\n"
    )
    (source / "install.info").write_text(install_info, encoding="utf-8")
    (build / "install.info").symlink_to(
        os.path.relpath(source / "install.info", build)
    )

    first = relocate_v2(root)
    for path in (
        source / "rungms",
        source / "install.info",
        source / "Makefile",
        build / "install.info",
    ):
        content = path.read_text(encoding="utf-8")
        assert "/legacy/build-host/" not in content
    assert "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" in (source / "rungms").read_text(
        encoding="utf-8"
    )
    rungms = (source / "rungms").read_text(encoding="utf-8")
    assert "if ( $?GMS_SCRATCH ) set SCR=$GMS_SCRATCH" in rungms
    assert "if ( $?GMS_RESTART ) set USERSCR=$GMS_RESTART" in rungms
    assert "/validation/gamess/2024-r2-p1/scratch" not in rungms
    assert "/installations/gamess/2024-r2-p1/restart" not in rungms
    assert "$(shell tcsh -fc" in (source / "Makefile").read_text(
        encoding="utf-8"
    )
    assert "$GMS_RUNTIME_LIB" in (source / "install.info").read_text(encoding="utf-8")
    assert {item["status"] for item in first["portable_gamess_files"]} == {
        "portable_link",
        "rewritten",
    }

    second = relocate_v2(root)
    assert {item["status"] for item in second["portable_gamess_files"]} == {
        "already_portable",
        "portable_link",
    }


def test_aiida_repository_path_is_rewritten_to_project_relative(tmp_path: Path):
    root = tmp_path / "managed-cache"
    repository = root / "state/aiida/.aiida/repository/old-repository"
    repository.mkdir(parents=True)
    (repository / "database.sqlite").write_bytes(b"sqlite")
    config_path = root / "state/aiida/.aiida/config.json"
    config_path.write_text(
        json.dumps(
            {
                "profiles": {
                    "researchchembench": {
                        "storage": {
                            "backend": "core.sqlite_dos",
                            "config": {
                                "filepath": "/legacy/server/ResearchChemBench/.software_cache/"
                                "state/aiida/.aiida/repository/old-repository"
                            },
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    first = relocate_v2(root)
    assert first["aiida_config"]["status"] == "rewritten"
    rewritten = json.loads(config_path.read_text(encoding="utf-8"))
    assert rewritten["profiles"]["researchchembench"]["storage"]["config"]["filepath"] == (
        "repository/old-repository"
    )
    second = relocate_v2(root)
    assert second["aiida_config"]["status"] == "already_portable"


def test_vasp_makefile_path_is_rewritten_to_relative_environment(tmp_path: Path):
    root = tmp_path / "managed-cache"
    makefile = root / "installations/vasp/6.3.2/makefile.include"
    makefile.parent.mkdir(parents=True)
    makefile.write_text(
        "VASP_ENV = /inspire/hdd/global_user/example/ResearchChemBench/.tool_envs/vasp\n"
        "BLASPACK = -L$(VASP_ENV)/lib -lblas\n",
        encoding="utf-8",
    )

    first = relocate_v2(root)
    rewritten = makefile.read_text(encoding="utf-8")
    assert first["vasp_makefile"]["status"] == "rewritten"
    assert "/inspire/" not in rewritten
    assert "RESEARCHCHEMBENCH_ENV_ROOT" in rewritten
    assert "general-modern-openmpi5" in rewritten

    second = relocate_v2(root)
    assert second["vasp_makefile"]["status"] == "already_portable"


def test_acpype_relocation_uses_bundled_python_and_is_idempotent(tmp_path: Path):
    root = tmp_path / "managed-cache"
    launcher = root / "installations/acpype/2023.10.27/python/bin/acpype"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        "#!/bin/sh\n'''exec' /legacy/server/.envs/openff/bin/python \"$0\" \"$@\"\n' '''\n",
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    first = relocate_v2(root)
    text = launcher.read_text(encoding="utf-8")
    assert first["portable_acpype_launcher"]["status"] == "rewritten"
    assert "${install_root}/deps/bin/python" in text
    assert "BABEL_LIBDIR" in text
    assert "BABEL_DATADIR" in text
    assert "/legacy/server" not in text

    second = relocate_v2(root)
    assert second["portable_acpype_launcher"]["status"] == "already_portable"


def test_kinbot_nwchem_reaction_family_patch_is_idempotent(tmp_path: Path):
    root = tmp_path / "managed-cache"
    source = root / "installations/kinbot/source-2.2.2/kinbot/reac_family.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        "    elif rxn.qc.qc == 'nn_pes' and step >= rxn.max_step:\n"
        "        code = 'nn_pes'\n",
        encoding="utf-8",
    )

    first = relocate_v2(root)
    assert first["kinbot_nwchem_reaction_family"]["status"] == "rewritten"
    text = source.read_text(encoding="utf-8")
    assert "elif rxn.qc.qc == 'nwchem':" in text
    assert "Code = 'NWChem'" in text

    second = relocate_v2(root)
    assert second["kinbot_nwchem_reaction_family"]["status"] == "already_portable"
    assert source.read_text(encoding="utf-8") == text


def test_repository_path_rewrite_is_idempotent_and_preserves_punctuation():
    legacy_root = ".software_" + "cache"
    original = (
        f"binary={legacy_root}/orca/6.1.1/orca\n"
        "managed=.software_cache/installations/orca/6.1.1/orca\n"
        f"note={legacy_root}/amber/26.\n"
    )
    rewritten, count = rewrite_text(original)
    assert count == 3
    assert "binary=.software_cache/installations/orca/6.1.1/orca" in rewritten
    assert "managed=.software_cache/installations/orca/6.1.1/orca" in rewritten
    assert "note=.software_cache/installations/amber/26." in rewritten
    assert rewrite_text(rewritten)[0] == rewritten


def test_repository_path_rewrite_preserves_directory_trailing_slash():
    value = ".software_cache/installations/<software>/<version>/"
    rewritten, _ = rewrite_text(value)
    assert rewritten == value
