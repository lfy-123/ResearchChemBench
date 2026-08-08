from chemistry_toolbox.scripts.normalize_pip_freeze import normalize_pip_freeze


def test_normalize_pip_freeze_removes_host_paths_and_legacy_layout() -> None:
    root = "/srv/ResearchChemBench"
    frozen = (
        "\n".join(
            (
                "-e git+ssh://git@local-alias/example/ResearchChemBench.git@abc#egg=researchchem_mcp_tools",
                f"gplearn @ file://{root}/.software_cache/gplearn/0.4.3/packages/gplearn.whl#sha256=abc",
                f"kinbot @ file://{root}/.software_cache/kinbot/source-2.2.2",
            )
        )
        + "\n"
    )

    result = normalize_pip_freeze(frozen, project_root=root)

    assert result.splitlines() == [
        "-e ${PROJECT_ROOT}",
        "gplearn @ file://${PROJECT_ROOT}/.software_cache/packages/gplearn/0.4.3/packages/gplearn.whl#sha256=abc",
        "kinbot @ file://${PROJECT_ROOT}/.software_cache/installations/kinbot/source-2.2.2",
    ]


def test_normalize_pip_freeze_updates_obsolete_local_editable_path() -> None:
    assert (
        normalize_pip_freeze(
            "-e /srv/ResearchChemBench/chemistry_toolbox\n",
            project_root="/srv/ResearchChemBench",
        )
        == "-e ${PROJECT_ROOT}\n"
    )
