"""
scanner/score.py — Security score calculator

Calculates a security score from 0 to 100 based on the findings
returned by the ScanEngine.

Scoring logic:
- Each check has a weight (how much it impacts the score)
- Critical findings have the highest negative impact
- Medium findings have a moderate impact
- Low findings have a small impact
- Info/pass findings do not reduce the score

Score interpretation:
- 90-100: Excellent
- 70-89:  Good
- 50-69:  Fair
- 30-49:  Poor
- 0-29:   Critical
"""


class ScoreCalculator:
    """
    Calculates a 0-100 security score from a list of findings.
    
    Example usage:
        calculator = ScoreCalculator(findings)
        score = calculator.calculate_score()
        label = calculator.get_score_label(score)
    """

    # Weight of each severity level on the score
    # Higher weight = bigger negative impact on score
    SEVERITY_WEIGHTS = {
        "critical": 25,
        "medium": 10,
        "low": 5,
        "info": 0
    }

    def __init__(self, findings: list):
        """
        Initialize the calculator with a list of findings.
        
        Args:
            findings: list of finding dicts returned by ScanEngine.run_scan()
        """
        self.findings = findings

    def calculate_score(self) -> int:
        """
        Calculate the security score from 0 to 100.
        
        Logic:
        - Start at 100
        - For each failed check, subtract points based on severity
        - Score cannot go below 0
        
        Returns:
            integer score between 0 and 100
        """
        score = 100

        for finding in self.findings:
            # Only penalize failed checks
            if finding.get("status") == "fail":
                severity = finding.get("severity", "low")
                penalty = self.SEVERITY_WEIGHTS.get(severity, 0)
                score -= penalty

        # Score cannot be negative
        return max(0, score)

    def get_severity_counts(self) -> dict:
        """
        Count findings by severity level.
        
        Returns:
            dict with counts for each severity:
            { "critical": 2, "medium": 3, "low": 1, "info": 4 }
        """
        counts = {
            "critical": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        for finding in self.findings:
            if finding.get("status") == "fail":
                severity = finding.get("severity", "low")
                if severity in counts:
                    counts[severity] += 1

        return counts

    def get_score_label(self, score: int) -> str:
        """
        Return a human-readable label for a given score.
        
        Args:
            score: integer between 0 and 100
            
        Returns:
            label string: "Excellent", "Good", "Fair", "Poor" or "Critical"
        """
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        elif score >= 30:
            return "Poor"
        else:
            return "Critical"