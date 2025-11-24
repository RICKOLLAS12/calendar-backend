"""
Management command to view and analyze application logs.
Usage: python manage.py view_logs [--type=TYPE] [--lines=N] [--grep=PATTERN]
"""
import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'View and analyze application logs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['django', 'api', 'security', 'errors', 'all'],
            default='all',
            help='Type of logs to view (default: all)'
        )
        parser.add_argument(
            '--lines',
            type=int,
            default=50,
            help='Number of lines to display (default: 50)'
        )
        parser.add_argument(
            '--grep',
            type=str,
            help='Filter logs containing this pattern'
        )
        parser.add_argument(
            '--tail',
            action='store_true',
            help='Show the last N lines (like tail command)'
        )

    def handle(self, *args, **options):
        log_type = options['type']
        lines = options['lines']
        grep_pattern = options['grep']
        tail_mode = options['tail']

        logs_dir = Path(settings.BASE_DIR) / 'logs'

        if not logs_dir.exists():
            raise CommandError(f"Logs directory does not exist: {logs_dir}")

        log_files = self._get_log_files(logs_dir, log_type)

        if not log_files:
            self.stdout.write(self.style.WARNING(f"No log files found for type: {log_type}"))
            return

        for log_file in log_files:
            self._display_log_file(log_file, lines, grep_pattern, tail_mode)

    def _get_log_files(self, logs_dir, log_type):
        """Get list of log files based on type"""
        file_mapping = {
            'django': ['django.log'],
            'api': ['api.log'],
            'security': ['security.log'],
            'errors': ['errors.log'],
            'all': ['django.log', 'api.log', 'security.log', 'errors.log']
        }

        files = file_mapping.get(log_type, [])
        return [logs_dir / f for f in files if (logs_dir / f).exists()]

    def _display_log_file(self, log_file, lines, grep_pattern, tail_mode):
        """Display contents of a log file"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Apply filters
            if grep_pattern:
                content = [line for line in content if re.search(grep_pattern, line, re.IGNORECASE)]

            if tail_mode:
                content = content[-lines:]
            else:
                content = content[-lines:]

            if not content:
                self.stdout.write(self.style.WARNING(f"No matching lines in {log_file.name}"))
                return

            # Display header
            self.stdout.write(self.style.SUCCESS(f"\n=== {log_file.name} ==="))

            # Display content
            for line in content:
                # Colorize based on log level
                if 'ERROR' in line:
                    self.stdout.write(self.style.ERROR(line.rstrip()))
                elif 'WARNING' in line:
                    self.stdout.write(self.style.WARNING(line.rstrip()))
                elif 'INFO' in line:
                    self.stdout.write(self.style.SUCCESS(line.rstrip()))
                else:
                    self.stdout.write(line.rstrip())

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Log file not found: {log_file}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading {log_file}: {e}"))