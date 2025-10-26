# engine/orchestrator.py

import time
import schedule

# Import agent classes
from agents.portfolio_manager import PortfolioManagerAgent
from agents.capital_allocator import CapitalAllocatorAgent
from agents.meta_mind import MetaMindAgent

class Orchestrator:
    """The main scheduler and entry point for the autonomous operation."""

    def __init__(self):
        print("Initializing Orchestrator and Agents...")
        self.portfolio_manager = PortfolioManagerAgent()
        self.capital_allocator = CapitalAllocatorAgent()
        self.meta_mind = MetaMindAgent()
        self.day_counter = 0

    def setup_schedules(self):
        print("Setting up agent schedules...")
        # Meta-learning loop is the fastest
        schedule.every().hour.do(self.meta_mind.observe_system_performance)
        schedule.every().day.at("01:00").do(self.run_daily_tasks)

        # Business loops run on slower cadences
        schedule.every().monday.at("02:00").do(self.run_weekly_tasks)
        # Using a counter for monthly and quarterly for simulation purposes

    def run_daily_tasks(self):
        print(f"\n==================== DAY {self.day_counter} ====================")
        self.day_counter += 1
        experiment_id = self.meta_mind.orient_and_hypothesize()
        self.meta_mind.run_experiment(experiment_id)

        if self.day_counter % 30 == 0:
            self.run_monthly_tasks()
        if self.day_counter % 90 == 0:
            self.run_quarterly_tasks()

    def run_weekly_tasks(self):
        self.portfolio_manager.evaluate_new_ideas()

    def run_monthly_tasks(self):
        self.capital_allocator.allocate_monthly_profits()

    def run_quarterly_tasks(self):
        self.portfolio_manager.review_portfolio_performance()

    def run(self):
        print("Autonomous Operation is now LIVE.")
        self.setup_schedules()
        # Run one cycle immediately for demonstration
        self.run_daily_tasks()
        self.run_weekly_tasks()

        # Main loop
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    # In a real system, this would likely be a long-running daemon.
    # For this scaffold, we will just run one full cycle of tasks to demonstrate.
    print("--- Running a single demonstration cycle --- ")
    orchestrator.run_daily_tasks()
    orchestrator.run_weekly_tasks()
    orchestrator.run_monthly_tasks()
    orchestrator.run_quarterly_tasks()
    print("\n--- Demonstration cycle complete. --- ")
    print("To run as a service, you would call orchestrator.run()")
