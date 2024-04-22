from nameko_sqlalchemy.database import Session

from tour_shared.repositories import SQLAlchemyStore, BaseStoreRepository


class ProcessorRepository(BaseStoreRepository):
    def __init__(self, db_session: Session):
        super().__init__()
        self._sqlalchemy_store = SQLAlchemyStore(db_session)

        self._stores = [self._sqlalchemy_store]
