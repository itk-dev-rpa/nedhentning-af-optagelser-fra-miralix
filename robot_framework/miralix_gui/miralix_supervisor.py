'''A module for navigating the Supervisor section of Miralix'''

import time
from datetime import datetime, timedelta
import uiautomation as auto


def navigate_to_call_list(window: auto.WindowControl):
    window.ButtonControl().GetInvokePattern().Invoke()
    window.MenuItemControl().GetInvokePattern().Invoke()

    supervisor_window = auto.WindowControl(Name = "OfficeTeam Supervisor", searchDepth=1)
    if not supervisor_window.Exists(10, 1):
        print("supervisor window not found")

    # Open Køopkald
    henvendelser_button = supervisor_window.RadioButtonControl(AutomationId = "CallsNavButton")
    for _ in range(10):
        if henvendelser_button.IsEnabled == 1:
            break
        time.sleep(1)
    else:
        raise TimeoutError("Henvendelser was never enabled")
    henvendelser_button.GetSelectionItemPattern().Select()
    supervisor_window.RadioButtonControl(AutomationId = "CallsNavQueueCalls").Click(simulateMove=False)


def search_for_calls(target_queue: str, supervisor_window: auto.WindowControl):
    supervisor_window.CheckBoxControl(Name = "Optaget").DoubleClick(simulateMove=False)

    date_fields_id = "PART_TextBox"
    from_date_field = supervisor_window.EditControl(AutomationId=date_fields_id, foundIndex=1)
    from_date = datetime.now() - timedelta(days=14)
    from_date_field.GetValuePattern().SetValue(from_date.strftime("day %d-%m-%Y %H:%M"))
    show_button = supervisor_window.ButtonControl(Name = "Vis")
    show_button.GetInvokePattern().Invoke()

    time.sleep(2)
    supervisor_window.ProgressBarControl().Disappears(30)

    call_queue = supervisor_window.EditControl(AutomationId="PART_EditableTextBox")
    call_queue.SendKeys("{ctrl}a{delete}{back}")
    call_queue.SendKeys(target_queue, 0.1)
    show_button.GetInvokePattern().Invoke()


def iterate_through_calls(supervisor_window: auto.WindowControl):
    grid = supervisor_window.DataGridControl(AutomationID="QueueCallDataGrid")
    for i in range(grid.GetGridPattern().RowCount):
        data_row = grid.DataItemControl(foundIndex=i+1)
        download_audio_file(data_row, 'c:root_lol')


def download_audio_file(data_row: auto.DataItemControl, save_dir: str) -> str:
    '''Download an audio file'''
    data_row.DoubleClick(simulateMove=False)
    context = auto.WindowControl(AutomationId="ThisWindow")
    save_button = context.ButtonControl(AutomationId="SaveAudio")
    for _ in range(40):
        if save_button.IsEnabled == 1:
            break
        time.sleep(0.5)
    save_button.GetInvokePattern().Invoke()

    # Tjek metoden i Folkeregisterbøderobotten
    file_directory = context.ToolBarControl(AutomationId="1001")
    file_directory.RightClick(simulateMove=False)
    edit_address = auto.MenuItemControl(AutomationId="1280")
    edit_address.GetInvokePattern().Invoke()

    address_text = context.EditControl(AutomationId="41477")
    address_text.GetValuePattern().SetValue(save_dir)
    file_name = context.ComboBoxControl(AutomationId="FileNameControlHost").EditControl()
    file_name_saved = file_name.GetValuePattern().Value

    context.ButtonControl(AutomationId="1").GetInvokePattern().Invoke()
    return file_name_saved
