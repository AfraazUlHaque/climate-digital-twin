assimilation_history = []

def add_snapshot(snapshot):
    assimilation_history.append(snapshot)
    if len(assimilation_history) > 100:
        assimilation_history.pop(0)

def get_history():
    return assimilation_history