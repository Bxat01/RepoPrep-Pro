def __init__(self):
    super().__init__()
    self.cleaning_thread = None
    self.project_file_count = 0
    self.init_ui()
    self.apply_styles()
    
    self.set_application_icon()
    
def set_application_icon(self):

    icon = self.load_external_icon()
    if icon.isNull():
        icon = create_default_icon()
    
    self.setWindowIcon(icon)
    
def load_external_icon(self):
    import os
    from pathlib import Path
    
    icon_files = [
        "icon.ico",
        "app.ico",
        "icon.png",
        "assets/icon.ico",
        "assets/icon.png",
    ]
    
    for icon_file in icon_files:
        icon_path = Path(__file__).parent.parent / icon_file
        if os.path.exists(icon_path):
            return QIcon(str(icon_path))
    
    return QIcon()