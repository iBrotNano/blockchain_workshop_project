from project.project import Project


def test_init_sets_project_path(tmp_path):
    project = Project(tmp_path)
    assert project.project_path == tmp_path
    assert project.get_project_path() == tmp_path


def test_init_initializes_files_empty_list(tmp_path):
    project = Project(tmp_path)
    assert project.files == []
    assert project.get_files() == []


# TODO: Add missing tests
