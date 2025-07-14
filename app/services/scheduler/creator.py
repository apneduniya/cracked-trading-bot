import typing as t
from datetime import datetime

from tinydb import TinyDB

from app.core.logging import logger
from app.core.config import config
from app.models.creators import TokenCreatorDetails
from app.services.core.scheduler import BaseScheduler
from app.services.scheduler.jobs.creator import create_creator_background_job
from app.static.default import CREATORS_DATABASE_FILE   


class CreatorScheduler(BaseScheduler):
    """
    Scheduler specifically for fetching creator's posts who launch their token on believe.
    """
    interval: int = 60 * 5 # 5 minutes
    
    def __init__(self):
        super().__init__()
        self.db = TinyDB(CREATORS_DATABASE_FILE)
        logger.info("Initialized CreatorScheduler")

    def get_token_creators(self) -> t.Optional[t.List[TokenCreatorDetails]]:
        """Get all token creators from database"""
        data = self.db.all() if self.db.all() else None
        if data:
            return [TokenCreatorDetails(**tc) for tc in data]
        return None

    def create_schedules(self) -> None:
        """Create schedules for all registered resource hubs"""
        logger.info(f"Creating schedule for creator's posts analysis with interval {self.interval} seconds")

        token_creators = self.get_token_creators()
        if not token_creators:
            logger.info("No token creators found")
            return
        
        usernames = [tc.username for tc in token_creators]
        
        self.add_job(
            func=create_creator_background_job,
            args=[usernames],
            trigger='interval',
            seconds=self.interval,
            next_run_time=datetime.now() if config.CREATOR_SCHEDULER_RUN_ON_STARTUP else None
        )
