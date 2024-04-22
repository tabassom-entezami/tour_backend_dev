import abc

from nameko_sqlalchemy.database import Session


class BaseStore(abc.ABC):
    @abc.abstractmethod
    def enter(self):
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self):
        raise NotImplementedError


class SQLAlchemyStore(BaseStore):
    def __init__(self, session: Session):
        self._session = session

        self._in_transaction = False
        self._started_transaction = False

    @property
    def session(self):
        if self._in_transaction and not self._started_transaction:
            self._session.__enter__()
            self._started_transaction = True
        return self._session

    def enter(self):
        self._in_transaction = True

    def exit(self, exc_type, exc_val, exc_tb):
        if self._started_transaction:
            self._session.__exit__(exc_type, exc_val, exc_tb)
            self._started_transaction = False

    def flush(self):
        return self._session.flush()


class BaseStoreRepository:
    def __init__(self):
        self._stores = []
        self._depth = 0
        self._in_transaction = False

    def __enter__(self):
        if self._depth == 0:
            self._in_transaction = True

            for store in self._stores:
                store.enter()

        self._depth += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._depth -= 1

        if self._depth == 0:
            self._in_transaction = False

            for store in self._stores:
                store.exit(exc_type, exc_val, exc_tb)

    def flush(self):
        for store in self._stores:
            store.flush()
