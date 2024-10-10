class Button:
    def __init__(self, x, y, name, onClick):
        self.x = x
        self.y = y
        self.name = name
        self.onClick = onClick


#check if all field are entered by the user
def valid_inputs(entries, labels):
    for lbl in labels:
        if entries[lbl] == None:
            return False
    return True