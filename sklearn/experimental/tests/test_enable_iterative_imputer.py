"""Tests for making sure experimental imports work as expected."""

import textwrap

import pytest

from sklearn.utils import _IS_WASM
from sklearn.utils._testing import assert_run_python_script_without_output


@pytest.mark.xfail(_IS_WASM, reason="cannot start subprocess")
def test_imports_strategies():
    # Make sure different import strategies work or fail as expected.

    # Since Python caches the imported modules, we need to run a child process
    # for every test case. Else, the tests would not be independent
    # (manually removing the imports from the cache (sys.modules) is not
    # recommended and can lead to many complications).
    pattern = "IterativeImputer is experimental"
    good_import = """
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    """
    assert_run_python_script_without_output(
        textwrap.dedent(good_import), pattern=pattern
    )

    good_import_with_ensemble_first = """
    import sklearn.ensemble
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    """
    assert_run_python_script_without_output(
        textwrap.dedent(good_import_with_ensemble_first),
        pattern=pattern,
    )

    bad_imports = f"""
    import pytest

    with pytest.raises(ImportError, match={pattern!r}):
        from sklearn.impute import IterativeImputer

    import sklearn.experimental
    with pytest.raises(ImportError, match={pattern!r}):
        from sklearn.impute import IterativeImputer
    """
    assert_run_python_script_without_output(
        textwrap.dedent(bad_imports),
        pattern=pattern,
    )