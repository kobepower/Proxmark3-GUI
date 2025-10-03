#!/usr/bin/env python3
"""
🧠 PM3 Command Parser - Dynamic Command Discovery
Automatically discovers and parses PM3 commands from help output
Makes the GUI future-proof against firmware updates
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field

logger = logging.getLogger('CyberNinjaRFID')

@dataclass
class PM3Command:
    """Represents a single PM3 command"""
    name: str
    category: str
    description: str = ""
    usage: str = ""
    examples: List[str] = field(default_factory=list)
    subcommands: List[str] = field(default_factory=list)

class PM3CommandParser:
    """
    Dynamically parses PM3 commands from help output
    Future-proof against firmware updates
    """

    def __init__(self, pm3_device=None):
        self.pm3_device = pm3_device
        self.commands = {}
        self.categories = {}

    def parse_help_output(self, help_text: str) -> Dict[str, PM3Command]:
        """
        Parse 'help' output to discover available commands
        """
        commands = {}

        # Split into lines
        lines = help_text.split('\n')

        current_category = "general"

        for line in lines:
            line = line.strip()

            # Detect category headers (e.g., "High Frequency commands:")
            if any(keyword in line.lower() for keyword in ['commands:', 'category:', 'module:']):
                # Extract category name
                match = re.search(r'([\w\s]+)\s*commands?:', line, re.IGNORECASE)
                if match:
                    current_category = match.group(1).strip().lower()
                    if current_category not in self.categories:
                        self.categories[current_category] = []
                continue

            # Parse command lines (format: "command -- description" or "command - description")
            if '--' in line or (len(line) > 3 and line[0].isalpha() and ' - ' in line):
                parts = re.split(r'\s+(?:--|-)\s+', line, 1)
                if len(parts) == 2:
                    cmd_name = parts[0].strip()
                    description = parts[1].strip()

                    # Create command object
                    cmd = PM3Command(
                        name=cmd_name,
                        category=current_category,
                        description=description
                    )

                    commands[cmd_name] = cmd

                    # Add to category
                    if current_category in self.categories:
                        self.categories[current_category].append(cmd_name)
                    else:
                        self.categories[current_category] = [cmd_name]

        self.commands = commands
        logger.info(f"📚 Discovered {len(commands)} commands across {len(self.categories)} categories")
        return commands

    def parse_module_help(self, module: str, help_text: str) -> List[PM3Command]:
        """
        Parse module-specific help (e.g., 'hf help', 'lf help')
        """
        commands = []
        lines = help_text.split('\n')

        for line in lines:
            line = line.strip()

            # Look for command patterns
            if line.startswith(module):
                # Extract command and description
                match = re.match(rf'{module}\s+([\w\s]+?)\s+(?:--|-)\s+(.+)', line)
                if match:
                    subcmd = match.group(1).strip()
                    desc = match.group(2).strip()

                    cmd = PM3Command(
                        name=f"{module} {subcmd}",
                        category=module,
                        description=desc
                    )
                    commands.append(cmd)

        logger.info(f"📚 Discovered {len(commands)} commands in '{module}' module")
        return commands

    def discover_all_commands(self) -> Dict[str, PM3Command]:
        """
        Discover ALL commands by querying PM3 help system
        """
        if not self.pm3_device:
            logger.warning("⚠️ No PM3 device connected, can't discover commands")
            return {}

        all_commands = {}

        try:
            # Get main help
            self.pm3_device.console("help", capture=True, quiet=True)
            help_output = self.pm3_device.grabbed_output
            main_commands = self.parse_help_output(help_output)
            all_commands.update(main_commands)

            # Discover module-specific commands
            modules = ['hf', 'lf', 'hw', 'data', 'trace', 'mem', 'smart', 'script']

            for module in modules:
                try:
                    self.pm3_device.console(f"{module} help", capture=True, quiet=True)
                    module_help = self.pm3_device.grabbed_output

                    module_commands = self.parse_module_help(module, module_help)
                    for cmd in module_commands:
                        all_commands[cmd.name] = cmd

                except Exception as e:
                    logger.debug(f"Could not parse '{module}' help: {e}")

            self.commands = all_commands
            logger.info(f"🎯 Total commands discovered: {len(all_commands)}")

        except Exception as e:
            logger.error(f"Error discovering commands: {e}")

        return all_commands

    def get_commands_by_category(self, category: str) -> List[PM3Command]:
        """Get all commands in a category"""
        if category in self.categories:
            return [self.commands[cmd] for cmd in self.categories[category] if cmd in self.commands]
        return []

    def search_commands(self, query: str) -> List[PM3Command]:
        """Search commands by name or description"""
        query = query.lower()
        results = []

        for cmd in self.commands.values():
            if query in cmd.name.lower() or query in cmd.description.lower():
                results.append(cmd)

        return results

    def save_commands_cache(self, filepath: Path):
        """Save discovered commands to cache file"""
        try:
            cache_data = {
                'commands': {
                    name: {
                        'name': cmd.name,
                        'category': cmd.category,
                        'description': cmd.description,
                        'usage': cmd.usage,
                        'examples': cmd.examples,
                        'subcommands': cmd.subcommands,
                    }
                    for name, cmd in self.commands.items()
                },
                'categories': self.categories,
            }

            with open(filepath, 'w') as f:
                json.dump(cache_data, f, indent=2)

            logger.info(f"💾 Saved command cache to {filepath}")

        except Exception as e:
            logger.error(f"Error saving command cache: {e}")

    def load_commands_cache(self, filepath: Path) -> bool:
        """Load commands from cache file"""
        try:
            if not filepath.exists():
                return False

            with open(filepath, 'r') as f:
                cache_data = json.load(f)

            # Reconstruct commands
            self.commands = {}
            for name, data in cache_data.get('commands', {}).items():
                self.commands[name] = PM3Command(
                    name=data['name'],
                    category=data['category'],
                    description=data.get('description', ''),
                    usage=data.get('usage', ''),
                    examples=data.get('examples', []),
                    subcommands=data.get('subcommands', []),
                )

            self.categories = cache_data.get('categories', {})

            logger.info(f"📂 Loaded {len(self.commands)} commands from cache")
            return True

        except Exception as e:
            logger.error(f"Error loading command cache: {e}")
            return False

    def get_smart_suggestions(self, partial_command: str) -> List[str]:
        """Get command suggestions based on partial input"""
        partial = partial_command.lower().strip()

        if not partial:
            return []

        suggestions = []

        # Exact prefix match
        for cmd_name in self.commands.keys():
            if cmd_name.lower().startswith(partial):
                suggestions.append(cmd_name)

        # If no prefix matches, try substring
        if not suggestions:
            for cmd_name in self.commands.keys():
                if partial in cmd_name.lower():
                    suggestions.append(cmd_name)

        return sorted(suggestions)[:10]  # Top 10 suggestions

    def load_command_profiles(self, filepath: Path) -> Dict[str, str]:
        """
        Load command profiles/presets from JSON/YAML file
        Format: {"Profile Name": "pm3 command"}
        """
        try:
            if not filepath.exists():
                logger.warning(f"Profile file not found: {filepath}")
                return {}

            with open(filepath, 'r') as f:
                profiles = json.load(f)

            logger.info(f"📋 Loaded {len(profiles)} command profiles")
            return profiles

        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
            return {}

    def save_command_profiles(self, profiles: Dict[str, str], filepath: Path):
        """Save command profiles to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(profiles, f, indent=2)

            logger.info(f"💾 Saved {len(profiles)} profiles to {filepath}")

        except Exception as e:
            logger.error(f"Error saving profiles: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Test with sample help output
    sample_help = """
    Help text
    =========

    General commands:
    help -- This text
    quit -- Exit program
    exit -- Exit program

    High Frequency commands:
    hf search -- Search for HF tags
    hf 14a reader -- Read ISO14443A tag
    hf 14a info -- Get tag information

    Low Frequency commands:
    lf search -- Search for LF tags
    lf em 410x reader -- Read EM410x tag
    lf t55xx detect -- Detect T55xx tag
    """

    parser = PM3CommandParser()
    commands = parser.parse_help_output(sample_help)

    print(f"\n📚 Discovered {len(commands)} commands:")
    for name, cmd in commands.items():
        print(f"  {name:20} [{cmd.category:15}] - {cmd.description}")

    print(f"\n📁 Categories: {list(parser.categories.keys())}")

    # Test search
    print(f"\n🔍 Search 'read':")
    results = parser.search_commands('read')
    for cmd in results:
        print(f"  {cmd.name} - {cmd.description}")

    # Test suggestions
    print(f"\n💡 Suggestions for 'hf 14':")
    suggestions = parser.get_smart_suggestions('hf 14')
    for sug in suggestions:
        print(f"  {sug}")
