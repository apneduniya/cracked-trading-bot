import typing as t
from abc import ABC, abstractmethod
from datetime import datetime

from app.core.logging import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class BaseScheduler(ABC):
    """
    Abstract base class for all schedulers
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def create_schedules(self) -> None:
        """Create all necessary schedules"""
        pass

    def start(self) -> None:
        """Start the scheduler"""
        logger.info(f"Starting {self.__class__.__name__}")
        self.scheduler.start()

    def shutdown(self) -> None:
        """Shutdown the scheduler"""
        logger.info(f"Shutting down {self.__class__.__name__}")
        self.scheduler.shutdown()

    def add_job(self, func: t.Callable, args: t.List = None, trigger: str = 'interval', 
                seconds: int = None, next_run_time: datetime = None) -> None:
        """
        Add a job to the scheduler
        
        Args:
            func (Callable): Function to schedule
            args (List, optional): Arguments for the function. Defaults to None.
            trigger (str, optional): Trigger type. Defaults to 'interval'.
            seconds (int, optional): Interval in seconds. Defaults to None.
            next_run_time (datetime, optional): When to run next. Defaults to None.
        """
        logger.info(f"Adding job for {func.__name__} with trigger {trigger}")
        self.scheduler.add_job(
            func=func,
            args=args,
            trigger=trigger,
            seconds=seconds,
            next_run_time=next_run_time
        ) 