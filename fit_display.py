"""
FIT File Display Constants and Utilities

Shared display mappings for FIT workout files.
Used by both Mac and Windows uploaders for consistent UI.
"""

# Colors for sport type badges (hex colors)
SPORT_COLORS = {
    'running': '#22c55e',
    'cycling': '#f97316',
    'swimming': '#3b82f6',
    'strength_training': '#ef4444',
    'training': '#8b5cf6',
    'walking': '#84cc16',
    'hiking': '#a3e635',
    'fitness_equipment': '#06b6d4',  # Cyan for cardio/HIIT
}

# Human-readable display names for FIT sport types
SPORT_DISPLAY_NAMES = {
    'fitness_equipment': 'Cardio',
    'training': 'Strength',
    'running': 'Running',
    'cycling': 'Cycling',
    'swimming': 'Swimming',
    'walking': 'Walking',
    'hiking': 'Hiking',
}

# Human-readable display names for FIT sub_sport types
SUB_SPORT_DISPLAY_NAMES = {
    'strength_training': 'Strength',
    'generic': None,  # Use sport name instead
    'cardio_training': 'Cardio',
    'hiit': 'HIIT',
    'indoor_cycling': 'Indoor Cycling',
    'indoor_running': 'Treadmill',
    'lap_swimming': 'Lap Swimming',
    'open_water': 'Open Water',
}

# Default color for unknown sport types
DEFAULT_SPORT_COLOR = '#6b7280'


def get_sport_display(sport, sub_sport=None):
    """
    Get the display name for a sport/sub_sport combination.

    Args:
        sport: The FIT sport type string (e.g., 'fitness_equipment', 'training')
        sub_sport: Optional FIT sub_sport type string (e.g., 'strength_training', 'generic')

    Returns:
        Human-readable display name string
    """
    # Prefer sub_sport if it has a meaningful display name
    if sub_sport and sub_sport in SUB_SPORT_DISPLAY_NAMES:
        display = SUB_SPORT_DISPLAY_NAMES[sub_sport]
        if display is not None:
            return display

    # Check if sub_sport is not generic and not in our mapping - use it as-is
    if sub_sport and sub_sport != 'generic' and sub_sport not in SUB_SPORT_DISPLAY_NAMES:
        return sub_sport.replace('_', ' ').title()

    # Fall back to sport display name
    if sport in SPORT_DISPLAY_NAMES:
        return SPORT_DISPLAY_NAMES[sport]

    # Last resort - format the sport string
    return sport.replace('_', ' ').title() if sport else 'Workout'


def get_sport_color(sport, sub_sport=None):
    """
    Get the badge color for a sport/sub_sport combination.

    Args:
        sport: The FIT sport type string
        sub_sport: Optional FIT sub_sport type string

    Returns:
        Hex color string (e.g., '#22c55e')
    """
    # Use sub_sport color if it's strength training
    if sub_sport == 'strength_training':
        return SPORT_COLORS.get('strength_training', DEFAULT_SPORT_COLOR)

    # Use sport color
    return SPORT_COLORS.get(sport, DEFAULT_SPORT_COLOR)


def format_duration(seconds):
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds (int or float)

    Returns:
        Formatted string like "1:30" or "45s"
    """
    if not seconds or seconds <= 0:
        return ""

    seconds = int(seconds)
    if seconds >= 3600:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}:{mins:02d}:00"
    elif seconds >= 60:
        mins = seconds // 60
        secs = seconds % 60
        if secs > 0:
            return f"{mins}:{secs:02d}"
        return f"{mins} min"
    else:
        return f"{seconds}s"


def format_reps(reps):
    """
    Format reps value to display string.

    Args:
        reps: Rep count (int) or string like "8-12"

    Returns:
        Formatted string like "10 reps" or "8-12 reps"
    """
    if not reps:
        return ""
    return f"{reps} reps" if isinstance(reps, int) else f"{reps} reps"


def format_distance(meters):
    """
    Format distance in meters to human-readable string.

    Args:
        meters: Distance in meters (int or float)

    Returns:
        Formatted string like "500m" or "1.5km"
    """
    if not meters or meters <= 0:
        return ""

    if meters >= 1000:
        km = meters / 1000
        if km == int(km):
            return f"{int(km)}km"
        return f"{km:.1f}km"
    return f"{int(meters)}m"
