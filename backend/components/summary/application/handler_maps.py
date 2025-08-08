from components.summary.domain import commands
from components.summary.application.summary_service import SummaryService

COMMAND_HANDLER_MAPS = {
    commands.SaveSummary: SummaryService.save_summary,
    commands.UpdateSummary: SummaryService.update_summary,
    commands.DeleteSummary: SummaryService.delete_summary,
}

EVENT_HANDLER_MAPS = {}
