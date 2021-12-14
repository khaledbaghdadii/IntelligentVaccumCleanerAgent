import cx_Freeze

executables = [cx_Freeze.Executable("Game2.py")]

cx_Freeze.setup(
    name="Smart Agents",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["images/cat.png","images/dirt.gif","images/dog.png","images/tile.png", "images/down_wall.png", "images/up_wall.png","images/left_wall.png","images/right_wall.png","images/vacuum-cleaner.png"]}},
    executables= executables

)