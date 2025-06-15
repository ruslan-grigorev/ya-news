import pytest


from engine_class import Engine


@pytest.fixture(scope='session')
def engine():
    return Engine()

@pytest.fixture(autouse=True)
def start_engine(engine):
    engine.is_running = True  # Запустим двигатель.
    yield  # В этот момент начинает выполняться тест.
    engine.is_running = False  # Заглушим двигатель.
