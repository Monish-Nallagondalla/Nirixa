---
name: calendar-scheduler
description: Convert actionable tasks, writing slots, and career milestones from My-OS thoughts into Google Calendar events.
---

# Calendar Scheduler Skill (`calendar-scheduler`)

Use this skill whenever the user says "add this to my calendar", "schedule this task", or when a sparring session produces clear actionable follow-ups.

## Instructions

1. **Extract Actionable Task Details**:
   - Title (e.g., "Draft LinkedIn Post: Moving from Execution to Ownership")
   - Date & Time (e.g., Tomorrow at 10:00 AM)
   - Duration (Default: 30-45 minutes)

2. **Generate Event / iCal Sync**:
   Execute the calendar sync script:
   ```bash
   python system/scripts/calendar_sync.py "Task Title" "YYYY-MM-DD HH:MM" 45
   ```

3. **Confirm Event Creation**:
   Provide the `.ics` event file link to the user and remind them that opening the file instantly syncs the event to Google Calendar / Outlook / Apple Calendar.
