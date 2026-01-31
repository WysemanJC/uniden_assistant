"""Parser for Uniden scanner database files (.hpd, .cfg format)."""
from decimal import Decimal
from typing import Dict, List, Any


class UnidenFileParser:
    """Parses Uniden scanner database files in .hpd/.cfg tab-separated format."""

    def __init__(self):
        self.encoding = 'utf-8'

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a Uniden .hpd or .cfg file.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Dictionary containing parsed data
        """
        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                content = f.read()
            return self.parse_content(content)
        except Exception as e:
            return {'error': str(e)}

    def parse_content(self, content: str) -> Dict[str, Any]:
        """Parse file content string."""
        lines = content.strip().split('\n')
        data = {
            'frequencies': [],
            'metadata': {}
        }

        for line in lines:
            if not line.strip() or line.startswith(';'):
                continue

            parts = line.split('\t')
            if len(parts) >= 4:
                try:
                    freq_data = self._parse_frequency_line(parts)
                    if freq_data:
                        data['frequencies'].append(freq_data)
                except Exception:
                    continue

        return data

    def _parse_frequency_line(self, parts: List[str]) -> Dict[str, Any]:
        """Parse a single frequency line."""
        if len(parts) < 4:
            return None

        try:
            return {
                'frequency': Decimal(parts[0]),
                'name': parts[1].strip(),
                'modulation': parts[2].strip().upper(),
                'description': parts[3].strip() if len(parts) > 3 else '',
            }
        except (ValueError, IndexError):
            return None

    def export_to_file(self, frequencies: List[Dict], output_path: str) -> bool:
        """Export frequencies to Uniden format file."""
        try:
            with open(output_path, 'w', encoding=self.encoding) as f:
                for freq in frequencies:
                    line = '\t'.join([
                        str(freq.get('frequency', '')),
                        freq.get('name', ''),
                        freq.get('modulation', 'FM'),
                        freq.get('description', '')
                    ])
                    f.write(line + '\n')
            return True
        except Exception:
            return False
