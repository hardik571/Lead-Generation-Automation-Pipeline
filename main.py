"""
Lead Generation Automation — Main Entry Point
==============================================
Usage:
    # Run once and export to Excel
    python main.py

    # Run once with a specific email prefix
    python main.py --prefix info

    # Start the scheduler (runs every 24h by default)
    python main.py --schedule

    # Start scheduler, run every 6 hours
    python main.py --schedule --interval 6
"""

import argparse
from save_leads import save_leads_to_excel
from scheduler import start_scheduler


def main():
    parser = argparse.ArgumentParser(
        description="Lead Generation Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run in scheduler mode (continuous, recurring scrapes)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=24,
        help="Hours between scheduled runs (default: 24, only used with --schedule)"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="contact",
        choices=["contact", "info", "hello", "support", "sales"],
        help="Email prefix for guessing (default: contact)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Output directory for Excel files (default: current directory)"
    )

    args = parser.parse_args()

    if args.schedule:
        print(f"Starting scheduler — running every {args.interval} hour(s).")
        start_scheduler(interval_hours=args.interval)
    else:
        print("Running one-time lead generation...")
        filepath = save_leads_to_excel(output_dir=args.output, prefix=args.prefix)
        if filepath:
            print(f"\nDone! Leads saved to: {filepath}")
        else:
            print("\nNo leads were collected.")


if __name__ == "__main__":
    main()
