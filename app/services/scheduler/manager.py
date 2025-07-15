import typing as t
from app.core.logging import logger
from app.services.core.scheduler import BaseScheduler


class SchedulerManager:
    """
    Manager for all schedulers in the application
    """
    
    def __init__(self):
        self.schedulers: t.List[BaseScheduler] = []
        logger.debug("Initialized SchedulerManager")

    def register_scheduler(self, scheduler: BaseScheduler) -> None:
        """
        Register a scheduler with the manager
        
        Args:
            scheduler (BaseScheduler): Scheduler to register
        """
        self.schedulers.append(scheduler)
        logger.info(f"Registered scheduler: {scheduler.__class__.__name__}")

    def create_all_schedules(self) -> None:
        """Create schedules for all registered schedulers"""
        for scheduler in self.schedulers:
            try:
                logger.info(f"Creating schedules for {scheduler.__class__.__name__}")
                scheduler.create_schedules()
            except Exception as e:
                logger.error(f"Error creating schedules for {scheduler.__class__.__name__}: {e}")

    def start_all(self) -> None:
        """Start all registered schedulers"""
        for scheduler in self.schedulers:
            try:
                logger.info(f"Starting {scheduler.__class__.__name__}")
                scheduler.start()
            except Exception as e:
                logger.error(f"Error starting {scheduler.__class__.__name__}: {e}")

    def shutdown_all(self) -> None:
        """Shutdown all registered schedulers"""
        for scheduler in self.schedulers:
            try:
                logger.info(f"Shutting down {scheduler.__class__.__name__}")
                scheduler.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down {scheduler.__class__.__name__}: {e}")