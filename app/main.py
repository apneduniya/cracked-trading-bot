import asyncio

from app.core.logging import logger

from app.providers.bot_controller import get_bot_controller

from app.services.scheduler.manager import SchedulerManager
from app.services.scheduler.launchcoin import LaunchcoinScheduler


scheduler_manager = SchedulerManager()


async def start_bot() -> None:
    bot_controller = get_bot_controller()

    logger.info("Starting bot...")
    await bot_controller.start()

    
async def start_scheduler() -> None:
    launchcoin_scheduler = LaunchcoinScheduler()

    scheduler_manager.register_scheduler(launchcoin_scheduler)


    logger.info("Creating and starting all schedules...")
    scheduler_manager.create_all_schedules()
    scheduler_manager.start_all()


async def main() -> None:
    try:
        await asyncio.gather(
            start_bot(),
            start_scheduler()
        )
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())