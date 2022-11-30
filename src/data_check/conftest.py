"""
The fixtures of Pytest for data check steps
"""
import pytest
import pandas as pd
import wandb


def pytest_addoption(parser):
    parser.addoption("--csv", action="store")
    parser.addoption("--ref", action="store")
    parser.addoption("--kl_threshold", action="store")
    parser.addoption("--min_price", action="store")
    parser.addoption("--max_price", action="store")


@pytest.fixture(scope='session')
def data(request):
    """
    Read data csv file from W&B artifact
    """
    run = wandb.init(job_type="data_tests", resume=True)

    data_path = run.use_artifact(request.config.option.csv).file()

    if data_path is None:
        pytest.fail("You must provide the --csv option on the command line")

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def ref_data(request):
    """
    Read reference data csv file from W&B artifact
    """
    run = wandb.init(job_type="data_tests", resume=True)

    data_path = run.use_artifact(request.config.option.ref).file()

    if data_path is None:
        pytest.fail("You must provide the --ref option on the command line")

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def kl_threshold(request):
    """
    Get and check KL threshold parameter
    """
    kl_threshold = request.config.option.kl_threshold

    if kl_threshold is None:
        pytest.fail("You must provide a threshold for the KL test")

    return float(kl_threshold)


@pytest.fixture(scope='session')
def min_price(request):
    """
    Get and check min_price parameter
    """
    min_price = request.config.option.min_price

    if min_price is None:
        pytest.fail("You must provide min_price")

    return float(min_price)


@pytest.fixture(scope='session')
def max_price(request):
    """
    Get and check max_price parameter
    """
    max_price = request.config.option.max_price

    if max_price is None:
        pytest.fail("You must provide max_price")

    return float(max_price)
