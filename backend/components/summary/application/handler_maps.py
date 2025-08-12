from components.summary.application.summary_service import SummaryService
from components.summary.domain import commands

COMMAND_HANDLER_MAPS = {
    commands.SaveSummary: SummaryService.save_summary,
    commands.UpdateSummary: SummaryService.update_summary,
    commands.DeleteSummary: SummaryService.delete_summary,
}

EVENT_HANDLER_MAPS = {}
