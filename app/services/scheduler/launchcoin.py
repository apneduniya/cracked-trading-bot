import typing as t
from datetime import datetime

from app.core.logging import logger
from app.core.config import config
from app.services.core.scheduler import BaseScheduler
from app.services.scheduler.jobs.launchcoin import create_launchcoin_background_job
from app.static.default import LAUNCHCOIN_USERNAME


class LaunchcoinScheduler(BaseScheduler):
    """
    Scheduler specifically for fetching creator details who launch their token on believe.
    """
    interval: int = config.LAUNCHCOIN_SCHEDULER_INTERVAL
    
    def __init__(self):
        super().__init__()
        self.username: str = LAUNCHCOIN_USERNAME
        logger.debug("Initialized LaunchcoinScheduler")

    def create_schedules(self) -> None:
        """Create schedules for all registered resource hubs"""
        logger.info(f"Creating schedule for {self.username} with interval {self.interval} seconds")

        self.add_job(
            func=create_launchcoin_background_job,
            args=[self. username],
            trigger='interval',
            seconds=self.interval,
            next_run_time=datetime.now() if config.LAUNCHCOIN_SCHEDULER_RUN_ON_STARTUP else None
        ) 