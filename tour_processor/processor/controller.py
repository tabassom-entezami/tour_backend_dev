import logging

from nameko_sqlalchemy import Database

from tour_shared import models
from tour_shared.middlewares import Middleware, translation_middleware

from processor.repositories import ProcessorRepository
from processor.services import ProcessorService

_logger = logging.getLogger(__name__)
dummy_ai = {}


class ProcessorController(metaclass=Middleware):
    name = 'processor'

    db = Database(models.DeclarativeBase, engine_options={'pool_pre_ping': True})

    middlewares = [translation_middleware]

    def _get_service(self, access_info):
        repo = ProcessorRepository(db_session=self.db.session)
        return ProcessorService(access_info, repo)
